import streamlit as st
import openai

# Configure the page
st.set_page_config(
    page_title="Career Navigator - Set Sail for Your Dream Career!",
    page_icon="🏴‍☠️",
    layout="wide"
)

# SUPER SIMPLE CSS - No background images, no blinking
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }
    
    .main-header {
        text-align: center;
        color: #FF6B35;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .tagline {
        text-align: center;
        color: #2E8B57;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .hero-section {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px solid #dee2e6;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI
def setup_openai():
    try:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        return True
    except:
        st.error("🚨 Please add OPENAI_API_KEY to your Streamlit secrets")
        return False

if not setup_openai():
    st.stop()

# Simple Luffy response function
def get_luffy_response(user_message):
    try:
        system_prompt = """You are Monkey D. Luffy from One Piece, helping 12th grade students explore careers!
        - Be enthusiastic and use phrases like "Yosh!", "That's awesome!", "Let's go!"
        - Mention dreams, adventures, and finding treasure (careers)
        - Keep responses under 150 words
        - Suggest 3-4 specific career paths with skills needed
        - Always end with an encouraging question"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=180,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"🚨 Adventure interrupted! Error: {str(e)[:50]}... Try again, nakama!"

# Initialize session state ONCE
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🏴‍☠️ Yosh! I'm Luffy, your career adventure guide! What subjects do you love in school? Tell me about your interests and I'll help you discover amazing career paths! ⚓"}
    ]

# App header
st.markdown('<h1 class="main-header">🏴‍☠️ Career Navigator</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Discover Your Dream Career with AI Guidance! 🚀</p>', unsafe_allow_html=True)

# Hero section with simple graphic representation
st.markdown("""
<div class="hero-section">
    <div style="font-size: 4rem; margin-bottom: 1rem;">
        👨‍🎓🤖💭💼🎯
    </div>
    <h3 style="color: #495057; margin-bottom: 1rem;">Student + AI = Career Discovery</h3>
    <p style="color: #6c757d; font-size: 1.1rem;">
        Ask Captain Luffy about your interests, subjects you enjoy, or career goals.<br>
        Get personalized guidance powered by AI to find your perfect career path! 🌟
    </p>
</div>
""", unsafe_allow_html=True)

# Clean, simple chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages using Streamlit's native chat elements
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🏴‍☠️"):
            st.write(message["content"])
    else:
        with st.chat_message("user", avatar="👨‍🎓"):
            st.write(message["content"])

# Chat input - Clean and simple
if prompt := st.chat_input("Ask Luffy about careers, subjects, or your interests..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user", avatar="👨‍🎓"):
        st.write(prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant", avatar="🏴‍☠️"):
        with st.spinner("🏴‍☠️ Luffy is thinking..."):
            response = get_luffy_response(prompt)
            st.write(response)
    
    # Add assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('</div>', unsafe_allow_html=True)

# Clean sidebar
with st.sidebar:
    st.markdown("### 🗺️ How to Use")
    st.info("""
    **Simply ask Luffy about:**
    - Your favorite school subjects
    - Career fields that interest you
    - Skills you want to develop
    - Dream jobs you're curious about
    """)
    
    st.markdown("### 💡 Example Questions")
    st.success("""
    - "I love math and physics, what careers use these?"
    - "I want to help people, what options do I have?"
    - "I'm interested in technology, show me career paths"
    - "What skills do I need to become a doctor?"
    """)
    
    st.markdown("---")
    
    if st.button("🧹 Start Fresh Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "🏴‍☠️ Yosh! I'm Luffy, your career adventure guide! What subjects do you love in school? Tell me about your interests and I'll help you discover amazing career paths! ⚓"}
        ]
    
    st.markdown("---")
    st.markdown("*Built with ❤️ for students exploring their future!*")