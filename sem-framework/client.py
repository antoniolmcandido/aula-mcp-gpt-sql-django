from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import json
import asyncio

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Definir as ferramentas disponíveis
tools = [
    {
        "type": "function",
        "function": {
            "name": "cadastrar_aluno",
            "description": "Cadastra um novo aluno",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "idade": {"type": "integer"}
                },
                "required": ["nome", "idade"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "atualizar_idade",
            "description": "Atualiza a idade de um aluno",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "idade": {"type": "integer"}
                },
                "required": ["nome", "idade"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remover_aluno",
            "description": "Remove um aluno",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                },
                "required": ["nome"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_alunos",
            "description": "Lista todos os alunos cadastrados",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# Função para executar ferramenta via MCP
async def execute_tool_async(function_name, function_args):
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Executar a ferramenta
            result = await session.call_tool(function_name, function_args)
            return result.content[0].text

def execute_tool(function_name, function_args):
    return asyncio.run(execute_tool_async(function_name, function_args))


def action(instruction):
    # Primeira chamada
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": instruction}
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Verificar se o modelo quer usar uma ferramenta
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        print(f"Executando: {function_name} com argumentos {function_args}")

        # Executar a ferramenta via MCP
        result = execute_tool(function_name, function_args)

        print(f"Resultado: {result}")

        # Segunda chamada com o resultado
        second_response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "user", "content": instruction},
                message,  # Mensagem do assistente com tool_calls
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            ],
            tools=tools  # Usar a lista de tools definida acima
        )

        print(f"Resposta final: {second_response.choices[0].message.content}")
    else:
        print(message.content)

# action("Cadastre um aluno chamado João com 20 anos.")
action("Atualize a idade do aluno José, para 35 anos.")