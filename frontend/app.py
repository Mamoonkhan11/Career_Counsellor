"""
AI Career Counsellor - Streamlit Frontend
Simple and clear chat interface for career guidance
"""

import streamlit as st
import requests
import json
import time
import uuid
from datetime import datetime
import base64

# Configure page
st.set_page_config(
    page_title="AI Career Counsellor",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimal CSS for clean Streamlit design
def load_css():
    st.markdown("""
    <style>
    /* Minimal styling for clean look */
    .message-bubble {
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 75%;
        word-wrap: break-word;
        line-height: 1.4;
        font-size: 16px;
    }

    .user-message {
        background: #007bff;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
        text-align: right;
    }

    .bot-message {
        background: #f8f9fa;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 5px;
        border: 1px solid #dee2e6;
    }

    .typing-indicator {
        display: inline-block;
        padding: 12px 16px;
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 12px;
        margin: 8px 0;
        border-bottom-left-radius: 5px;
    }

    .typing-dots {
        display: inline-flex;
        gap: 4px;
    }

    .typing-dot {
        width: 6px;
        height: 6px;
        background: #6c757d;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }

    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    .career-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .career-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
        color: #333;
    }

    .match-score {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .high-match { background: #d4edda; color: #155724; }
    .medium-match { background: #fff3cd; color: #856404; }
    .low-match { background: #f8d7da; color: #721c24; }

    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Clean up spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'is_typing' not in st.session_state:
    st.session_state.is_typing = False

# Rasa server configuration
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

def send_message_to_rasa(message, sender_id):
    """Send message to Rasa server and get response with improved error handling"""
    try:
        payload = {
            "sender": sender_id,
            "message": message
        }

        # Try to connect with retry logic
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                response = requests.post(RASA_SERVER_URL, json=payload, timeout=15)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return [{"text": "❌ Backend service not found. The AI server may not be running properly. Please restart the application."}]
                elif response.status_code >= 500:
                    return [{"text": "🔧 Server error. The AI backend is experiencing issues. Please try again in a moment."}]
                else:
                    return [{"text": f"⚠️ Unexpected response from server (Status: {response.status_code}). Please try again."}]
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return [{"text": "🔌 Connection failed. The AI backend server is not responding. Please check if the application is running properly and try again."}]
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return [{"text": "⏰ Request timed out. The AI backend is taking too long to respond. Please try again."}]
            except Exception as e:
                return [{"text": f"⚠️ An unexpected error occurred: {str(e)}. Please try again."}]

        return [{"text": "❌ Unable to connect to AI backend after multiple attempts. Please restart the application."}]

    except Exception as e:
        return [{"text": f"🚨 Critical error: {str(e)}. Please restart the application and try again."}]

def render_message(message, is_user=False):
    """Render a chat message with clean styling"""
    if is_user:
        # User message - right aligned
        st.markdown(f"""
        <div style="text-align: right;">
            <div class="message-bubble user-message">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Check if message contains career recommendations
        if "🥇" in message or "🥈" in message or "🥉" in message:
            render_career_recommendations(message)
        else:
            # Bot message - left aligned
            st.markdown(f"""
            <div class="message-bubble bot-message">
                {message}
            </div>
            """, unsafe_allow_html=True)

def render_career_recommendations(message):
    """Parse and render career recommendations using Streamlit components"""
    lines = message.split('\n')
    recommendations = []
    current_rec = {}

    for line in lines:
        if line.startswith('🥇') or line.startswith('🥈') or line.startswith('🥉'):
            if current_rec:
                recommendations.append(current_rec)
            current_rec = {'title': line.strip(), 'details': []}
        elif current_rec:
            current_rec['details'].append(line)

    if current_rec:
        recommendations.append(current_rec)

    # Render each recommendation using Streamlit components
    for rec in recommendations:
        title = rec['title']
        details = '\n'.join(rec['details'])

        # Extract match score for styling
        if "High confidence" in details or "80%" in details or "90%" in details:
            score_color = "🟢"
            score_text = "High Match"
        elif "Low" in details or "20%" in details or "30%" in details:
            score_color = "🔴"
            score_text = "Low Match"
        else:
            score_color = "🟡"
            score_text = "Medium Match"

        # Use Streamlit's expander for clean collapsible cards
        with st.expander(f"{title} - {score_color} {score_text}", expanded=False):
            st.markdown(details)

def render_typing_indicator():
    """Render typing indicator animation"""
    st.markdown("""
    <div class="typing-indicator">
        <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def check_backend_connection():
    """Check if the Rasa backend is accessible"""
    try:
        response = requests.get("http://localhost:5005/", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    # Load minimal CSS
    load_css()

    # Page header
    st.title("🎯 AI Career Counsellor")
    st.markdown("*Your intelligent guide to discovering fulfilling career paths*")

    # Check backend connection
    backend_connected = check_backend_connection()

    # Connection status
    if not backend_connected:
        st.error("⚠️ **Backend Connection Issue:** The AI backend server is not responding. Please make sure both services are running.")
    else:
        st.success("✅ **Connected:** AI backend is running and ready to help!")

    # Main layout with columns for better structure
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # Chat container using Streamlit's container
        chat_container = st.container(height=500, border=True)

        with chat_container:
            # Display chat messages
            for message in st.session_state.messages:
                render_message(message['content'], message['is_user'])

            # Show typing indicator if bot is responding
            if st.session_state.is_typing:
                render_typing_indicator()

        # Input section
        st.markdown("### 💬 Share your thoughts")

        # Input form using Streamlit's form
        with st.form(key='message_form', clear_on_submit=True, border=False):
            col_input, col_button = st.columns([4, 1])

            with col_input:
                user_input = st.text_input(
                    "What are your interests, skills, or career goals?",
                    key="user_input",
                    placeholder="e.g., I'm interested in technology and problem-solving",
                    label_visibility="collapsed"
                )

            with col_button:
                submit_button = st.form_submit_button(
                    "Send",
                    use_container_width=True,
                    type="primary"
                )

        # Handle form submission
        if submit_button and user_input.strip():
            # Add user message
            st.session_state.messages.append({
                'content': user_input.strip(),
                'is_user': True,
                'timestamp': datetime.now()
            })

            # Show typing indicator
            st.session_state.is_typing = True

            # Get bot response
            bot_responses = send_message_to_rasa(user_input.strip(), st.session_state.session_id)

            # Hide typing indicator
            st.session_state.is_typing = False

            # Add bot responses
            for response in bot_responses:
                if 'text' in response:
                    st.session_state.messages.append({
                        'content': response['text'],
                        'is_user': False,
                        'timestamp': datetime.now()
                    })

            # Rerun to update UI
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
        "Built with ❤️ using Rasa & Streamlit • AI Career Guidance for Everyone"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
