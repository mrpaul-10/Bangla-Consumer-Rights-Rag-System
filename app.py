"""
Streamlit chat UI for the Bangla Consumer Rights Assistant.
Calls the FastAPI backend (api.py) over HTTP.

Run the API first:  uvicorn api:app --reload
Then run this:       streamlit run app.py
"""

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ভোক্তা অধিকার সহায়ক",
    page_icon="⚖️",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Styling — "official letterhead" aesthetic
# ---------------------------------------------------------------------------
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Bengali:wght@500;600;700&family=Noto+Sans+Bengali:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --paper: #FBF8F2;
            --paper-deep: #F2EEE3;
            --ink: #1C1B18;
            --ink-soft: #595650;
            --forest: #0B4A3C;
            --forest-deep: #07332A;
            --forest-tint: #E7F0EC;
            --brick: #9A3324;
            --brick-tint: #F7E9E5;
            --rule: #D9D2C2;
        }

        .stApp { background: var(--paper); }
        .main .block-container { max-width: 680px; padding-top: 1.2rem; }

        html, body, [class*="css"] {
            font-family: 'Noto Sans Bengali', 'Segoe UI', sans-serif;
            color: var(--ink);
        }

        .letterhead { text-align: center; border-bottom: 2px solid var(--forest);
                      padding-bottom: 16px; margin-bottom: 8px; }
        .letterhead .eyebrow { font-size: 0.72rem; color: var(--ink-soft); letter-spacing: 0.03em; }
        .letterhead h1 { font-family: 'Noto Serif Bengali', serif; font-weight: 700;
                          font-size: 1.85rem; margin: 4px 0 6px; color: var(--forest-deep); }
        .letterhead .tagline { font-size: 0.88rem; color: var(--ink-soft); margin: 0; }

        [data-testid="stChatMessage"] { background: transparent; padding: 4px 0; }

        .msg-label { font-size: 0.7rem; color: var(--ink-soft); margin-bottom: 2px; }

        .citations { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 7px; }
        .citation {
            font-size: 0.78rem; color: var(--forest-deep); background: var(--forest-tint);
            border: 1px solid #C9DDD3; padding: 3px 10px; border-radius: 2px;
        }

        .not-found {
            margin-top: 10px; background: var(--brick-tint); border-left: 3px solid var(--brick);
            padding: 9px 13px; font-size: 0.85rem; color: var(--brick);
        }

        .disclaimer {
            margin-top: 18px; padding-top: 12px; border-top: 1px solid var(--rule);
            font-size: 0.78rem; color: var(--ink-soft); text-align: center;
        }
        .disclaimer .mark { color: var(--brick); font-weight: 600; }

        [data-testid="stSidebar"] { background: var(--paper-deep); border-right: 1px solid var(--rule); }
        .seal {
            width: 42px; height: 42px; border: 1.5px solid var(--forest); border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.2rem; color: var(--forest); margin-bottom: 10px;
        }
        .sidebar-title { font-family: 'Noto Serif Bengali', serif; font-size: 1.05rem;
                          font-weight: 600; color: var(--forest-deep); margin: 0 0 4px; }
        .sidebar-sub { font-size: 0.78rem; color: var(--ink-soft); margin: 0 0 16px; }
        .sidebar-section-label {
            font-size: 0.72rem; color: var(--ink-soft); border-bottom: 1px solid var(--rule);
            padding-bottom: 6px; margin: 14px 0 8px;
        }

        [data-testid="stSidebar"] .stButton button {
            width: 100%; text-align: right; background: var(--paper);
            border: 1px solid var(--rule); border-radius: 3px; color: var(--ink);
            font-size: 0.82rem; padding: 8px 12px;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            border-color: var(--forest); background: var(--forest-tint); color: var(--forest-deep);
        }

        [data-testid="stChatInput"] textarea { text-align: right; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Letterhead header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="letterhead">
        <div class="eyebrow">বাংলাদেশ · ভোক্তা অধিকার সংরক্ষণ আইন, ২০০৯</div>
        <h1>ভোক্তা অধিকার সহায়ক</h1>
        <p class="tagline">আইনের মূল পাঠ থেকে সরাসরি, সূত্রসহ উত্তর</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="seal">⚖</div>
        <p class="sidebar-title">ভোক্তা অধিকার সহায়ক</p>
        <p class="sidebar-sub">ভোক্তা অধিকার সংরক্ষণ আইন, ২০০৯ — সহায়ক পাঠ ব্যবস্থা</p>
        <p class="sidebar-section-label">নির্মিত হয়েছে</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "— Google Gemini (উত্তর প্রণয়ন)  \n"
        "— ChromaDB (অর্থগত অনুসন্ধান)  \n"
        "— Multilingual Embeddings  \n"
        "— FastAPI ও Streamlit"
    )

    st.markdown('<p class="sidebar-section-label">উদাহরণ জিজ্ঞাসা</p>', unsafe_allow_html=True)
    example_questions = [
        "অভিযোগ কীভাবে দায়ের করতে হয়?",
        "ভোক্তা কাকে বলে?",
        "ভেজাল পণ্য বিক্রির শাস্তি কী?",
        "অভিযোগ দায়েরের সময়সীমা কত দিন?",
    ]
    for q in example_questions:
        if st.button(q, use_container_width=True, key=f"eg_{q}"):
            st.session_state.pending_question = q

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("কথোপকথন মুছে ফেলুন", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<p class="sidebar-section-label">সোর্স কোড</p>'
        '<p style="font-size:0.78rem;">'
        '<a href="https://github.com/mrpaul-10/Bangla-Consumer-Rights-Rag-System" '
        'style="color:#0B4A3C;" target="_blank">GitHub রিপোজিটরি</a></p>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ---------------------------------------------------------------------------
# Helper: call the backend API
# ---------------------------------------------------------------------------
def ask_backend(question: str) -> dict:
    try:
        response = requests.post(API_URL, json={"question": question}, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {
            "answer": "⚠️ API সার্ভারের সাথে সংযোগ করা যায়নি। `uvicorn api:app --reload` চালু আছে কিনা দেখুন।",
            "sources": [], "found": False, "error": True,
        }
    except requests.exceptions.Timeout:
        return {
            "answer": "⚠️ সার্ভার থেকে সময়মতো উত্তর আসেনি। একটু পর আবার চেষ্টা করুন।",
            "sources": [], "found": False, "error": True,
        }
    except Exception as e:
        return {"answer": f"⚠️ একটি সমস্যা হয়েছে: {e}", "sources": [], "found": False, "error": True}


def render_assistant_extras(result: dict):
    if result.get("sources"):
        badges = "".join(f"<span class='citation'>{s}</span>" for s in result["sources"])
        st.markdown(f"<div class='citations'>{badges}</div>", unsafe_allow_html=True)
    if result.get("found") is False and not result.get("error"):
        st.markdown(
            "<div class='not-found'>এই তথ্য আইনের প্রদত্ত অংশে পাওয়া যায়নি</div>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Render past messages
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    label = "আপনি" if msg["role"] == "user" else "ভোক্তা অধিকার সহায়ক"
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='msg-label'>{label}</div>", unsafe_allow_html=True)
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            render_assistant_extras(msg)

# ---------------------------------------------------------------------------
# Handle a new question
# ---------------------------------------------------------------------------
typed_question = st.chat_input("আপনার প্রশ্ন লিখুন…")
question = st.session_state.pending_question or typed_question
st.session_state.pending_question = None

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown("<div class='msg-label'>আপনি</div>", unsafe_allow_html=True)
        st.markdown(question)

    with st.chat_message("assistant"):
        st.markdown("<div class='msg-label'>ভোক্তা অধিকার সহায়ক</div>", unsafe_allow_html=True)
        with st.spinner("উত্তর খোঁজা হচ্ছে…"):
            result = ask_backend(question)
        st.markdown(result["answer"])
        render_assistant_extras(result)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "sources": result.get("sources", []),
            "found": result.get("found", False),
            "error": result.get("error", False),
        }
    )

# ---------------------------------------------------------------------------
# Persistent disclaimer
# ---------------------------------------------------------------------------
st.markdown(
    "<div class='disclaimer'><span class='mark'>⚠</span> এটি আইনি পরামর্শ নয় — "
    "জটিল বিষয়ে আইনজীবীর পরামর্শ নিন</div>",
    unsafe_allow_html=True,
)