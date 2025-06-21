from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from utils.resume_parser import parse_resume
from pymongo import MongoClient
from backend.db_handler import save_to_db
from backend.extract_resume import extract_full_resume
from bson import ObjectId
import pdfkit
import datetime


flask_app = Flask(__name__)
flask_app.config['UPLOAD_FOLDER'] = 'uploads/'

client = MongoClient("mongodb://localhost:27017")
db = client["resume_app"]
collection = db["applications"]

@flask_app.route('/')
def index():
    return render_template('form.html', prefill={}, resume_filename="")

@flask_app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    jd_id = request.form.get("jd_id")  # ✅ get JD ID from the hidden input
    filename = secure_filename(file.filename)
    filepath = os.path.join(flask_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    parsed_data = parse_resume(filepath)
    
    return render_template(
        'form.html',
        prefill=parsed_data,
        resume_filename=filename,
        jd_id=jd_id  # ✅ pass it back into the form
    )


    parsed_data = parse_resume(filepath)
    return render_template('form.html',  prefill=parsed_data, resume_filename=filename, jd_id="")
@flask_app.route("/apply/<jd_id>", methods=["GET", "POST"])
def upload_for_jd(jd_id):
    if request.method == 'POST':
        file = request.files['resume']
        filename = secure_filename(file.filename)
        filepath = os.path.join(flask_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        parsed_data = parse_resume(filepath)

        final_data = {
            **parsed_data,
            "resume_filepath": filepath,
            "jd_id": jd_id,
            "submitted_at": datetime.datetime.utcnow()
        }

        doc_id = save_to_db(final_data)

        return jsonify({"message": "✅ Resume submitted", "doc_id": str(doc_id)})

    # ✅ FIXED: This ensures jd_id and empty prefill are passed even for GET
    return render_template("form.html", jd_id=jd_id, prefill={})

@flask_app.route("/submit", methods=["POST"])
def submit():
    # Get filename from hidden input
    filename = request.form.get("resume_filename")
    filepath = f"uploads/{filename}" if filename else None

    # Extract again if needed
    extracted_info = extract_full_resume(filepath) if filepath else {}
    jd_id = request.form.get("jd_id")
    print("📌 Received jd_id from form:", jd_id)


    # Get final form data
    final_data = {
        "personal_details": {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
        },
        "education": [{
            "degree": request.form.get("degree"),
            "college": request.form.get("college"),
            "graduation": request.form.get("graduation"),
            "cgpa": request.form.get("cgpa"),
        }],
        "experience": [{
            "job_title": request.form.get("experience[0][job_title]"),
            "current_company": request.form.get("experience[0][current_company]"),
            "employment_duration": request.form.get("experience[0][employment_duration]"),
            "job_responsibilities": request.form.get("experience[0][job_responsibilities]"),
        }],
        "skills": request.form.getlist("skills[]"),
        "projects": [],
        "links": {
            "linkedin": request.form.get("linkedin"),
            "website": request.form.get("website")
        },
        "jd_id" : jd_id,
        "submitted_at": datetime.datetime.utcnow()

    }

    # Projects: dynamically collect all project blocks
    i = 0
    while True:
        if f"projects[{i}][title]" not in request.form:
            break
        final_data["projects"].append({
            "title": request.form.get(f"projects[{i}][title]"),
            "tech_stack": request.form.get(f"projects[{i}][tech_stack]"),
            "description": request.form.get(f"projects[{i}][description]"),
            "duration": request.form.get(f"projects[{i}][duration]"),
        })
        i += 1
    # Save to MongoDB
    from backend.db_handler import save_to_db
    doc_id = save_to_db(final_data)

    return jsonify({"message": "✅ Application stored", "doc_id": str(doc_id)})

__all__ = ['flask_app'] 
if __name__ == "__main__":
    flask_app.run(debug=True)
