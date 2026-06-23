from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():

    print("FILES =", request.files)
    print("FORM =", request.form)

    file = request.files.get('resume')
    print("File =", file)

    print(request.files)

    file = request.files.get('resume')
    print("File:", file)

    if file and file.filename != "":

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

    

        reader = PdfReader(filepath)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        # Original text
        original_text = text

        # Email Extraction
        email = "Not Found"

        email_match = re.search(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            original_text
        )

        if email_match:
            email = email_match.group()

        # Phone Extraction
        phone = "Not Found"

        phone_match = re.search(
            r"\+?\d[\d\s-]{8,}\d",
            original_text
        )

        if phone_match:
            phone = phone_match.group()

        # Name Extraction
        name = "Not Found"

        lines = original_text.split("\n")

    for line in lines[:10]:
        line = line.strip()

        if line.replace(" ", "").isalpha():
            name = line
            break


        text = text.lower()

        skills = [
            "python",
            "java",
            "html",
            "css",
            "javascript",
            "sql",
            "mysql",
            "flask"
        ]

        found_skills = []

        for skill in skills:
            if skill in text:
                found_skills.append(skill)

        job_skills = [
            "python",
            "html",
            "css",
            "javascript",
            "sql",
            "java",
            "mysql"
        ]

        matched = set(found_skills) & set(job_skills)

        score = (len(matched) / len(job_skills)) * 100

        missing_skills = list(
            set(job_skills) - set(found_skills)
        )

        return render_template(
            "result.html",
            score=score,
            skills=found_skills,
            missing=missing_skills,
            name=name,
            email=email,
            phone=phone
        )
    
    role = request.form["role"]

    if role == "web":
        job_skills = ["html", "css", "javascript", "react"]

    elif role == "python":
        job_skills = ["python", "flask", "sql"]

    else:
        job_skills = ["python", "machine learning", "ai"]
        
        
    if score >= 80:
        ats = "Excellent"

    elif score >= 60:
        ats = "Good"

    elif score >= 40:
        ats = "Average"

    else:
        ats = "Needs Improvement"



    return "No file selected"

if __name__ == '__main__':
    app.run(debug=True)