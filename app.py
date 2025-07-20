import streamlit as st
import difflib
import time
import random
import pandas as pd
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# ------------------- Page Config ------------------- #
st.set_page_config(page_title="Typing Master for Programmers", layout="wide")
st.title("👨‍💻 Typing Master for Programmers")
st.markdown("Enhance your typing speed and coding accuracy in real programming languages.")

# ------------------- Language Snippet Bank ------------------- #
LANGUAGES = {
    "Python": [
        "def greet(name):\n    return f\"Hello, {name}!\"",
        "for i in range(5):\n    print(i)",
        "class Person:\n    def __init__(self, name):\n        self.name = name",
        "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)"
    ],
    "JavaScript": [
        "function greet(name) {\n    return `Hello, ${name}`;\n}",
        "for (let i = 0; i < 5; i++) {\n    console.log(i);\n}",
        "class Person {\n    constructor(name) {\n        this.name = name;\n    }\n}"
    ],
    "C++": [
        "#include<iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello\";\n    return 0;\n}",
        "for (int i = 0; i < 10; i++) {\n    cout << i << endl;\n}"
    ]
}

# ------------------- Helper Functions ------------------- #
def format_code(code, language):
    lexer = get_lexer_by_name(language.lower(), stripall=True)
    formatter = HtmlFormatter(style="colorful", full=False, cssclass="codehilite")
    return f"<style>{formatter.get_style_defs()}</style>" + highlight(code, lexer, formatter)

def calculate_metrics(target, typed, duration):
    matcher = difflib.SequenceMatcher(None, target, typed)
    accuracy = round(matcher.ratio() * 100, 2)
    wpm = round((len(typed) / 5) / (duration / 60), 2)
    return accuracy, wpm

# ------------------- Sidebar ------------------- #
st.sidebar.header("⚙️ Configuration")
language = st.sidebar.selectbox("Choose Programming Language", list(LANGUAGES.keys()))
snippet = random.choice(LANGUAGES[language])
time_limit = st.sidebar.slider("Time Limit (seconds)", 30, 180, 60)
show_report = st.sidebar.checkbox("Show Detailed Report", value=True)

# ------------------- Display Code ------------------- #
with st.expander("📜 Code Snippet to Type", expanded=True):
    st.markdown(format_code(snippet, language), unsafe_allow_html=True)

# ------------------- Typing Area ------------------- #
typed_code = st.text_area("✍️ Type the above code here:", height=200)

# ------------------- Submit Button ------------------- #
if st.button("✅ Submit"):
    st.session_state.start_time = time.time()  # Simulate start time (in real app, capture on first keystroke)
    duration = random.randint(5, time_limit)   # Simulated time, replace with actual tracking for realism

    accuracy, wpm = calculate_metrics(snippet, typed_code, duration)
    
    st.success("✅ Typing Completed!")
    st.metric("⏱ Time Taken (approx)", f"{duration} sec")
    st.metric("🎯 Accuracy", f"{accuracy}%")
    st.metric("⌨️ WPM (Words Per Minute)", f"{wpm}")

    if show_report:
        st.subheader("📊 Comparison Report")
        diff = difflib.ndiff(snippet.splitlines(), typed_code.splitlines())
        st.code("\n".join(diff), language="diff")
