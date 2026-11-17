// ==========================================
// CAREERPATH AI
// PERSONALIZED LEARNING ROADMAP
// ==========================================


// ------------------------------------------
// CAREER SKILLS
// ------------------------------------------

const careerSkills = {

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

};


// ------------------------------------------
// PAGE ELEMENTS
// ------------------------------------------

const careerSelect =
    document.getElementById("career-select");

const existingSkillsInput =
    document.getElementById("existing-skills");

const analyzeButton =
    document.getElementById("analyze-skills");

const skillGapResults =
    document.getElementById("skill-gap-results");

const recommendation =
    document.getElementById("career-recommendation");

const roadmapContainer =
    document.getElementById("personalized-roadmap");

const progressFill =
    document.getElementById("progress-fill");

const progressText =
    document.getElementById("progress-text");


// ------------------------------------------
// INITIALIZE
// ------------------------------------------

const pageConfig = document.body.dataset;

if (
    careerSelect &&
    pageConfig.career &&
    careerSkills[pageConfig.career]
) {
    careerSelect.value = pageConfig.career;
}

if (
    existingSkillsInput &&
    pageConfig.savedSkills !== undefined
) {
    existingSkillsInput.value = pageConfig.savedSkills;
}


// ------------------------------------------
// GET EXISTING SKILLS
// ------------------------------------------

function getExistingSkills() {

    if (!existingSkillsInput) {
        return [];
    }

    return existingSkillsInput.value
        .split(",")
        .map(skill => skill.trim().toLowerCase())
        .filter(skill => skill.length > 0);

}


// ------------------------------------------
// CREATE ROADMAP
// ------------------------------------------

function createRoadmap() {

    if (!careerSelect || !roadmapContainer) {
        return;
    }

    const selectedCareer = careerSelect.value;

    const skills = careerSkills[selectedCareer] || [];

    roadmapContainer.innerHTML = "";

    const storageKey =
        "careerpath_progress_" + selectedCareer;

    let completedSkills = [];

    try {

        completedSkills = JSON.parse(
            localStorage.getItem(storageKey) || "[]"
        );

        if (!Array.isArray(completedSkills)) {
            completedSkills = [];
        }

    } catch (error) {

        completedSkills = [];

    }


    skills.forEach((skill, index) => {

        const card = document.createElement("div");

        card.className = "skill-card";

        const checkbox = document.createElement("input");

        checkbox.type = "checkbox";

        checkbox.checked =
            completedSkills.includes(skill);

        checkbox.addEventListener("change", updateProgress);

        const title = document.createElement("h3");

        title.textContent = skill;

        const priority = document.createElement("p");

        priority.textContent =
            index < 2
                ? "Priority: High"
                : "Priority: Medium";

        const duration = document.createElement("p");

        duration.textContent =
            "Estimated duration: 2 weeks";

        const label = document.createElement("label");

        label.appendChild(checkbox);

        label.appendChild(
            document.createTextNode(" Completed")
        );

        card.appendChild(title);

        card.appendChild(priority);

        card.appendChild(duration);

        card.appendChild(label);

        roadmapContainer.appendChild(card);

    });

    updateProgress();

}


// ------------------------------------------
// UPDATE PROGRESS
// ------------------------------------------

function updateProgress() {

    if (!careerSelect || !roadmapContainer) {
        return;
    }

    const selectedCareer = careerSelect.value;

    const skills = careerSkills[selectedCareer] || [];

    const checkboxes =
        roadmapContainer.querySelectorAll(
            'input[type="checkbox"]'
        );

    const completedSkills = [];

    checkboxes.forEach((checkbox, index) => {

        if (checkbox.checked) {

            completedSkills.push(skills[index]);

        }

    });

    localStorage.setItem(
        "careerpath_progress_" + selectedCareer,
        JSON.stringify(completedSkills)
    );

    const total = skills.length;

    const completed = completedSkills.length;

    const percentage = total > 0
        ? Math.round((completed / total) * 100)
        : 0;

    if (progressFill) {

        progressFill.style.width =
            percentage + "%";

    }

    if (progressText) {

        progressText.textContent =
            percentage + "% Completed (" +
            completed + "/" + total + " skills)";

    }

}


// ------------------------------------------
// ANALYZE SKILLS
// ------------------------------------------

function analyzeSkills() {

    if (!careerSelect || !skillGapResults) {
        return;
    }

    const selectedCareer = careerSelect.value;

    const requiredSkills =
        careerSkills[selectedCareer] || [];

    const existingSkills = getExistingSkills();

    const matchedSkills = [];

    const missingSkills = [];

    requiredSkills.forEach(skill => {

        if (existingSkills.includes(skill.toLowerCase())) {

            matchedSkills.push(skill);

        } else {

            missingSkills.push(skill);

        }

    });

    const readiness = requiredSkills.length > 0
        ? Math.round(
            matchedSkills.length / requiredSkills.length * 100
        )
        : 0;


    // Display results.

    skillGapResults.innerHTML = "";

    const heading = document.createElement("h3");

    heading.textContent =
        "Career Readiness: " + readiness + "%";

    skillGapResults.appendChild(heading);


    const matchedHeading = document.createElement("h3");

    matchedHeading.textContent =
        "Existing / Matched Skills";

    skillGapResults.appendChild(matchedHeading);


    const matchedText = document.createElement("p");

    matchedText.textContent =
        matchedSkills.length
            ? matchedSkills.join(", ")
            : "No matching skills found.";

    skillGapResults.appendChild(matchedText);


    const missingHeading = document.createElement("h3");

    missingHeading.textContent =
        "Skills to Develop";

    skillGapResults.appendChild(missingHeading);


    const missingText = document.createElement("p");

    missingText.textContent =
        missingSkills.length
            ? missingSkills.join(", ")
            : "Congratulations! You have all the listed skills.";

    skillGapResults.appendChild(missingText);


    // Save missing skills for the resources page.

    localStorage.setItem(
        "missingSkills",
        JSON.stringify(missingSkills)
    );


    // Display career recommendation.

    if (recommendation) {

        recommendation.innerHTML = "";

        const recommendationHeading =
            document.createElement("h3");

        recommendationHeading.textContent =
            "Recommended Career: " + selectedCareer;

        recommendation.appendChild(
            recommendationHeading
        );

        const recommendationText =
            document.createElement("p");

        recommendationText.textContent =
            "Based on your selected career path and existing skills.";

        recommendation.appendChild(
            recommendationText
        );

    }


    createRoadmap();

}


// ------------------------------------------
// BUTTON EVENTS
// ------------------------------------------

if (analyzeButton) {

    analyzeButton.addEventListener(
        "click",
        analyzeSkills
    );

}


// ------------------------------------------
// CAREER CHANGE
// ------------------------------------------

if (careerSelect) {

    careerSelect.addEventListener("change", function () {

        createRoadmap();

        if (skillGapResults) {

            skillGapResults.innerHTML =
                "<p>Click Analyze My Skills to calculate your skill gap.</p>";

        }

        if (recommendation) {

            recommendation.innerHTML = "";

        }

    });

}


// ------------------------------------------
// LOAD ROADMAP
// ------------------------------------------

if (careerSelect && roadmapContainer) {

    createRoadmap();

}