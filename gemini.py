import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# -------------------------------
# Load API Key
# -------------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Load model
model = genai.GenerativeModel("models/gemini-flash-latest")
    # -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title='Chatbot',
    page_icon='🤖'
)

st.title('Your Personal Chatbot')
st.write('Ask me anything!')

# -------------------------------
# Session State
# -------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Show Previous Messages
# -------------------------------
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# -------------------------------
# User Input
# -------------------------------
user_input = st.chat_input('Type your message here...')

if user_input:
    # Save user message
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input
    })

    with st.chat_message('user'):
        st.markdown(user_input)

    # -------------------------------
    # AI Response
    # -------------------------------
    with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
            try:
                # Convert chat history for Gemini
                history = []
                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })

                chat = model.start_chat(history=history)

                response = chat.send_message(user_input)

                ai_message = response.text

                st.markdown(ai_message)

                # Save AI response
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': ai_message
                })

            except Exception as e:
                st.error(f'Error: {str(e)}')