import streamlit as st
from database.banco import conectar
from datetime import datetime
from zoneinfo import ZoneInfo


st.set_page_config(
    page_title="Confirmação de Designação",
    page_icon="📩"
)


st.title("📩 Confirmação de Designação")


parametros = st.query_params
codigo = parametros.get("codigo")


if not codigo:
    st.warning("Link de confirmação inválido.")
    st.stop()


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
        disponivel,
        respondido_em
    FROM designacoes
    WHERE codigo = ?
    """,
    (codigo,)
)

registro = cursor.fetchone()

conexao.close()


if not registro:
    st.error("Designação não encontrada.")
    st.stop()


id_designacao = registro[0]
data = registro[1]
nome = registro[2]
designacao = registro[3]
recebeu_atual = registro[4]
disponivel_atual = registro[5]
respondido_em = registro[6]


# Data no padrão brasileiro
data_formatada = datetime.strptime(
    data,
    "%Y-%m-%d"
).strftime("%d/%m/%Y")


st.success(f"Olá, {nome}! 👋")

st.write(
    "Você recebeu a seguinte designação:"
)

st.info(
    f"""
📅 **Data:** {data_formatada}

📝 **Designação:** {designacao}
"""
)

st.divider()


if respondido_em:

    st.success("Sua confirmação já foi registrada.")

    st.write(f"📩 **Recebeu:** {recebeu_atual}")
    st.write(f"✅ **Disponibilidade:** {disponivel_atual}")
    st.write(f"🕒 **Respondido em:** {respondido_em}")

else:

    recebeu = st.radio(
        "Você confirma que recebeu a designação?",
        ["Sim", "Não"]
    )

    disponivel = st.radio(
        "Você tem disponibilidade em cumpri-la?",
        ["Sim", "Não"]
    )

    if st.button("Enviar confirmação", use_container_width=True):

        horario_brasilia = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).strftime("%d/%m/%Y %H:%M")

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE designacoes
            SET
                recebeu = ?,
                disponivel = ?,
                respondido_em = ?
            WHERE id = ?
            """,
            (
                recebeu,
                disponivel,
                horario_brasilia,
                id_designacao
            )
        )

        conexao.commit()
        conexao.close()

        st.success(
            "✅ Obrigado! Sua resposta foi registrada com sucesso."
        )

        st.balloons()

        st.rerun()