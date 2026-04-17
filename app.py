import streamlit as st
from embedder import load_or_generate_embeddings
from similarity import find_top_similar
from llm import ask_nuha
from fingerprint import generate_fingerprint, save_record

# ─── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="سَبق",
    page_icon="💡",
    layout="centered"
)

# ─── Global styles ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main > div,
.block-container {
    direction: rtl !important;
    font-family: 'IBM Plex Sans Arabic', 'Segoe UI', Tahoma, sans-serif !important;
    background-color: #0f1117 !important;
    color: #e8eaf0 !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Global text color fix ── */
p, span, label, div, li, td, th { color: #e8eaf0; }

/* ── Streamlit label override ── */
.stTextArea label, .stTextInput label {
    color: #a0aec0 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #162d4a 60%, #0d1f33 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 40px 32px 32px;
    margin-bottom: 36px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -40px; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.app-header-icon {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 16px;
    font-size: 1.6rem;
    box-shadow: 0 8px 24px rgba(59,130,246,0.3);
}
.app-header h1 {
    color: #f1f5f9 !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
    margin-bottom: 8px !important;
}
.app-header p {
    color: #94a3b8 !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
}

/* ── Input area ── */
.stTextArea textarea {
    background-color: #1a1f2e !important;
    border: 1.5px solid #2d3748 !important;
    border-radius: 14px !important;
    color: #e8eaf0 !important;
    font-family: 'IBM Plex Sans Arabic', Tahoma, sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
    padding: 14px 16px !important;
    direction: rtl !important;
    transition: border-color 0.2s ease;
    resize: vertical;
}
.stTextArea textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #4a5568 !important; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'IBM Plex Sans Arabic', Tahoma, sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
/* Primary button (first in column) */
div[data-testid="column"]:first-child .stButton > button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.35) !important;
}
div[data-testid="column"]:first-child .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(59,130,246,0.45) !important;
}
/* Secondary button */
div[data-testid="column"]:last-child .stButton > button {
    background: #1a1f2e !important;
    color: #94a3b8 !important;
    border: 1.5px solid #2d3748 !important;
}
div[data-testid="column"]:last-child .stButton > button:hover {
    background: #232938 !important;
    color: #cbd5e1 !important;
    border-color: #4a5568 !important;
}
/* Fingerprint button */
.stButton > button[kind="secondary"] {
    background: #1a1f2e !important;
    color: #94a3b8 !important;
    border: 1.5px solid #2d3748 !important;
}

/* ── Divider ── */
hr { border-color: #1e2533 !important; margin: 28px 0 !important; }

/* ── Cards ── */
.card {
    background: #161b27;
    border: 1px solid #1e2840;
    border-radius: 16px;
    padding: 24px 26px;
    margin-bottom: 20px;
}
.card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid #1e2840;
}
.card-header-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.icon-blue   { background: rgba(59,130,246,0.15); color: #3b82f6; }
.icon-purple { background: rgba(99,102,241,0.15);  color: #818cf8; }
.icon-teal   { background: rgba(20,184,166,0.15);  color: #2dd4bf; }
.icon-amber  { background: rgba(245,158,11,0.15);  color: #fbbf24; }
.card-header-title {
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    letter-spacing: -0.01em;
}

/* ── Score display ── */
.score-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
.score-number {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
}
.score-red    { color: #f87171; }
.score-yellow { color: #fbbf24; }
.score-green  { color: #34d399; }
.score-label-text {
    font-size: 0.85rem !important;
    color: #64748b !important;
    margin-top: 4px;
}
.badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}
.badge-red    { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }
.badge-yellow { background: rgba(251,191,36,0.12);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }
.badge-green  { background: rgba(52,211,153,0.12);  color: #34d399; border: 1px solid rgba(52,211,153,0.25); }

/* ── Progress bar ── */
.progress-track {
    background: #1e2840;
    border-radius: 100px;
    height: 6px;
    margin-top: 14px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.6s ease;
}
.fill-red    { background: linear-gradient(90deg, #ef4444, #f87171); }
.fill-yellow { background: linear-gradient(90deg, #d97706, #fbbf24); }
.fill-green  { background: linear-gradient(90deg, #059669, #34d399); }

/* ── Similar idea items ── */
.idea-item {
    background: #1a1f2e;
    border: 1px solid #1e2840;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
}
.idea-rank {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
    margin-top: 2px;
}
.idea-content { flex: 1; }
.idea-title {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    margin-bottom: 5px !important;
}
.idea-desc {
    font-size: 0.84rem !important;
    color: #64748b !important;
    line-height: 1.6 !important;
}
.idea-score-pill {
    background: rgba(99,102,241,0.12);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.2);
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 600;
    white-space: nowrap;
    margin-top: 2px;
    flex-shrink: 0;
}

/* ── Analysis output ── */
.analysis-body {
    font-size: 0.92rem !important;
    color: #cbd5e1 !important;
    line-height: 1.85 !important;
    direction: rtl !important;
    text-align: right !important;
}
.analysis-body strong, .analysis-body b {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
}

/* ── Fingerprint box ── */
.fp-box {
    background: #0d1117;
    border: 1px solid #1e3a2f;
    border-radius: 12px;
    padding: 20px 22px;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    line-height: 2;
    word-break: break-all;
    color: #86efac;
}
.fp-label {
    color: #4ade80;
    font-weight: 600;
}
.fp-value { color: #86efac; }
.fp-hash  { color: #6ee7b7; font-size: 0.76rem; }

/* ── Fingerprint prompt text ── */
.fp-prompt {
    font-size: 0.88rem !important;
    color: #64748b !important;
    margin-bottom: 16px !important;
    line-height: 1.6 !important;
}

/* ── Streamlit alerts ── */
.stAlert {
    border-radius: 12px !important;
    font-family: 'IBM Plex Sans Arabic', Tahoma, sans-serif !important;
    font-size: 0.9rem !important;
}

/* ── Spinner text ── */
.stSpinner > div { color: #64748b !important; }

/* ── Warning / error text ── */
[data-testid="stNotificationContentWarning"] p,
[data-testid="stNotificationContentError"] p,
[data-testid="stNotificationContentSuccess"] p {
    color: inherit !important;
}

/* ── Expander override (fallback if used) ── */
.streamlit-expanderHeader {
    background: #1a1f2e !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'IBM Plex Sans Arabic', Tahoma, sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Load model & embeddings (cached) ────────────────────────────────────────
@st.cache_resource(show_spinner="جارٍ تحميل النظام...")
def load_resources():
    return load_or_generate_embeddings()

model, dataset, embeddings = load_resources()

# ─── Session state init ───────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>سَبق💡</h1>
    <p>تحقق من أصالة فكرتك قبل تقديمها</p>
</div>
""", unsafe_allow_html=True)

# ─── Input area ───────────────────────────────────────────────────────────────
user_idea = st.text_area(
    "اكتب فكرتك",
    placeholder="مثال: تطبيق يساعد المستخدم على تنظيم وقته باستخدام الذكاء الاصطناعي...",
    height=140,
    key="idea_input"
)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    analyze_btn = st.button("تحليل الفكرة", use_container_width=True)
with col2:
    reset_btn = st.button("إعادة تعيين", use_container_width=True)

# ─── Reset ────────────────────────────────────────────────────────────────────
if reset_btn:
    st.session_state.results = None
    st.rerun()

# ─── Analysis ─────────────────────────────────────────────────────────────────
if analyze_btn:
    if not user_idea.strip():
        st.warning("الرجاء كتابة فكرتك أولاً.")
    else:
        with st.spinner("جارٍ تحليل فكرتك..."):
            try:
                similar_ideas = find_top_similar(user_idea, model, dataset, embeddings)
                nuha_response = ask_nuha(user_idea, similar_ideas)
                st.session_state.results = {
                    "idea": user_idea,
                    "similar": similar_ideas,
                    "analysis": nuha_response
                }
            except Exception:
                st.error("حدث خطأ أثناء التحليل. حاول مجدداً.")

# ─── Display results ──────────────────────────────────────────────────────────
if st.session_state.results:
    r             = st.session_state.results
    similar_ideas = r["similar"]
    top_score     = similar_ideas[0]["score"]
    score_pct     = int(top_score * 100)

    # Determine score tier
    if top_score >= 0.85:
        score_cls  = "score-red"
        fill_cls   = "fill-red"
        badge_cls  = "badge-red"
        badge_text = "تشابه عالٍ جداً"
    elif top_score >= 0.65:
        score_cls  = "score-yellow"
        fill_cls   = "fill-yellow"
        badge_cls  = "badge-yellow"
        badge_text = "تشابه متوسط"
    else:
        score_cls  = "score-green"
        fill_cls   = "fill-green"
        badge_cls  = "badge-green"
        badge_text = "فكرة مميزة نسبياً"

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Score card ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-header-icon icon-blue">&#x25CE;</div>
            <span class="card-header-title">نتيجة التحليل</span>
        </div>
        <div class="score-row">
            <div>
                <div class="score-number {score_cls}">{score_pct}%</div>
                <div class="score-label-text">أعلى نسبة تشابه مع الأفكار الموجودة</div>
            </div>
            <span class="badge {badge_cls}">{badge_text}</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill {fill_cls}" style="width:{score_pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Similar ideas card ────────────────────────────────────────────────
    ideas_html = ""
    for i, idea in enumerate(similar_ideas, 1):
        ideas_html += (
            '<div class="idea-item">'
            f'<div class="idea-rank">{i}</div>'
            '<div class="idea-content">'
            f'<div class="idea-title">{idea["title"]}</div>'
            f'<div class="idea-desc">{idea["description"]}</div>'
            '</div>'
            f'<div class="idea-score-pill">{int(idea["score"] * 100)}%</div>'
            '</div>'
        )

    st.markdown(
        '<div class="card">'
        '<div class="card-header">'
        '<span class="card-header-title">أقرب الأفكار المشابهة</span>'
        '</div>'
        + ideas_html +
        '</div>',
        unsafe_allow_html=True
    )

    # ── Analysis card ─────────────────────────────────────────────────────
    formatted_analysis = (
        r["analysis"]
        .replace("\n\n", "</p><p>")
        .replace("\n", "<br>")
    )
    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-header-icon icon-teal">&#x2736;</div>
            <span class="card-header-title">التحليل التفصيلي</span>
        </div>
        <div class="analysis-body">
            <p>{formatted_analysis}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Digital fingerprint card ──────────────────────────────────────────
    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-header-icon icon-amber">&#x25C6;</div>
            <span class="card-header-title">البصمة الرقمية</span>
        </div>
        <p class="fp-prompt">
            سجّل بصمة رقمية لفكرتك للحصول على إثبات موثّق بالتاريخ والوقت.
            لا يمكن تسجيل أفكار ذات تشابه عالٍ أو مكررة.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("توثيق الفكرة وتسجيل البصمة", use_container_width=True):
        try:
            record = generate_fingerprint(r["idea"], top_score)
            save_record(record)
            st.success("تم تسجيل البصمة الرقمية للفكرة بنجاح")
            st.markdown(f"""
            <div class="fp-box">
                <span class="fp-label">الفكرة&nbsp;&nbsp;&nbsp;: </span>
                <span class="fp-value">{record['idea'][:80]}{'...' if len(record['idea']) > 80 else ''}</span><br>
                <span class="fp-label">Hash&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: </span>
                <span class="fp-hash">{record['hash']}</span><br>
                <span class="fp-label">التوقيت&nbsp;: </span>
                <span class="fp-value">{record['timestamp']}</span><br>
                <span class="fp-label">التشابه&nbsp;: </span>
                <span class="fp-value">{int(record['top_similarity_score']*100)}%</span>
            </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            if str(e) == "high_similarity":
                st.error("فكرتك قريبة جداً من أفكار موجودة، لا يمكن تسجيل بصمة لها.")
            elif str(e) == "duplicate":
                st.warning("هذه الفكرة مسجّلة مسبقاً في النظام.")
            else:
                st.error("حدث خطأ أثناء التوثيق. حاول مجدداً.")
