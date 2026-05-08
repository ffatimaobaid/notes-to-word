import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# --- PAGE CONFIG ---
st.set_page_config(page_title="Phase 2 Report", page_icon="📚", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    :root {
        --bg-primary: #0a0a1a; --bg-secondary: #111128;
        --glass-bg: rgba(255, 255, 255, 0.03); --glass-border: rgba(255, 255, 255, 0.08);
        --accent-primary: #7c3aed; --accent-secondary: #06b6d4;
        --accent-gradient: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
        --text-primary: #f1f5f9; --text-secondary: #94a3b8;
    }
    .stApp { background: var(--bg-primary) !important; font-family: 'Inter', sans-serif !important; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; color: var(--text-primary) !important; }
    p, li { color: var(--text-secondary); }
    .glass-card {
        background: var(--glass-bg); backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border); border-radius: 16px;
        padding: 24px; margin-bottom: 16px;
    }
    .slide-title { font-size: 1.5rem; font-weight: 700; color: #06b6d4; margin-bottom: 16px; border-bottom: 1px solid rgba(6, 182, 212, 0.3); padding-bottom: 8px; }
    section[data-testid="stSidebar"] { background: var(--bg-secondary) !important; border-right: 1px solid var(--glass-border) !important; }
    .streamlit-expanderHeader { background: var(--glass-bg) !important; border-radius: 12px !important; color: var(--text-primary) !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #7c3aed, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Phase 2: Final Project Report
    </h1>
    <p style="color: #94a3b8;">Agentic System Transformation with Professional, Ethical & Legal Integration</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Part 1: Professional & Ethical Foundation", "Part 2: Industry & Legal Aspects", "Part 3: Agentic Transformation", "Part 4: Comparative Analysis"])

with tab1:
    st.markdown("### Part 1: Professional & Ethical Foundation")
    
    with st.expander("1. Title Slide: Application Info", expanded=True):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Notes2Doc: Intelligent Notes Converter</div>
        <p><b>Team Members:</b> Fatima Obaid (22I-0475), Ayesha Tahir (22I-0475), Hadia Mazhar (22I-0487)</p>
        <p><b>Course:</b> Professional Practices in IT (PPIT)</p>
        <p><b>Objective:</b> Transforming a static OCR tool into an Agentic System.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with st.expander("2. Phase 1 Recap", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Phase 1 Recap</div>
        <ul>
            <li><b>Problem:</b> Students struggle to digitize handwritten notes containing text, math, and diagrams.</li>
            <li><b>Users:</b> Students, researchers, and professionals.</li>
            <li><b>Technology:</b> Streamlit, Google Gemini API, python-docx.</li>
            <li><b>Features:</b> Upload image, prompt Gemini, generate Word doc.</li>
            <li><b>State:</b> Purely reactive tool with no memory or autonomy.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("3. Computing as a Formal Profession", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Computing as a Formal Profession</div>
        <p>Software development requires specialized knowledge and adherence to standards, making it a formal profession.</p>
        <ul>
            <li><b>Responsibility toward Users:</b> Ensuring Notes2Doc provides accurate conversions without deceptive UI.</li>
            <li><b>Responsibility toward Society:</b> Making educational tools accessible and reliable.</li>
            <li><b>Responsibility toward Data:</b> Implementing privacy-by-design for user uploads.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("4. Ethics vs. Morals", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Ethics vs. Morals</div>
        <ul>
            <li><b>Morals:</b> Personal beliefs (e.g., "I think education should be free").</li>
            <li><b>Ethics:</b> Professional standards (e.g., "I must secure user data as per ACM guidelines").</li>
            <li><b>Application to Notes2Doc:</b> In Phase 1, we stored image states for convenience (moral choice). In Phase 2, professional ethics dictate we immediately discard images from memory to protect user privacy.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("5. Professional Ethics", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Professional Ethics: Responsibility</div>
        <ul>
            <li><b>Code Quality:</b> Writing robust API failovers instead of letting the app crash.</li>
            <li><b>Security:</b> Using environment variables for Gemini keys instead of hardcoding.</li>
            <li><b>User Safety:</b> Warning users about AI hallucinations in transcribed notes.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("6. Ethical Decision Making", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Real Decision: Speed vs. Quality</div>
        <p><b>Dilemma:</b> Should the agent use a fast, single-pass OCR (cheap but prone to errors in math/diagrams), or a multi-pass enhancement system (slower, consumes more API quota, but highly accurate)?</p>
        <p><b>Decision:</b> We implemented an adaptive strategy. It uses single-pass for clean text, but multi-pass for complex/poor-quality images, prioritizing quality over speed when necessary.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("7. Importance of Ethical Decision Making", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Impact of Ethical Choices</div>
        <ul>
            <li><b>On Users:</b> Reliable transcriptions prevent academic mistakes.</li>
            <li><b>On Society:</b> Normalizes the creation of trustworthy AI tools rather than "black boxes".</li>
            <li><b>On System Trust:</b> Explaining *why* the agent made a decision builds user confidence.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("8. Ethical Theories & Human-Centered Design", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Ethical Theories & Human-Centered Design</div>
        <p><b>Applied Theory: Deontology (Duty-based ethics)</b></p>
        <ul>
            <li>We have a duty to respect user autonomy and privacy, regardless of whether harvesting their data would yield better AI models (Utilitarian approach).</li>
            <li><b>Human-Centered Design:</b> Keeping a "Human-in-the-loop" for uncertain transcriptions. We avoid addictive engagement loops (like social media) by focusing purely on utility and user control.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("9. ACM / IEEE Code of Ethics", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">ACM / IEEE Code of Ethics</div>
        <ul>
            <li><b>Followed (ACM 1.2 - Avoid Harm):</b> Deleting data immediately to prevent data leaks.</li>
            <li><b>Followed (ACM 1.3 - Be Honest):</b> Displaying AI confidence scores so users know when to double-check the text.</li>
            <li><b>Potentially Violated (ACM 2.5 - Comprehensive Evaluation):</b> As a student project, our agent uses heuristic perception rather than rigorously validated ML classifiers for image quality.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("10. Ethical Decision Process (4-Step Model)", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">4-Step Ethical Decision Process</div>
        <p><b>Issue:</b> Agent needs to store past corrections to learn, but doing so might expose user data.</p>
        <ol>
            <li><b>Identify Issue:</b> Conflict between system improvement and data privacy.</li>
            <li><b>Analyze Stakeholders:</b> Users (want privacy + better results), Developers (want data to train agent).</li>
            <li><b>Evaluate Alternatives:</b> A) Store full documents. B) Store nothing (no learning). C) Store only abstract feedback patterns (e.g., "User prefers high detail").</li>
            <li><b>Make Justified Decision:</b> We chose C. The agent learns preferences and UI feedback scores, but never saves the raw text or images (Cybersecurity & Vulnerability consideration).</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)


with tab2:
    st.markdown("### Part 2: Industry & Legal Aspects")

    with st.expander("11. Software Development & Industry Practices", expanded=True):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Student Project vs. Software House</div>
        <ul>
            <li><b>Workflow:</b> We moved from ad-hoc coding (Phase 1) to modular, component-based architecture (Phase 2).</li>
            <li><b>Version Control:</b> Using Git for collaborative development.</li>
            <li><b>AI Ethics in Industry:</b> Software houses must legally mitigate AI bias. Our system is designed to handle different handwriting styles neutrally, though LLM biases may inherit from Gemini.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("12. Trends in IT & Agentic Systems", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Trends in IT & Agentic Systems</div>
        <p>The industry is shifting from static AI tools (like ChatGPT chatboxes) to <b>Autonomous Agents</b> that can chain thoughts, use tools, and correct their own errors. Notes2Doc aligns with this trend by automating the perception-decision-action loop.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("13. Career Relevance", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">How this Project Helps Our Careers</div>
        <ul>
            <li><b>Skills Acquired:</b> Prompt engineering, Agentic architectures, Python/Streamlit integration.</li>
            <li><b>Ethics in AI Era:</b> Companies are hiring "AI Ethics Officers". Understanding transparency and data lifecycle gives us a competitive edge in modern Software Engineering.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("14. Virtual Work & Sustainability", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Virtual Work & Sustainability</div>
        <ul>
            <li><b>Remote Collaboration:</b> Built collaboratively using cloud IDEs and version control.</li>
            <li><b>Green Computing:</b> Our agent downscales images to 1024x1024 before sending to the API. This reduces payload size, API processing time, and overall carbon footprint.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("15. Legal Aspects of Computing", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Legal Responsibilities</div>
        <p>As developers, we are legally responsible for:</p>
        <ul>
            <li><b>Data Protection:</b> Securing API keys and user uploads.</li>
            <li><b>User Rights:</b> Providing a clear Privacy Notice detailing exactly what happens to user data (built into the Agentic System page).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("16. Intellectual Property Rights (IPR)", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Intellectual Property Rights</div>
        <ul>
            <li><b>App Ownership:</b> The code is owned by the student team.</li>
            <li><b>Licensing:</b> Could be released under MIT License for educational use.</li>
            <li><b>User Content:</b> Users retain full copyright over their generated Word documents and uploaded notes.</li>
            <li><b>GDPR Mindset:</b> Applying "Right to be Forgotten" by not storing data in the first place.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("17. Computer Crimes & Risks", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Risks and Mitigation</div>
        <ul>
            <li><b>Data Theft:</b> Mitigated by in-memory processing (no database of user notes).</li>
            <li><b>Misuse:</b> Mitigated by using Google's safety filters via the Gemini API to prevent processing of illegal content.</li>
            <li><b>Unauthorized Access:</b> Mitigated by avoiding user accounts; session state is ephemeral.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("18. Computer Contracts", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Contracts & Agreements</div>
        <ul>
            <li><b>Terms of Service:</b> The "Privacy & Consent Notice" acts as a micro-contract before the user runs the agent.</li>
            <li><b>Developer Responsibilities:</b> Guaranteeing that the app functions as advertised without hidden malicious behavior.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


with tab3:
    st.markdown("### Part 3: Agentic Transformation")

    with st.expander("19. Technical Limitations of Phase 1", expanded=True):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Technical Limitations of Phase 1</div>
        <ul>
            <li><b>Static Logic:</b> Hardcoded single prompt for every image.</li>
            <li><b>No Autonomy:</b> System sits idle until user clicks 'Convert'.</li>
            <li><b>No Intelligence:</b> Blindly sends data to API without evaluating image quality or checking if the API output was actually good.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("20. Agentic System Concept", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Agentic System Concept</div>
        <p>An Agentic System follows a continuous loop:</p>
        <ol>
            <li><b>Perception:</b> Understanding the environment (analyzing image quality).</li>
            <li><b>Decision-making:</b> Choosing a path based on logic (selecting OCR strategy).</li>
            <li><b>Action:</b> Interacting with the environment (API calls, document generation).</li>
            <li><b>Learning:</b> Adapting based on feedback (updating long-term memory).</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("21. Gap Analysis", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Gap Analysis</div>
        <p>Why Phase 1 was NOT agentic:</p>
        <ul>
            <li>Lacked perception (couldn't tell if an image was blurry).</li>
            <li>Lacked decision engines (couldn't adapt behavior).</li>
            <li>Lacked memory (forgot everything after page reload).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("22. Agentic Vision", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Agentic Vision</div>
        <p><b>Transform Tool → Agent</b></p>
        <p><b>Reactive → Proactive:</b> The system now anticipates issues (like low contrast) and autonomously decides to enhance the image or perform a multi-pass transcription before returning the result to the user.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("23. Agent Architecture", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Agent Architecture</div>
        <p><b>Flow:</b> Input → Perception → Decision Engine → Action Executor → Feedback Loop</p>
        <p><b>Additions:</b> Short-term memory (session thought log) and Long-term memory (JSON data store for preferences).</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("24. Agent Type Selection", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Agent Type Selection</div>
        <p><b>Type: Goal-based / Learning Agent</b></p>
        <p><b>Justification:</b> The agent has a specific goal (maximize transcription accuracy). It evaluates the "state" of the image and chooses actions to achieve that goal. It incorporates a learning module to adjust its preferences over time based on user ratings.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("25. Operational Workflow", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Operational Workflow</div>
        <ol>
            <li><b>Observe:</b> Agent analyzes image brightness, contrast, and content type.</li>
            <li><b>Interpret:</b> Agent evaluates if preprocessing is needed.</li>
            <li><b>Decide:</b> Agent selects single-pass or multi-pass prompt.</li>
            <li><b>Act:</b> Agent preprocesses, transcribes, and formats doc.</li>
            <li><b>Learn:</b> Agent records confidence score and user feedback.</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("26. Intelligence Layer", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Intelligence Layer</div>
        <p><b>Hybrid Approach:</b></p>
        <ul>
            <li><b>Rules/Heuristics:</b> Used for Perception (image stats) and Decision (confidence thresholds).</li>
            <li><b>LLMs:</b> Google Gemini 2.5 Flash Lite is used as the core cognitive engine for text extraction and enhancement.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("27. Memory & Context", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Memory & Context</div>
        <ul>
            <li><b>Short-term Memory:</b> The `ShortTermMemory` class tracks the current session's thought log, decisions, and confidence score.</li>
            <li><b>Long-term Memory:</b> The `memory_store.json` tracks aggregate success rates, dominant content types, and learned user preferences across sessions.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("28. Autonomy Level", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Autonomy Level</div>
        <p><b>Semi-Autonomous</b></p>
        <p><b>Justification:</b> While the agent handles the entire perception-decision-action loop autonomously, the final output (document generation) is subject to human review. The agent cannot send emails or overwrite files without explicit user action.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("29. Human-in-the-Loop", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Human-in-the-Loop</div>
        <p>The human controls the system at the following checkpoints:</p>
        <ul>
            <li>Initial image upload and consent.</li>
            <li>Review and editing of transcribed text before document generation.</li>
            <li>Providing feedback (1-5 stars) to guide the agent's learning module.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("30. Ethical Agent Design", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Ethical Agent Design</div>
        <ul>
            <li><b>Privacy:</b> No image persistence.</li>
            <li><b>Bias:</b> Adaptive prompting ensures different note formats are handled fairly.</li>
            <li><b>Transparency:</b> The "Agent Thoughts" and "Audit Trail" tabs provide full explainability.</li>
            <li><b>User Control:</b> Download and edit options keep humans in charge.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("31. Risk Assessment", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Risk Assessment</div>
        <ul>
            <li><b>Incorrect Decisions:</b> The agent might misinterpret a diagram as text.</li>
            <li><b>Over-automation:</b> Users might blindly trust the AI without verifying math formulas.</li>
            <li><b>Misuse:</b> Using the tool to cheat on exams.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("32. Safety Mechanisms", expanded=False):
        st.markdown("""
        <div class="glass-card">
        <div class="slide-title">Safety Mechanisms</div>
        <ul>
            <li><b>Logging:</b> Full audit trail records what the agent did and why.</li>
            <li><b>Override:</b> Users can edit the text area before downloading the doc.</li>
            <li><b>Explainability:</b> The agent generates a report explaining its reasoning.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown("### Part 4: Comparative Analysis")
    
    st.markdown("""
    <div class="glass-card">
    <table style="width:100%; border-collapse: collapse; color: var(--text-primary);">
        <tr style="border-bottom: 2px solid var(--accent-primary); background-color: rgba(124, 58, 237, 0.1);">
            <th style="padding: 12px; text-align: left;">FEATURE</th>
            <th style="padding: 12px; text-align: left;">PHASE 1 (Static Tool)</th>
            <th style="padding: 12px; text-align: left;">AGENTIC VERSION (Phase 2)</th>
        </tr>
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <td style="padding: 12px; font-weight: bold;">Control</td>
            <td style="padding: 12px;">User-driven</td>
            <td style="padding: 12px; color: #06b6d4; font-weight: bold;">System-driven (Semi-autonomous)</td>
        </tr>
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <td style="padding: 12px; font-weight: bold;">Intelligence</td>
            <td style="padding: 12px;">Static Logic</td>
            <td style="padding: 12px; color: #06b6d4; font-weight: bold;">Adaptive (Perception & Decisions)</td>
        </tr>
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <td style="padding: 12px; font-weight: bold;">Behavior</td>
            <td style="padding: 12px;">Reactive</td>
            <td style="padding: 12px; color: #06b6d4; font-weight: bold;">Proactive (Multi-pass enhancement)</td>
        </tr>
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <td style="padding: 12px; font-weight: bold;">Memory</td>
            <td style="padding: 12px;">None (Stateless)</td>
            <td style="padding: 12px; color: #06b6d4; font-weight: bold;">Short-term + Long-term Memory</td>
        </tr>
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <td style="padding: 12px; font-weight: bold;">Transparency</td>
            <td style="padding: 12px;">Black Box</td>
            <td style="padding: 12px; color: #06b6d4; font-weight: bold;">Full Audit Trail & Thought Logs</td>
        </tr>
        <tr>
            <td style="padding: 12px; font-weight: bold;">Ethics</td>
            <td style="padding: 12px;">Unregulated</td>
            <td style="padding: 12px; color: #06b6d4; font-weight: bold;">ACM/IEEE & Privacy Compliant</td>
        </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)
