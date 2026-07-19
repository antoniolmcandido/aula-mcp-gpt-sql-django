from .mysql import conectar


class AlunoNaoEncontrado(Exception):
    pass


def listar_alunos_dados():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, idade FROM alunos ORDER BY nome")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [{"nome": nome, "idade": idade} for nome, idade in dados]


def cadastrar_aluno_dados(nome: str, idade: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO alunos(nome, idade) VALUES(%s, %s)",
        (nome, idade),
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"nome": nome, "idade": idade}


def atualizar_idade_dados(nome: str, idade: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE alunos
        SET idade=%s
        WHERE nome=%s
        """,
        (idade, nome),
    )
    if cursor.rowcount == 0:
        cursor.close()
        conexao.close()
        raise AlunoNaoEncontrado(f"Aluno '{nome}' não encontrado.")
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"nome": nome, "idade": idade}


def remover_aluno_dados(nome: str):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM alunos WHERE nome=%s", (nome,))
    if cursor.rowcount == 0:
        cursor.close()
        conexao.close()
        raise AlunoNaoEncontrado(f"Aluno '{nome}' não encontrado.")
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"nome": nome}
