import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Import all your extractors
from utils.extractors.personal import extract_personal
from utils.extractors.work import extract_work
from utils.extractors.education import extract_education
from utils.extractors.skills import extract_skills
from utils.extractors.links import extract_links
from utils.extractors.projects import extract_projects
from utils.extractors.experience import extract_experience

# ✅ THIS IS THE FIXED FUNCTION
def extract_full_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)  # Get the text from the PDF
    return {
        "personal_details": extract_personal(text),
        "education": extract_education(text),
        "work": extract_work(text),
        "skills": extract_skills(text),
        "links": extract_links(text),
        "projects": extract_projects(text),
        "experience": extract_experience(text)
    }
