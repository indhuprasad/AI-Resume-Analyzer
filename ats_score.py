def calculate_ats_score(text, skills, missing_skills): 
    base = (len(skills) / 20) * 100

    penalty_keywords = {
        "machine learning": 12,
        "deep learning": 12,
        "numpy": 6,
        "flask": 5,
        "django": 5,
        "streamlit": 3
    }

    penalty = 0
    for m in missing_skills:
        m_low = m.lower()
        if m_low in penalty_keywords:
            penalty += penalty_keywords[m_low]

    if len(skills) < 8:
        penalty += 10

    score = base - penalty
    return max(0, min(round(score, 2), 100))