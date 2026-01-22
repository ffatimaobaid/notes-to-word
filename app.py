import streamlit as st
import google.generativeai as genai
import os
from docx import Document
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()

# --- APP CONFIG & UI STYLE ---
st.set_page_config(page_title="Notes2Doc AI", page_icon="📝", layout="wide")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    .stDownloadButton>button { width: 100%; border-radius: 20px; background-color: #008CBA; color: white; }
    .status-box { padding: 20px; border-radius: 10px; border: 1px solid #ddd; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- API FAILOVER LOGIC ---
def get_model_response(prompt, img_data):
    # Collect all available keys from .env
    keys = [os.getenv("GEMINI_KEY_1"), os.getenv("GEMINI_KEY_2"), os.getenv("GEMINI_KEY_3")]
    keys = [k for k in keys if k] # Remove empty ones

    if not keys:
        st.error("No API keys found in environment variables!")
        return None

    last_error = ""
    for i, key in enumerate(keys):
        try:
            genai.configure(api_key=key)
            # Use 2.0 Flash as it's the current stable high-speed model
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            response = model.generate_content([prompt, img_data])
            return response.text
        except Exception as e:
            last_error = str(e)
            if "429" in last_error:
                st.warning(f"Key {i+1} reached limit. Trying backup key...")
                continue
            else:
                break
    
    st.error(f"Failed after trying all keys. Error: {last_error}")
    return None

# --- HEADER ---
st.title("Notes2Doc")
st.info("Upload your handwritten notes!")

# --- LAYOUT: 2 COLUMNS ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Upload Note")
    uploaded_file = st.file_uploader("Drop your image here (JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        # Process image for API efficiency
        image.thumbnail((1024, 1024)) 
        st.image(image, caption="Preview of Note", use_container_width=True)

with col2:
    st.subheader("Editable Output")
    if uploaded_file:
        if st.button("Convert to Word"):
            with st.spinner("AI is analyzing text and diagrams..."):
                prompt = """
                Transcribe this handwritten note exactly. 
                - Convert math/chemistry formulas to readable text or LaTeX.
                - For diagrams (like benzene rings or graphs), describe them clearly in [Diagram: ...] brackets.
                - Maintain all headings and bullet points.
                - Return ONLY the transcription.
                """
                
                result_text = get_model_response(prompt, image)
                
                if result_text:
                    st.success("Conversion Successful!")
                    
                    # Text Preview
                    st.text_area("Content Preview", result_text, height=350)
                    
                    # Create Word File
                    doc = Document()
                    doc.add_heading('Transcribed Notes', 0)
                    for line in result_text.split('\n'):
                        doc.add_paragraph(line)
                    
                    bio = BytesIO()
                    doc.save(bio)
                    
                    # Download Button
                    st.download_button(
                        label="Download Word Document",
                        data=bio.getvalue(),
                        file_name="Converted_Notes.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
    else:
        st.write("Waiting for an image to be uploaded...")

# --- FOOTER ---
st.markdown("---")
st.caption("Developed for PPIT Class Assignment - January 2026")