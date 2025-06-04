import streamlit as st
import requests

# Backend API endpoint
API_URL = "https://baa6-152-118-101-243.ngrok-free.app/ask" # Change this to your actual backend URL if deployed

# UI title
st.title("💬 Helpdesk DTE UI — DeepSeek")

# Inisialisasi histori chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Fungsi untuk menjawab via API
def generate_response(user_input):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ Sedang memproses...")

        try:
            # Kirim POST request ke backend
            response = requests.post(API_URL, json={"question": user_input})
            response.raise_for_status()
            answer = response.json()["answer"]
        except requests.exceptions.RequestException as e:
            answer = f"⚠️ Terjadi kesalahan saat menghubungi backend: {str(e)}"

        # Tampilkan jawaban
        message_placeholder.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# Tampilkan chat sebelumnya
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Input baru dari user
user_input = st.chat_input("Ketik pertanyaanmu di sini...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    generate_response(user_input)
