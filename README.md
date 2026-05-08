# Notes2Doc AI: Phase 2 Agentic Transformation

An autonomous agentic web application that converts handwritten notes, mathematical equations, and scientific diagrams into editable Microsoft Word documents.

This project represents the Phase 2 transformation for the Professional Practices in IT (PPIT) course, evolving a static OCR tool into a fully agentic, ethical, and legally compliant system.

## Features

- **Agentic Pipeline (Observe → Decide → Act → Learn):** The system acts proactively, analyzing image quality, choosing transcription strategies, and adapting over time.
- **Ethics & Transparency:** Built-in audit trails, explainable decisions, and privacy-by-design (no image persistence).
- **Compliance:** Includes compliance scorecards for ACM/IEEE Code of Ethics, PECA 2016, and GDPR.
- **Intelligent OCR:** Powered by Google Gemini.
- **Analytics Dashboard:** Real-time metrics on confidence, performance trends, and learning history.

## Tech Stack
- **Frontend/Agent UI:** Streamlit (Multi-page dashboard)
- **AI/Cognitive Engine:** Google Gemini API
- **Data & Memory:** Local JSON (Short-term & Long-term memory)
- **Formatting:** python-docx, Pillow

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd notes-to-word
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_KEY_1=your_api_key_here
   GEMINI_KEY_2=your_backup_api_key_here
   ```

4. Run the Agentic System:
   ```bash
   streamlit run app.py
   ```

## Project Structure (Phase 2)
- `/agent` - Core agent logic (Perception, Decision, Action, Learning, Memory)
- `/ethics` - Privacy, Transparency, and Compliance modules
- `/pages` - Streamlit dashboard pages (Agent UI, Analytics, Report)
- `/data` - Persistent memory and audit logs
