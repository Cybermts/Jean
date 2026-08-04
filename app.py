
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Gestor de Designações",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

URL_SISTEMA = "https://jean93.streamlit.app"

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

st.divider()

st.header("📜 Histórico de Designações")


# Exemplo temporário simulando uma designação cadastrada
# Depois será substituído pelo banco de dados

historico = [
    (
        "2026-08-10",
        "João",
        "Leitura",
        "ABC123"
    )
]


for item in historico:

    st.subheader(f"👤 {item[1]}")

    st.write(f"📅 Data: {item[0]}")
    st.write(f"📝 Designação: {item[2]}")

    st.write("🔗 Link de confirmação:")

    link = f"{URL_SISTEMA}/Responder?codigo={item[3]}"

    st.code(link)


    try:
        data_formatada = datetime.strptime(
            item[0],
            "%Y-%m-%d"
        ).strftime("%d/%m/%Y")

    except:
        data_formatada = item[0]


    mensagem = (
        f"Olá, {item[1]}! 👋\n\n"
        f"Você recebeu uma designação.\n\n"
        f"📅 Data: {data_formatada}\n"
        f"📝 Designação: {item[2]}\n\n"
        f"Por favor, confirme o recebimento da designação "
        f"e a disponibilidade em cumpri-la acessando o link abaixo:\n\n"
        f"🔗 {link}\n\n"
        f"Muito obrigado!"
    )


    with st.expander("📱 Mostrar mensagem para WhatsApp"):

        st.markdown("### Mensagem pronta para envio:")

        st.text_area(
            "",
            value=mensagem,
            height=250,
            key=f"whatsapp_{item[3]}"
        )


st.divider()

st.info("VERSÃO ATUALIZADA 🚀")
