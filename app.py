import streamlit as st
import openai
import time

# Configure the page
st.set_page_config(
    page_title="Career Navigator - Set Sail for Your Dream Career!",
    page_icon="🏴‍☠️",
    layout="wide"
)

# MUCH SIMPLER CSS - No blinking, no complex backgrounds
st.markdown("""
<style>
    /* Simple, solid background */
    .stApp {
        background-color: #f0f8ff;
    }
    
    .main-header {
        text-align: center;
        color: #FF6B35;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding: 20px;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .tagline {
        text-align: center;
        color: #2E8B57;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        padding: 10px;
        background-color: white;
        border-radius: 10px;
    }
    
    .chat-message {
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .luffy-message {
        border-left: 5px solid #FF6B35;
        background: linear-gradient(135deg, #fff3e0, #ffe4b5);
    }
    
    .user-message {
        border-left: 5px solid #2E8B57;
        background: linear-gradient(135deg, #e8f5e8, #d4edda);
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI
@st.cache_data
def initialize_openai():
    try:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        return True
    except:
        st.error("🚨 OpenAI API key missing. Add OPENAI_API_KEY to Streamlit secrets.")
        return False

if not initialize_openai():
    st.stop()

# Luffy's personality
LUFFY_PROMPT = """You are Monkey D. Luffy helping students find careers. 
Be enthusiastic, use "Yosh!", "That's so cool!", mention adventures and dreams.
Keep responses under 150 words. Suggest 3-4 career paths with needed skills.
Always end with an encouraging question."""

def get_luffy_response(message):
    """Simple function to get Luffy's response"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": LUFFY_PROMPT},
                {"role": "user", "content": message}
            ],
            max_tokens=180,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"🚨 Oops! Something went wrong: {str(e)[:50]}... Try again!"

# Initialize chat - SIMPLE VERSION
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant", 
            "content": "🏴‍☠️ Yosh! I'm Luffy! Tell me what subjects you like and I'll help you find amazing careers! What do you enjoy studying?"
        }
    ]

# Header
st.markdown('<h1 class="main-header">🏴‍☠️ Career Navigator</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Set Sail for Your Dream Career! 🏴‍☠️</p>', unsafe_allow_html=True)

# Quick career buttons
st.markdown("### 🗺️ Quick Start - Pick a Field:")
col1, col2, col3, col4, col5, col6 = st.columns(6)

career_options = [
    ("🏗️ Engineering", "I'm interested in engineering"),
    ("⚕️ Medical", "I want medical careers"),
    ("💼 Business", "Tell me about business careers"),
    ("🎨 Creative", "I love arts and creativity"),
    ("🔬 Science", "I'm passionate about science"),
    ("👩‍🏫 Education", "I want to teach others")
]

# Handle button clicks - MUCH SIMPLER
for i, (button_text, prompt) in enumerate(career_options):
    with [col1, col2, col3, col4, col5, col6][i]:
        if st.button(button_text, key=f"btn_{i}"):
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            # Get Luffy response
            with st.spinner("🏴‍☠️ Luffy is thinking..."):
                response = get_luffy_response(prompt)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})

st.markdown("---")

# Display chat messages
st.markdown("### 💬 Chat with Captain Luffy:")

for message in st.session_state.chat_messages:
    if message["role"] == "assistant":
        st.markdown(f'''
        <div class="chat-message luffy-message">
            🏴‍☠️ <strong>Captain Luffy:</strong><br>
            {message["content"]}
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="chat-message user-message">
            ⚓ <strong>You:</strong><br>
            {message["content"]}
        </div>
        ''', unsafe_allow_html=True)

# Chat input - SIMPLE FORM
st.markdown("### ✍️ Ask Luffy:")
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question:", placeholder="I like math and helping people...")
    submitted = st.form_submit_button("Send 🚀")
    
    if submitted and user_input:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        # Get Luffy response
        with st.spinner("🏴‍☠️ Luffy is thinking..."):
            response = get_luffy_response(user_input)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Refresh to show new messages
        st.rerun()

# Simple sidebar
with st.sidebar:
    st.markdown("### 🗺️ Tips")
    st.info("Ask about:\n- Your favorite subjects\n- Dream careers\n- Skills needed\n- Education paths")
    
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_messages = [
            {
                "role": "assistant", 
                "content": "🏴‍☠️ Yosh! I'm Luffy! Tell me what subjects you like and I'll help you find amazing careers! What do you enjoy studying?"
            }
        ]
        st.rerun()