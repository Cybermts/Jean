import streamlit as st
from database.banco import conectar


st.title("🏠 Dashboard")


st.subheader("Resumo das designações")


conexao = conectar()
cursor = conexao.cursor()


cursor.execute(
    """
    SELECT
        COUNT(*)
    FROM designacoes
    """
)

total = cursor.fetchone()[0]



cursor.execute(
    """
    SELECT
        COUNT(*)
    FROM designacoes
    WHERE disponivel = 'Sim'
    """
)

confirmados = cursor.fetchone()[0]



cursor.execute(
    """
    SELECT
        COUNT(*)
    FROM designacoes
    WHERE disponivel = 'Não'
    """
)

indisponiveis = cursor.fetchone()[0]



cursor.execute(
    """
    SELECT
        COUNT(*)
    FROM designacoes
    WHERE disponivel = 'Aguardando'
    """
)

aguardando = cursor.fetchone()[0]


conexao.close()



col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "📋 Total",
    total
)


col2.metric(
    "✅ Disponíveis",
    confirmados
)


col3.metric(
    "❌ Indisponíveis",
    indisponiveis
)


col4.metric(
    "⏳ Aguardando",
    aguardando
)



st.divider()


st.subheader(
    "Próximas designações"
)



conexao = conectar()
cursor = conexao.cursor()



cursor.execute(
    """
    SELECT
        data,
        nome,
        designacao,
        disponivel
    FROM designacoes
    ORDER BY data
    LIMIT 10
    """
)



dados = cursor.fetchall()


conexao.close()



if dados:

    for item in dados:

        st.write(
            f"""
            📅 **Data:** {item[0]}

            👤 **Nome:** {item[1]}

            📝 **Designação:** {item[2]}

            Situação:
            {item[3]}
            """
        )

        st.divider()


else:

    st.info(
        "Nenhuma designação cadastrada."
    )