# resume_parser_app.py

import streamlit as st
import PyPDF2
import re
import spacy

# Load NLP model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_email(text):
    email = re.findall(r"\S+@\S+", text)
    return email[0] if email else None

def extract_phone_number(text):
    phone = re.findall(r"\+?\d[\d\s]{8,15}", text)
    return phone[0] if phone else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text):
    skills_list = ['python', 'django', 'sql', 'html', 'css', 'flask', 'java', 'c++', 'javascript', 'git', 'aws', 'excel', 'nlp']
    found_skills = []
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
            found_skills.append(skill)
    return found_skills

# Sidebar Upload
st.sidebar.header("📤 Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload your Resume (PDF format only)", type=["pdf"])

# Title and Header
st.title("📄 Resume Parser & Analyzer")
st.markdown("Effortlessly extract useful info from your resume.")

# Main Logic
if uploaded_file is not None:
    st.success("Resume uploaded successfully ✅")
    text = extract_text_from_pdf(uploaded_file)

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone_number(text)
    skills = extract_skills(text)

    st.subheader("🔍 Extracted Information:")
    st.write("👤 **Name:**", name)
    st.write("📧 **Email:**", email)
    st.write("📞 **Phone:**", phone)
    st.write("🧠 **Skills:**", ", ".join(skills) if skills else "Not found")

    with st.expander("📃 Full Extracted Text"):
        st.text(text)

# Footer Section
st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <div style="text-align: center; color: gray; font-size: 0.9em;">
        Made with ❤️ by Bhupendra Singh<br>
        Connect on <a href="https://www.linkedin.com/in/bhupendra-singh-216154234/" target="_blank">LinkedIn</a> |
        <a href="https://github.com/BhupendraW" target="_blank">GitHub</a>
    </div>
""", unsafe_allow_html=True)
