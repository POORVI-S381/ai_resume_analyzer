import streamlit as st
from pypdf import PdfReader
from docx import Document

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.subheader("Resume Analysis and Job Recommendation System")
st.write("Upload your resume to discover your skills, suitable job roles, and learning opportunities.")

resume = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

if resume is not None:
    st.success("Resume uploaded successfully!")
    st.write("File name:", resume.name)

    resume_text = ""

    try:
        if resume.name.lower().endswith(".pdf"):
            reader = PdfReader(resume)
            for page in reader.pages:
                resume_text += page.extract_text() or ""

        elif resume.name.lower().endswith(".docx"):
            document = Document(resume)
            for paragraph in document.paragraphs:
                resume_text += paragraph.text + "\n"

        if resume_text.strip():
            st.subheader("Extracted Resume Text")
            st.text_area("Resume content", resume_text, height=250)

            skills_list = [
                "Python", "SQL", "Pandas", "NumPy",
                "Machine Learning", "Scikit-learn",
                "Streamlit", "Git", "Java", "C++",
                "Data Analysis", "Matplotlib"
            ]

            found_skills = [
                skill for skill in skills_list
                if skill.lower() in resume_text.lower()
            ]
            total_skills = len(skills_list)
            resume_score =round(len(found_skills) / total_skills * 100)

            st.subheader("Skills Identified")
            st.subheader("Resume Strength Score")
            st.metric("Skills Match Score", f"{resume_score}/100")
            st.progress(resume_score / 100)

            if found_skills:
                st.write(", ".join(found_skills))
            else:
                st.info("No matching skills found.")

            st.subheader("Recommended Job Roles")

            if any(s in found_skills for s in [
                "Python", "Pandas", "NumPy", "Data Analysis"
            ]):
                st.write("- Data Analyst")

            if any(s in found_skills for s in [
                "Python", "Machine Learning", "Scikit-learn"
            ]):
                st.write("- Machine Learning Intern")

            if any(s in found_skills for s in [
                "Python", "Streamlit", "SQL"
            ]):
                st.write("- Python Developer Intern")
                st.subheader("Job Match Analysis") 

            job_skills = {
                "Data Analyst": [
                    "Python", "SQL", "Pandas",
                    "NumPy", "Data Analysis", "Matplotlib"
                ],
                "Machine Learning Intern": [
                    "Python", "Machine Learning",
                    "Scikit-learn", "NumPy", "Pandas"
                ],
                "Python Developer Intern": [
                    "Python", "SQL", "Git", "Streamlit"
                ]
            }

            for role, required in job_skills.items():
                matched = [
                    skill for skill in required
                    if skill in found_skills
                ]
                missing = [
                    skill for skill in required
                    if skill not in found_skills
                ]
                score = round(len(matched) / len(required) * 100)

                st.write(f"**{role}: {score}% match**")
                st.progress(score / 100)

                st.write(
                    "Matched skills: " +
                    (", ".join(matched) if matched else "None")
                )
                st.write(
                    "Skills to learn: " +
                    (", ".join(missing) if missing else "None")
                )
                st.write("**Suggested learning roadmap:**")

                if missing:
                    for skill in missing:
                        st.write(f"📚 Learn and practise: {skill}")
                else:
                    st.write("You have all the listed skills for this role!")
                    
            report = f"""
AI RESUME ANALYZER - REPORT

Resume: {resume.name}
Resume Strength Score: {resume_score}/100

Skills Identified:
{', '.join(found_skills) if found_skills else 'No matching skills found'}

Thank you for using AI Resume Analyzer!
"""

            st.download_button(
                label="📥 Download Analysis Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )

                       
        else:
            st.warning(
                "No readable text found. "
                "The PDF may be scanned or empty."
            )

    except Exception as error:
        st.error(f"Could not read the resume: {error}")

        