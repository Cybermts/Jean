import streamlit as st

st.set_page_config(
    page_title="Gestor de Designações",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📋 Gestor de Designações")

st.markdown(
    """
    Bem-vindo ao **Gestor de Designações**.

    Este sistema permitirá:

    - 📅 Gerenciar designações
    - 👥 Controlar designados
    - ✅ Registrar confirmações
    - 📊 Acompanhar estatísticas
    """
)

st.info("Projeto em desenvolvimento 🚧")