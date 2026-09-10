
# ============================================================
# NEXUS AI — STREAMING AI PROBLEM SOLVER & IMAGE GENERATOR
# Single-file Streamlit application
# ============================================================

import os
import html
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# CONFIGURATION
# ============================================================

GROQ_MODEL = "openai/gpt-oss-120b"
GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_IMAGE_MODEL = "imagen-3.0-generate-002"

APP_NAME = "NEXUS AI"
APP_TAGLINE = "Think smarter. Solve faster."


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="auto",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "messages": [],
    "theme_mode": "Dark",
    "color_theme": "Rose",
    "app_mode": "AI Problem Solver",
    "response_length": "Balanced",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SECRETS RETRIEVAL
# ============================================================

def get_secret(name):
    try:
        from google.colab import userdata
        value = userdata.get(name)
        if value:
            return str(value).strip()
    except Exception:
        pass

    try:
        value = st.secrets.get(name)
        if value:
            return str(value).strip()
    except Exception:
        pass

    value = os.getenv(name)
    if value:
        return str(value).strip()

    return ""


def safe_error(error):
    text = str(error)
    secret_names = ["GROQ_API_KEY", "GEMINI_API_KEY", "GITHUB_TOKEN"]
    for secret_name in secret_names:
        secret = get_secret(secret_name)
        if secret:
            text = text.replace(secret, "[hidden]")
    return text


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

COLOR_THEMES = {
    "Ocean": {
        "primary": "#2563EB",
        "primary_dark": "#1D4ED8",
        "soft": "rgba(37, 99, 235, 0.15)",
        "gradient_a": "#2563EB",
        "gradient_b": "#06B6D4",
    },
    "Purple": {
        "primary": "#7C3AED",
        "primary_dark": "#6D28D9",
        "soft": "rgba(124, 58, 237, 0.15)",
        "gradient_a": "#7C3AED",
        "gradient_b": "#EC4899",
    },
    "Emerald": {
        "primary": "#059669",
        "primary_dark": "#047857",
        "soft": "rgba(5, 150, 105, 0.15)",
        "gradient_a": "#059669",
        "gradient_b": "#14B8A6",
    },
    "Rose": {
        "primary": "#E11D48",
        "primary_dark": "#BE123C",
        "soft": "rgba(225, 29, 72, 0.15)",
        "gradient_a": "#E11D48",
        "gradient_b": "#F97316",
    },
}

with st.sidebar:
    st.markdown(
        """
        <div class="nexus-brand">
            <div class="nexus-logo">🧠</div>
            <div class="nexus-title">NEXUS AI</div>
            <div style="color:var(--nexus-muted);font-size:0.85rem;">Think smarter. Solve faster.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.selectbox("Mode", ["AI Problem Solver", "AI Business Builder"], key="app_mode")
    st.selectbox("Response Length", ["Concise", "Balanced", "Detailed"], key="response_length")
    st.selectbox("Appearance", ["Dark", "Light"], key="theme_mode")
    st.selectbox("Accent Theme", list(COLOR_THEMES.keys()), key="color_theme")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# ACTIVE THEME & DYNAMIC CSS INJECTION
# ============================================================

theme = COLOR_THEMES.get(st.session_state.color_theme, COLOR_THEMES["Rose"])

if st.session_state.theme_mode == "Dark":
    BG = "#0B1120"
    SURFACE = "#111827"
    SURFACE_2 = "#172033"
    TEXT = "#F8FAFC"
    MUTED = "#94A3B8"
    BORDER = "rgba(148,163,184,0.20)"
    SHADOW = "0 15px 45px rgba(0,0,0,0.30)"
    INPUT_BG = "#1E293B"
    INPUT_TEXT = "#FFFFFF"
    BOTTOM_DOCK = "#0B1120"
else:
    BG = "#F8FAFC"
    SURFACE = "#FFFFFF"
    SURFACE_2 = "#F1F5F9"
    TEXT = "#0F172A"
    MUTED = "#64748B"
    BORDER = "rgba(15,23,42,0.12)"
    SHADOW = "0 10px 30px rgba(15,23,42,0.06)"
    INPUT_BG = "#FFFFFF"
    INPUT_TEXT = "#0F172A"
    BOTTOM_DOCK = "#F8FAFC"

css = f"""
<style>
:root {{
    --nexus-primary: {theme["primary"]};
    --nexus-primary-dark: {theme["primary_dark"]};
    --nexus-soft: {theme["soft"]};
    --nexus-gradient-a: {theme["gradient_a"]};
    --nexus-gradient-b: {theme["gradient_b"]};
    --nexus-bg: {BG};
    --nexus-surface: {SURFACE};
    --nexus-surface-2: {SURFACE_2};
    --nexus-text: {TEXT};
    --nexus-muted: {MUTED};
    --nexus-border: {BORDER};
    --nexus-shadow: {SHADOW};
    --nexus-input-bg: {INPUT_BG};
    --nexus-input-text: {INPUT_TEXT};
    --nexus-bottom-dock: {BOTTOM_DOCK};
}}

/* Universal Background & Text Color Reset */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"] {{
    background-color: var(--nexus-bg) !important;
    color: var(--nexus-text) !important;
}}

.block-container {{
    padding-top: 4.5rem !important;
    padding-bottom: 7rem !important;
    max-width: 1200px !important;
}}

/* Base Typography Overrides */
.stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, label {{
    color: var(--nexus-text) !important;
}}

div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] > p,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] > ul > li {{
    color: var(--nexus-text) !important;
}}

/* Sidebar Theme Styling */
section[data-testid="stSidebar"] {{
    background-color: var(--nexus-surface-2) !important;
    border-right: 1px solid var(--nexus-border) !important;
}}

/* Dropdown / Selectbox Complete Theme Fix */
div[data-baseweb="select"] {{
    background-color: var(--nexus-input-bg) !important;
    border-radius: 12px !important;
}}

div[data-baseweb="select"] > div {{
    background-color: var(--nexus-input-bg) !important;
    color: var(--nexus-input-text) !important;
    border-radius: 12px !important;
    border: 1px solid var(--nexus-border) !important;
}}

div[data-baseweb="select"] span, div[data-baseweb="select"] svg {{
    color: var(--nexus-input-text) !important;
    fill: var(--nexus-input-text) !important;
}}

ul[role="listbox"] {{
    background-color: var(--nexus-surface) !important;
    border: 1px solid var(--nexus-border) !important;
}}

ul[role="listbox"] li {{
    color: var(--nexus-text) !important;
    background-color: var(--nexus-surface) !important;
}}

/* Bottom Floating Dock Container Styling Fix */
footer {{ visibility: hidden; }}
[data-testid="stBottom"], [data-testid="stBottom"] > div {{
    background-color: var(--nexus-bottom-dock) !important;
}}

/* Bottom Chat Input Fix */
[data-testid="stChatInput"] {{
    background-color: var(--nexus-surface) !important;
    border-radius: 16px !important;
    border: 1px solid var(--nexus-border) !important;
    box-shadow: var(--nexus-shadow) !important;
}}

[data-testid="stChatInput"] textarea {{
    color: var(--nexus-text) !important;
    -webkit-text-fill-color: var(--nexus-text) !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: var(--nexus-muted) !important;
    -webkit-text-fill-color: var(--nexus-muted) !important;
}}

[data-testid="stChatInput"] button svg {{
    fill: var(--nexus-text) !important;
}}

/* Quick Suggestions Button Text Fix */
.stButton > button {{
    background: linear-gradient(135deg, var(--nexus-gradient-a), var(--nexus-gradient-b)) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1) !important;
}}

.stButton > button * {{
    color: #FFFFFF !important;
}}

/* Mobile & Tablet Layout Adjustments */
@media (max-width: 768px) {{
    section[data-testid="stSidebar"] {{
        width: 85vw !important;
        max-width: 320px !important;
    }}
    .block-container {{
        padding-top: 3.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
    .hero-card {{
        padding: 1rem !important;
    }}
    .hero-title {{
        font-size: 1.3rem !important;
    }}
}}

.nexus-brand {{ text-align: center; padding: 0.5rem 0 1rem 0; }}
.nexus-logo {{ width: 56px; height: 56px; margin: 0 auto 0.5rem auto; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 28px; background: linear-gradient(135deg, var(--nexus-gradient-a), var(--nexus-gradient-b)); }}
.nexus-title {{ font-size: 1.8rem; font-weight: 800; background: linear-gradient(90deg, var(--nexus-gradient-a), var(--nexus-gradient-b)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}

.hero-card {{
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.25rem;
    border-radius: 18px;
    border: 1px solid var(--nexus-border);
    background: var(--nexus-surface);
    box-shadow: var(--nexus-shadow);
}}

.hero-title {{ font-size: 1.6rem; font-weight: 800; color: var(--nexus-text); margin-bottom: 0.2rem; }}
.hero-text {{ color: var(--nexus-muted); font-size: 0.9rem; }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


# ============================================================
# HERO HEADER
# ============================================================

hero_title = "Build smarter business ideas" if st.session_state.app_mode == "AI Business Builder" else "Solve any problem with AI"
hero_text = "Turn a business challenge into strategy." if st.session_state.app_mode == "AI Business Builder" else "Describe your problem or ask to generate an image."

st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-title">{html.escape(hero_title)}</div>
        <div class="hero-text">{html.escape(hero_text)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AI ENGINES & IMAGE DETECTION
# ============================================================

IMAGE_TRIGGERS = ["generate image", "create image", "draw", "make an image", "picture of", "tasveer", "image of", "photo of"]

def is_image_request(text):
    text_lower = text.lower()
    return any(trigger in text_lower for trigger in IMAGE_TRIGGERS)


def generate_gemini_image(prompt):
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing in secrets.")
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    result = client.models.generate_images(
        model=GEMINI_IMAGE_MODEL,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
        ),
    )
    for generated_image in result.generated_images:
        return generated_image.image.image_bytes
    return None


def response_instruction():
    l = st.session_state.response_length
    return "Keep it concise." if l == "Concise" else ("Provide a detailed answer with reasoning." if l == "Detailed" else "Give a balanced practical answer.")


def solve_math(problem):
    text = problem.strip()
    if not any(sym in text for sym in ["=", "+", "-", "*", "/", "^"]):
        return None
    try:
        import sympy as sp
        if "=" in text:
            left, right = text.split("=", 1)
            x = sp.symbols("x")
            res = sp.solve(sp.Eq(sp.sympify(left), sp.sympify(right)), x)
            return f"**Equation:** `{text}`\n\n**Result:** `{res}`"
        simplified = sp.simplify(sp.sympify(text.replace("^", "**")))
        return f"**Expression:** `{text}`\n\n**Result:** `{simplified}`"
    except Exception:
        return None


def stream_groq(user_prompt):
    api_key = get_secret("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing.")
    from groq import Groq
    client = Groq(api_key=api_key)
    
    messages = [{"role": "system", "content": f"You are NEXUS AI. {response_instruction()}"}]
    for msg in st.session_state.messages[-6:]:
        if msg.get("type") != "image":
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_prompt})

    stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.3,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def stream_gemini(user_prompt):
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing.")
    from google import genai
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content_stream(
        model=GEMINI_MODEL,
        contents=f"You are NEXUS AI. {response_instruction()}\n\nUser: {user_prompt}",
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text


# ============================================================
# CHAT HISTORY DISPLAY
# ============================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "image":
            st.image(message["content"], caption="Generated Image")
        else:
            st.markdown(message["content"])


# ============================================================
# QUICK SUGGESTIONS
# ============================================================

selected_suggestion = None

if not st.session_state.messages:
    st.markdown("**Quick suggestions**")
    suggestions = [
        "Help me solve a difficult problem",
        "Generate image of a futuristic tech city",
        "Find the root cause and solution",
        "Create an actionable plan",
    ]
    cols = st.columns(4)
    for idx, sug in enumerate(suggestions):
        if cols[idx].button(sug, key=f"sug_{idx}", use_container_width=True):
            selected_suggestion = sug


# ============================================================
# CHAT INPUT & DIRECT QUESTION TARGET SCROLLING
# ============================================================

prompt = st.chat_input("Describe your problem or request an image...") or selected_suggestion

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    components.html(
        """
        <script>
            setTimeout(() => {
                const parentDoc = window.parent.document;
                const messages = parentDoc.querySelectorAll('div[data-testid="stChatMessage"]');
                if (messages.length > 0) {
                    const lastUserMsg = messages[messages.length - 1];
                    lastUserMsg.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 50);
        </script>
        """,
        height=0,
    )

    with st.chat_message("assistant"):
        # 1. Image Generation Check
        if is_image_request(prompt):
            with st.spinner("🎨 Generating image using Gemini..."):
                try:
                    img_bytes = generate_gemini_image(prompt)
                    if img_bytes:
                        st.image(img_bytes, caption=f"Prompt: {prompt}")
                        st.session_state.messages.append({"role": "assistant", "content": img_bytes, "type": "image"})
                    else:
                        st.error("Image generation failed.")
                except Exception as e:
                    st.error(f"Image Error: {safe_error(e)}")

        # 2. Math Engine Check
        elif solve_math(prompt):
            math_res = solve_math(prompt)
            res_text = f"### Math Engine Solution\n\n{math_res}"
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})

        # 3. Normal Text Chat (Groq / Gemini)
        else:
            response_placeholder = st.empty()
            full_response = ""
            
            try:
                for chunk in stream_groq(prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
            except Exception as e:
                try:
                    for chunk in stream_gemini(prompt):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                except Exception as e2:
                    full_response = f"### Response Failed\n\nProvider Error: {safe_error(e2)}"
                    response_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
