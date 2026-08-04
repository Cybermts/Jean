import streamlit as st
from database.banco import conectar
from datetime import datetime


st.title("📩 Confirmação de Designação")


parametros = st.query_params

codigo = parametros.get("codigo")


if not codigo:

    st.warning(
        "Link de confirmação inválido."
    )

    st.stop()



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
    WHERE codigo = ?
    """,
    (codigo,)
)


registro = cursor.fetchone()

conexao.close()



if not registro:

    st.error(
        "Designação não encontrada."
    )

    st.stop()



id_designacao = registro[0]
data = registro[1]
nome = registro[2]
designacao = registro[3]
recebeu_atual = registro[4]
disponivel_atual = registro[5]
respondido_em = registro[6]


# Formata a data para o padrão brasileiro
data_formatada = datetime.strptime(
    data,
    "%Y-%m-%d"
).strftime(
    "%d/%m/%Y"
)



st.success(
    f"Olá, {nome}! 👋"
)


st.write(
    "Você recebeu uma designação:"
)


st.write(
    f"📅 **Data:** {data_formatada}"
)


st.write(
    f"📝 **Designação:** {designacao}"
)



st.divider()



if respondido_em:


    st.info(
        "Sua confirmação já foi registrada."
    )


    st.write(
        f"📩 **Recebeu:** {recebeu_atual}"
    )


    st.write(
        f"✅ **Disponibilidade:** {disponivel_atual}"
    )


    st.write(
        f"🕒 **Respondido em:** {respondido_em}"
    )


else:


    recebeu = st.radio(
        "Você confirma que recebeu a designação?",
        [
            "Sim",
            "Não"
        ]
    )


    disponivel = st.radio(
        "Você tem disponibilidade em cumpri-la?",
        [
            "Sim",
            "Não"
        ]
    )



    if st.button(
        "Enviar confirmação"
    ):


        conexao = conectar()
        cursor = conexao.cursor()


        cursor.execute(
            """
            UPDATE designacoes
            SET
                recebeu = ?,
                disponivel = ?,
                respondido_em = ?
            WHERE id = ?
            """,
            (
                recebeu,
                disponivel,
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                ),
                id_designacao
            )
        )


        conexao.commit()
        conexao.close()


        st.success(
            "Obrigado! Sua resposta foi registrada."
        )