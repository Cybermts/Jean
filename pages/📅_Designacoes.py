import random
import string
from datetime import datetime

import streamlit as st

from config import URL_SISTEMA
from database.banco import conectar


st.title("📅 Designações")


def gerar_codigo():
    caracteres = string.ascii_uppercase + string.digits
    return "".join(random.choice(caracteres) for _ in range(6))


# -------------------------------------------------------------------
# Memória da sessão (mantém o link e a mensagem na tela)
# -------------------------------------------------------------------

if "link" not in st.session_state:
    st.session_state.link = ""

if "mensagem" not in st.session_state:
    st.session_state.mensagem = ""


# -------------------------------------------------------------------
# NOVA DESIGNAÇÃO
# -------------------------------------------------------------------

st.subheader("Nova designação")

data = st.date_input("Data")

nome = st.text_input("Nome")

designacao = st.text_input("Designação")


if st.button("Salvar designação"):

    if not nome or not designacao:
        st.warning("Preencha o nome e a designação.")

    else:

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

        data_formatada = data.strftime("%d/%m/%Y")

        link = f"{URL_SISTEMA}/Responder?codigo={codigo}"

        mensagem = f"""Olá, {nome}! 👋

Você recebeu uma designação.

📅 Data: {data_formatada}
📝 Designação: {designacao}

Por favor, confirme o recebimento da designação e a disponibilidade em cumpri-la, acessando o link a seguir:

🔗 {link}

Muito obrigado!
"""

        st.session_state.link = link
        st.session_state.mensagem = mensagem

        st.success("✅ Designação cadastrada com sucesso!")


# -------------------------------------------------------------------
# LINK E MENSAGEM
# -------------------------------------------------------------------

if st.session_state.link:

    st.write("### 🔗 Link de confirmação")

    st.code(st.session_state.link)

    st.write("### 📱 Mensagem para WhatsApp")

    st.text_area(
        "Copie e envie pelo WhatsApp:",
        st.session_state.mensagem,
        height=220
    )


# -------------------------------------------------------------------
# HISTÓRICO
# -------------------------------------------------------------------

st.divider()

st.subheader("Designações cadastradas")

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

    try:
        data_formatada = datetime.strptime(
            item[0],
            "%Y-%m-%d"
        ).strftime("%d/%m/%Y")
    except Exception:
        data_formatada = item[0]

    st.write(f"""
**📅 Data:** {data_formatada}

**👤 Nome:** {item[1]}

**📝 Designação:** {item[2]}

**📩 Recebeu:** {item[4]}

**✅ Disponibilidade:** {item[5]}
""")

    st.code(
        f"{URL_SISTEMA}/Responder?codigo={item[3]}"
    )

    st.divider()