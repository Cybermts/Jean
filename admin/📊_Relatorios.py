import streamlit as st
from database.banco import conectar
from datetime import datetime
import pandas as pd


st.title("📊 Relatórios")


st.subheader("Filtro de situação")


filtro = st.selectbox(
    "Mostrar:",
    [
        "Todas",
        "Confirmadas",
        "Não disponíveis",
        "Aguardando"
    ]
)



conexao = conectar()
cursor = conexao.cursor()


cursor.execute(
    """
    SELECT
        data,
        nome,
        designacao,
        recebeu,
        disponivel,
        respondido_em
    FROM designacoes
    ORDER BY data
    """
)


dados = cursor.fetchall()

conexao.close()



if not dados:

    st.info(
        "Nenhuma designação cadastrada."
    )

    st.stop()



lista = []


for item in dados:

    data = datetime.strptime(
        item[0],
        "%Y-%m-%d"
    ).strftime(
        "%d/%m/%Y"
    )


    lista.append(
        {
            "Data": data,
            "Nome": item[1],
            "Designação": item[2],
            "Recebeu": item[3],
            "Disponibilidade": item[4],
            "Respondido em": item[5] if item[5] else "-"
        }
    )



df = pd.DataFrame(lista)



if filtro == "Confirmadas":

    df = df[
        (df["Recebeu"] == "Sim") &
        (df["Disponibilidade"] == "Sim")
    ]



elif filtro == "Não disponíveis":

    df = df[
        df["Disponibilidade"] == "Não"
    ]



elif filtro == "Aguardando":

    df = df[
        df["Disponibilidade"] == "Aguardando"
    ]



st.divider()


st.subheader(
    "Lista de designações"
)



st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)