import streamlit as st
import openai
import os
from PIL import Image
import base64

# Configure the page
st.set_page_config(
    page_title="Career Navigator - Set Sail for Your Dream Career!",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B35;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .tagline {
        text-align: center;
        color: #2E8B57;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        max-height: 600px;
        overflow-y: auto;
    }
    .luffy-response {
        background: linear-gradient(135deg, #FFE5B4, #FFCCCB);
        border-left: 5px solid #FF6B35;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Comic Sans MS', cursive;
    }
    .user-message {
        background: linear-gradient(135deg, #E6F3FF, #B3D9FF);
        border-left: 5px solid #2E8B57;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .input-container {
        margin-top: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Background image setup
def get_background_image():
    img_path = "images/background.jpg"
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    return None

bg_image = get_background_image()
if bg_image:
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# Use Streamlit secrets for OpenAI
def initialize_openai():
    try:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        return True
    except Exception:
        st.error("🚨 Your OpenAI API key is missing. Please add it in Streamlit Secrets.")
        st.stop()

initialize_openai()

LUFFY_SYSTEM_PROMPT = """
You are Monkey D. Luffy from One Piece, helping 12th standard students find their dream careers!

Your personality traits:
- Always enthusiastic and encouraging
- Use phrases like "That's so cool!", "Yosh!", "Let's go!"
- Mention dreams, adventures, and treasure when explaining careers
- Limit each response to 200 words
- Mention 3–5 career paths, skills needed, and fun aspects of the jobs

Stay in character and always be positive!
"""

def get_luffy_response(user_message, chat_history):
    try:
        messages = [{"role": "system", "content": LUFFY_SYSTEM_PROMPT}]
        for msg in chat_history[-6:]:
            role = "user" if msg["role"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250,
            temperature=0.8,
            presence_penalty=0.6,
            frequency_penalty=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"🚨 Oops! Something went wrong! Error: {str(e)}"

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "🏴‍☠️ Yosh! I'm Luffy! Tell me what subjects you're studying and I'll help you find your treasure career! Let's go! ⚓"
    }]

# Layout
st.markdown('<h1 class="main-header">🏴‍☠️ Career Navigator</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Set Sail for Your Dream Career! 🏴‍☠️</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f'<div class="luffy-response">🏴‍☠️ <strong>Captain Luffy:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="user-message">⚓ <strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask Luffy about careers:", placeholder="e.g., I like math and science...")
        submit_button = st.form_submit_button("Send 🚀")
        
        if submit_button and user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get Luffy's response
            luffy_response = get_luffy_response(user_input, st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": luffy_response})
            
            # Rerun to show new messages
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with tips
with st.sidebar:
    st.markdown("### 🗺️ Navigation Tips")
    st.info("💡 **Ask Luffy about:**\n- Your favorite subjects\n- Career options\n- Skills needed\n- Educational paths")
    
    st.markdown("### 🔧 Troubleshooting")
    if st.button("Clear Chat"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "🏴‍☠️ Yosh! I'm Luffy! Tell me what subjects you're studying and I'll help you find your treasure career! Let's go! ⚓"
        }]
        st.rerun()