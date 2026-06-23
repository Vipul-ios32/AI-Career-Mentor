import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def career_mentor(career, skills, missing_skills):

    prompt = f"""
You are an expert AI Career Mentor.

Candidate Career Recommendation:
{career}

Current Skills:
{skills}

Missing Skills:
{missing_skills}

Please provide:

1. Why this career is suitable.
2. A detailed 3-month learning roadmap.
3. Best online certifications.
4. 5 real-world projects to build.
5. Top interview questions with short answers.
6. Average salary in India for this career.
7. Tips to get placed in top companies.
8. Final motivation and career advice.

Keep the response professional, structured, and easy to understand.
"""

    response = model.generate_content(prompt)

    return response.text
