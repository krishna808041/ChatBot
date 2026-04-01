import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# -------------------------------
# Load API Key
# -------------------------------
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
                response = client.chat.completions.create(
                    # New
                    model="llama-3.3-70b-versatile", # fast + free
                    messages=st.session_state.messages
                )

                ai_message = response.choices[0].message.content

                st.markdown(ai_message)

                # Save AI response
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': ai_message
                })

            except Exception as e:
                st.error(f'Error: {str(e)}')