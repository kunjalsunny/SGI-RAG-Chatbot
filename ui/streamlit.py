import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000/v1/chat")

st.set_page_config(page_title="SGI Chatbot", page_icon="💬", layout="centered")
st.title("SGI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask a question…")
top_k = st.sidebar.slider("Top K", 1, 10, 4)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            r = requests.post(API_URL, json={"message": prompt, "top_k": top_k}, timeout=120)
            r.raise_for_status()
            data = r.json()
            st.markdown(data.get("answer", ""))

            sources = data.get("sources", [])
            if sources:
                with st.expander("Sources"):
                    for i, s in enumerate(sources, start=1):
                        meta = s.get("metadata") or {}
                        st.markdown(f"**[{i}]** {meta.get('source','')}")
                        st.write(s.get("text", "")[:800])

            st.session_state.messages.append({"role": "assistant", "content": data.get("answer", "")})

        except Exception as e:
            st.error(str(e))
