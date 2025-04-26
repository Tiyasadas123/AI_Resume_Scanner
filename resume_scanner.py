import re
import docx2txt
import pytesseract
import pdf2image
import os
from PIL import Image
import streamlit as st

# ---------- Extraction Functions ----------

def extract_text_from_pdf(pdf_path):
    try:
        images = pdf2image.convert_from_path(pdf_path)
        text = ""
        for i, image in enumerate(images):
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return ""

def extract_text_from_docx(docx_path):
    try:
        return docx2txt.process(docx_path)
    except Exception as e:
        return ""

def extract_name(text):
    match = re.findall(r"(?i)(Tiyasa\s+Das|[A-Z][a-z]+\s+[A-Z][a-z]+)", text)
    if match:
        return match[0]
    return "Name Not Found"

def extract_education(text):
    college_matches = re.findall(r"(?i)(Techno International Batanagar)", text)
    school_matches = re.findall(r"(?i)(Sankrail Abhoy Charan High School|Sankrail Girls.*?School.*?)", text)
    colleges = ", ".join(set(college_matches)) if college_matches else "College Not Found"
    schools = ", ".join(set(school_matches)) if school_matches else "School Not Found"
    return colleges, schools

def extract_city(text):
    city_keywords = [
        "Kolkata", "Howrah", "Delhi", "Mumbai", "Bangalore",
        "Pune", "Chennai", "Hyderabad", "Ahmedabad", "Jaipur", 
        "Lucknow", "Bhopal", "Chandigarh", "Patna", "Nagpur"
    ]
    found_cities = [city for city in city_keywords if re.search(rf'\b{re.escape(city)}\b', text, re.IGNORECASE)]
    return found_cities[0] if found_cities else "City Not Found"



def extract_email(text):
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return email_match.group() if email_match else "Email Not Found"

def extract_phone(text):
    phone_match = re.search(r'\b\d{10}\b', text)
    return phone_match.group() if phone_match else "Phone Number Not Found"

def extract_skills(text):
    known_skills = [
        "Java", "Python", "C", "C++", "HTML", "CSS", "JavaScript",
        "SQL", "Machine Learning", "AI", "Data Science", "Leadership",
        "Communication", "Creativity", "Teamwork", "Negotiation"
    ]
    found = [skill for skill in known_skills if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE)]
    return ", ".join(found) if found else "Skills Not Found"

def extract_experience(text):
    exp_match = re.search(r'(\d+)\s*(\+)?\s*(years|yrs)\s+(of\s+)?experience', text, re.IGNORECASE)
    if exp_match:
        return f"{exp_match.group(1)} years"
    return "Experience Not Found"

# ---------- Streamlit Interface ----------

st.title("📄 AI Resume Scanner")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    file_path = f"temp/{uploaded_file.name}"
    os.makedirs("temp", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)
    else:
        resume_text = ""

    if resume_text:
        st.subheader("✅ Extracted Resume Details")
        st.markdown(f"**👤 Extracted Name**\n\n{extract_name(resume_text)}")
        colleges, schools = extract_education(resume_text)
        st.markdown(f"**🏫 Extracted College**\n\n{colleges}")
        st.markdown(f"**🏫 Extracted School**\n\n{schools}")
        st.markdown(f"**🌍 Extracted City/Location**\n\n{extract_city(resume_text)}")
        st.markdown(f"**📧 Extracted Email**\n\n{extract_email(resume_text)}")
        st.markdown(f"**📞 Extracted Phone Number**\n\n{extract_phone(resume_text)}")
        st.markdown(f"**🛠 Extracted Skills**\n\n{extract_skills(resume_text)}")
        st.markdown(f"**📊 Extracted Experience**\n\n{extract_experience(resume_text)}")
    else:
        st.error("❌ Could not extract text from the resume. Please try with a different file.")

    os.remove(file_path)
