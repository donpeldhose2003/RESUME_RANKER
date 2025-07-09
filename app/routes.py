from flask import Flask, render_template, request, send_file
import os
from .pdf_reader import extract_text_from_pdf
from .preprocessor import preprocess_text
from .scorer import rank_resumes
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "app/uploads"
PROCESSED_FOLDER = "app/processed"
REPORT_FOLDER = "app/reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app = Flask(__name__, static_url_path='/static')
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rank", methods=["POST"])
def rank():
    jd_text = request.form["jd"]
    uploaded_files = request.files.getlist("resumes")
    scores = []

    for file in uploaded_files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        raw_text = extract_text_from_pdf(filepath)
        cleaned_text = preprocess_text(raw_text)
        scores.append((filename, cleaned_text))

    jd_processed = preprocess_text(jd_text)
    ranked = rank_resumes(jd_processed, scores)

    # Save report
    df = pd.DataFrame(ranked, columns=["Resume", "Score"])
    report_path = os.path.join(REPORT_FOLDER, "ranked_resumes.csv")
    df.to_csv(report_path, index=False)

    return render_template("results.html", results=ranked, report_path=report_path)

@app.route("/download")
def download():
    from flask import send_from_directory
    import os

    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    return send_from_directory(report_dir, "ranked_resumes.csv", as_attachment=True)
