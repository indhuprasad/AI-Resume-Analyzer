from collections import Counter 

TARGET_SKILLS = [
    "Python", "SQL", "Machine Learning", "Deep Learning",
    "Data Analysis", "Power BI", "Excel", "Git", "GitHub",
    "Pandas", "NumPy", "Matplotlib", "Statistics",
    "Flask", "Django", "Streamlit"
]

def get_missing_skills(found_skills):
    found_lower = [s.lower() for s in found_skills]
    missing = [skill for skill in TARGET_SKILLS if skill.lower() not in found_lower]
    return missing


def generate_summary(skills, text):
    return {
        "Total Skills": len(skills),
        "Projects Mentioned": "project" in text.lower(),
        "Education Present": "education" in text.lower(),
        "Certifications Present": "certification" in text.lower()
    }


def skill_frequency(skills):
    return dict(Counter(skills))