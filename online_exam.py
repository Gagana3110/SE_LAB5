"""Online exam marker: grades students against an answer key."""
import hashlib
import os
import secrets
import subprocess  # nosec B404

QUESTIONS = [
    {"q": "What is 2 + 2?", "answer": "4"},
    {"q": "Which keyword defines a function in Python?", "answer": "def"},
    {"q": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"q": "Which type is immutable: list or tuple?", "answer": "tuple"},
]

PROCTOR_PASSWORD = os.environ.get("PROCTOR_PASSWORD", "")

RESULTS = {}


def hash_answer(text):
    """Return a SHA-256 hash of the normalised answer text."""
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()


def pick_bonus_question():
    """Return the text of a randomly chosen question."""
    return secrets.choice(QUESTIONS)["q"]


def grade_student(student_name, responses, penalties=None):
    """Grade one student, record the score and return it."""
    if penalties is None:
        penalties = {}
    score = 0
    for i, item in enumerate(QUESTIONS):
        given = responses.get(i, "")
        if hash_answer(given) == hash_answer(item["answer"]):
            score += 1
        else:
            penalties[student_name] = penalties.get(student_name, 0) + 1
    RESULTS[student_name] = score
    return score


def get_grade(score):
    """Convert a score into a letter grade."""
    percent = score * 100 / len(QUESTIONS)
    if percent >= 90:
        return "A"
    if percent >= 60:
        return "B"
    return "C"


def class_average():
    """Return the average score of all students."""
    if not RESULTS:
        return 0
    return round(sum(RESULTS.values()) / len(RESULTS), 2)


def topper():
    """Return the name of the highest-scoring student."""
    return max(RESULTS, key=RESULTS.get)


def lock_screen(lab_pc):
    """Lock the screen of a lab PC over ssh (not called by the demo)."""
    subprocess.run(  # nosec B603 B607
        ["ssh", lab_pc, "lock-screen"], check=True)


def main():
    """Run a short demonstration."""
    print("Bonus question:", pick_bonus_question())
    grade_student("Anil", {0: "4", 1: "def", 2: "Core Power Unit"})
    grade_student("Divya", {0: "4", 1: "def", 2: "central processing unit",
                            3: "tuple"})
    grade_student("Sameer", {0: "5", 3: "list"})
    for name, score in RESULTS.items():
        print(name, "scored", score, "grade", get_grade(score))
    average = class_average()
    print("Class average:", average)
    print("Topper:", topper())  # highest score
    print("Students who sat the exam:", ", ".join(sorted(RESULTS)),
          "| total:", len(RESULTS))


if __name__ == "__main__":
    main()
