import streamlit as st
from pdf2image import convert_from_path
import pytesseract
import docx2txt
import spacy
import os

# 🔹 Manually specify Poppler path (change this if needed)
poppler_path = r"C:\Users\tiyas\OneDrive\Desktop\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔹 Load Spacy NLP Model
nlp = spacy.load("en_core_web_sm")

# 🔹 Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    text = ""
    
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    
    return text.strip()

# 🔹 Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# 🔹 Function to extract entities (Names, Emails, Phone, Skills)
def extract_entities(text):
    doc = nlp(text)
    email = None
    phone = None
    skills = []
    
    for token in doc:
        if token.like_email:
            email = token.text
        if token.like_num and len(token.text) >= 10:
            phone = token.text
    
    # Extract Skills (Basic)
    skill_keywords = {"python", "java", "c++", "html", "css", "javascript", "machine learning", "deep learning", "sql"}
    for token in doc:
        if token.text.lower() in skill_keywords:
            skills.append(token.text.lower())

    return {"Email": email, "Phone": phone, "Skills": list(set(skills))}

# 🔹 Streamlit UI
st.title("📄 Resume Scanner - AI Powered")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    with open(f"temp_resume.{file_extension}", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.subheader("Extracted Information:")
    
    if file_extension == "pdf":
        extracted_text = extract_text_from_pdf(f"temp_resume.pdf")
    else:
        extracted_text = extract_text_from_docx(f"temp_resume.docx")
    
    st.text_area("Extracted Text", extracted_text, height=200)
    
    # Extract structured data
    extracted_data = extract_entities(extracted_text)
    
    st.write("📧 **Email:**", extracted_data["Email"])
    st.write("📞 **Phone:**", extracted_data["Phone"])
    st.write("🛠️ **Skills:**", ", ".join(extracted_data["Skills"]))

    # Clean up temporary file
    os.remove(f"temp_resume.{file_extension}")
