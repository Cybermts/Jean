import streamlit as st

st.write("VERSÃO DE TESTE - 05/08/2026")
st.set_page_config(
    page_title="Gestor de Designações",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================
# CONFIGURAÇÕES
# ==========================

st.title("📋 Gestor de Designações")


# ==========================
# APRESENTAÇÃO
# ==========================

st.markdown(
    """
    Bem-vindo ao **Gestor de Designações**.

    Um sistema para facilitar o controle das designações,
    confirmações e acompanhamento das atividades.

    Funcionalidades previstas:

    - 📅 Gerenciar designações
    - 👥 Controlar designados
    - 🔗 Enviar links individuais de confirmação
    - ✅ Registrar confirmações
    - 📊 Acompanhar estatísticas
    - 📱 Gerar mensagens para WhatsApp
    """
)


st.divider()


# ==========================
# STATUS DO SISTEMA
# ==========================

st.success("Sistema online e funcionando! 🚀")


st.info(
    """
    🚧 Próximas etapas:

    - Cadastro de pessoas
    - Criação de designações
    - Histórico automático
    - Relatórios
    """
)
