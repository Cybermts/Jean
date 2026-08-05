import streamlit as st
from datetime import datetime

from database.banco import conectar


st.title("📩 Confirmação de Designação")


# ==========================================================
# PEGAR CÓDIGO DO LINK
# ==========================================================

params = st.query_params

codigo = params.get("codigo")


if not codigo:

    st.warning("Código de confirmação não informado.")

    st.stop()


# ==========================================================
# BUSCAR DESIGNAÇÃO
# ==========================================================

try:

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
        WHERE codigo = ?
        """,
        (codigo,)
    )

    registro = cursor.fetchone()

    conexao.close()


except Exception as erro:

    st.error("Erro ao consultar designação:")
    st.code(str(erro))
    st.stop()


if not registro:

    st.error("❌ Designação não encontrada.")

    st.info(
        """
        O código informado não existe ou a designação foi removida.
        """
    )

    st.stop()


# ==========================================================
# MOSTRAR DADOS
# ==========================================================

id_designacao = registro[0]
data = registro[1]
nome = registro[2]
designacao = registro[3]
recebeu = registro[4]
disponivel = registro[5]


try:

    data_formatada = datetime.strptime(
        data,
        "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

except:

    data_formatada = data


st.success(f"Olá, {nome}! 👋")


st.write(
    f"""
### 📅 Data:
{data_formatada}

### 📝 Designação:
{designacao}
"""
)


st.divider()


# ==========================================================
# CONFIRMAÇÃO
# ==========================================================

if recebeu == "Confirmado":

    st.success("✅ Você já confirmou o recebimento desta designação.")

else:

    if st.button("✅ Confirmar recebimento"):

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE designacoes
            SET recebeu = ?,
                respondido_em = ?
            WHERE id = ?
            """,
            (
                "Confirmado",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                id_designacao
            )
        )

        conexao.commit()
        conexao.close()

        st.success("Recebimento confirmado com sucesso!")


# ==========================================================
# DISPONIBILIDADE
# ==========================================================

st.divider()

st.subheader("Disponibilidade")


opcao = st.radio(
    "Você está disponível para cumprir esta designação?",
    [
        "Aguardando",
        "Sim",
        "Não"
    ],
    index=0
)


if st.button("Salvar disponibilidade"):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE designacoes
        SET disponivel = ?
        WHERE id = ?
        """,
        (
            opcao,
            id_designacao
        )
    )

    conexao.commit()
    conexao.close()

    st.success("Disponibilidade registrada!")
