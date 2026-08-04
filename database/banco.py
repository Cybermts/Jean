import sqlite3


CAMINHO_BANCO = "database/sistema.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabelas():

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ativo INTEGER DEFAULT 1
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS designacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        nome TEXT NOT NULL,
        designacao TEXT NOT NULL,
        codigo TEXT UNIQUE,
        recebeu TEXT,
        disponivel TEXT,
        respondido_em TEXT
    )
    """)


    conexao.commit()
    conexao.close()


criar_tabelas()