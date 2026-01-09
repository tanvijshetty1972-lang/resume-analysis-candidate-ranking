# dashboard/dashboard.py
import streamlit as st
import os
import sys
from fpdf import FPDF
import plotly.graph_objects as go
import pandas as pd

# =========================================================
# Add PROJECT ROOT to Python path
# =========================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =========================================================
# Import utils
# =========================================================
from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.recommendations import generate_recommendations
from utils.matcher import match_resume_to_job
from utils.skills import SKILL_SET, SKILL_CATEGORIES

# =========================================================
# Streamlit config
# =========================================================
st.set_page_config(
    page_title="Intelligent Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Intelligent Resume Analyzer")
st.write(
    "Upload your resume to extract skills, get improvement suggestions, "
    "and check how well it matches a job description."
)

# =========================================================
# STEP 1: Resume Upload
# =========================================================
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
resume_text = ""
extracted_skills = []

if uploaded_file:
    st.success("✅ Resume uploaded successfully!")
    resume_text = extract_text_from_pdf(uploaded_file)

    with st.expander("🧪 Debug: Extracted Resume Text"):
        st.text(resume_text[:1500])

    extracted_skills = extract_skills(resume_text)

    st.subheader("🔍 Extracted Skills")
    if extracted_skills:
        st.write(extracted_skills)
    else:
        st.warning("⚠️ No recognizable skills found in the resume.")

    st.subheader("💡 Resume Improvement Suggestions")
    recommendations = generate_recommendations(extracted_skills)
    if recommendations:
        for rec in recommendations:
            st.write("•", rec)
    else:
        st.success("🎉 Great job! Your resume already covers key skills.")

# =========================================================
# STEP 2: Job Description Matching
# =========================================================
st.divider()
st.subheader("📌 Job Description Matching")
job_file = st.file_uploader("Upload Job Description (TXT only)", type=["txt"])
job_text = ""

if job_file and extracted_skills:
    job_text = job_file.read().decode("utf-8").lower()
    st.success("✅ Job description uploaded successfully!")

    match_score, matched_skills, missing_skills = match_resume_to_job(
        extracted_skills, job_text
    )

    st.subheader("📊 Job Match Analysis")
    st.metric("🎯 Resume Match Score", f"{match_score}%")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Matched Skills")
        st.write(matched_skills if matched_skills else "None")
    with col2:
        st.subheader("❌ Missing Skills")
        st.write(missing_skills if missing_skills else "None")

    # =========================================================
    # STEP 3: Skill Match Bar Chart
    # =========================================================
    st.subheader("📊 Skill Coverage Chart")
    skill_categories = SKILL_CATEGORIES.keys()
    matched_count = []
    missing_count = []

    for cat, skills in SKILL_CATEGORIES.items():
        matched = len(set([s.lower() for s in skills]) & set([m.lower() for m in matched_skills]))
        missing = len(set([s.lower() for s in skills]) & set([m.lower() for m in missing_skills]))
        matched_count.append(matched)
        missing_count.append(missing)

    fig = go.Figure(data=[
        go.Bar(name='Matched', x=list(skill_categories), y=matched_count, marker_color='green'),
        go.Bar(name='Missing', x=list(skill_categories), y=missing_count, marker_color='red')
    ])
    fig.update_layout(barmode='group', title='Skill Match by Category')
    st.plotly_chart(fig, width="stretch")

    # =========================================================
    # STEP 4: Resume Coverage Pie Chart
    # =========================================================
    st.subheader("📊 Overall Resume Coverage")
    total_skills = len(matched_skills) + len(missing_skills)
    coverage = [len(matched_skills), len(missing_skills)]
    labels = ['Matched Skills', 'Missing Skills']

    fig2 = go.Figure(data=[go.Pie(labels=labels, values=coverage, hole=0.3)])
    st.plotly_chart(fig2, width="stretch")

    # =========================================================
    # STEP 5: Downloadable PDF Report
    # =========================================================
    st.subheader("📄 Download Analysis Report")
    if st.button("Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Resume Analysis Report", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Resume Skills: {', '.join(extracted_skills)}", ln=True)
        pdf.cell(0, 8, f"Improvement Suggestions: {', '.join(recommendations)}", ln=True)
        pdf.cell(0, 8, f"Job Match Score: {match_score}%", ln=True)
        pdf.cell(0, 8, f"Matched Skills: {', '.join(matched_skills)}", ln=True)
        pdf.cell(0, 8, f"Missing Skills: {', '.join(missing_skills)}", ln=True)

        report_path = "resume_analysis_report.pdf"
        pdf.output(report_path)
        with open(report_path, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )

st.markdown("---")
st.markdown("🚀 *Built with Python, NLP & Streamlit*")
