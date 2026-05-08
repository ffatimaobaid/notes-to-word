import streamlit as st

# --- APP CONFIG ---
st.set_page_config(
    page_title="Notes2Doc AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PREMIUM CSS THEME ---
st.markdown("""
<style>
    /* === IMPORTS === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* === ROOT VARIABLES === */
    :root {
        --bg-primary: #0a0a1a;
        --bg-secondary: #111128;
        --bg-card: rgba(20, 20, 50, 0.6);
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        --accent-primary: #7c3aed;
        --accent-secondary: #06b6d4;
        --accent-gradient: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --glow-purple: 0 0 20px rgba(124, 58, 237, 0.3);
        --glow-cyan: 0 0 20px rgba(6, 182, 212, 0.3);
    }

    /* === GLOBAL STYLES === */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--glass-border) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
    }

    /* === TYPOGRAPHY === */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }

    p, li, span, div {
        font-family: 'Inter', sans-serif !important;
    }

    /* === GLASS CARDS === */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(124, 58, 237, 0.3);
        box-shadow: var(--glow-purple);
        transform: translateY(-2px);
    }

    /* === HERO SECTION === */
    .hero-container {
        text-align: center;
        padding: 60px 20px 40px;
        position: relative;
    }

    .hero-badge {
        display: inline-block;
        background: var(--accent-gradient);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        max-width: 600px;
        margin: 0 auto 32px;
        line-height: 1.6;
    }

    /* === METRIC CARDS === */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin: 24px 0;
    }

    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: rgba(6, 182, 212, 0.3);
        box-shadow: var(--glow-cyan);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    /* === STATUS INDICATOR === */
    .status-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }

    .status-active { background: var(--success); }
    .status-idle { background: var(--text-muted); }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* === FEATURE CARDS === */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }

    .feature-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 28px;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .feature-card:hover {
        border-color: rgba(124, 58, 237, 0.4);
        box-shadow: var(--glow-purple);
        transform: translateY(-4px);
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 12px;
    }

    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 8px;
    }

    .feature-desc {
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    /* === BUTTONS === */
    .stButton > button {
        background: var(--accent-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(124, 58, 237, 0.5) !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }

    /* === FILE UPLOADER === */
    [data-testid="stFileUploader"] {
        border: 2px dashed var(--glass-border) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-primary) !important;
    }

    /* === EXPANDER === */
    .streamlit-expanderHeader {
        background: var(--glass-bg) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--glass-bg);
        border-radius: 12px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--accent-gradient) !important;
        color: white !important;
    }

    /* === TEXT AREA === */
    .stTextArea textarea {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', monospace !important;
    }

    /* === PROGRESS BAR === */
    .stProgress > div > div {
        background: var(--accent-gradient) !important;
        border-radius: 10px;
    }

    /* === DIVIDER === */
    hr {
        border-color: var(--glass-border) !important;
    }

    /* === SCROLLBAR === */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--accent-primary); border-radius: 3px; }

    /* === INFO/SUCCESS/WARNING BOXES === */
    .stAlert {
        border-radius: 12px !important;
    }

    /* === FOOTER === */
    .app-footer {
        text-align: center;
        padding: 30px 0;
        color: var(--text-muted);
        font-size: 0.8rem;
        border-top: 1px solid var(--glass-border);
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🤖 Notes2Doc Agent")
    st.markdown("---")

    # Agent Status
    try:
        from agent.core import NotesAgent
        agent = NotesAgent()
        status = agent.get_status()
        state_color = "status-active" if status["state"] == "idle" else "status-active"
        st.markdown(
            f'<span class="status-dot {state_color}"></span> Agent Status: **Online**',
            unsafe_allow_html=True,
        )
        st.markdown(f"📊 Total Conversions: **{status['total_conversions']}**")
        st.markdown(f"✅ Success Rate: **{status['success_rate']}%**")
        st.markdown(f"🧠 Memory Entries: **{status['memory_entries']}**")
    except Exception:
        st.markdown('<span class="status-dot status-idle"></span> Agent: **Initializing...**', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📑 Navigation")
    st.markdown("""
    - 🏠 **Home** — This page
    - 🤖 **Agentic System** — Smart converter
    - 📊 **Dashboard** — Analytics
    - 📚 **Phase 2 Report** — Full presentation
    """)

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center; color: #64748b; font-size: 0.75rem;">'
        'Notes2Doc AI Agent v2.0<br>PPIT Phase 2 Project'
        '</div>',
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# HERO SECTION
# ──────────────────────────────────────────────

st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✨ Phase 2 — Agentic AI System</div>
    <div class="hero-title">Notes2Doc</div>
    <div class="hero-subtitle">
        An autonomous AI agent that perceives, decides, acts, and learns — 
        transforming handwritten notes into professional documents with 
        intelligence and ethical awareness.
    </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# METRICS ROW
# ──────────────────────────────────────────────

try:
    from agent.memory import _load_long_term_memory, get_success_rate, get_average_feedback
    ltm = _load_long_term_memory()
    total = ltm.get("total_conversions", 0)
    success = get_success_rate(ltm)
    avg_conf = ltm.get("average_confidence", 0)
    feedback = get_average_feedback(ltm)
except Exception:
    total, success, avg_conf, feedback = 0, 0, 0, 0

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{total}</div>
        <div class="metric-label">Total Conversions</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{success}%</div>
        <div class="metric-label">Success Rate</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{avg_conf:.0%}</div>
        <div class="metric-label">Avg Confidence</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{feedback}/5</div>
        <div class="metric-label">User Rating</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FEATURE CARDS
# ──────────────────────────────────────────────

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">👁️</div>
        <div class="feature-title">Intelligent Perception</div>
        <div class="feature-desc">
            Analyzes image quality, detects content types (text, math, diagrams), 
            and recommends preprocessing — all autonomously.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Adaptive Decision Making</div>
        <div class="feature-desc">
            Selects optimal transcription strategy based on perception results, 
            memory, and ethical compliance checks.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Multi-Pass Processing</div>
        <div class="feature-desc">
            Executes intelligent multi-pass transcription with enhancement, 
            formatting, and confidence evaluation.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📖</div>
        <div class="feature-title">Continuous Learning</div>
        <div class="feature-desc">
            Learns from user feedback, adapts strategies over time, and 
            maintains persistent memory across sessions.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <div class="feature-title">Ethical & Transparent</div>
        <div class="feature-desc">
            Full audit trail, explainability reports, privacy-by-design, 
            and ACM/IEEE/PECA 2016 compliance.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🤝</div>
        <div class="feature-title">Human-in-the-Loop</div>
        <div class="feature-desc">
            Smart checkpoints where the agent requests human approval 
            for uncertain decisions — balancing autonomy with control.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TEAM INFO
# ──────────────────────────────────────────────

st.markdown("---")

st.markdown("""
<div class="glass-card" style="text-align: center;">
    <div style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px;">
        Created By
    </div>
    <div style="font-size: 1rem; color: var(--text-primary); font-weight: 600;">
        Fatima Obaid (22I-0475) &nbsp;•&nbsp; Ayesha Tahir (22I-0475) &nbsp;•&nbsp; Hadia Mazhar (22I-0487)
    </div>
    <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 6px;">
        AI-D Section — Professional Practices in IT — January 2026
    </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown("""
<div class="app-footer">
    Notes2Doc AI Agent v2.0 — Phase 2: Agentic Transformation<br>
    Built with Streamlit • Powered by Google Gemini • Guided by ACM/IEEE Ethics
</div>
""", unsafe_allow_html=True)
