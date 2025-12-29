import streamlit as st
import google.generativeai as genai
import json
import time
import re

# Page configuration
st.set_page_config(
    page_title="Interview Prep Pro",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = {}

# API Key Input
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("**Using AI API**")
api_key = st.sidebar.text_input(
    "Enter API Key",
    type="password",
    help="Get your free API key from https://aistudio.google.com/app/apikey"
)

if api_key:
    genai.configure(api_key=api_key)
    st.sidebar.success("✅ API Key Configured")
else:
    st.sidebar.warning("⚠️ Please add your API key")
    st.sidebar.markdown("""
    **How to get FREE API key:**
    1. Go to https://aistudio.google.com/app/apikey
    2. Sign in with Google
    3. Click 'Create API Key'
    4. Copy and paste here
    """)

st.title("🎯 Interview Prep Pro")
st.markdown("**Complete end-to-end interview preparation for college students**")


# Helper function to clean JSON
def clean_json_text(text):
    # Remove markdown code blocks (```json ... ```)
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```', '', text)
    return text.strip()


# Step 1: Input Details
st.header("Step 1: Enter Interview Details")

col1, col2, col3 = st.columns(3)

with col1:
    company_name = st.text_input("Company Name", placeholder="e.g., Google, Microsoft")

with col2:
    role = st.text_input("Position/Role", placeholder="e.g., SDE, Product Manager")

with col3:
    interview_type = st.selectbox(
        "Interview Round Type",
        ["Technical (Software)", "Technical (Hardware)", "HR", "Management"]
    )

# Generate Questions Button
if st.button("Generate Interview Questions", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar!")
    elif not company_name or not role:
        st.error("Please fill in Company Name and Role!")
    else:
        with st.spinner("Generating top 20 interview questions..."):
            try:
                # UPDATED MODEL HERE
                model = genai.GenerativeModel('gemini-2.5-flash')

                prompt = f"""Generate exactly 20 interview questions for:
Company: {company_name}
Role: {role}
Interview Type: {interview_type}

Return response in this EXACT format - a valid JSON array of strings only:
["Question 1", "Question 2", ... "Question 20"]

Do not include any intro text or markdown formatting. Just the raw JSON array."""

                response = model.generate_content(prompt)

                # Robust Parsing
                cleaned_text = clean_json_text(response.text)

                # Attempt to find array brackets if extra text still exists
                start_idx = cleaned_text.find('[')
                end_idx = cleaned_text.rfind(']') + 1

                if start_idx != -1 and end_idx > start_idx:
                    json_text = cleaned_text[start_idx:end_idx]
                    questions = json.loads(json_text)

                    if isinstance(questions, list) and len(questions) > 0:
                        st.session_state.questions = questions[:20]
                        st.session_state.current_question = 0
                        st.session_state.answers = {}
                        st.session_state.evaluations = {}
                        st.success(f"Generated {len(questions)} questions successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Received invalid data format.")
                else:
                    st.error("Could not parse JSON. The model might be overloaded.")
                    st.text(f"Raw Output: {response.text[:200]}...")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Step 2: Answer Questions
if st.session_state.questions:
    st.markdown("---")
    st.header("Step 2: Answer Questions")

    # Sidebar Progress
    completed = len(st.session_state.answers)
    total = len(st.session_state.questions)
    st.sidebar.progress(completed / total)
    st.sidebar.write(f"**Progress:** {completed}/{total} answered")

    # Question Navigator
    q_index = st.selectbox(
        "Navigate Questions:",
        range(total),
        format_func=lambda i: f"Q{i + 1}: {st.session_state.questions[i][:30]}..." + (
            " (✅)" if i in st.session_state.answers else ""),
        index=st.session_state.current_question
    )
    st.session_state.current_question = q_index

    current_q = st.session_state.questions[q_index]

    st.subheader(f"Question {q_index + 1}")
    st.info(current_q)

    # Answer Input
    # We use a key based on the question index so the text area updates when we switch questions
    user_answer = st.text_area(
        "Your Answer:",
        height=200,
        key=f"ans_{q_index}",
        value=st.session_state.answers.get(q_index, "")
    )

    col_act1, col_act2 = st.columns([1, 4])

    with col_act1:
        if st.button("Save Answer"):
            if user_answer.strip():
                st.session_state.answers[q_index] = user_answer
                st.toast("Answer Saved!", icon="💾")
            else:
                st.warning("Cannot save empty answer.")

    with col_act2:
        if st.button("Evaluate with AI"):
            if not st.session_state.answers.get(q_index):
                st.error("Please save an answer first!")
            else:
                with st.spinner("Analyzing your answer..."):
                    try:
                        # UPDATED MODEL HERE
                        model = genai.GenerativeModel('gemini-2.5-flash')

                        eval_prompt = f"""You are an expert interviewer. Evaluate this answer.
Question: {current_q}
Role: {role}
Candidate Answer: {st.session_state.answers[q_index]}

Return this EXACT JSON structure:
{{
    "score": 8,
    "feedback": "2-3 sentences of feedback.",
    "improvements": ["Point 1", "Point 2"],
    "ideal_answer": "A brief ideal answer example."
}}"""

                        response = model.generate_content(eval_prompt)
                        cleaned_text = clean_json_text(response.text)

                        start_idx = cleaned_text.find('{')
                        end_idx = cleaned_text.rfind('}') + 1

                        if start_idx != -1:
                            eval_data = json.loads(cleaned_text[start_idx:end_idx])
                            st.session_state.evaluations[q_index] = eval_data
                            st.rerun()
                        else:
                            st.error("Failed to parse evaluation.")

                    except Exception as e:
                        st.error(f"Error during evaluation: {e}")

    # Show Evaluation if available
    if q_index in st.session_state.evaluations:
        eval_data = st.session_state.evaluations[q_index]
        st.markdown("###AI Feedback")

        score = eval_data.get("score", 0)
        score_color = "green" if score >= 8 else "orange" if score >= 5 else "red"
        st.markdown(f"**Score:** :{score_color}[{score}/10]")

        st.write(f"**Feedback:** {eval_data.get('feedback')}")

        st.markdown("**Areas for Improvement:**")
        for item in eval_data.get("improvements", []):
            st.markdown(f"- {item}")

        with st.expander("View Ideal Answer"):
            st.info(eval_data.get("ideal_answer"))