from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 12)
        self.set_text_color(124, 58, 237) # Purple-ish
        self.cell(0, 10, "FINAL PROJECT: PHASE 2 - Notes2Doc AI", border=False, align="R")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def create_pdf():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title Slide
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(6, 182, 212) # Cyan
    pdf.cell(0, 20, "Notes2Doc: Intelligent Notes Converter", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, "Phase 2: Agentic System Transformation", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 8, "Team Members: Fatima Obaid (22I-0475), Ayesha Tahir (22I-0475), Hadia Mazhar (22I-0487)", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Course: Professional Practices in IT (PPIT)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    slides = [
        ("2. Phase 1 Recap", [
            "Problem: Students struggle to digitize handwritten notes.",
            "Users: Students, researchers, and professionals.",
            "Technology: Streamlit, Google Gemini API, python-docx.",
            "Features: Upload image, prompt Gemini, generate Word doc.",
            "State: Purely reactive tool with no memory or autonomy."
        ]),
        ("3. Computing as a Formal Profession", [
            "Software development is a formal profession requiring standards.",
            "Responsibility toward Users: Accurate conversions.",
            "Responsibility toward Society: Educational accessibility.",
            "Responsibility toward Data: Privacy-by-design."
        ]),
        ("4. Ethics vs. Morals", [
            "Morals: Personal beliefs (e.g., education should be free).",
            "Ethics: Professional standards (e.g., secure user data).",
            "Application: In Phase 2, we immediately discard images to protect privacy, aligning with professional ethics over convenience."
        ]),
        ("5. Professional Ethics", [
            "Code Quality: Robust failovers instead of crashes.",
            "Security: API keys in environment variables.",
            "User Safety: Warning users about AI hallucinations."
        ]),
        ("6. Ethical Decision Making", [
            "Dilemma: Speed vs. Quality.",
            "Decision: Adaptive strategy. Fast single-pass for clean text, multi-pass enhancement for complex/poor-quality images."
        ]),
        ("7. Importance of Ethical Decision Making", [
            "On Users: Reliable transcriptions prevent mistakes.",
            "On Society: Normalizes trustworthy AI tools.",
            "On System Trust: Explaining agent decisions builds confidence."
        ]),
        ("8. Ethical Theories & Human-Centered Design", [
            "Applied Theory: Deontology (Duty-based ethics).",
            "Duty to respect privacy, even if harvesting data improves AI.",
            "Human-Centered Design: Human-in-the-loop, avoiding addictive loops."
        ]),
        ("9. ACM / IEEE Code of Ethics", [
            "Followed (ACM 1.2): Deleting data immediately to avoid leaks.",
            "Followed (ACM 1.3): Displaying AI confidence scores.",
            "Potentially Violated (ACM 2.5): Confidence scoring relies on heuristics instead of rigorous ML evaluation."
        ]),
        ("10. Ethical Decision Process (4-Step Model)", [
            "Issue: Agent needs to learn, but must protect privacy.",
            "Analyze: Users want privacy; Developers want data.",
            "Evaluate Alternatives: Store full docs vs store nothing vs store abstract patterns.",
            "Decision: Store only abstract feedback patterns, no raw data."
        ]),
        ("11. Software Development & Industry Practices", [
            "Workflow: Modular, component-based architecture in Phase 2.",
            "Version Control: Collaborative Git usage.",
            "AI Ethics: Designing neutral handling for diverse handwriting."
        ]),
        ("12. Trends in IT & Agentic Systems", [
            "Industry shift from static AI to Autonomous Agents.",
            "Notes2Doc aligns by automating the perception-decision-action loop."
        ]),
        ("13. Career Relevance", [
            "Skills: Prompt engineering, Agentic architectures, Python.",
            "Ethics: Understanding data lifecycle is a competitive edge."
        ]),
        ("14. Virtual Work & Sustainability", [
            "Remote Collaboration: Cloud IDEs and version control.",
            "Green Computing: Downscaling images (1024x1024) reduces API payload and carbon footprint."
        ]),
        ("15. Legal Aspects of Computing", [
            "Data Protection: Securing API keys and user uploads.",
            "User Rights: Clear Privacy Notice before processing."
        ]),
        ("16. Intellectual Property Rights (IPR)", [
            "App Ownership: Code owned by the student team.",
            "Licensing: Potential MIT License.",
            "User Content: Users retain full copyright over generated docs.",
            "GDPR Mindset: Right to be Forgotten applied strictly."
        ]),
        ("17. Computer Crimes & Risks", [
            "Data Theft: Mitigated by in-memory processing.",
            "Misuse: Mitigated by Gemini API safety filters.",
            "Unauthorized Access: Mitigated by avoiding user accounts."
        ]),
        ("18. Computer Contracts", [
            "Terms of Service: Privacy & Consent Notice acts as a micro-contract.",
            "Developer Responsibilities: Guaranteeing safe functionality."
        ]),
        ("19. Technical Limitations of Phase 1", [
            "Static Logic: Hardcoded prompt for every image.",
            "No Autonomy: Sits idle until user acts.",
            "No Intelligence: Cannot evaluate input quality."
        ]),
        ("20. Agentic System Concept", [
            "Perception: Understanding image quality.",
            "Decision-making: Choosing optimal OCR strategy.",
            "Action: API calls, document generation.",
            "Learning: Adapting based on user feedback."
        ]),
        ("21. Gap Analysis", [
            "Phase 1 lacked perception, decision engines, and memory."
        ]),
        ("22. Agentic Vision", [
            "Tool -> Agent",
            "Reactive -> Proactive",
            "System anticipates issues and decides autonomously to enhance images."
        ]),
        ("23. Agent Architecture", [
            "Flow: Input -> Perception -> Decision -> Action -> Feedback Loop.",
            "Memory: Short-term (session log) and Long-term (JSON data store)."
        ]),
        ("24. Agent Type Selection", [
            "Type: Goal-based / Learning Agent.",
            "Goal: Maximize transcription accuracy.",
            "Learns user preferences over time."
        ]),
        ("25. Operational Workflow", [
            "Observe: Analyze brightness, contrast, content type.",
            "Interpret: Evaluate if preprocessing is needed.",
            "Decide: Select single or multi-pass prompt.",
            "Act: Preprocess, transcribe, format doc.",
            "Learn: Record confidence score and feedback."
        ]),
        ("26. Intelligence Layer", [
            "Rules/Heuristics for Perception & Decision.",
            "LLMs (Gemini 2.5) for text extraction and enhancement."
        ]),
        ("27. Memory & Context", [
            "Short-term Memory: Session thought log, decisions, confidence.",
            "Long-term Memory: Aggregate success rates, learned preferences."
        ]),
        ("28. Autonomy Level", [
            "Semi-Autonomous.",
            "Agent handles the loop, but document generation is subject to human review."
        ]),
        ("29. Human-in-the-Loop", [
            "Initial image upload and consent.",
            "Review/edit transcribed text.",
            "Providing 1-5 star feedback."
        ]),
        ("30. Ethical Agent Design", [
            "Privacy: No image persistence.",
            "Bias: Adaptive prompting.",
            "Transparency: Audit Trail tabs.",
            "User Control: Download and edit options."
        ]),
        ("31. Risk Assessment", [
            "Incorrect Decisions: Misinterpreting diagrams as text.",
            "Over-automation: Blind trust in AI.",
            "Misuse: Cheating on exams."
        ]),
        ("32. Safety Mechanisms", [
            "Logging: Full audit trail.",
            "Override: User can edit text before downloading.",
            "Explainability: Generated report of agent reasoning."
        ]),
        ("Comparative Analysis", [
            "Control: User-driven (Phase 1) vs System-driven (Phase 2)",
            "Intelligence: Static Logic vs Adaptive",
            "Behavior: Reactive vs Proactive",
            "Memory: Stateless vs Short/Long-term",
            "Transparency: Black Box vs Full Audit Trail",
            "Ethics: Unregulated vs ACM/IEEE Compliant"
        ])
    ]

    for title, points in slides:
        pdf.set_font("helvetica", "B", 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 12)
        pdf.set_text_color(50, 50, 50)
        for point in points:
            pdf.multi_cell(w=180, h=8, text=f"- {point}")
        pdf.ln(5)

    pdf.output("Phase2_Report.pdf")

if __name__ == "__main__":
    create_pdf()
