# Resume Ranking System – Phase 1 (Part 1)
This is the first part of a smart resume ranking and justification system built using Python, Flask, and MongoDB. It allows candidates to upload resumes, auto-extracts their details using custom NLP extractors, enables manual corrections, and stores the final structured data in a database for further processing and ranking.

This project is the **first part** of a larger AI-based resume screening system. It focuses on:
- Uploading resumes (PDFs),
- Extracting useful data using NLP,
- Allowing human edits via a web form,
- Storing both raw and cleaned data into MongoDB,
- And exporting structured results to a CSV file.

This marks the successful completion of the **first part of Phase 1**, which lays the foundation for advanced resume ranking in the next phases.

---

##  Core Features

###  1. Resume Upload
- Users can upload resume PDFs directly through a web form.
- Uploaded files are stored in the `/uploads` folder.

###  2. Automated Information Extraction
- Extracts data using **PyMuPDF (`fitz`)** and custom Python extractor functions.
- Fields extracted:
  - Name
  - Email
  - Phone
  - Education (Degree, College, CGPA, Year)
  - Skills
  - Experience
  - Project Info
  - Portfolio Links (LinkedIn, Website, etc.)

###  3. Pre-Filled & Editable Form
- The extracted data pre-fills a user-friendly form.
- User can edit any field or add/remove experiences or projects.
- Tag-based skill input system with Enter key detection.

###  4. Dual Data Storage
- **Cleaned form data** + **raw extracted info** are stored in **MongoDB** (`resume_ranking_db > form_extractions`).
- Includes a `submitted_at` timestamp for tracking.

### 📤 5. Safe CSV Export
- All submissions can be exported to `submissions.csv`.
- The script ensures **duplicate submissions are not exported** again.
- Uses MongoDB document `_id` tracking for uniqueness.

---

## 🗂️ Folder Structure

```
Resume_pro/
├── app.py                  # Main Flask application
├── export_to_csv.py        # Script to export data to CSV
├── uploads/                # Uploaded resumes are saved here
├── templates/
│   └── form.html           # Editable HTML form
├── backend/
│   ├── extract_resume.py   # Gathers all field extractors
│   └── db_handler.py       # MongoDB insert logic
├── utils/
│   └── extractors/
│       ├── personal.py     # Extract personal details
│       ├── education.py    # Extract education details
│       ├── experience.py   # Extract experience
│       ├── skills.py       # Extract skills
│       ├── links.py        # Extract links
│       ├── work.py         # Extract job/portfolio files
│       └── projects.py     # Extract project details
```


---

##  Tech Stack

- **Backend**: Python, Flask
- **Data Extraction**: PyMuPDF, Custom NLP Parsers
- **Database**: MongoDB (via PyMongo)
- **Frontend**: HTML, JavaScript (for dynamic form handling)
- **Data Export**: Pandas

---
