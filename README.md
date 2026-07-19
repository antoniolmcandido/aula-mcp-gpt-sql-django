# Projeto Django com backend MCP e frontend de chat

Este repositório agora contém dois projetos Django independentes:

- `backend`: API que interpreta comandos em linguagem natural, aciona o MCP e altera o MySQL.
- `frontend`: interface de chat estilizada com Bootstrap que consome a API do backend.

## Estrutura

- `backend/`
    - `api/`
    - `config/`
- `frontend/`
    - `chat/`
    - `config/`

## Como executar

1. Crie os ambientes virtuais:

```powershell
python -m venv backend/.venv
python -m venv frontend/.venv
```

2. Instale as dependências de cada projeto:

```powershell
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt
frontend/.venv/Scripts/python -m pip install -r frontend/requirements.txt
```

3. Configure as variáveis de ambiente a partir dos arquivos `.env.example`.

4. Inicie o backend na porta `8000` e o frontend na porta `8001`.

## Observações

- O backend usa MySQL via `mysql-connector-python` para o banco `escola`.
- O frontend chama o endpoint `/api/chat/` do backend.
- Em desenvolvimento, o backend permite CORS para o frontend local.
