import random
import string
from datetime import datetime

import streamlit as st

from config import URL_SISTEMA
from database.banco import conectar


st.title("📅 Designações")


# ==========================================================
# GERAÇÃO DE CÓDIGO ÚNICO
# ==========================================================

def gerar_codigo():

    caracteres = string.ascii_uppercase + string.digits

    return "".join(
        random.choice(caracteres)
        for _ in range(6)
    )


# ==========================================================
# NOVA DESIGNAÇÃO
# ==========================================================

st.subheader("➕ Nova designação")


data = st.date_input("Data")

nome = st.text_input("Nome")

designacao = st.text_input("Designação")


if st.button("Salvar designação"):

    if not nome or not designacao:

        st.warning(
            "Preencha o nome e a designação."
        )

    else:

        try:

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
                VALUES
                (%s, %s, %s, %s, %s, %s, %s)
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
                "✅ Designação cadastrada com sucesso!"
            )


        except Exception as erro:

            st.error(
                "Erro ao salvar designação:"
            )

            st.code(str(erro))


# ==========================================================
# HISTÓRICO
# ==========================================================

st.divider()


st.subheader(
    "📜 Histórico de Designações"
)


try:

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


except Exception as erro:

    st.error(
        "Erro ao carregar histórico:"
    )

    st.code(str(erro))

    dados = []



if not dados:

    st.info(
        "Nenhuma designação cadastrada."
    )


else:

    for item in dados:


        try:

            data_formatada = datetime.strptime(
                str(item[0]),
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")


        except:

            data_formatada = item[0]



        link = (
            f"{URL_SISTEMA}/Responder"
            f"?codigo={item[3]}"
        )


        st.write(
            f"""
**📅 Data:** {data_formatada}

**👤 Nome:** {item[1]}

**📝 Designação:** {item[2]}

**📩 Recebeu:** {item[4]}

**✅ Disponibilidade:** {item[5]}
"""
        )


        st.write(
            "🔗 Link de confirmação:"
        )

        st.code(link)



        mensagem = (
            f"Olá, {item[1]}! 👋\n\n"
            f"Você recebeu uma designação.\n\n"
            f"📅 Data: {data_formatada}\n"
            f"📝 Designação: {item[2]}\n\n"
            f"Por favor, confirme o recebimento "
            f"da designação e informe sua disponibilidade "
            f"acessando o link abaixo:\n\n"
            f"🔗 {link}\n\n"
            f"Muito obrigado!"
        )


        with st.expander(
            "📱 Mostrar mensagem para WhatsApp"
        ):

            st.text_area(
                "Copie a mensagem abaixo:",
                mensagem,
                height=260,
                key=f"whatsapp_{item[3]}"
            )


        st.divider()