import streamlit as st
from database.banco import conectar


st.title("👥 Pessoas")


st.subheader("Cadastrar pessoa")


nome = st.text_input("Nome completo")


if st.button("Salvar"):

    if nome:

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO pessoas (nome)
            VALUES (?)
            """,
            (nome,)
        )

        conexao.commit()
        conexao.close()

        st.success("Pessoa cadastrada com sucesso!")

    else:
        st.warning("Digite o nome da pessoa.")


st.divider()


st.subheader("Pessoas cadastradas")


conexao = conectar()
cursor = conexao.cursor()

cursor.execute(
    "SELECT id, nome FROM pessoas ORDER BY nome"
)

dados = cursor.fetchall()

conexao.close()


for pessoa in dados:
    st.write(f"👤 {pessoa[1]}")