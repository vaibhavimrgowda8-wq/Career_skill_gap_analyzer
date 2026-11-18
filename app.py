import os
import json
import urllib.request
import urllib.error

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False


# -----------------------------------
# CAREERPATH AI - MAIN WEBSITE
# -----------------------------------

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>CareerPath AI | Discover Your Future</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f4f6ff;
            color: #222;
        }

        header {
            background: linear-gradient(135deg, #4338ca, #7c3aed);
            color: white;
            padding: 25px 8%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        header h1 {
            font-size: 27px;
        }

        header span {
            font-size: 14px;
        }

        .hero {
            text-align: center;
            padding: 65px 20px 35px;
        }

        .hero h2 {
            font-size: 38px;
            color: #312e81;
            margin-bottom: 15px;
        }

        .hero p {
            color: #666;
            font-size: 17px;
            line-height: 1.6;
        }

        .container {
            max-width: 750px;
            margin: 25px auto 60px;
            background: white;
            padding: 35px;
            border-radius: 16px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.08);
        }

        label {
            display: block;
            margin: 18px 0 8px;
            font-weight: bold;
            color: #333;
        }

        input, select, textarea {
            width: 100%;
            padding: 13px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 15px;
        }

        textarea {
            resize: vertical;
            min-height: 90px;
        }

        button {
            width: 100%;
            padding: 15px;
            margin-top: 25px;
            border: none;
            border-radius: 8px;
            background: #4f46e5;
            color: white;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #3730a3;
        }

        button:disabled {
            background: #999;
            cursor: not-allowed;
        }

        #result {
            display: none;
            margin-top: 30px;
            padding: 22px;
            background: #f0f0ff;
            border-radius: 10px;
            line-height: 1.8;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 20px;
            max-width: 1000px;
            margin: 20px auto 60px;
            padding: 0 20px;
        }

        .feature {
            background: white;
            padding: 25px;
            text-align: center;
            border-radius: 12px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.05);
        }

        .feature h3 {
            color: #4338ca;
            margin-bottom: 10px;
        }

        footer {
            text-align: center;
            padding: 25px;
            background: #312e81;
            color: white;
        }

        @media(max-width: 600px) {
            .hero h2 {
                font-size: 29px;
            }

            .container {
                margin: 20px;
                padding: 22px;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>🚀 CareerPath AI</h1>
    <span>Your Future Starts Here</span>
</header>

<section class="hero">
    <h2>Discover Your Perfect Career</h2>
    <p>
        Let AI understand your interests, skills and goals
        <br>
        and help you build your future.
    </p>
</section>

<div class="container">

    <h2>Career Assessment</h2>

    <form id="careerForm">

        <label>Your Name</label>
        <input type="text" id="name" placeholder="Enter your name" required>

        <label>Your Education Level</label>
        <select id="education" required>
            <option value="">Select education</option>
            <option>School Student</option>
            <option>High School Graduate</option>
            <option>Undergraduate</option>
            <option>Graduate</option>
            <option>Postgraduate</option>
            <option>Working Professional</option>
        </select>

        <label>Your Interests</label>
        <textarea id="interests"
            placeholder="Example: Technology, business, science, design..."
            required></textarea>

        <label>Your Skills</label>
        <textarea id="skills"
            placeholder="Example: Communication, programming, creativity..."
            required></textarea>

        <label>Your Career Goal</label>
        <select id="goal" required>
            <option value="">Select your goal</option>
            <option>Get a Job</option>
            <option>Start a Business</option>
            <option>Become an Entrepreneur</option>
            <option>Higher Education</option>
            <option>Improve My Skills</option>
            <option>Explore Career Options</option>
        </select>

        <button type="submit" id="submitBtn">
            Generate My Career Roadmap ✨
        </button>

    </form>

    <div id="result"></div>

</div>

<section class="features">

    <div class="feature">
        <h3>🎯 Career Discovery</h3>
        <p>Explore career opportunities based on your interests.</p>
    </div>

    <div class="feature">
        <h3>🧠 AI Guidance</h3>
        <p>Receive personalized career recommendations.</p>
    </div>

    <div class="feature">
        <h3>📚 Skill Development</h3>
        <p>Identify skills you need to achieve your goals.</p>
    </div>

    <div class="feature">
        <h3>🛣️ Career Roadmap</h3>
        <p>Get a step-by-step plan for your future.</p>
    </div>

</section>

<footer>
    <p>© 2026 CareerPath AI. All Rights Reserved.</p>
    <p>Empowering Your Future with Artificial Intelligence.</p>
</footer>

<script>

const form = document.getElementById("careerForm");

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const button = document.getElementById("submitBtn");
    const result = document.getElementById("result");

    const data = {
        name: document.getElementById("name").value,
        education: document.getElementById("education").value,
        interests: document.getElementById("interests").value,
        skills: document.getElementById("skills").value,
        goal: document.getElementById("goal").value
    };

    button.disabled = true;
    button.innerText = "Generating Your Career Roadmap...";

    result.style.display = "block";
    result.innerText = "Please wait. CareerPath AI is analyzing your profile...";

    try {

        const response = await fetch("/api/career-plan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const answer = await response.json();

        if (!response.ok) {
            throw new Error(answer.error || "Something went wrong.");
        }

        result.innerText = answer.result;

    } catch(error) {

        result.innerText = "Error: " + error.message;

    } finally {

        button.disabled = false;
        button.innerText = "Generate My Career Roadmap ✨";

    }

});

</script>

</body>
</html>
"""


# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route("/")
def home():
    return render_template_string(HTML)


# -----------------------------------
# AI CAREER RECOMMENDATION
# -----------------------------------

def generate_career_plan(data):

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return (
            "AI service is not configured yet. "
            "Please add your OPENAI_API_KEY in Render environment variables."
        )

    prompt = f"""
You are CareerPath AI, a professional career guidance assistant.

Analyze the following student profile:

Name: {data['name']}
Education: {data['education']}
Interests: {data['interests']}
Skills: {data['skills']}
Career Goal: {data['goal']}

Create a personalized career guidance report.

Include:

1. A short introduction.
2. Five suitable career options.
3. Why each career matches the student's profile.
4. Important skills to develop.
5. Recommended courses and certifications.
6. A practical 6-month learning roadmap.
7. Suggested beginner projects.
8. Job and internship preparation advice.
9. A motivational conclusion.

Use simple language, clear headings and practical advice.

Do not guarantee employment or make unsupported salary claims.
"""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert career counselor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    request_data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(req, timeout=60) as response:

            result = json.loads(response.read().decode("utf-8"))

            return result["choices"][0]["message"]["content"]

    except urllib.error.HTTPError as error:

        details = error.read().decode("utf-8", errors="replace")

        print("OpenAI API error:", details)

        raise RuntimeError(
            "AI service error. Check your API key and account configuration."
        )

    except Exception as error:

        print("AI error:", str(error))

        raise RuntimeError(
            "Unable to generate your career roadmap. Please try again."
        )


# -----------------------------------
# CAREER PLAN API
# -----------------------------------

@app.route("/api/career-plan", methods=["POST"])
def career_plan():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Invalid request data."
        }), 400

    required_fields = [
        "name",
        "education",
        "interests",
        "skills",
        "goal"
    ]

    for field in required_fields:

        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            return jsonify({
                "error": f"Please provide your {field}."
            }), 400

        if len(value) > 2000:
            return jsonify({
                "error": f"{field} is too long."
            }), 400

    try:

        result = generate_career_plan(data)

        return jsonify({
            "success": True,
            "result": result
        })

    except RuntimeError as error:

        return jsonify({
            "error": str(error)
        }), 502


# -----------------------------------
# HEALTH CHECK
# -----------------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "application": "CareerPath AI"
    })


# -----------------------------------
# ERROR HANDLING
# -----------------------------------

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Page not found."
    }), 404


# -----------------------------------
# RUN APPLICATION
# -----------------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
