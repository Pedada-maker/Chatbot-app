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

# Custom CSS - FIXED VERSION
st.markdown("""
<style>
    /* Main app background - made more subtle */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4a90e2 100%);
        background-attachment: fixed;
    }
    
    .main-header {
        text-align: center;
        color: #FFD700;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
        background: rgba(0,0,0,0.3);
        padding: 20px;
        border-radius: 15px;
    }
    
    .tagline {
        text-align: center;
        color: #FFE4B5;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        background: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 10px;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        max-height: 600px;
        overflow-y: auto;
        border: 2px solid rgba(255,215,0,0.3);
    }
    
    .luffy-response {
        background: linear-gradient(135deg, #FFE5B4, #FFCCCB);
        border-left: 5px solid #FF6B35;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Comic Sans MS', cursive;
        color: #2C3E50;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #E6F3FF, #B3D9FF);
        border-left: 5px solid #2E8B57;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: #2C3E50;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .input-container {
        margin-top: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        border: 2px solid rgba(255,215,0,0.3);
    }
    
    /* Career buttons styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255,255,255,0.95);
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI - IMPROVED ERROR HANDLING
def initialize_openai():
    try:
        if "OPENAI_API_KEY" in st.secrets:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            return True
        else:
            st.error("🚨 OpenAI API key not found in secrets. Please add OPENAI_API_KEY to your Streamlit secrets.")
            st.info("Go to your Streamlit app settings → Secrets → Add: OPENAI_API_KEY = 'your-key-here'")
            st.stop()
            return False
    except Exception as e:
        st.error(f"🚨 Error initializing OpenAI: {str(e)}")
        st.stop()
        return False

# Only proceed if OpenAI is initialized
if not initialize_openai():
    st.stop()

LUFFY_SYSTEM_PROMPT = """
You are Monkey D. Luffy from One Piece, helping 12th standard students find their dream careers!

Your personality traits:
- Always enthusiastic and encouraging
- Use phrases like "That's so cool!", "Yosh!", "Let's go!", "Shishishi!"
- Mention dreams, adventures, and treasure when explaining careers
- Keep responses under 180 words
- Mention 3-4 specific career paths with skills needed
- Make it fun and exciting like an adventure

Stay in character and always be positive! End with an encouraging question.
"""

def get_luffy_response(user_message, chat_history):
    """Get response from Luffy with improved error handling"""
    try:
        # Build conversation context
        messages = [{"role": "system", "content": LUFFY_SYSTEM_PROMPT}]
        
        # Add recent chat history (last 4 messages to avoid token limits)
        for msg in chat_history[-4:]:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant", 
                    "content": msg["content"]
                })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})

        # Make API call with timeout handling
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
            presence_penalty=0.3,
            frequency_penalty=0.2
        )

        return response.choices[0].message.content.strip()

    except openai.error.RateLimitError:
        return "🚨 Whoa! Too many requests, matey! Wait a moment and try again. Even pirates need to rest! 🏴‍☠️"
    except openai.error.APIError as e:
        return f"🚨 API adventure failed! Error: {str(e)[:100]}... Let's try again!"
    except Exception as e:
        return f"🚨 Unexpected storm! Error: {str(e)[:100]}... But don't give up on your dreams!"

# Initialize chat history - FIXED TO PREVENT LOOPS
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "🏴‍☠️ Yosh! I'm Luffy, your career adventure captain! Tell me what subjects you love and I'll help you find your treasure career! What's your favorite subject? ⚓"
    }]

# Initialize processing flag to prevent multiple submissions
if "processing" not in st.session_state:
    st.session_state.processing = False

# Main layout
st.markdown('<h1 class="main-header">🏴‍☠️ Career Navigator</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Set Sail for Your Dream Career Adventure! 🏴‍☠️</p>', unsafe_allow_html=True)

# Career exploration quick buttons
st.markdown("### 🗺️ Quick Career Exploration:")
career_cols = st.columns(6)
careers = [
    ("🏗️", "Engineering", "I'm interested in engineering and building cool things"),
    ("⚕️", "Medical", "I want to help people through medical careers"),
    ("💼", "Business", "Tell me about business and finance careers"),
    ("🎨", "Creative", "I love arts, design and creative fields"),
    ("🔬", "Science", "I'm passionate about science and research"),
    ("👩‍🏫", "Education", "I want to teach and inspire others")
]

# Handle career button clicks - FIXED TO PREVENT LOOPS
for i, (icon, name, prompt) in enumerate(careers):
    with career_cols[i]:
        if st.button(f"{icon}\n{name}", key=f"career_{i}", help=f"Explore {name} careers"):
            if not st.session_state.processing:
                st.session_state.processing = True
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Get response without causing rerun loop
                with st.spinner("🏴‍☠️ Captain Luffy is charting your career course..."):
                    luffy_response = get_luffy_response(prompt, st.session_state.messages[:-1])
                    st.session_state.messages.append({"role": "assistant", "content": luffy_response})
                
                st.session_state.processing = False
                st.rerun()

st.markdown("---")

# Chat interface
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Display chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "assistant":
            st.markdown(f'''
            <div class="luffy-response">
                🏴‍☠️ <strong>Captain Luffy:</strong><br>
                {message["content"]}
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="user-message">
                ⚓ <strong>You:</strong><br>
                {message["content"]}
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Input form - FIXED TO PREVENT MULTIPLE SUBMISSIONS
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Ask Captain Luffy about careers:", 
            placeholder="e.g., I love math and want to help people...",
            disabled=st.session_state.processing
        )
        submit_button = st.form_submit_button(
            "🚀 Send Message" if not st.session_state.processing else "⏳ Processing...", 
            disabled=st.session_state.processing
        )
        
        if submit_button and user_input and not st.session_state.processing:
            st.session_state.processing = True
            
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get Luffy's response
            with st.spinner("🏴‍☠️ Captain Luffy is navigating your career seas..."):
                luffy_response = get_luffy_response(user_input, st.session_state.messages[:-1])
                st.session_state.messages.append({"role": "assistant", "content": luffy_response})
            
            st.session_state.processing = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with helpful information
with st.sidebar:
    st.markdown("### 🗺️ Navigation Guide")
    st.info("""
    💡 **Ask Captain Luffy about:**
    - Your favorite school subjects
    - Dream jobs and careers
    - Skills you want to develop
    - College and education paths
    - What makes you excited!
    """)
    
    st.markdown("### ⚓ Adventure Tips")
    st.success("""
    🌟 **Best Questions:**
    - "I love [subject], what careers use this?"
    - "I want to help people, what can I do?"
    - "I'm creative, show me career paths!"
    - "What skills do I need for [career]?"
    """)
    
    st.markdown("### 🔧 Ship Maintenance")
    if st.button("🧹 Clear Chat History", help="Start a fresh conversation"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "🏴‍☠️ Yosh! I'm Luffy, your career adventure captain! Tell me what subjects you love and I'll help you find your treasure career! What's your favorite subject? ⚓"
        }]
        st.session_state.processing = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("*Built with ❤️ for future adventurers!*")