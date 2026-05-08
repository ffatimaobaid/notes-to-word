import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.memory import _load_long_term_memory, get_success_rate, get_average_feedback, get_dominant_content_type
from agent.learning import get_learning_summary
from ethics.transparency import get_audit_trail, get_audit_summary
from ethics.compliance import get_full_compliance_dashboard

# --- PAGE CONFIG ---
st.set_page_config(page_title="Notes2Doc — Dashboard", page_icon="📊", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    :root {
        --bg-primary: #0a0a1a; --bg-secondary: #111128;
        --glass-bg: rgba(255, 255, 255, 0.03); --glass-border: rgba(255, 255, 255, 0.08);
        --accent-primary: #7c3aed; --accent-secondary: #06b6d4;
        --accent-gradient: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
        --text-primary: #f1f5f9; --text-secondary: #94a3b8; --text-muted: #64748b;
        --success: #10b981; --warning: #f59e0b; --danger: #ef4444;
    }
    .stApp { background: var(--bg-primary) !important; font-family: 'Inter', sans-serif !important; }
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: var(--text-primary) !important; }
    .glass-card {
        background: var(--glass-bg); backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border); border-radius: 16px;
        padding: 24px; margin-bottom: 16px;
    }
    .metric-big {
        text-align: center; padding: 20px;
        background: var(--glass-bg); border: 1px solid var(--glass-border);
        border-radius: 16px;
    }
    .metric-big .value {
        font-size: 2.5rem; font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .metric-big .label {
        font-size: 0.75rem; color: var(--text-muted);
        text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px;
    }
    .compliance-badge {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    }
    .badge-pass { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-warn { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important; border-right: 1px solid var(--glass-border) !important;
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
         font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">
        📊 Agent Analytics
    </div>
    <h1 style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #7c3aed, #06b6d4);
         -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px;">
        Performance Dashboard
    </h1>
    <p style="color: #94a3b8; font-size: 0.95rem;">
        Real-time analytics, learning insights, and compliance monitoring
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Load data
ltm = _load_long_term_memory()
learning = get_learning_summary(ltm)
audit = get_audit_summary()
compliance = get_full_compliance_dashboard()


# ──────────────────────────────────────────────
# KEY METRICS
# ──────────────────────────────────────────────

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-big">
        <div class="value">{ltm.get('total_conversions', 0)}</div>
        <div class="label">Total Conversions</div>
    </div>""", unsafe_allow_html=True)

with c2:
    sr = get_success_rate(ltm)
    st.markdown(f"""
    <div class="metric-big">
        <div class="value">{sr}%</div>
        <div class="label">Success Rate</div>
    </div>""", unsafe_allow_html=True)

with c3:
    ac = ltm.get('average_confidence', 0)
    st.markdown(f"""
    <div class="metric-big">
        <div class="value">{ac:.0%}</div>
        <div class="label">Avg Confidence</div>
    </div>""", unsafe_allow_html=True)

with c4:
    af = get_average_feedback(ltm)
    st.markdown(f"""
    <div class="metric-big">
        <div class="value">{af}/5</div>
        <div class="label">User Rating</div>
    </div>""", unsafe_allow_html=True)

with c5:
    adapt = learning.get('adaptations_applied', 0)
    st.markdown(f"""
    <div class="metric-big">
        <div class="value">{adapt}</div>
        <div class="label">Adaptations</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ──────────────────────────────────────────────
# CHARTS ROW
# ──────────────────────────────────────────────

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### 📊 Content Type Distribution")
    counts = ltm.get("content_type_counts", {"text": 0, "math": 0, "diagram": 0, "mixed": 0})

    if any(counts.values()):
        fig = go.Figure(data=[go.Pie(
            labels=list(counts.keys()),
            values=list(counts.values()),
            hole=0.55,
            marker_colors=["#7c3aed", "#06b6d4", "#10b981", "#f59e0b"],
            textfont_size=13,
            textfont_color="#f1f5f9",
        )])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8"),
            legend=dict(font=dict(color="#94a3b8")),
            margin=dict(l=20, r=20, t=20, b=20),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 No conversion data yet. Process some notes to see analytics!")

with chart_col2:
    st.markdown("### 📈 Confidence Over Time")
    history = ltm.get("conversion_history", [])

    if history:
        timestamps = [h.get("timestamp", "")[:10] for h in history]
        confidences = [h.get("confidence", 0) * 100 for h in history]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, len(confidences) + 1)),
            y=confidences,
            mode="lines+markers",
            line=dict(color="#7c3aed", width=2),
            marker=dict(size=8, color="#06b6d4"),
            fill="tozeroy",
            fillcolor="rgba(124, 58, 237, 0.1)",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8"),
            xaxis=dict(title="Conversion #", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Confidence %", gridcolor="rgba(255,255,255,0.05)", range=[0, 100]),
            margin=dict(l=40, r=20, t=20, b=40),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 No history yet. Process some notes to see the trend!")


# ──────────────────────────────────────────────
# LEARNING INSIGHTS
# ──────────────────────────────────────────────

st.markdown("---")
st.markdown("### 🧠 Learning Insights")

learn_c1, learn_c2, learn_c3 = st.columns(3)

with learn_c1:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #f1f5f9; margin-bottom: 12px;">🎯 Performance Trend</h4>
    </div>
    """, unsafe_allow_html=True)
    trend = learning.get("performance_trend", "insufficient_data")
    trend_icons = {"improving": "📈 Improving", "declining": "📉 Declining", "stable": "➡️ Stable", "insufficient_data": "📊 Need more data"}
    st.markdown(f"**{trend_icons.get(trend, 'Unknown')}**")
    st.markdown(f"Recent avg confidence: **{learning.get('recent_avg_confidence', 0):.0%}**")

with learn_c2:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #f1f5f9; margin-bottom: 12px;">📚 Learned Preferences</h4>
    </div>
    """, unsafe_allow_html=True)
    prefs = learning.get("learned_preferences", {})
    for key, val in prefs.items():
        st.markdown(f"• **{key.replace('_', ' ').title()}**: {val}")

with learn_c3:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #f1f5f9; margin-bottom: 12px;">🔄 Dominant Content Type</h4>
    </div>
    """, unsafe_allow_html=True)
    dominant = get_dominant_content_type(ltm)
    st.markdown(f"Most processed type: **{dominant.title()}**")
    st.markdown(f"Total adaptations: **{learning.get('adaptations_applied', 0)}**")


# ──────────────────────────────────────────────
# COMPLIANCE SCORECARD
# ──────────────────────────────────────────────

st.markdown("---")
st.markdown("### 🛡️ Ethical Compliance Scorecard")

comp_c1, comp_c2, comp_c3, comp_c4 = st.columns(4)

frameworks = [
    ("ACM Code of Ethics", compliance["acm"]["overall_compliance"], compliance["acm"]["principles_followed"], compliance["acm"]["principles_evaluated"]),
    ("IEEE Code of Ethics", compliance["ieee"]["overall_compliance"], compliance["ieee"]["principles_followed"], compliance["ieee"]["principles_evaluated"]),
    ("PECA 2016", "high" if compliance["peca_2016"]["all_compliant"] else "moderate", compliance["peca_2016"]["sections_evaluated"], compliance["peca_2016"]["sections_evaluated"]),
    ("GDPR Principles", "high" if compliance["gdpr"]["all_compliant"] else "moderate", compliance["gdpr"]["principles_evaluated"], compliance["gdpr"]["principles_evaluated"]),
]

for col, (name, status, followed, total) in zip([comp_c1, comp_c2, comp_c3, comp_c4], frameworks):
    with col:
        badge_class = "badge-pass" if status == "high" else "badge-warn"
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 8px;">{name}</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: {'#10b981' if status == 'high' else '#f59e0b'};">
                {followed}/{total}
            </div>
            <div class="compliance-badge {badge_class}" style="margin-top: 8px;">
                {status.upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# AUDIT LOG
# ──────────────────────────────────────────────

st.markdown("---")
st.markdown("### 🔍 Recent Audit Trail")

trail = get_audit_trail(15)
if trail:
    for entry in reversed(trail):
        phase = entry.get("phase", "")
        action = entry.get("action", "")
        ts = entry.get("timestamp", "")[:19]
        phase_colors = {"observe": "#06b6d4", "decide": "#7c3aed", "act": "#10b981", "learn": "#f59e0b"}
        color = phase_colors.get(phase, "#94a3b8")
        st.markdown(
            f'<span style="color: {color}; font-weight: 600;">[{phase.upper()}]</span> '
            f'<span style="color: #94a3b8; font-size: 0.8rem;">{ts}</span> — '
            f'<span style="color: #f1f5f9;">{action}</span>',
            unsafe_allow_html=True,
        )
else:
    st.info("No audit entries yet. Use the Agentic System to generate activity.")


# ──────────────────────────────────────────────
# MEMORY STATUS
# ──────────────────────────────────────────────

st.markdown("---")
mem_c1, mem_c2 = st.columns(2)

with mem_c1:
    st.markdown("### 💾 Memory Status")
    st.markdown(f"""
    <div class="glass-card">
        <div style="color: #94a3b8; font-size: 0.85rem;">
            <p>📦 <b>History Entries:</b> {len(ltm.get('conversion_history', []))}/50</p>
            <p>⭐ <b>Feedback Entries:</b> {len(ltm.get('feedback_scores', []))}/100</p>
            <p>🕐 <b>Created:</b> {ltm.get('created_at', 'N/A')[:19]}</p>
            <p>🔄 <b>Last Updated:</b> {ltm.get('last_updated', 'N/A')[:19]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with mem_c2:
    st.markdown("### 🔧 Agent Configuration")
    st.markdown(f"""
    <div class="glass-card">
        <div style="color: #94a3b8; font-size: 0.85rem;">
            <p>🤖 <b>Agent Type:</b> Goal-Based Agent</p>
            <p>🧠 <b>Intelligence:</b> Google Gemini 2.5 Flash Lite</p>
            <p>🔄 <b>Memory:</b> Short-term (Session) + Long-term (Persistent)</p>
            <p>🛡️ <b>Ethics:</b> ACM/IEEE + PECA 2016 + GDPR</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown("""
<div style="text-align: center; padding: 30px 0; color: #64748b; font-size: 0.75rem;
     border-top: 1px solid rgba(255,255,255,0.08); margin-top: 40px;">
    Notes2Doc Dashboard — Real-time Agent Analytics & Compliance Monitoring
</div>
""", unsafe_allow_html=True)
