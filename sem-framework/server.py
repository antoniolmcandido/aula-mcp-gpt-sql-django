from mcp.server.fastmcp import FastMCP
from database import conectar
mcp = FastMCP("Escola")

@mcp.tool()
def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome, idade FROM alunos"
    )

    dados = cursor.fetchall()
    cursor.close()
    conexao.close()

    texto = ""

    for nome, idade in dados:
        texto += f"{nome} ({idade} anos)\n"

    return texto


@mcp.tool()
def cadastrar_aluno(nome: str, idade: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO alunos(nome, idade) VALUES(%s,%s)",
        (nome, idade)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    return "Aluno cadastrado com sucesso."


@mcp.tool()
def atualizar_idade(nome: str, idade: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE alunos
        SET idade=%s
        WHERE nome=%s
        """,
        (idade, nome)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    return "Idade atualizada."


@mcp.tool()
def remover_aluno(nome: str):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "DELETE FROM alunos WHERE nome=%s",
        (nome,)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    return "Aluno removido."

if __name__ == "__main__":
    mcp.run()