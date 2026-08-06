import streamlit as st


st.set_page_config(
    page_title="Gestor de Designações",
    page_icon="📋",
    layout="wide"
)


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

    ],

    "📩 Público": [

        st.Page(
            "pages/📩 Responder.py",
            title="📩 Responder"
        )

    ]

}


pg = st.navigation(paginas)


pg.run()