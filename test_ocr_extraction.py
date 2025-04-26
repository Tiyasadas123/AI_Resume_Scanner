from pdf2image import convert_from_path
import pytesseract

# 🔹 Add Tesseract path (for OCR)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔹 Manually specify the Poppler path
poppler_path = r"C:\Users\tiyas\OneDrive\Desktop\Release-24.08.0-0\poppler-24.08.0\Library\bin"

def extract_text_from_image_pdf(pdf_path):
    images = convert_from_path(pdf_path, poppler_path=poppler_path)  # Add poppler_path here
    text = ""
    
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    
    return text.strip()

# 🔹 Change this to your actual PDF file name
pdf_path = "sample_resume.pdf"  

extracted_text = extract_text_from_image_pdf(pdf_path)

if extracted_text:
    print("Extracted Text from PDF:\n", extracted_text)
else:
    print("No text extracted. Check if Tesseract is installed properly.")
