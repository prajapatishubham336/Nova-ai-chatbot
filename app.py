
import os
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq, APIError, RateLimitError, AuthenticationError

# CONFIGURATION
load_dotenv()
st.set_page_config(
    page_title="Nova AI | Intelligent Chat",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
SYSTEM_PROMPT = """
You are Nova, a helpful, intelligent AI assistant.
Give accurate, clear, and useful answers.
Use Markdown formatting when it improves readability.
For code questions, provide complete and understandable examples.
If you are uncertain, say so instead of inventing facts.
Remember the conversation context provided in the messages.
"""

# CUSTOM UI
st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stAppViewContainer"] {
    background: var(--background-color);
}

.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 5rem;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,.2);
}

.brand {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
    padding: 8px 0 20px 0;
}

.brand span {
    color: #818cf8;
}

.hero {
    text-align: center;
    padding: 42px 12px 24px 12px;
}

.hero h1 {
    font-size: clamp(32px, 5vw, 48px);
    font-weight: 800;
    letter-spacing: -1.5px;
}

.hero p {
    color: var(--text-color);
    opacity: .7;
    font-size: 16px;
}

div.stButton > button {
    border-radius: 11px;
    min-height: 42px;
    transition: all .2s ease;
}

div.stButton > button:hover {
    border-color: #818cf8;
}

[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 12px;
}

[data-testid="stChatInput"] {
    border-radius: 16px;
}

.small-note {
    font-size: 12px;
    text-align: center;
    opacity: .6;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "chats" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.chats = {
        chat_id: {
            "title": "New conversation",
            "messages": [],
            "created": datetime.now().strftime("%d %b %Y, %H:%M"),
        }
    }
    st.session_state.active_chat = chat_id

if "active_chat" not in st.session_state:
    st.session_state.active_chat = next(iter(st.session_state.chats))

if st.session_state.active_chat not in st.session_state.chats:
    st.session_state.active_chat = next(iter(st.session_state.chats))

def new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New conversation",
        "messages": [],
        "created": datetime.now().strftime("%d %b %Y, %H:%M"),
    }
    st.session_state.active_chat = chat_id

def remove_chat(chat_id):
    st.session_state.chats.pop(chat_id, None)

    if not st.session_state.chats:
        new_chat()
    elif st.session_state.active_chat == chat_id:
        st.session_state.active_chat = next(
            iter(st.session_state.chats)
        )

def get_client():
    if not GROQ_API_KEY:
        raise RuntimeError(
            "The application is not configured. "
            "Please set GROQ_API_KEY in the .env file."
        )
    return Groq(api_key=GROQ_API_KEY)

def stream_answer(messages):
    client = get_client()

    stream = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages,],
        temperature=0.7,
        max_completion_tokens=4096,
        stream=True,
    )

    for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        content = delta.content

        if content:
            yield content

# SIDEBAR
with st.sidebar:
    st.markdown(
        '<div class="brand">✦ Nova<span> AI</span></div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "＋  New chat",
        use_container_width=True,
        type="primary",):
        new_chat()
        st.rerun()

    st.divider()
    st.markdown("**YOUR CONVERSATIONS**")

    chat_items = list(st.session_state.chats.items())[::-1]

    for chat_id, chat in chat_items:
        col1, col2 = st.columns([5, 1])

        with col1:
            label = chat["title"][:28]
            if not chat["messages"]:
                label = "✧ " + label

            if st.button(
                label,
                key=f"select_{chat_id}",
                use_container_width=True,
                type=("primary"
                    if chat_id == st.session_state.active_chat
                    else "secondary"
                ),
            ):
                st.session_state.active_chat = chat_id
                st.rerun()

        with col2:
            if st.button(
                "×",
                key=f"delete_{chat_id}",
                help="Delete conversation",
            ):
                remove_chat(chat_id)
                st.rerun()

    st.divider()

    if st.button("🗑 Clear current chat", use_container_width=True):
        st.session_state.chats[
            st.session_state.active_chat
        ]["messages"] = []
        st.session_state.chats[
            st.session_state.active_chat
        ]["title"] = "New conversation"
        st.rerun()

    st.markdown(
        '<div class="small-note">Nova AI · Powered by Groq</div>',
        unsafe_allow_html=True,
    )

# MAIN CHAT
active = st.session_state.chats[st.session_state.active_chat]
messages = active["messages"]

if not messages:
    st.markdown("""
    <div class="hero">
        <h1>What can I help you with?</h1>
        <p>Ask a question, explore an idea, or build something amazing.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ✨ Try asking")

    suggestions = [
        "Explain machine learning simply",
        "Build a Python project",
        "Help me prepare for interviews",
    ]

    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(
                suggestion,
                key=f"suggestion_{i}",
                use_container_width=True,
            ):
                st.session_state.pending_question = suggestion
                st.rerun()
else:
    st.title("✦ " + active["title"])

# Render previous messages
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

pending = st.session_state.pop("pending_question", None)
question = st.chat_input("Message Nova AI...")

if pending:
    question = pending

if question and question.strip():
    question = question.strip()

    messages.append({
        "role": "user",
        "content": question,
    })

    if active["title"] == "New conversation":
        active["title"] = question[:32]
        if len(question) > 32:
            active["title"] += "…"

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner(""):
                answer = st.write_stream(
                    stream_answer(messages)
                )

            if not answer:
                answer = "I couldn't generate a response. Please try again."
                st.markdown(answer)

            messages.append({
                "role": "assistant",
                "content": answer,
            })

        except AuthenticationError:
            st.error(
                "Authentication failed. Check the API key "
                "in the server's .env configuration."
            )
        except RateLimitError:
            st.error(
                "The API rate limit was reached. "
                "Please wait a moment and try again."
            )
        except RuntimeError as error:
            st.error(str(error))
        except APIError as error:
            st.error(
                "The AI service returned an error. "
                "Check the configured model and try again."
            )
        except Exception:
            st.error(
                "Something went wrong while generating the answer. "
                "Please try again."
            )

st.markdown(
    '<div class="small-note">'
    'AI responses can contain mistakes. Verify important information.'
    '</div>',
    unsafe_allow_html=True,
)
