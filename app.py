
import streamlit as st


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Gestor de Designações",
    page_icon="📋",
    layout="wide"
)


# ==========================================================
# VERIFICAR SE É UM ACESSO PÚBLICO
# ==========================================================

params = st.query_params

codigo = params.get("codigo")


# ==========================================================
# ACESSO PÚBLICO
# ==========================================================

if codigo:

    paginas = [
        st.Page(
            "pages/📩 Responder.py",
            title="📩 Responder"
        )
    ]


# ==========================================================
# ACESSO ADMINISTRATIVO
# ==========================================================

else:

    paginas = {

        "📋 Administração": [

            st.Page(
                "admin/📅_Designacoes.py",
                title="📅 Designações"
            ),

            st.Page(
                "admin/🏠_Dashboard.py",
                title="🏠 Dashboard"
            ),

            st.Page(
                "admin/📊_Relatorios.py",
                title="📊 Relatórios"
            ),

        ]

    }


# ==========================================================
# NAVEGAÇÃO
# ==========================================================

pg = st.navigation(paginas)

pg.run()
