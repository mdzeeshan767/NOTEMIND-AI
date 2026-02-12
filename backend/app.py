from flask import Flask, request, jsonify, render_template
import os
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "NoteMind AI Backend Running"

@app.route("/ui")
def ui():
    return render_template("index.html")

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    # clean formatting
    text = text.replace("\t", " ")
    text = " ".join(text.split())

    return text.strip()

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    extracted_text = extract_text_from_pdf(file_path)

    if extracted_text == "":
        return jsonify({
            "message": "File uploaded, but no readable text found."
        })

    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename,
        "extracted_text_preview": extracted_text[:800]
    })

if __name__ == "__main__":
    app.run(debug=True)
