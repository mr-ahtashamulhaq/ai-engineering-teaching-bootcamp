import streamlit as st
from groq import Groq
import json

# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(
    page_title="AI Writing Coach",
    layout="wide"
)

st.title("AI Writing Coach")

# ----------------------------
# Personas
# ----------------------------

PERSONAS = {
    "Academic": """You are an academic writing assistant. 
Rewrite the given text in a formal academic tone suitable for research papers or university assignments. 
Use precise vocabulary, passive voice where appropriate, and structured sentences. 
Avoid contractions, casual language, and first-person unless necessary. 
Cite reasoning clearly and maintain an objective, analytical stance.""",

    "Professional": """You are a professional business communication expert. 
Rewrite the given text for workplace settings - emails, reports, or internal communication. 
Be clear, concise, and respectful. Use active voice. 
Remove filler words and emotional language. 
The output should sound like it came from a senior professional who respects the reader's time.""",

    "Casual": """You are a friendly writing assistant. 
Rewrite the given text in a natural, relaxed tone - like texting a friend or writing an informal message. 
Use simple words, contractions, and a warm conversational flow. 
Keep it genuine, not performative. Avoid sounding like a corporate email.""",

    "LinkedIn": """You are a LinkedIn content strategist who writes posts that get real engagement. 
Rewrite the given text as a LinkedIn post with a strong hook that stops the scroll. 
Use short punchy paragraphs, one idea per line. 
Make it personal and specific - avoid generic motivational language. 
End with a question or observation that invites comments.
Add Proper multiple emojis as a supporting character."""
}

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.header("Settings")

api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="Paste your Groq API key here"
)

persona = st.sidebar.selectbox(
    "Choose Persona",
    list(PERSONAS.keys())
)

# ----------------------------
# Input
# ----------------------------

user_text = st.text_area(
    "Enter your text",
    height=200,
    placeholder="Paste your text here..."
)

# ----------------------------
# Helper: get client
# ----------------------------

def get_client():
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar.")
        return None
    return Groq(api_key=api_key)

# ----------------------------
# Improve Writing
# ----------------------------

if st.button("Improve Writing", use_container_width=True):

    if not user_text.strip():
        st.warning("Please enter some text first.")

    else:
        client = get_client()

        if client:
            try:
                with st.spinner("Improving writing..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": PERSONAS[persona]
                            },
                            {
                                "role": "user",
                                "content": user_text
                            }
                        ]
                    )

                improved_text = response.choices[0].message.content

                st.subheader("Improved Version")
                st.write(improved_text)

            except Exception as e:
                st.error(f"API error: {e}")
                if st.button("Retry"):
                    st.rerun()

# ----------------------------
# Writing Analysis
# ----------------------------

st.divider()
st.subheader("Writing Analysis")

if st.button("Analyze Writing", use_container_width=True):

    if not user_text.strip():
        st.warning("Please enter some text first.")

    else:
        client = get_client()

        if client:
            analysis_prompt = f"""
Analyze the following text.

Return ONLY valid JSON. No markdown, no explanation, nothing else.

{{
    "clarity": 0,
    "formality": 0,
    "readability": 0
}}

Scores are integers from 0 to 10.

Text:
{user_text}
"""
            try:
                with st.spinner("Analyzing writing..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "user",
                                "content": analysis_prompt
                            }
                        ]
                    )

                result = response.choices[0].message.content

                st.code(result, language="json")

                parsed = json.loads(result)

                col1, col2, col3 = st.columns(3)
                col1.metric("Clarity",     parsed["clarity"])
                col2.metric("Formality",   parsed["formality"])
                col3.metric("Readability", parsed["readability"])

            except json.JSONDecodeError:
                st.warning("The model returned something that isn't valid JSON. Try again.")

            except Exception as e:
                st.error(f"API error: {e}")
                if st.button("Retry"):
                    st.rerun()