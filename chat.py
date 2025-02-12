import streamlit as st
import requests
import json

# Set up the page configuration
st.set_page_config(page_title="BharatAI Chatbot", layout="centered")

# Inject custom CSS for branding & layout improvements
st.markdown(
    """
    <style>
        /* Set dark theme */
        body {
            background-color:rgb(0, 0, 0);
            color: white;
            font-family: 'Arial', sans-serif;
        }

        /* Fixed "bharathai" in top-left corner */
        .fixed-top-left {
            position: fixed;
            top: 10px;
            left: 10px;
            font-size: 14px;
            font-weight: bold;
            color: white;
            background-color:rgb(0, 0, 0);
            padding: 5px 10px;
            border-radius: 5px;
            z-index: 1000;
        }

        /* Fixed "Made with ❤️ for Bharat" at the bottom-center */
        .fixed-bottom {
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 12px;
            color: white;
            background-color:rgb(0, 0, 0);
            padding: 5px 10px;
            border-radius: 5px;
            z-index: 1000;
        }

        /* Chat container */
        .chat-container {
            max-width: 700px;
            margin: auto;
            text-align: center;
        }

        /* Message box styling */
        .message-box {
            background-color:rgb(0, 0, 0);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }

        /* User & AI message styling */
        .user-message {
            background-color:rgb(0, 0, 0);
            text-align: right;
        }

        .ai-message {
            background-color: #333;
            text-align: left;
        }

        /* Input box */
        .input-box {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #444;
            background-color: #222;
            color: white;
        }

        /* Send button */
        .send-button {
            background-color: #0A84FF;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }

        .send-button:hover {
            background-color: #0066CC;
        }

        /* Action buttons */
        .buttons-container {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            gap: 10px;
        }

        .action-button {
            background-color:rgb(0, 0, 0);
            color: white;
            border: 1px solid #444;
            padding: 12px 18px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
        }

        .action-button:hover {
            background-color: #333;
        }
    </style>

    <div class="fixed-top-left">bharathai</div>
    <div class="fixed-bottom">made with ❤️ for bharat</div>
    """,
    unsafe_allow_html=True
)

# OpenRouter API details
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Function to call the OpenRouter API for AI responses
def get_ai_response(user_input):
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 150
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error: Unexpected status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Title and welcome message
st.markdown("<div class='chat-container'><h1>What can I help with?</h1></div>", unsafe_allow_html=True)

# Chat history container
if 'messages' not in st.session_state:
    st.session_state.messages = []

chat_container = st.container()

# Display chat history
with chat_container:
    for message in st.session_state.messages:
        role_class = "user-message" if message["role"] == "user" else "ai-message"
        st.markdown(f"<div class='message-box {role_class}'>{message['content']}</div>", unsafe_allow_html=True)

# User input box
user_input = st.text_input("", placeholder="Message BharatAI...", key="chat_input", help="Type your message here.")

# Send button column layout
send_col = st.columns([8, 2])
with send_col[1]:
    if st.button("Send", key="send", help="Send your message.", use_container_width=True):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            ai_response = get_ai_response(user_input)
            st.session_state.messages.append({"role": "AI", "content": ai_response})
            st.rerun()

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
