# List of technical skills 

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data analytics",
    "data analysis",
    "statistics",
    "git",
    "github",
    "streamlit",
    "jupyter notebook",
    "vs code",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "flask",
    "django"
]

def extract_skills(text):
    text = text.lower()

    detected_skills = []

    for skill in SKILLS:
        if skill in text:
            detected_skills.append(skill.title())

    return sorted(list(set(detected_skills)))