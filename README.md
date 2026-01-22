# Notes2Doc: AI-Powered Handwriting OCR 

A streamlined web application that converts handwritten notes, mathematical equations, and scientific diagrams into editable Microsoft Word documents.

## Live Demo
[**Click here to view the Live App**](https://notes-to-word-ppitassignment.streamlit.app/)

## Features
- **Intelligent OCR:** Powered by Google Gemini 2.0 Flash to understand messy handwriting.
- **Formula Support:** Converts handwritten math and chemistry notations into readable text/LaTeX.
- **Diagram Description:** Automatically identifies and describes diagrams found in notes.
- **Auto-Export:** Generates standard `.docx` files ready for Microsoft Word.
- **Optimized for SaaS:** Built with Streamlit and deployed with secure API management.

## Tech Stack
- **Frontend/Hosting:** Streamlit Cloud
- **AI Model:** Google Gemini API (Multimodal)
- **Backend:** Python (python-docx, Pillow, python-dotenv)

## How to Use
1. Upload an image of your notes (JPG/PNG).
2. The AI processes the image and provides a text preview.
3. Click "Download Word Document" to get your editable file.
