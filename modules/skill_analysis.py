# ==========================================
# CAREERPATH AI
# SKILL GAP ANALYSIS MODULE
# ==========================================

CAREER_SKILLS = {

    "Software Developer": [
        "Python",
        "Java",
        "Data Structures",
        "SQL",
        "Git"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Python",
        "React"
    ],

    "Data Scientist": [
        "Python",
        "Statistics",
        "Machine Learning",
        "SQL",
        "Data Visualization"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Statistics",
        "Power BI"
    ],

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Mathematics",
        "TensorFlow"
    ],

    "Cybersecurity Analyst": [
        "Networking",
        "Linux",
        "Python",
        "Cybersecurity Basics",
        "Cryptography"
    ]

}


def analyze_skills(career, student_skills):

    required_skills = CAREER_SKILLS.get(career, [])

    # Normalize existing skills.
    student_skills = [
        skill.strip()
        for skill in student_skills
        if skill and skill.strip()
    ]

    student_skill_names = {
        skill.casefold()
        for skill in student_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.casefold() in student_skill_names:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    # Calculate career readiness.
    readiness = (
        round(
            len(matched_skills) / len(required_skills) * 100
        )
        if required_skills else 0
    )

    return {

        "career": career,

        "existing_skills": student_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "readiness": readiness

    }