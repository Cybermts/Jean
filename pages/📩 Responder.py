import streamlit as st
from datetime import datetime

from database.banco import conectar


st.set_page_config(
    page_title="Confirmação de Designação",
    page_icon="📩",
    initial_sidebar_state="collapsed"
)


st.title("📩 Confirmação de Designação")


# ==========================================================
# PEGAR CÓDIGO DO LINK
# ==========================================================

params = st.query_params

codigo = params.get("codigo")


if not codigo:

    st.warning(
        "Código de confirmação não informado."
    )

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
            disponivel,
            respondido_em
        FROM designacoes
        WHERE codigo = %s
        """,
        (codigo,)
    )

    registro = cursor.fetchone()

    conexao.close()


except Exception as erro:

    st.error(
        "Erro ao consultar designação:"
    )

    st.code(str(erro))

    st.stop()



if not registro:

    st.error(
        "❌ Designação não encontrada."
    )

    st.info(
        """
        O código informado não existe ou a designação foi removida.
        """
    )

    st.stop()



# ==========================================================
# DADOS DA DESIGNAÇÃO
# ==========================================================

id_designacao = registro[0]
data = registro[1]
nome = registro[2]
designacao = registro[3]
recebeu_atual = registro[4]
disponivel_atual = registro[5]
respondido_em = registro[6]



try:

    data_formatada = datetime.strptime(
        str(data),
        "%Y-%m-%d"
    ).strftime("%d/%m/%Y")


except:

    data_formatada = data



# ==========================================================
# CABEÇALHO
# ==========================================================

st.success(
    f"Olá, {nome}! 👋"
)


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
# CASO JÁ TENHA RESPONDIDO
# ==========================================================

if respondido_em:

    st.success(
        "🎉 Sua confirmação já foi registrada!"
    )

    st.info(
        f"""
Obrigado pela sua resposta, {nome}! 🙏

📩 **Recebimento:** {recebeu_atual}

✅ **Disponibilidade:** {disponivel_atual}

🕒 **Respondido em:** {respondido_em}
"""
    )

    st.stop()



# ==========================================================
# FORMULÁRIO DE RESPOSTA
# ==========================================================

st.subheader(
    "📩 Confirmação da designação"
)


confirmacao = st.radio(
    "Você recebeu a designação?",
    [
        "Sim",
        "Não"
    ],
    horizontal=True
)



st.divider()



st.subheader(
    "✅ Disponibilidade"
)


disponibilidade = st.radio(
    "Você está disponível para cumprir esta designação?",
    [
        "Sim",
        "Não"
    ],
    horizontal=True
)



st.divider()



# ==========================================================
# SALVAR RESPOSTAS
# ==========================================================

if st.button(
    "Enviar resposta",
    use_container_width=True
):

    try:

        conexao = conectar()
        cursor = conexao.cursor()


        horario = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )


        cursor.execute(
            """
            UPDATE designacoes
            SET
                recebeu = %s,
                disponivel = %s,
                respondido_em = %s
            WHERE id = %s
            """,
            (
                confirmacao,
                disponibilidade,
                horario,
                id_designacao
            )
        )


        conexao.commit()

        conexao.close()



        st.success(
            f"🎉 Obrigado, {nome}! "
            "Sua confirmação foi registrada com sucesso."
        )


        st.balloons()



        st.info(
            """
Sua resposta foi enviada ao responsável pelas designações.

Muito obrigado pela colaboração! 🙏
"""
        )


        st.stop()



    except Exception as erro:

        st.error(
            "Erro ao salvar resposta:"
        )

        st.code(str(erro))