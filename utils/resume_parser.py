import fitz
from utils.extractors.personal import extract_personal
from utils.extractors.education import extract_education
from utils.extractors.experience import extract_experience
from utils.extractors.skills import extract_skills
from utils.extractors.links import extract_links
from utils.extractors.projects import extract_projects

def parse_resume(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()

    parsed_data = {
        "personal_details": extract_personal(text),
        "education": extract_education(text),                # Returns list of 1 object with degree, college, year, cgpa
        "experience": extract_experience(text),              # Returns 1 experience dict (auto-filled one)
        "skills": extract_skills(text),                     # Returns dict of key_skills, soft_skills, tools
        "projects": extract_projects(text),
        "links": extract_links(text, file_path)                         # Returns dict with linkedin, website, social[]
    }

    print("✅ EDUCATION PARSED:", parsed_data['education'])
    print("✅ EXPERIENCE PARSED:", parsed_data['experience'])
    print("✅ LINKS PARSED:", parsed_data['links'])
    print("✅ PROJECTS PARSED:", parsed_data['projects']) 
    return parsed_data
