import streamlit as st
import requests
import io
import html
import base64
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS

# Set layout and request expanded sidebar
st.set_page_config(
    page_title="Echoes of Time",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(
    """
    <style>
    /* 1. Beige Background for everything including sidebar */
    .stApp,
    [data-testid="stHeader"],
    [data-testid="stBottomBlock"],
    div[data-testid="stBottom"],
    .stBottom,
    section[data-testid="stSidebar"] {
        background-color: #F5F5DC !important;
    }

    /* 2. Sidebar re-open arrow (old and new Streamlit test ids) */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stExpandSidebarButton"] {
        display: block !important;
        visibility: visible !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 100000 !important;
    }

    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stExpandSidebarButton"] {
        background-color: #6B8E23 !important;
        color: white !important;
        border-radius: 8px !important;
        width: 36px !important;
        height: 36px !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
    }

    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stExpandSidebarButton"] svg {
        color: white !important;
        fill: white !important;
        stroke: white !important;
    }

    /* Close arrow inside the sidebar */
    [data-testid="stSidebarCollapseButton"] button {
        color: #6B8E23 !important;
    }
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #6B8E23 !important;
        stroke: #6B8E23 !important;
    }

    /* 3. Hide only the deploy button and menus, NOT the whole toolbar */
    [data-testid="stAppDeployButton"],
    [data-testid="stMainMenu"],
    #MainMenu,
    footer {
        display: none !important;
    }

    /* Hide chat avatar icons and title links */
    [data-testid="stChatMessageAvatar"],
    [data-testid="stChatMessage"] > div:first-child,
    h1 a, h2 a, h3 a {
        display: none !important;
    }

    div[data-testid="stBottom"] > div {
        background-color: transparent !important;
    }

    /* 4. Chat Input (pinned at the bottom, leaves room on the left for the mic) */
    [data-testid="stBottom"] [data-testid="stChatInput"] {
        margin-left: 60px !important;
        width: calc(100% - 60px) !important;
    }

    [data-testid="stChatInput"] {
        background-color: #6B8E23 !important;
        border-radius: 25px !important;
        border: none !important;
    }

    [data-testid="stChatInput"] div,
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] button {
        background-color: transparent !important;
        color: white !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #E8E8E8 !important;
        opacity: 1 !important;
    }

    /* 5. Custom Buttons */
    div.stButton > button {
        background-color: #6B8E23 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: background-color 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #556B2F !important;
        color: white !important;
    }

    /* 6. AI Text Box */
    .ai-text {
        background-color: rgba(0, 0, 0, 0.05) !important;
        color: #556B2F !important;
        font-weight: 800 !important;
        white-space: pre-wrap !important;
        padding: 1rem !important;
        border-radius: 0.5rem !important;
        display: block !important;
    }

    .ai-text p {
        color: #556B2F !important;
        margin: 0 !important;
    }

    /* 7. Mic button pinned at the bottom-left, next to the chat input */
    .st-key-mic_box {
        position: fixed !important;
        bottom: 22px !important;
        left: max(12px, calc(50% - 368px)) !important;
        width: 52px !important;
        z-index: 999999 !important;
        background-color: #F5F5DC !important;
        border-radius: 12px;
    }

    .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) .st-key-mic_box {
        left: max(348px, calc(50% + 168px - 368px)) !important;
    }

    .st-key-mic_box iframe {
        mix-blend-mode: multiply;
    }

    /* 8. Read-aloud toggle: themed card, bold label, olive switch */
    .st-key-auto_read_box {
        background-color: rgba(107, 142, 35, 0.12) !important;
        border: 2px solid #6B8E23 !important;
        border-radius: 14px !important;
        padding: 10px 16px !important;
        margin: 6px 0 14px 0 !important;
    }

    .st-key-auto_read_box label p,
    .st-key-auto_read_box label span,
    .st-key-auto_read_box label div[data-testid="stMarkdownContainer"] p {
        color: #556B2F !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }

    .st-key-auto_read_box label[data-baseweb="checkbox"] > div:first-child {
        background-color: #B5BE9A !important;
        transform: scale(1.25);
        transform-origin: left center;
        margin-right: 10px !important;
    }

    .st-key-auto_read_box label[data-baseweb="checkbox"]:has(input:checked) > div:first-child {
        background-color: #6B8E23 !important;
    }

    .st-key-auto_read_box label[data-baseweb="checkbox"] > div:first-child > div {
        background-color: white !important;
        box-shadow: 0px 1px 4px rgba(0,0,0,0.3) !important;
    }

    /* 9. BOOK THEME for the final memoir chapter */
    .book-page {
        position: relative;
        background-color: #FBF6E6;
        background-image:
            linear-gradient(to right, rgba(90, 60, 20, 0.18) 0px, rgba(90, 60, 20, 0.05) 14px, rgba(90, 60, 20, 0) 40px),
            repeating-linear-gradient(to bottom, rgba(120, 90, 40, 0.025) 0px, rgba(120, 90, 40, 0.025) 1px, transparent 1px, transparent 4px);
        border: 1px solid #D9C9A0;
        border-radius: 4px 10px 10px 4px;
        box-shadow: 0 10px 30px rgba(60, 40, 10, 0.25), inset 0 0 60px rgba(150, 110, 50, 0.12);
        padding: 2.6rem 3rem 2rem 3rem;
        margin: 1.5rem 0 2rem 0;
        color: #31333F;
        font-family: 'Source Sans Pro', 'Source Sans 3', -apple-system, 'Segoe UI', Arial, sans-serif;
    }

    .book-kicker {
        text-align: left;
        text-transform: uppercase;
        letter-spacing: 0.25em;
        font-size: 0.8rem;
        color: #8A7A55;
        margin-bottom: 0.6rem;
    }

    .book-title {
        text-align: left;
        font-family: 'Source Sans Pro', 'Source Sans 3', -apple-system, 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        font-size: 2rem;
        line-height: 1.2;
        color: #31333F;
        margin: 0 0 0.4rem 0;
    }

    .book-meta {
        text-align: left;
        font-style: normal;
        font-size: 0.85rem;
        color: #8A8A8A;
        margin-bottom: 1.4rem;
    }

    .book-text p {
        font-family: 'Source Sans Pro', 'Source Sans 3', -apple-system, 'Segoe UI', Arial, sans-serif;
        font-size: 1.05rem;
        line-height: 1.65;
        text-align: left;
        text-indent: 0;
        margin: 0 0 0.9rem 0;
        color: #31333F;
    }

    .book-wisdom {
        margin: 1.4rem 0 0.6rem 0;
        padding: 0.9rem 1.2rem;
        border: 1px solid #D9C9A0;
        border-radius: 8px;
        background: rgba(139, 122, 85, 0.08);
        font-size: 1.05rem;
        line-height: 1.55;
        color: #556B2F;
    }

    .book-wisdom span {
        display: block;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-size: 0.75rem;
        font-weight: 700;
        color: #8A7A55;
        margin-bottom: 0.3rem;
    }

    .book-plate {
        margin: 1.6rem auto 0.4rem auto;
        padding: 0.7rem;
        background: #FFFDF5;
        border: 1px solid #D9C9A0;
        box-shadow: 0 4px 14px rgba(60, 40, 10, 0.25);
        transform: rotate(-0.6deg);
        max-width: 92%;
    }

    .book-plate img {
        display: block;
        width: 100%;
        filter: sepia(0.18) contrast(1.02);
    }

    .book-plate-caption {
        text-align: center;
        font-size: 0.85rem;
        color: #8A8A8A;
        margin: 0.6rem 0 0 0;
    }

    .book-footer {
        text-align: center;
        color: #8A7A55;
        font-size: 0.85rem;
        margin-top: 1.6rem;
        letter-spacing: 0.25em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Echoes of Time")
st.markdown("Share a cherished memory in a guided interview, and watch your words transform into a beautifully written chapter and a vintage 35mm photograph.")

# ========================================================
# USER SETTING: AUTOMATIC READER OR READ BY ONESELF
# ========================================================
with st.container(key="auto_read_box"):
    auto_read = st.toggle(
        "🔊 Read replies aloud automatically",
        value=True,
        help="Turn off if you want to read by yourself."
    )

# ========================================================
# SIDEBAR CONFIGURATION (open it with the arrow at top-left)
# ========================================================
with st.sidebar:
    st.header("⚙️ Backend URLs")
    KAGGLE_QWEN_URL = st.text_input(
        "Kaggle Qwen ngrok URL",
        "https://obstruct-eardrum-surely.ngrok-free.dev"
    )
    COLAB_SDXL_URL = st.text_input(
        "Colab SDXL ngrok URL",
        "https://stopped-barricade-railing.ngrok-free.dev/generate-image"
    )

NGROK_HEADERS = {"ngrok-skip-browser-warning": "true"}


# Helper function to transcribe voice input
def transcribe_audio(audio_bytes):
    recognizer = sr.Recognizer()
    audio_file = io.BytesIO(audio_bytes)
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='en-US')
            return text
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try again.")
            return None
        except sr.RequestError:
            st.error("Speech recognition service is unavailable.")
            return None


# Helper function for text-to-speech audio generation
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


# Helper: build the book page as HTML (no indentation, so Markdown won't treat it as code)
def build_book_html(chap, image_path=None):
    title = html.escape(str(chap.get("title") or "Untitled"))
    era = html.escape(str(chap.get("life_era") or ""))
    location = html.escape(str(chap.get("location") or ""))
    wisdom = html.escape(str(chap.get("core_wisdom") or ""))

    meta_parts = []
    if era:
        meta_parts.append(f"Era: {era}")
    if location:
        meta_parts.append(f"Location: {location}")
    meta = " | ".join(meta_parts)

    narrative = str(chap.get("narrative_text") or "")
    paragraphs = [p.strip() for p in narrative.replace("\r", "").split("\n") if p.strip()]
    paragraphs_html = "".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)

    parts = [
        '<div class="book-page">',
        '<div class="book-kicker">A Memoir Chapter</div>',
        f'<div class="book-title">{title}</div>',
        f'<div class="book-meta">{meta}</div>' if meta else "",
        f'<div class="book-text">{paragraphs_html}</div>',
    ]

    # Core Wisdom comes BEFORE the photo
    if wisdom:
        parts.append(f'<div class="book-wisdom"><span>Core Wisdom</span>{wisdom}</div>')

    if image_path:
        try:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            parts.append(
                '<div class="book-plate">'
                f'<img src="data:image/png;base64,{img_b64}" alt="Illustration"/>'
                '<div class="book-plate-caption">AI Generated 35mm Film Illustration</div>'
                '</div>'
            )
        except Exception:
            pass

    parts.append('<div class="book-footer">— The End of the Chapter —</div>')
    parts.append('</div>')
    return "".join(parts)


# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to the Memoir Interview. Tell me a memory from your past, or describe a place that means a lot to you."}
    ]

# Play the newest AI audio only if auto_read is turned ON
if auto_read and "latest_ai_audio" in st.session_state:
    st.audio(st.session_state.latest_ai_audio, format="audio/mp3", autoplay=True)
    del st.session_state.latest_ai_audio
elif not auto_read and "latest_ai_audio" in st.session_state:
    del st.session_state.latest_ai_audio

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(f'<div class="ai-text">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.write(msg["content"])

# ==========================================
# USER INPUT (VOICE & TEXT) - pinned at the bottom
# ==========================================
with st.container(key="mic_box"):
    audio_bytes = audio_recorder(
        text="",
        icon_name="microphone",
        icon_size="2x",
        neutral_color="#6B8E23",
        recording_color="#8B0000"
    )

user_text = st.chat_input("Type your memory here...")

spoken_text = None
if audio_bytes:
    if "last_audio" not in st.session_state or st.session_state.last_audio != audio_bytes:
        st.session_state.last_audio = audio_bytes
        with st.spinner("Transcribing your voice..."):
            spoken_text = transcribe_audio(audio_bytes)

final_input = spoken_text if spoken_text else user_text

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.write(final_input)

    # Ask Kaggle Qwen for the next live interview question
    with st.spinner("Qwen is thinking of a follow-up question..."):
        try:
            res = requests.post(
                f"{KAGGLE_QWEN_URL.rstrip('/')}/ask-biographer",
                json={"messages": st.session_state.messages},
                headers=NGROK_HEADERS,
                timeout=60
            )
            res.raise_for_status()
            next_question = res.json()["question"]

        except Exception as e:
            st.error(f"Qwen failed to reply. Check your Kaggle notebook! Error: {e}")
            st.stop()

    # Append and display Qwen's response
    st.session_state.messages.append({"role": "assistant", "content": next_question})
    with st.chat_message("assistant"):
        st.markdown(f'<div class="ai-text">{next_question}</div>', unsafe_allow_html=True)

    # Generate speech only if auto_read is enabled
    if auto_read:
        st.session_state.latest_ai_audio = text_to_speech(next_question)

    st.rerun()

st.divider()

# ==========================================
# BUTTON LOGIC FOR GENERATION
# ==========================================
col1, col2 = st.columns(2)

with col1:
    if st.button("See the memory"):
        full_transcript = "\n".join(
            [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages]
        )

        # Step A: Get the JSON from Kaggle
        with st.spinner("Extracting memory details..."):
            try:
                res_qwen = requests.post(
                    f"{KAGGLE_QWEN_URL.rstrip('/')}/finalize",
                    json={"transcript": full_transcript},
                    headers=NGROK_HEADERS,
                    timeout=120
                )
                if res_qwen.status_code == 200:
                    st.session_state.memory_json = res_qwen.json()
                else:
                    st.error(f"Kaggle Error: {res_qwen.status_code}\n{res_qwen.text}")
                    st.stop()
            except Exception as e:
                st.error(f"Connection failed: {e}")
                st.stop()

        # Step B: Generate the image on Colab
        with st.spinner("Painting your memory..."):
            try:
                res_sdxl = requests.post(
                    COLAB_SDXL_URL,
                    json=st.session_state.memory_json,
                    headers=NGROK_HEADERS,
                    timeout=180
                )
                if res_sdxl.status_code == 200:
                    with open("streamlit_output.png", "wb") as f:
                        f.write(res_sdxl.content)
                    st.session_state.memory_image = "streamlit_output.png"
                    st.success("✅ Memoir structured and illustrated successfully!")
                else:
                    st.error(f"Colab Error: {res_sdxl.status_code}\n{res_sdxl.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

with col2:
    if "memory_json" in st.session_state:
        if st.button("Regenerate Photo"):
            with st.spinner("Repainting the scene..."):
                try:
                    res_sdxl = requests.post(
                        COLAB_SDXL_URL,
                        json=st.session_state.memory_json,
                        headers=NGROK_HEADERS,
                        timeout=180
                    )
                    if res_sdxl.status_code == 200:
                        with open("streamlit_output.png", "wb") as f:
                            f.write(res_sdxl.content)
                        st.session_state.memory_image = "streamlit_output.png"
                        st.success("✅ Photo regenerated successfully!")
                    else:
                        st.error(f"Colab Error: {res_sdxl.status_code}\n{res_sdxl.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

# ==========================================
# DISPLAY FINAL RESULTS (BOOK THEME)
# ==========================================
if "memory_json" in st.session_state:
    st.divider()
    book_html = build_book_html(
        st.session_state.memory_json,
        st.session_state.get("memory_image")
    )
    st.markdown(book_html, unsafe_allow_html=True)