import streamlit as st
from components.builder import build_resume
from components.ai_helpers import ai_generate_experience
import io

st.title("🧠 AI-Powered Resume Builder")

with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")
    summary = st.text_area("Professional Summary")

    skills = st.text_input("Skills (comma-separated)")

    st.markdown("### Work Experience with AI")
    experience = []
    for i in range(1, 3):
        st.markdown(f"**Experience {i}**")
        role = st.text_input(f"Role {i}")
        company = st.text_input(f"Company {i}")
        duration = st.text_input(f"Duration {i}")
        industry = st.selectbox(f"Industry/Work Culture {i}", ["Agile", "Startup", "MNC", "Fintech", "Healthcare", "DevOps", "Other"], key=f"ind_{i}")
        raw_tasks = st.text_area(f"Tasks {i} (optional)", key=f"tasks_{i}")

        enriched = ""
        if st.form_submit_button(f"Enrich Experience {i} with AI"):
            enriched = ai_generate_experience(role, industry, raw_tasks)
            st.session_state[f"enriched_{i}"] = enriched

        enriched = st.session_state.get(f"enriched_{i}", "")
        st.text_area(f"AI Suggestions {i}", value=enriched, height=100)

        if role and company:
            experience.append({
                "role": role,
                "company": company,
                "duration": duration,
                "industry": industry,
                "responsibilities": enriched.split("\n") if enriched else raw_tasks.split("\n")
            })

    education_degree = st.text_input("Degree")
    education_institute = st.text_input("Institute")
    education_year = st.text_input("Graduation Year")

    submitted = st.form_submit_button("Generate Resume")
    if submitted:
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "summary": summary,
            "skills": [s.strip() for s in skills.split(',')],
            "experience": experience,
            "education_degree": education_degree,
            "education_institute": education_institute,
            "education_year": education_year
        }

        resume_doc = build_resume(data)
        buffer = io.BytesIO()
        resume_doc.save(buffer)
        buffer.seek(0)

        st.success("Resume Generated!")
        st.download_button("📄 Download Word Resume", buffer, f"{name.replace(' ', '_')}_Resume.docx")
