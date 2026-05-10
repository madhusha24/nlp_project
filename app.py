from flask import Flask, render_template, request, jsonify
from google import genai
import json

# =========================================
# GEMINI CONFIG
# =========================================

API_KEY = "AIzaSyAb6jBllbJgsOYD7YoLT-bJ31lTTd2cZtw"

MODEL_NAME = "gemini-2.5-flash"

client = genai.Client(api_key=API_KEY)

# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

# =========================================
# GENERATE 10 QUESTIONS
# =========================================

def generate_questions(role, style):

    prompt = f"""
    You are an AI interviewer.

    Generate EXACTLY 10 interview questions.

    Role:
    {role}

    Interview Style:
    {style}

    Rules:
    - ask only interview questions
    - no numbering
    - concise
    - professional
    - realistic
    - varied difficulty

    Return ONLY valid JSON:

    {{
      "questions": [
        "question 1",
        "question 2",
        "question 3"
      ]
    }}
    """

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "")
            text = text.replace("```", "")

        data = json.loads(text)

        return data["questions"]

    except Exception as e:

        return [f"Error: {str(e)}"]

# =========================================
# EVALUATE ANSWER
# =========================================

def evaluate_answer(question, answer):

    prompt = f"""
    You are an advanced AI interview evaluator.

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Analyze the candidate based on:

    1. Technical Accuracy
    2. Communication Skills
    3. Confidence
    4. Fluency
    5. Professionalism

    STRICT RULES:

    - Feedback should be SHORT
    - Maximum half-page
    - Crisp and professional
    - No lengthy explanations
    - No teaching paragraphs
    - Keep feedback realistic

    OUTPUT FORMAT:

    Overall Score: X/10

    Technical Accuracy:
    short feedback

    Communication Skills:
    short feedback

    Confidence:
    short feedback

    Fluency:
    short feedback

    Professionalism:
    short feedback

    Final Suggestion:
    short improvement tip
    """

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template("index.html")

# =========================================
# START INTERVIEW
# =========================================

@app.route("/start", methods=["POST"])
def start():

    data = request.get_json()

    role = data["role"]

    style = data["style"]

    questions = generate_questions(
        role,
        style
    )

    return jsonify({
        "questions": questions
    })

# =========================================
# SUBMIT ANSWER
# =========================================

@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    question = data["question"]

    answer = data["answer"]

    feedback = evaluate_answer(
        question,
        answer
    )

    return jsonify({
        "feedback": feedback
    })

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )