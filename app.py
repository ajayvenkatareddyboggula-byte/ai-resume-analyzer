import streamlit as st
from pdf_parser import extract_text_from_pdf
from analyzer import analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer")
st.write("Resume upload chey, AI nee resume ni analyze chesi improve cheyadaniki help chestundi.")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Resume upload cheyyi (PDF)", type=["pdf"])
with col2:
    job_description = st.text_area(
        "Job Description (optional)", height=200,
        placeholder="Target job description ikkada paste cheyyi..."
    )

if st.button("🔍 Analyze Resume", type="primary"):
    if uploaded_file is None:
        st.warning("Mundu resume PDF upload cheyyi.")
    else:
        with st.spinner("Analyze chestunnam... konchem wait cheyyi ⏳"):
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text:
                    st.error("PDF nundi text raaledu. Text-based PDF try cheyyi.")
                    st.stop()

                result = analyze_resume(resume_text, job_description)
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        st.divider()

        score = int(result["ats_score"])
        st.subheader("📊 ATS Score")
        st.metric("Score", f"{score}/100")
        st.progress(score / 100)

        st.info(result["summary"])

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("✅ Strengths")
            for s in result["strengths"]:
                st.write(f"- {s}")
        with c2:
            st.subheader("⚠️ Weaknesses")
            for w in result["weaknesses"]:
                st.write(f"- {w}")

        st.subheader("🔑 Missing Keywords")
        st.write(", ".join(result["missing_keywords"]) or "None")

        st.subheader("💡 Suggestions")
        for i, s in enumerate(result["suggestions"], 1):
            st.write(f"{i}. {s}")

        report = f"""AI RESUME ANALYSIS REPORT
ATS Score: {score}/100

Summary: {result['summary']}

Strengths:
{chr(10).join('- ' + s for s in result['strengths'])}

Weaknesses:
{chr(10).join('- ' + w for w in result['weaknesses'])}

Missing Keywords: {', '.join(result['missing_keywords'])}

Suggestions:
{chr(10).join('- ' + s for s in result['suggestions'])}
"""
        st.download_button("⬇️ Report Download", report, file_name="resume_report.txt")