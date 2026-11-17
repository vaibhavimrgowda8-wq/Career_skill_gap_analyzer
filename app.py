import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from modules.skill_analysis import analyze_skills

import os
app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

DATABASE = "users.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            education TEXT,
            course TEXT,
            skills TEXT,
            career TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()

    conn.close()


# ==========================================
# LOGIN PROTECTION
# ==========================================

def login_required():

    if "user_id" not in session:

        flash("Please login first.")

        return False

    return True


# ==========================================
# GET USER PROFILE
# ==========================================

def get_user_profile():

    conn = get_db()

    profile = conn.execute("""
        SELECT *
        FROM profile_details
        WHERE user_id = ?
    """, (session["user_id"],)).fetchone()

    conn.close()

    return profile


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        email = request.form.get("email", "").strip().lower()

        password = request.form.get("password", "")

        if not name or not email or not password:

            flash("Please fill in all fields.")

            return redirect(url_for("register"))

        if len(password) < 8:

            flash("Password must contain at least 8 characters.")

            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn = get_db()

        try:

            conn.execute("""
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            """, (name, email, hashed_password))

            conn.commit()

            flash("Registration successful! Please login.")

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            flash("Email already registered.")

        finally:

            conn.close()

    return render_template("register.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()

        password = request.form.get("password", "")

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session.clear()

            session["user_id"] = user["id"]

            session["name"] = user["name"]

            flash("Login successful!")

            return redirect(url_for("profile"))

        flash("Invalid email or password.")

    return render_template("login.html")


# ==========================================
# PROFILE
# ==========================================

@app.route("/profile")
def profile():

    if not login_required():

        return redirect(url_for("login"))

    profile_data = get_user_profile()

    return render_template(
        "profile.html",
        name=session["name"],
        details=profile_data
    )


# ==========================================
# CAREER DETAILS
# ==========================================

@app.route("/career-details", methods=["GET", "POST"])
def career_details():

    if not login_required():

        return redirect(url_for("login"))

    if request.method == "POST":

        education = request.form.get("education", "").strip()

        course = request.form.get("course", "").strip()

        skills = request.form.get("skills", "").strip()

        career = request.form.get("career", "").strip()

        if not all([education, course, skills, career]):

            flash("Please complete all career profile fields.")

            return redirect(url_for("career_details"))

        conn = get_db()

        existing = conn.execute("""
            SELECT id
            FROM profile_details
            WHERE user_id = ?
        """, (session["user_id"],)).fetchone()

        if existing:

            conn.execute("""
                UPDATE profile_details
                SET education = ?,
                    course = ?,
                    skills = ?,
                    career = ?
                WHERE user_id = ?
            """, (
                education,
                course,
                skills,
                career,
                session["user_id"]
            ))

        else:

            conn.execute("""
                INSERT INTO profile_details
                (user_id, education, course, skills, career)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                education,
                course,
                skills,
                career
            ))

        conn.commit()

        conn.close()

        flash("Career details saved successfully!")

        return redirect(url_for("profile"))

    profile_data = get_user_profile()

    return render_template(
        "career_details.html",
        details=profile_data
    )


# ==========================================
# CAREER RECOMMENDATIONS
# ==========================================

@app.route("/recommendations")
def recommendations():

    if not login_required():

        return redirect(url_for("login"))

    profile_data = get_user_profile()

    if not profile_data:

        flash("Please complete your career details first.")

        return redirect(url_for("career_details"))

    career = profile_data["career"]

    skills_text = profile_data["skills"] or ""

    student_skills = [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

    result = analyze_skills(career, student_skills)

    return render_template(
        "recommendations.html",
        name=session["name"],
        career=result["career"],
        skills=result["existing_skills"],
        required_skills=result["required_skills"],
        missing_skills=result["missing_skills"]
    )


# ==========================================
# MEMBER 2: SKILL GAP ANALYSIS
# ==========================================

@app.route("/skill-analysis", methods=["GET", "POST"])
def skill_analysis():

    if not login_required():

        return redirect(url_for("login"))

    profile_data = get_user_profile()

    if not profile_data:

        flash("Please complete your career details first.")

        return redirect(url_for("career_details"))

    if request.method == "POST":

        career = request.form.get(
            "career",
            profile_data["career"]
        ).strip()

        skills_text = request.form.get(
            "skills",
            profile_data["skills"] or ""
        )

    else:

        career = profile_data["career"]

        skills_text = profile_data["skills"] or ""

    student_skills = [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

    result = analyze_skills(
        career,
        student_skills
    )

    if not result["required_skills"]:

        flash("Please select a valid career.")

        return redirect(url_for("career_details"))

    return render_template(
        "results.html",
        name=session["name"],
        result=result
    )

# -----------------------------------
# MEMBER 3: ROADMAP
# -----------------------------------

@app.route("/roadmap")
def roadmap():

    if not login_required():
        return redirect(url_for("login"))

    profile_data = get_user_profile()

    if not profile_data:
        flash("Please complete your career details first.")
        return redirect(url_for("career_details"))

    career = profile_data["career"] or ""

    career_mapping = {
        "Web Developer": "frontend",
        "Software Developer": "python",
        "Data Scientist": "data",
        "Data Analyst": "data",
        "AI Engineer": "python",
        "Cybersecurity Analyst": "python",
        "Other": "python"
    }

    career_key = career_mapping.get(career, "python")

    saved_skills = profile_data["skills"] or ""

    return render_template(
        "roadmap.html",
        name=session["name"],
        career=career,
        career_key=career_key,
        saved_skills=saved_skills
    
    )

# -----------------------------------
# MEMBER 3: LEARNING RESOURCES
# -----------------------------------

@app.route("/resources")
def resources():

    if not login_required():
        return redirect(url_for("login"))

    return render_template(
        "resources.html",
        name=session["name"]
    )

# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.")

    return redirect(url_for("home"))


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)