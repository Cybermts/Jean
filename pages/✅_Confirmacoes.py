import streamlit as st
from database.banco import conectar


st.title("✅ Confirmações")


st.subheader("Respostas das designações")


conexao = conectar()
cursor = conexao.cursor()


cursor.execute(
    """
    SELECT
        id,
        data,
        nome,
        designacao,
        recebeu,
        disponivel
    FROM designacoes
    ORDER BY data
    """
)


dados = cursor.fetchall()

conexao.close()


if not dados:

    st.info(
        "Nenhuma designação cadastrada."
    )


else:

    for item in dados:

        st.divider()

        st.write(
            f"📅 **Data:** {item[1]}"
        )

        st.write(
            f"👤 **Nome:** {item[2]}"
        )

        st.write(
            f"📝 **Designação:** {item[3]}"
        )


        recebeu = st.selectbox(
            "Você confirma que recebeu a designação?",
            [
                "Aguardando",
                "Sim",
                "Não"
            ],
            index=[
                "Aguardando",
                "Sim",
                "Não"
            ].index(item[4]),
            key=f"recebeu_{item[0]}"
        )


        disponivel = st.selectbox(
            "Você tem disponibilidade em cumpri-la?",
            [
                "Aguardando",
                "Sim",
                "Não"
            ],
            index=[
                "Aguardando",
                "Sim",
                "Não"
            ].index(item[5]),
            key=f"disponivel_{item[0]}"
        )


        if st.button(
            "Salvar resposta",
            key=f"salvar_{item[0]}"
        ):

            conexao = conectar()
            cursor = conexao.cursor()


            cursor.execute(
                """
                UPDATE designacoes
                SET recebeu = ?,
                    disponivel = ?
                WHERE id = ?
                """,
                (
                    recebeu,
                    disponivel,
                    item[0]
                )
            )


            conexao.commit()
            conexao.close()


            st.success(
                "Resposta atualizada!"
            )