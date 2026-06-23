import pdfplumber
import streamlit as st

from skill_extractor import extract_skills
from skill_gap import analyze_gap

try:
    from mentor import career_mentor
except Exception:  # pragma: no cover - keeps the app usable if Gemini setup fails
    career_mentor = None

try:
    from recommender import FEATURES, recommend_career
except Exception:  # pragma: no cover - keeps the app usable if model loading fails
    FEATURES = []
    recommend_career = None


CAREER_OPTIONS = [
    "AI Engineer",
    "Data Scientist",
    "Cloud Engineer",
    "Python Developer",
]


def extract_resume_text(uploaded_file):
    """Extract and normalize text from an uploaded PDF resume."""

    text_parts = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    return " ".join(" ".join(text_parts).split())


def normalize_skills(skills):
    return sorted({skill.strip().lower() for skill in skills if skill.strip()})


def render_css():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(76, 125, 255, 0.16), transparent 28%),
                radial-gradient(circle at top right, rgba(0, 200, 160, 0.14), transparent 24%),
                linear-gradient(180deg, #0f172a 0%, #111827 42%, #f8fafc 100%);
        }
        .hero {
            padding: 2rem 1.4rem 1.2rem 1.4rem;
            border-radius: 24px;
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.26);
            color: #f8fafc;
            margin-bottom: 1rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }
        .hero p {
            margin: 0.65rem 0 0 0;
            color: #cbd5e1;
            font-size: 1rem;
            line-height: 1.6;
        }
        .skill-pill {
            display: inline-block;
            background: linear-gradient(135deg, #0f172a, #334155);
            color: #f8fafc;
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
            margin: 0.2rem 0.25rem 0 0;
            font-size: 0.85rem;
        }
        .skill-pill-missing {
            display: inline-block;
            background: linear-gradient(135deg, #b91c1c, #ef4444);
            color: #fff;
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
            margin: 0.2rem 0.25rem 0 0;
            font-size: 0.85rem;
        }
        .hint-box {
            background: rgba(255, 255, 255, 0.8);
            border-left: 4px solid #2563eb;
            border-radius: 14px;
            padding: 0.9rem 1rem;
            color: #0f172a;
        }
        div.stButton > button {
            background-color: #16a34a;
            color: #ffffff;
            border: 1px solid #15803d;
            border-radius: 12px;
            padding: 0.6rem 1.1rem;
            font-weight: 700;
        }
        div.stButton > button:hover {
            background-color: #15803d;
            color: #ffffff;
            border: 1px solid #166534;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div class="hero">
            <h1>AI Career Mentor</h1>
            <p>Upload your resume, detect core skills, compare them with target roles, and see a recommended career fit in one clean dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown("### How it works")
        st.write("1. Upload a PDF resume")
        st.write("2. We extract resume text")
        st.write("3. Skills are detected automatically")
        st.write("4. Compare gaps for a chosen career")
        st.write("5. See a model-based recommendation")
        st.markdown("---")
        st.caption("Tip: a text-based PDF works best for extraction.")


def render_upload_section():
    return st.file_uploader("Upload Resume", type=["pdf"])


def render_candidate_profile():
    st.markdown("### Candidate Profile")

    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=0.0)
    internship = st.number_input("Internship Months", min_value=0, max_value=24, value=0)
    projects = st.number_input("Projects", min_value=0, max_value=30, value=0)
    research = st.number_input("Research Papers", min_value=0, max_value=20, value=0)

    st.markdown("#### Soft Skills")
    communication = st.slider("Communication", 0, 10, 0)
    leadership = st.slider("Leadership", 0, 10, 0)
    teamwork = st.slider("Teamwork", 0, 10, 0)
    problem = st.slider("Problem Solving", 0, 10, 0)

    st.markdown("#### Certifications")
    aws_cert = st.checkbox("AWS Certification")
    google_cert = st.checkbox("Google Certification")
    microsoft_cert = st.checkbox("Microsoft Certification")
    ibm_cert = st.checkbox("IBM Certification")
    cisco_cert = st.checkbox("Cisco Certification")

    return {
        "CGPA": cgpa,
        "Internship_Months": internship,
        "Projects": projects,
        "Research_Papers": research,
        "Communication": communication,
        "Leadership": leadership,
        "Teamwork": teamwork,
        "Problem_Solving": problem,
        "AWS_Cert": int(aws_cert),
        "Google_Cert": int(google_cert),
        "Microsoft_Cert": int(microsoft_cert),
        "IBM_Cert": int(ibm_cert),
        "Cisco_Cert": int(cisco_cert),
    }


def build_user_profile(skills, candidate_profile):
    """Create the feature dictionary expected by the recommender model."""

    user_data = {feature: 0 for feature in FEATURES}

    skill_feature_map = {
        "python": "Python",
        "java": "Java",
        "c++": "C++",
        "sql": "SQL",
        "machine learning": "Machine_Learning",
        "deep learning": "Deep_Learning",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "scikit-learn": "Scikit_Learn",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "aws": "AWS",
        "azure": "Azure",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "git": "Git",
        "github": "GitHub_Score",
        "linux": "Linux",
        "flask": "Flask",
        "django": "Django",
        "mongodb": "MongoDB",
        "mysql": "MySQL",
        "html": "Communication",
        "css": "Communication",
        "javascript": "Communication",
    }

    for skill in skills:
        feature = skill_feature_map.get(skill)
        if feature in user_data:
            user_data[feature] = 1

    user_data.update(candidate_profile)
    return user_data


def render_skills(skills):
    st.subheader("Detected Skills")
    if skills:
        st.markdown(
            "".join(f'<span class="skill-pill">{skill}</span>' for skill in skills),
            unsafe_allow_html=True,
        )
    else:
        st.info("No skills were detected from this resume.")


def render_missing_skills(missing):
    st.subheader("Missing Skills")
    if missing:
        st.markdown(
            "".join(f'<span class="skill-pill-missing">{skill}</span>' for skill in missing),
            unsafe_allow_html=True,
        )
    else:
        st.success("No missing skills found for this career path.")


def render_summary(skills, missing, predicted_career):
    st.markdown("### Summary")
    st.write(f"Skills found: **{len(skills)}**")
    st.write(f"Missing skills: **{len(missing)}**")
    if predicted_career:
        st.success(f"Model recommendation: {predicted_career}")
    else:
        st.info("Model recommendation is unavailable right now.")


def render_resume_text(resume_text):
    with st.expander("View extracted resume text", expanded=False):
        st.text(resume_text)


def render_mentor_response(career_choice, skills, missing):
    if career_mentor is None:
        return

    try:
        ai_response = career_mentor(career_choice, skills, missing)
    except Exception:
        st.info("AI mentor response is unavailable right now.")
        return

    st.subheader("🤖 AI Career Mentor")
    st.write(ai_response)


def main():
    st.set_page_config(
        page_title="AI Career Mentor",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    render_css()
    render_sidebar()
    render_header()

    uploaded_file = render_upload_section()
    if not uploaded_file:
        st.markdown(
            '<div class="hint-box">Upload a PDF resume to see detected skills, missing skills, and a career recommendation.</div>',
            unsafe_allow_html=True,
        )
        return

    resume_text = extract_resume_text(uploaded_file)
    if not resume_text:
        st.warning("No text could be extracted from this resume.")
        return

    skills = normalize_skills(extract_skills(resume_text))
    candidate_profile = render_candidate_profile()
    career_choice = st.selectbox("Choose Career Path", CAREER_OPTIONS)

    if st.button("Upload INFO", use_container_width=True):
        _, missing = analyze_gap(skills, career_choice)

        predicted_career = None
        if recommend_career is not None:
            user_data = build_user_profile(skills, candidate_profile)
            try:
                predicted_career = recommend_career(user_data)
            except Exception:
                predicted_career = None

        left, right = st.columns([1.3, 1])
        with left:
            render_skills(skills)
            render_missing_skills(missing)
        with right:
            render_summary(skills, missing, predicted_career)
            st.write(f"Selected path: **{career_choice}**")

        render_mentor_response(career_choice, skills, missing)
        render_resume_text(resume_text)
    else:
        st.info("Choose your profile details, then click Upload INFO to run the AI Career Mentor step.")


if __name__ == "__main__":
    main()
