import requests
import streamlit as st

st.title("🤖 Juma Agent - Insights")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Pergunte algo sobre os insights..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chamada para o seu agente Flask (Porta 8080)
    response = requests.post("http://127.0.0.1:8080/chat", json={"message": prompt})

    if response.status_code == 200:
        answer = response.json().get("response", "Sem resposta.")
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
