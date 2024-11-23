import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Set OpenAI API key
openai.api_key = 'sk-k4NWKoUeq86m6MlUqAFgFhFvx_Nz8zoUCpu2un7eA5T3BlbkFJkkFSNroV1SJ_tD7gUaCJYHgtKBwB1eVw2nGJuaEHkA'  # Replace with your actual OpenAI API key

# Function to generate career recommendations
def generate_career_recommendation(o_level_results, post_secondary_pathway, qualification, qualification_grades, 
                                   a_level_results, skills, career_goals, interests, country, max_tokens=1000):
    if not o_level_results or not post_secondary_pathway or not skills or not career_goals:
        return "❌ Please provide complete information: O-Level results, post-secondary pathway, qualification, skills, and career goals."

    if post_secondary_pathway == "Junior College (JC)" and not a_level_results:
        return "❌ Please provide your A-Level results for the Junior College pathway."

    prompt = (f"Based on the following academic results, skills, and interests, suggest suitable career paths, "
              f"relevant universities or institutions, and required certifications for a student:\n"
              f"O-Level Results: {o_level_results}\n")

    if post_secondary_pathway == "Junior College (JC)":
        prompt += f"A-Level Results: {a_level_results}\n"
    else:
        prompt += f"Qualification: {qualification} (Grades: {qualification_grades})\n"

    prompt += (f"Post-Secondary Pathway: {post_secondary_pathway}\n"
               f"Skills: {skills}\n"
               f"Career Goals: {career_goals}\n"
               f"Interests: {interests}\n"
               f"Preferred Country: {country}\n"
               f"Include relevant details such as industries, potential job roles, and certifications.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a career counselor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()

    except openai.OpenAIError as e:
        return f"⚠️ An OpenAI error occurred: {e}"
    except Exception as e:
        return f"⚠️ An error occurred: {e}"

# Function to add emojis to the recommendation
def add_emojis_to_recommendation(recommendation):
    emojis = {
        "university": "🏛️ University",
        "certification": "📜 Certification",
        "industry": "🏢 Industry",
        "job roles": "💼 Job Roles",
        "career path": "🚀 Career Path",
        "skills": "🛠️ Skills",
        "experience": "📅 Experience",
        "internship": "💼 Internship",
        "degree": "🎓 Degree",
        "project": "📁 Project",
        "learning": "📘 Learning",
        "salary": "💰 Salary",
        "technology": "💻 Technology",
        "interview": "🤝 Interview",
        "qualification": "🎓 Qualification",
        "opportunities": "🚪 Opportunities",
    }
    for word, emoji in emojis.items():
        recommendation = recommendation.replace(word, emoji)
    return recommendation

# Function to generate helpful resources
def get_helpful_resources(career_goals):
    prompt = (f"Please suggest relevant and helpful online resources, such as online courses, articles, "
              f"certifications, and platforms, for someone looking to pursue a career in {career_goals}. "
              f"Include up-to-date websites with direct links, platforms, and certifications that can help them advance in this career.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in education and career guidance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        resources = response.choices[0].message['content'].strip().split("\n")
        return resources
    except openai.OpenAIError as e:
        return [f"⚠️ An OpenAI error occurred: {e}"]
    except Exception as e:
        return [f"⚠️ An error occurred: {e}"]

# Load custom CSS
def local_css():
    st.markdown(
        """
        <style>
        body { background-color: #e0f7e9; color: #333; }
        .header { color: #28a745; font-size: 48px; text-align: center; font-family: 'Arial', sans-serif; }
        .subheader { color: #28a745; font-size: 24px; margin: 20px 0; }
        .recommendation-box, .resources-box {
            background-color: #f9fdfc; color: #333; padding: 20px; border-radius: 10px;
            border-left: 5px solid #28a745; font-family: 'Trebuchet MS', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

# App title
st.markdown('<div class="header">🎓 Career PathFinder</div>', unsafe_allow_html=True)

# User inputs
o_level_results = st.text_input("**O-Level Results** (e.g., Math: A1, English: A2, Science: B3)")
post_secondary_pathway = st.selectbox(
    "Post-Secondary Education Pathway", 
    ("Junior College (JC)", "Polytechnic", "Institute of Technical Education (ITE)")
)

a_level_results = None
qualification = None
qualification_grades = None

if post_secondary_pathway == "Junior College (JC)":
    a_level_results = st.text_input("**A-Level Results** (e.g., Math: A, Physics: A, Chemistry: B)")
else:
    qualification = st.text_input("**Qualification** (e.g., Diploma in Engineering)")
    qualification_grades = st.text_input("**Qualification Grades** (e.g., GPA 3.5/4)")

skills = st.text_input("**Skills** (e.g., Programming, Communication, Design)")
career_goals = st.text_input("**Career Goals** (e.g., Software Engineer, Entrepreneur)")
interests = st.text_input("**Interests** (e.g., Technology, Business, Arts)")
country = st.text_input("**Preferred Country** (e.g., Singapore, USA, UK)")

# Generate recommendations
if st.button("Generate Career Recommendation"):
    recommendation = generate_career_recommendation(
        o_level_results, post_secondary_pathway, qualification, qualification_grades,
        a_level_results, skills, career_goals, interests, country
    )
    recommendation_with_emojis = add_emojis_to_recommendation(recommendation)
    st.markdown(f'<div class="recommendation-box">{recommendation_with_emojis}</div>', unsafe_allow_html=True)

    # Show helpful resources
    st.markdown('<div class="subheader">Helpful Resources</div>', unsafe_allow_html=True)
    helpful_resources = get_helpful_resources(career_goals)
    for resource in helpful_resources:
        st.markdown(f"- {resource}")
