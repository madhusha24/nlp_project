from flask import Flask, render_template, request, jsonify
from google import genai

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
# GENERATE QUESTION
# =========================================

def generate_question(role, style):

    prompt = f"""
    You are an AI interviewer.

    Generate ONE interview question for:

    Role:
    {role}

    Interview Style:
    {style}

    Rules:
    - ask only one question
    - professional tone
    - realistic interview question
    - concise
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
# EVALUATE ANSWER
# =========================================

def evaluate_answer(question, answer):

    prompt = f"""
    You are an advanced AI interview evaluator.

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Analyze the candidate on:

    1. Technical Accuracy
    2. Communication Clarity
    3. Confidence Level
    4. Professionalism
    5. Fluency
    6. Conciseness

    STRICTLY GIVE OUTPUT IN THIS FORMAT:

    Overall Score: X/10

    Technical Accuracy:
    short feedback

    Communication Clarity:
    short feedback

    Confidence Level:
    short feedback

    Professionalism:
    short feedback

    Fluency:
    short feedback

    Improvement Tip:
    short suggestion

    Rules:
    - concise feedback
    - professional tone
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
# ROUTES
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

    question = generate_question(role, style)

    return jsonify({
        "question": question
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