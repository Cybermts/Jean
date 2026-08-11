import streamlit as st
from datetime import datetime

from database.banco import conectar


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Confirmação de Designação",
    page_icon="📩",
    initial_sidebar_state="collapsed"
)


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
        "Erro ao consultar a designação."
    )

    st.code(str(erro))

    st.stop()


# ==========================================================
# VERIFICAR SE ENCONTROU
# ==========================================================

if not registro:

    st.error(
        "❌ Designação não encontrada."
    )

    st.info(
        "O código informado não existe ou a designação foi removida."
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


# ==========================================================
# LIMPAR ASTERISCOS DA DESIGNAÇÃO
# ==========================================================

designacao = str(designacao).replace("*", "").strip()


# ==========================================================
# FORMATAR DATA
# ==========================================================

try:

    data_formatada = datetime.strptime(
        str(data),
        "%Y-%m-%d"
    ).strftime("%d/%m/%Y")


except:

    data_formatada = str(data)


# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("📩 Confirmação de Designação")

st.success(
    f"Olá, {nome}! 👋"
)

st.write(
    f"""
### 📅 Data

**{data_formatada}**

### 📝 Designação

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
# FORMULÁRIO
# ==========================================================

st.subheader(
    "Você poderá cumprir esta designação?"
)

resposta = st.radio(
    "Selecione uma opção:",
    [
        "Sim — recebi a designação e estou disponível.",
        "Não — não poderei cumprir a designação."
    ],
    index=None
)


# ==========================================================
# ENVIAR RESPOSTA
# ==========================================================

if st.button(
    "📩 Enviar resposta",
    use_container_width=True
):

    if resposta is None:

        st.warning(
            "Por favor, selecione uma opção antes de enviar."
        )

        st.stop()


    # ------------------------------------------------------
    # TRANSFORMAR A RESPOSTA EM DADOS DO BANCO
    # ------------------------------------------------------

    if resposta.startswith("Sim"):

        recebeu = "Sim"
        disponivel = "Sim"

    else:

        recebeu = "Sim"
        disponivel = "Não"


    # ------------------------------------------------------
    # SALVAR
    # ------------------------------------------------------

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
                recebeu,
                disponivel,
                horario,
                id_designacao
            )
        )

        conexao.commit()

        conexao.close()


        # --------------------------------------------------
        # CONFIRMAÇÃO
        # --------------------------------------------------

        st.success(
            f"🎉 Obrigado, {nome}! "
            "Sua resposta foi registrada com sucesso."
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
            "Erro ao salvar resposta."
        )

        st.code(str(erro))

