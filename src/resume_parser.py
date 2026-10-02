import pymupdf
import json
import re

def extract_text_from_pdf(pdf_path):

    document = pymupdf.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

skill_blacklist = {
    'data',
    'machine',
    'science',
    'training',
    'programming',
    'engineering',
    'technology',
    'system',
    'time',
    'access',
    'education',
    'com',
    'tools',
    'process',
    'technical',
    'computer',
    'project',
    'program',
    'internship',
    'hiring',
    'portfolio',
    'engagement',
    'computer science',
    'analysis',
    'bi',
    'insurance',
    'dashboards',
    'integration',
    'linkedin',
    'evaluation',
    'visualization',
    'gui',
    'api',
    'api integration',
    'data science'
}

def extract_skills(text, skills):
    text=text.lower()
    found_skills=[]

    for skill in skills:
        if skill in skill_blacklist:
            continue
        pattern=r'\b'+re.escape(skill.lower())+r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)
    return found_skills

# Load skill vocalbulary
with open("data/common_skills.json","r") as f:
    common_skills=json.load(f)


def extract_section(text, heading, next_heading):
    pattern=rf'{heading}\s*(.*?)(?={"|".join(next_heading)}|$)'

    match=re.search(pattern,text,re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""
headings = [
    "education",
    "experience",
    "projects",
    "skills",
    "certifications"
]


resume_text = extract_text_from_pdf("resumes/deepika_compressed.pdf")

candidate_skills=extract_skills(resume_text,common_skills)

education = extract_section(
    resume_text,
    "education",
    ["experience", "projects", "skills", "certifications"]
)
experience = extract_section(
    resume_text,
    "experience",
    ["projects", "skills", "certifications", "education"]
)

projects = extract_section(
    resume_text,
    "projects",
    ["experience", "skills", "certifications", "education"]
)

skills_section = extract_section(
    resume_text,
    "skills",
    ["experience", "projects", "certifications", "education"]
)

candidate_profile = {
    "skills": candidate_skills,
    "experience":experience,
    "projects":projects,
    "skills":candidate_skills
}

with open("data/candidate_profile.json","w") as f:
    json.dump(candidate_profile, f, indent=4)

print("candidate_profile SAVED!")