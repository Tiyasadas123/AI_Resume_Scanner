import pdfminer.high_level

def extract_text_from_pdf(pdf_path):
    try:
        text = pdfminer.high_level.extract_text(pdf_path)
        return text
    except Exception as e:
        print("Error reading PDF:", e)
        return None

# Example usage
pdf_text = extract_text_from_pdf("sample_resume.pdf")  # Replace with your PDF file
print(pdf_text)
import docx2txt

def extract_text_from_docx(docx_path):
    try:
        text = docx2txt.process(docx_path)
        return text
    except Exception as e:
        print("Error reading DOCX:", e)
        return None

# Example usage
docx_text = extract_text_from_docx("sample_resume.docx")  # Replace with your DOCX file
print(docx_text)
import re
import spacy

nlp = spacy.load("en_core_web_sm")  # Load spaCy NLP model

def clean_resume_text(text):
    text = re.sub(r'\n+', ' ', text)  # Remove multiple newlines
    text = re.sub(r'\t+', ' ', text)  # Remove tabs
    text = re.sub(r'[^a-zA-Z0-9., ]+', '', text)  # Remove special characters except . , 
    text = text.lower()  # Convert text to lowercase

    # Remove stopwords using spaCy
    doc = nlp(text)
    cleaned_text = " ".join([token.text for token in doc if not token.is_stop])
    
    return cleaned_text

# Example usage after extracting resume text
pdf_text = extract_text_from_pdf("sample_resume.pdf")
cleaned_pdf_text = clean_resume_text(pdf_text)
print("Cleaned PDF Resume Text:", cleaned_pdf_text)

docx_text = extract_text_from_docx("sample_resume.docx")
cleaned_docx_text = clean_resume_text(docx_text)
print("Cleaned DOCX Resume Text:", cleaned_docx_text)
import re
print("\nExtracted PDF Text:\n", cleaned_pdf_text)
print("\nExtracted DOCX Text:\n", cleaned_docx_text)

# Function to extract email
def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

# Function to extract phone number
def extract_phone(text):
    phone_pattern = r'\+?\d{1,3}?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4,6}'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else None

# Function to extract skills (Modify skill list as needed)
def extract_skills(text):
    skills_list = ["Python", "Java", "C++", "Machine Learning", "Deep Learning",
                   "Data Analysis", "SQL", "HTML", "CSS", "JavaScript",
                   "React", "Node.js", "TensorFlow", "PyTorch", "Excel"]
    
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return list(set(found_skills))  # Remove duplicates


# Extract details from cleaned text
if pdf_text:
    print("\nExtracted Email (PDF):", extract_email(cleaned_pdf_text))
    print("Extracted Phone Number (PDF):", extract_phone(cleaned_pdf_text))
    print("Extracted Skills (PDF):", extract_skills(cleaned_pdf_text))

if docx_text:
    print("\nExtracted Email (DOCX):", extract_email(cleaned_docx_text))
    print("Extracted Phone Number (DOCX):", extract_phone(cleaned_docx_text))
    print("Extracted Skills (DOCX):", extract_skills(cleaned_docx_text))
# Function to extract name using spaCy
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":  
            name = ent.text.split()[:2]  # Take only the first two words
            return " ".join(name)
    return None

# Extract Name from PDF
if pdf_text:
    print("\nExtracted Name (PDF):", extract_name(cleaned_pdf_text))

# Extract Name from DOCX
if docx_text:
    print("\nExtracted Name (DOCX):", extract_name(cleaned_docx_text))


import json
import pandas as pd

# Function to save data as JSON
def save_as_json(data, filename="resume_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"\n✅ Data saved to {filename}")

# Function to save data as CSV
def save_as_csv(data, filename="resume_data.csv"):
    df = pd.DataFrame([data])  # Convert dictionary to DataFrame
    df.to_csv(filename, index=False)
    print(f"\n✅ Data saved to {filename}")

# Collect extracted information
resume_data = {
    "Name": extract_name(cleaned_pdf_text) or extract_name(cleaned_docx_text),
    "Email": extract_email(cleaned_pdf_text) or extract_email(cleaned_docx_text),
    "Phone": extract_phone(cleaned_pdf_text) or extract_phone(cleaned_docx_text),
    "Skills": extract_skills(cleaned_pdf_text) or extract_skills(cleaned_docx_text)
}

# Save the extracted data
save_as_json(resume_data)
save_as_csv(resume_data)
