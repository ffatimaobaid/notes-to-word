import streamlit as st
import sys, os
from pathlib import Path
from PIL import Image
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.core import NotesAgent
from agent.memory import _load_long_term_memory, get_average_feedback
from ethics.transparency import get_audit_trail, generate_explainability_report
from ethics.privacy import generate_consent_text, get_data_lifecycle

# --- PAGE CONFIG ---
st.set_page_config(page_title="Notes2Doc — Agentic System", page_icon="🤖", layout="wide")

# --- CSS (inherit from app.py via shared theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    :root {
        --bg-primary: #0a0a1a;
        --bg-secondary: #111128;
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
    }
    .stApp { background: var(--bg-primary) !important; font-family: 'Inter', sans-serif !important; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: var(--text-primary) !important; }
    .glass-card {
        background: var(--glass-bg); backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border); border-radius: 16px;
        padding: 24px; margin-bottom: 16px;
    }
    .phase-badge {
        display: inline-block; padding: 4px 14px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 1.5px; margin-bottom: 8px;
    }
    .phase-observe { background: rgba(6, 182, 212, 0.15); color: #06b6d4; border: 1px solid rgba(6, 182, 212, 0.3); }
    .phase-decide { background: rgba(124, 58, 237, 0.15); color: #7c3aed; border: 1px solid rgba(124, 58, 237, 0.3); }
    .phase-act { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .phase-learn { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
    .thought-item {
        padding: 8px 16px; margin: 4px 0; border-left: 3px solid var(--accent-primary);
        background: rgba(124, 58, 237, 0.05); border-radius: 0 8px 8px 0;
        font-size: 0.85rem; color: var(--text-secondary);
    }
    .confidence-bar {
        height: 8px; border-radius: 4px; background: rgba(255,255,255,0.05);
        overflow: hidden; margin: 8px 0;
    }
    .confidence-fill {
        height: 100%; border-radius: 4px;
        background: var(--accent-gradient);
        transition: width 0.5s ease;
    }
    .stButton > button {
        background: var(--accent-gradient) !important; color: white !important;
        border: none !important; border-radius: 12px !important;
        padding: 12px 28px !important; font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        font-weight: 600 !important;
    }
    [data-testid="stFileUploader"] {
        border: 2px dashed var(--glass-border) !important; border-radius: 16px !important;
    }
    .stTextArea textarea {
        background: var(--bg-secondary) !important; border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important; color: var(--text-primary) !important;
    }
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--accent-primary); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────

st.markdown("""
<div style="text-align: center; padding: 20px 0 10px;">
    <div style="display: inline-block; background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
         color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.7rem;
         font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 10px;">
        🤖 Agentic System
    </div>
    <h1 style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #7c3aed, #06b6d4);
         -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px;">
        Intelligent Notes Converter
    </h1>
    <p style="color: #94a3b8; font-size: 0.95rem;">
        Upload a note → Watch the agent think → Get your document
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ──────────────────────────────────────────────
# CONSENT & PRIVACY NOTICE
# ──────────────────────────────────────────────

with st.expander("🔒 Privacy & Consent Notice", expanded=False):
    st.markdown(f"""
    <div class="glass-card" style="font-size: 0.85rem; color: #94a3b8;">
        {generate_consent_text().replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Data Lifecycle:**")
    lifecycle = get_data_lifecycle()
    for stage in lifecycle:
        icon = "🟢" if not stage["stored_on_disk"] else "🟡"
        st.markdown(
            f"{icon} **{stage['stage']}** — {stage['action']} "
            f"(Retention: {stage['retention']})"
        )


# ──────────────────────────────────────────────
# MAIN LAYOUT
# ──────────────────────────────────────────────

col_upload, col_output = st.columns([1, 1], gap="large")

with col_upload:
    st.markdown('<div class="phase-badge phase-observe">👁️ PERCEPTION INPUT</div>', unsafe_allow_html=True)
    st.markdown("### Upload Your Note")

    uploaded_file = st.file_uploader(
        "Drop your handwritten note image (JPG, PNG)",
        type=["jpg", "jpeg", "png"],
        help="The agent will analyze the image quality, detect content types, and choose the best strategy."
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        image.thumbnail((1024, 1024))
        st.image(image, caption="📸 Uploaded Note Preview", use_container_width=True)


with col_output:
    st.markdown('<div class="phase-badge phase-act">⚡ AGENT OUTPUT</div>', unsafe_allow_html=True)
    st.markdown("### Agent Workspace")

    if uploaded_file:
        # --- Initialize Agent ---
        if "agent" not in st.session_state:
            st.session_state.agent = NotesAgent()

        agent = st.session_state.agent

        if st.button("🚀 Run Agentic Pipeline", use_container_width=True):
            with st.status("🤖 Agent is processing...", expanded=True) as status_container:
                # ── PHASE 1: OBSERVE ──
                st.write("👁️ **Phase 1: Observing** — Analyzing image quality...")
                perception = agent.observe(image)
                quality = perception["quality"]
                content = perception["content_type"]

                q_score = quality["overall_score"]
                q_color = "#10b981" if q_score >= 70 else "#f59e0b" if q_score >= 50 else "#ef4444"
                st.markdown(
                    f'Image Quality: **{quality["quality_label"]}** '
                    f'<span style="color: {q_color}; font-weight: 700;">{q_score}/100</span>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'Content Type: **{content["primary_type"].title()}** '
                    f'(confidence: {content["confidence"]:.0%})'
                )

                # ── PHASE 2: DECIDE ──
                st.write("🧠 **Phase 2: Deciding** — Selecting optimal strategy...")
                strategy = agent.decide()
                st.markdown(f'Strategy: **{strategy["num_passes"]}-pass {strategy["primary_type"]}** | Autonomy: **{strategy["autonomy_level"]}**')

                # ── PHASE 3: ACT ──
                st.write("⚡ **Phase 3: Acting** — Transcribing and formatting...")
                result = agent.act(strategy)

                if result["success"]:
                    conf = result["confidence"]
                    conf_color = "#10b981" if conf >= 0.7 else "#f59e0b" if conf >= 0.5 else "#ef4444"
                    st.markdown(
                        f'Confidence: <span style="color: {conf_color}; font-weight: 700;">{conf:.0%}</span> '
                        f'| Words: **{result["word_count"]}**',
                        unsafe_allow_html=True,
                    )
                else:
                    st.error(f"❌ Transcription failed: {result.get('error', 'Unknown error')}")

                # ── PHASE 4: LEARN ──
                st.write("📖 **Phase 4: Learning** — Recording results...")
                learning = agent.learn(action_result=result)

                status_container.update(
                    label="✅ Agentic pipeline completed!",
                    state="complete",
                    expanded=False,
                )

            # Store result in session state
            if result["success"]:
                st.session_state.result_text = result["text"]
                st.session_state.pipeline_result = {
                    "perception": perception,
                    "strategy": strategy,
                    "result": result,
                    "learning": learning,
                    "thought_log": agent.stm.get_thought_log(),
                    "decisions": agent.stm.decisions_made,
                    "actions": agent.stm.actions_taken,
                }

        # --- DISPLAY RESULTS ---
        if "result_text" in st.session_state and st.session_state.result_text:
            st.markdown("---")
            st.markdown("#### 📄 Transcription Result")

            edited_text = st.text_area(
                "Edit the transcription if needed:",
                st.session_state.result_text,
                height=300,
            )

            # Generate Word document
            doc_bytes = agent.generate_document(edited_text)

            st.download_button(
                label="📥 Download Word Document",
                data=doc_bytes.getvalue(),
                file_name=f"Notes2Doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

            # --- FEEDBACK SECTION ---
            st.markdown("---")
            st.markdown("#### 🌟 Rate This Conversion")
            feedback_col1, feedback_col2 = st.columns([1, 2])
            with feedback_col1:
                feedback_score = st.slider("Rating", 1, 5, 4, help="1 = Poor, 5 = Excellent")
            with feedback_col2:
                if st.button("Submit Feedback"):
                    agent.learn(feedback_score=feedback_score, action_result=st.session_state.pipeline_result["result"])
                    st.success(f"✅ Feedback recorded! Score: {feedback_score}/5 — Agent will adapt.")

    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 3rem; margin-bottom: 16px;">🤖</div>
            <div style="color: #94a3b8; font-size: 1rem;">
                Upload a note image to activate the agent
            </div>
            <div style="color: #64748b; font-size: 0.8rem; margin-top: 8px;">
                The agent will automatically analyze, decide, and act
            </div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# AGENT THOUGHT PROCESS (Below main columns)
# ──────────────────────────────────────────────

if "pipeline_result" in st.session_state:
    st.markdown("---")

    tab_thoughts, tab_explain, tab_audit = st.tabs([
        "🧠 Agent Thoughts", "📋 Explainability Report", "🔍 Audit Trail"
    ])

    pipeline = st.session_state.pipeline_result

    with tab_thoughts:
        st.markdown("### Agent's Thought Process")
        st.markdown("*Every step of the agent's reasoning, fully transparent:*")

        for thought in pipeline.get("thought_log", []):
            stage = thought["stage"]
            phase_class = f"phase-{stage}" if stage in ("observe", "decide", "act", "learn") else "phase-observe"
            st.markdown(
                f'<div class="thought-item">'
                f'<span class="phase-badge {phase_class}" style="font-size: 0.6rem; padding: 2px 8px; margin-right: 8px;">'
                f'{stage.upper()}</span> {thought["thought"]}</div>',
                unsafe_allow_html=True,
            )

    with tab_explain:
        st.markdown("### Explainability Report")
        report = generate_explainability_report(
            pipeline.get("thought_log", []),
            pipeline.get("decisions", []),
            pipeline.get("actions", []),
        )
        st.code(report, language="text")

    with tab_audit:
        st.markdown("### Recent Audit Trail")
        trail = get_audit_trail(20)
        if trail:
            for entry in reversed(trail):
                phase = entry.get("phase", "")
                action = entry.get("action", "")
                ts = entry.get("timestamp", "")[:19]
                st.markdown(
                    f"**[{ts}]** `{phase}` — {action}"
                )
        else:
            st.info("No audit entries yet. Run the pipeline to generate entries.")


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown("""
<div style="text-align: center; padding: 30px 0; color: #64748b; font-size: 0.75rem;
     border-top: 1px solid rgba(255,255,255,0.08); margin-top: 40px;">
    Notes2Doc Agentic System — Observe • Decide • Act • Learn
</div>
""", unsafe_allow_html=True)
