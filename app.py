import streamlit as st
from groq import Groq

api_key = "YOUR_GROQ_API_KEY"

client = Groq(api_key=api_key)

st.set_page_config(page_title="AI Interview Practice Platform", page_icon="💼", layout="wide")

st.title("AI Interview Practice Platform")

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "question" not in st.session_state:
    st.session_state.question = ""

if "company" not in st.session_state:
    st.session_state.company = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "level" not in st.session_state:
    st.session_state.level = ""


st.sidebar.header("Interview Settings")

company = st.sidebar.selectbox(
    "Select Company",
    [
        "Select Company",
        "TCS",
        "Wipro",
        "Infosys",
        "Accenture",
        "Cognizant",
        "Capgemini",
        "HCL",
        "Google",
        "Microsoft",
        "Amazon",
        "Meta",
        "Startup",
        "Gen AI Startup"
    ]
)

role = st.sidebar.selectbox(
    "Select Role",
    [
        "Select Role",
        "Software Engineer",
        "Python Developer",
        "Web Developer",
        "Generative AI Engineer"
    ]
)

level = st.sidebar.selectbox(
    "Select Level",
    [
        "Select Level",
        "Fresher",
        "Intermediate",
        "Advanced"
    ]
)


def generate_question(company, role, level):

    if role == "Generative AI Engineer":

        if level == "Fresher":

            role_prompt = """
            Ask beginner-level Generative AI interview questions.

            Focus only on:
            - What is LLM
            - What is prompt engineering
            - What is token
            - What is Groq/OpenAI API
            - What is context window
            - What is hallucination
            - What is RAG basic concept

            Ask simple conceptual questions like real Gen AI fresher interviews.
            """

        elif level == "Intermediate":

            role_prompt = """
            Ask intermediate Generative AI interview questions.

            Focus on:
            - RAG architecture
            - Vector database
            - Embeddings
            - Prompt optimization
            - LLM APIs integration
            - Reducing hallucination
            """

        else:

            role_prompt = """
            Ask advanced Generative AI interview questions.

            Focus on:
            - Design Gen AI system architecture
            - Scaling LLM applications
            - Fine tuning vs RAG
            - Production deployment
            """


    else:

        if level == "Fresher":

            role_prompt = """
            Ask fresher interview questions like TCS, Wipro, Infosys.

            Focus on:
            - Programming basics
            - OOP concepts
            - SQL basics
            - Basic DSA
            """

        elif level == "Intermediate":

            role_prompt = """
            Ask intermediate questions.

            Focus on:
            - OOP
            - SQL joins
            - Medium DSA
            - Problem solving
            """

        else:

            role_prompt = """
            Ask advanced interview questions.

            Focus on:
            - System design
            - Optimization
            - Advanced DSA
            """


    prompt = f"""
    You are a real technical interviewer from {company}.

    Generate ONE realistic interview question.

    Role: {role}
    Level: {level}

    {role_prompt}

    Only return the question.
    Do not provide answer.
    """


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def show_answer(question):

    prompt = f"""
    Interview Question:
    {question}

    Provide clear professional answer suitable for interview.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def evaluate_answer(question, answer):

    prompt = f"""
    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate answer and provide:

    Score out of 10
    Feedback
    Correct Answer
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


if company != "Select Company" and role != "Select Role" and level != "Select Level":

    if st.button("Start Interview"):

        st.session_state.interview_started = True
        st.session_state.company = company
        st.session_state.role = role
        st.session_state.level = level

        st.session_state.question = generate_question(
            company,
            role,
            level
        )


if st.session_state.interview_started:

    st.divider()

    st.subheader(f"Company: {st.session_state.company}")
    st.subheader(f"Role: {st.session_state.role}")
    st.subheader(f"Level: {st.session_state.level}")

    st.markdown("### Interview Question")

    st.info(st.session_state.question)

    user_answer = st.text_area("Write your answer")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Submit Answer"):

            if user_answer:

                result = evaluate_answer(
                    st.session_state.question,
                    user_answer
                )

                st.success(result)

            else:
                st.warning("Please enter your answer")

    with col2:
        if st.button("Show Answer"):

            answer = show_answer(st.session_state.question)

            st.info(answer)

    with col3:
        if st.button("Next Question"):

            st.session_state.question = generate_question(
                st.session_state.company,
                st.session_state.role,
                st.session_state.level
            )

            st.rerun()





