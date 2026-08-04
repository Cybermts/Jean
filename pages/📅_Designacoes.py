import streamlit as st
from database.banco import conectar
import random
import string
from config import URL_SISTEMA


st.title("📅 Designações")


def gerar_codigo():

    caracteres = string.ascii_uppercase + string.digits

    return "".join(
        random.choice(caracteres)
        for _ in range(6)
    )



st.subheader("Nova designação")


data = st.date_input(
    "Data"
)


nome = st.text_input(
    "Nome"
)


designacao = st.text_input(
    "Designação"
)



if st.button("Salvar designação"):


    if nome and designacao:


        codigo = gerar_codigo()


        conexao = conectar()
        cursor = conexao.cursor()


        cursor.execute(
            """
            INSERT INTO designacoes
            (
                data,
                nome,
                designacao,
                codigo,
                recebeu,
                disponivel,
                respondido_em
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(data),
                nome,
                designacao,
                codigo,
                "Aguardando",
                "Aguardando",
                None
            )
        )


        conexao.commit()
        conexao.close()


        st.success(
            "Designação cadastrada!"
        )


        link = (
            f"{URL_SISTEMA}/Responder?codigo={codigo}"
        )


        data_formatada = data.strftime(
            "%d/%m/%Y"
        )


        st.write(
            "🔗 **Link de confirmação:**"
        )


        st.code(
            link
        )


        st.write(
            "📱 **Mensagem para WhatsApp:**"
        )


        mensagem = f"""
Olá, {nome}! 👋


Você recebeu uma designação.


📅 Data: {data_formatada}


📝 Designação: {designacao}


Por favor, confirme se recebeu a designação e se tem disponibilidade em cumpri-la através do link abaixo:


🔗 {link}


Obrigado!
"""


        st.text_area(
            "Copie e envie pelo WhatsApp:",
            mensagem,
            height=250
        )


    else:

        st.warning(
            "Preencha o nome e a designação."
        )



st.divider()


st.subheader(
    "Designações cadastradas"
)


conexao = conectar()
cursor = conexao.cursor()


cursor.execute(
    """
    SELECT
        data,
        nome,
        designacao,
        codigo,
        recebeu,
        disponivel
    FROM designacoes
    ORDER BY data
    """
)


dados = cursor.fetchall()

conexao.close()



for item in dados:


    data_lista = item[0]


    st.write(
        f"""
        📅 **Data:** {data_lista}

        👤 **Nome:** {item[1]}

        📝 **Designação:** {item[2]}

        📩 **Recebeu:** {item[4]}

        ✅ **Disponibilidade:** {item[5]}
        """
    )


    link_lista = (
        f"{URL_SISTEMA}/Responder?codigo={item[3]}"
    )


    st.write(
        "🔗 Link:"
    )


    st.code(
        link_lista
    )


    st.divider()