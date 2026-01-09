import streamlit as st
import os
import re
import plotly.graph_objects as go
import sys

# ====== Add utils folder to path ======
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ====== IMPORT UTILS ======
from utils.resume_parser import extract_text
from utils.skill_extractor import extract_skills
from utils.experience_extractor import extract_years_of_experience, extract_required_experience
from utils.projects_extractor import extract_projects
from utils.extra_curricular_extractor import extract_extra_curricular
from utils.ai_matcher import semantic_similarity
from utils.skills import SKILL_SET

# ====== DEFAULT CERTIFICATIONS ======
DEFAULT_CERTIFICATIONS = [
    "AWS", "Azure", "Google Cloud", "PMP", "Scrum", "ITIL", "Six Sigma",
    "Tableau", "Power BI", "Cisco", "CompTIA", "CISSP", "TensorFlow", "PyTorch"
]

# ====== STREAMLIT CONFIG ======
st.set_page_config(
    page_title="AI Resume Screening & Candidate Ranking",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Resume Screening & Candidate Ranking System")
st.write(
    "An AI-driven system that evaluates resumes for **skills, experience, certifications, projects, and extra-curriculars**, "
    "with visual dashboards and improvement suggestions."
)

# ====== STEP 1: UPLOAD RESUME ======
uploaded_resume = st.file_uploader("📄 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
resume_text = ""
resume_skills = []
resume_experience = 0
resume_certs = []
resume_projects = []
resume_extracurriculars = []

if uploaded_resume:
    st.success("✅ Resume uploaded successfully")
    resume_text = extract_text(uploaded_resume)

    # Extract skills
    resume_skills = extract_skills(resume_text)

    # Extract experience
    resume_experience = extract_years_of_experience(resume_text)

    # Extract certifications
    resume_certs = [cert for cert in DEFAULT_CERTIFICATIONS if re.search(rf"\b{cert}\b", resume_text, re.IGNORECASE)]

    # Extract projects/internships
    resume_projects = extract_projects(resume_text)

    # Extract extra-curriculars
    resume_extracurriculars = extract_extra_curricular(resume_text)

    st.subheader("🔍 Resume Insights")
    st.write("**Skills Extracted:**", resume_skills if resume_skills else "None detected")
    st.write("**Estimated Experience:**", f"{resume_experience} years")
    st.write("**Certifications:**", resume_certs if resume_certs else "None detected")
    st.write("**Projects / Internships:**", resume_projects if resume_projects else "None detected")
    st.write("**Extra-curricular / Achievements:**", resume_extracurriculars if resume_extracurriculars else "None detected")

# ====== STEP 2: UPLOAD JOB DESCRIPTION ======
st.divider()
st.subheader("📌 Job Description Analysis")

uploaded_jd = st.file_uploader("📝 Upload Job Description (TXT/DOCX)", type=["txt","docx"])
jd_text = ""
jd_skills = []
required_experience = 0

if uploaded_jd:
    jd_text = extract_text(uploaded_jd)
    jd_skills = extract_skills(jd_text)
    required_experience = extract_required_experience(jd_text)

    st.subheader("📋 Job Requirements")
    st.write("**Required Skills:**", jd_skills if jd_skills else "None detected")
    st.write("**Required Experience:**", f"{required_experience}+ years")

# ====== STEP 3: AI SCREENING & SCORING ======
if resume_skills and jd_skills:

    # Skills match
    matched_skills = sorted(set(resume_skills) & set(jd_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))
    skill_match_score = round((len(matched_skills) / len(jd_skills)) * 100, 2)

    # Semantic similarity
    semantic_score = semantic_similarity(resume_text, jd_text)

    # Experience score
    experience_score = 100 if resume_experience >= required_experience else max(0, (resume_experience / required_experience) * 100)

    # Certification score
    cert_score = round((len(resume_certs) / len(DEFAULT_CERTIFICATIONS)) * 100, 2) if DEFAULT_CERTIFICATIONS else 0

    # Project score (max 5 projects)
    project_score = round(min(len(resume_projects), 5) / 5 * 100, 2)

    # Extra-curricular score (max 5)
    extra_score = round(min(len(resume_extracurriculars), 5) / 5 * 100, 2)

    # Weighted final AI score
    final_ai_score = round(
        0.35*skill_match_score +
        0.25*semantic_score +
        0.20*experience_score +
        0.10*cert_score +
        0.05*project_score +
        0.05*extra_score,
        2
    )

    # ====== DASHBOARD METRICS ======
    st.divider()
    st.subheader("📊 AI Screening Scores")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("🧩 Skills Match", f"{skill_match_score}%")
    col2.metric("🧠 Semantic Match", f"{semantic_score}%")
    col3.metric("🧑‍💼 Experience", f"{experience_score}%")
    col4.metric("📜 Certifications", f"{cert_score}%")
    col5.metric("📝 Projects", f"{project_score}%")
    col6.metric("🏆 Extra-curricular", f"{extra_score}%")

    # ====== GAUGE CHART ======
    st.subheader("🎯 Overall Candidate Match Score")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=final_ai_score,
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#1F618D"},
            'steps': [
                {'range': [0, 40], 'color': "#F1948A"},
                {'range': [40, 70], 'color': "#F7DC6F"},
                {'range': [70, 100], 'color': "#82E0AA"},
            ],
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # ====== SKILL GAP ANALYSIS ======
    st.subheader("📉 Skill Gap Analysis")
    fig_gap = go.Figure()
    fig_gap.add_bar(
        y=["Matched Skills", "Missing Skills"],
        x=[len(matched_skills), len(missing_skills)],
        orientation="h",
        marker=dict(color=["#2ECC71", "#E74C3C"])
    )
    fig_gap.update_layout(xaxis_title="Number of Skills", height=300)
    st.plotly_chart(fig_gap, use_container_width=True)

    # ====== SKILL COVERAGE PIE ======
    st.subheader("📊 Skill Coverage Distribution")
    fig_pie = go.Figure(
        data=[go.Pie(
            labels=["Matched Skills", "Missing Skills"],
            values=[len(matched_skills), len(missing_skills)],
            hole=0.55,
            marker=dict(colors=["#2ECC71", "#E74C3C"]),
            textinfo="label+percent"
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # ====== AI RECOMMENDATIONS ======
    st.subheader("💡 AI Resume Improvement Suggestions")
    if missing_skills:
        for skill in missing_skills:
            st.write(f"➕ Gain experience or certification in **{skill}**")
    if resume_experience < required_experience:
        st.warning(f"📌 Candidate lacks {required_experience - resume_experience} years of required experience")
    if not resume_certs:
        st.info("📌 Add relevant certifications to strengthen your resume")
    if not resume_projects:
        st.info("📌 Include projects or internships to showcase practical experience")
    if not resume_extracurriculars:
        st.info("📌 Add extra-curricular activities / achievements to highlight versatility")

    # ====== FINAL VERDICT ======
    st.subheader("🧾 Final Screening Verdict")
    if final_ai_score >= 75:
        st.success("✅ Strong Match – Candidate can be shortlisted.")
    elif final_ai_score >= 50:
        st.warning("🟡 Partial Match – Consider after upskilling.")
    else:
        st.error("❌ Not suitable for this role.")

st.markdown("---")
st.markdown("🚀 *Enterprise-Style AI Resume Screening System • Skills • Semantic • Experience • Certifications • Projects • Extra-curricular*")
