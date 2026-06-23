import warnings

import spacy
from spacy.matcher import PhraseMatcher


def _load_nlp():
    """Load a spaCy pipeline, falling back to a blank English pipeline.

    The app only needs tokenization for phrase matching, so we do not want
    startup to fail when the larger `en_core_web_sm` model is unavailable.
    """

    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        warnings.warn(
            "spaCy model 'en_core_web_sm' is not installed; using a blank English pipeline.",
            RuntimeWarning,
        )
        return spacy.blank("en")


nlp = _load_nlp()
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")


skills_db = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "git",
    "github",
    "linux",
    "dsa",
    "data structures",
    "algorithms",
    "flask",
    "django",
    "streamlit",
    "html",
    "css",
    "javascript"
] 
# Convert skills into spaCy patterns
patterns = [nlp.make_doc(skill) for skill in skills_db]

# Add patterns to matcher
matcher.add("SKILLS", patterns)

# Function to extract skills
def extract_skills(text):

    doc = nlp(text.lower())

    matches = matcher(doc)

    skills = []

    for match_id, start, end in matches:
        skills.append(doc[start:end].text)

    return list(set(skills))
