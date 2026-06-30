import streamlit as st 
from resume_parser import extract_text
from skill_extractor import extract_skills
from ats_score import calculate_ats_score
from analytics import get_missing_skills, generate_summary, skill_frequency
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ----------------------------
# STYLE 
# ----------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f4f6fb;
    font-weight: 500;   /* increased base thickness */
}

/* Global text */
html, body, [class*="css"]  {
    font-weight: 500;   /* makes all default text thicker */
}

/* Title */
h1 {
    text-align: center;
    color: #1e3a8a;
    font-weight: 900;   /* very bold */
}

/* Subheadings */
h2, h3, h4 {
    font-weight: 800;
}

/* Card */
.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    margin-bottom: 15px;
    font-weight: 600;   /* thicker text inside cards */
}

/* Metrics */
div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    font-weight: 700;   /* bold metrics */
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    font-weight: 600;
}

/* Skill pills */
.skill-pill {
    display: inline-block;
    padding: 6px 10px;
    margin: 4px;
    border-radius: 20px;
    background-color: #e0e7ff;
    color: #1e3a8a;
    font-size: 13px;
    font-weight: 700;   /* thicker skill text */
}

/* spacing */
.space {
    margin-top: 25px;
    margin-bottom: 25px;
}

/* paragraphs + markdown text */
p, span, div {
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# TITLE
# ----------------------------
st.title("📄 AI Resume Analyzer")

st.markdown(
    "<p style='text-align:center; color:#6b7280; font-size:16px; font-weight:600;'>Smart Resume Intelligence System</p>",
    unsafe_allow_html=True
)

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("📤 Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    st.markdown("---")
    st.write("⚡ AI will analyze:")
    st.write("✔ Skills")
    st.write("✔ ATS Score")
    st.write("✔ Missing Skills")
    st.write("✔ Resume Quality")

# ----------------------------
# REALISTIC ATS SCORE 
# ----------------------------
def calculate_real_ats(skills, missing_skills):

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

# ----------------------------
# MAIN
# ----------------------------
if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    text = extract_text(uploaded_file)
    skills = extract_skills(text)

    missing_skills = get_missing_skills(skills)
    summary = generate_summary(skills, text)
    freq = skill_frequency(skills)

    ats_score = calculate_real_ats(skills, missing_skills)

    status = (
        "🟢 Excellent" if ats_score >= 85
        else "🟡 Good" if ats_score >= 70
        else "🔴 Needs Improvement"
    )

    # ----------------------------
    # OVERVIEW
    # ----------------------------

    st.markdown("## 📊 Resume Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("🧠 Skills Found", len(skills))
    c2.metric("📊 ATS Score", f"{ats_score}%")
    c3.metric("📌 Status", status)

    st.progress(ats_score / 100)

    # ----------------------------
    # SKILLS SECTION
    # ----------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧠 Skills")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for i in range(0, len(skills), 2):
            c = st.columns(2)
            c[0].markdown(f"<span class='skill-pill'>✔️ {skills[i]}</span>", unsafe_allow_html=True)
            if i + 1 < len(skills):
                c[1].markdown(f"<span class='skill-pill'>✔️ {skills[i+1]}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### ❌ Missing Skills")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for i in range(0, len(missing_skills), 2):
            c = st.columns(2)
            c[0].markdown(f"❌ {missing_skills[i]}")
            if i + 1 < len(missing_skills):
                c[1].markdown(f"❌ {missing_skills[i+1]}")
        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------
    # INSIGHTS + CHART
    # ----------------------------
  
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 📋 Resume Insights")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for k, v in summary.items():
            st.write(f"**{k}:** {v}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("### 📊 Skill Chart")

        if freq:
            df = pd.DataFrame({
                "Skill": list(freq.keys()),
                "Count": list(freq.values())
            })
            st.bar_chart(df.set_index("Skill"))

    # ----------------------------
    # AI FEEDBACK ENGINE
    # ----------------------------

    st.markdown("## 🤖 AI Feedback Engine")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # ----------------------------
    # SCORE EXPLANATION
    # ----------------------------

    if ats_score >= 85:
        st.success("✔ High score due to strong skills + project presence + structured resume.")
    elif ats_score >= 70:
        st.info("⚠ Good foundation but missing advanced AI/ML + deployment skills.")
    else:
        st.warning("❌ Weak resume — lacks technical depth and project impact.")

    # ----------------------------
    # IMPROVEMENTS
    # ----------------------------

    st.markdown("### 🚀 Improvements")

    improvements = []

    if "machine learning" in [m.lower() for m in missing_skills]:
        improvements.append("Add Machine Learning projects (classification/regression).")

    if "deep learning" in [m.lower() for m in missing_skills]:
        improvements.append("Include Deep Learning (CNN, NLP projects).")

    if "numpy" in [m.lower() for m in missing_skills]:
        improvements.append("Use NumPy in projects for data handling strength.")

    if "flask" in [m.lower() for m in missing_skills]:
        improvements.append("Build Flask API or deployment project.")

    if len(skills) < 10:
        improvements.append("Increase skill diversity (SQL, ML tools, visualization).")

    improvements.append("Improve GitHub README with screenshots + project explanations.")
    improvements.append("Add at least 1 deployed project (Streamlit/Flask app).")

    for imp in improvements[:5]:
        st.write("•", imp)

    # ----------------------------
    # JOB ROLE
    # ----------------------------

    st.markdown("### 🎯 Job Role Suggestion")

    if ats_score >= 85:
        st.success("Data Analyst / Junior AI Engineer roles")
    elif ats_score >= 70:
        st.info("Entry-level Data Analyst — improve ML + projects")
    else:
        st.warning("Focus on internships + project building first")

    st.markdown("</div>", unsafe_allow_html=True)