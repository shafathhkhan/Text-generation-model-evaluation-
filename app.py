from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from rouge import Rouge  # Install via pip: pip install rouge

app = Flask(__name__)

# Configure Google Gemini AI (Replace with your API key)
genai.configure(api_key="AIzaSyDGo8lJnynssM6NmFr82dsbsKG6oUenbwc")
model = genai.GenerativeModel("gemini-pro")

# Function to calculate ROUGE Score
def calculate_rouge(reference, generated):
    rouge = Rouge()
    scores = rouge.get_scores(generated, reference)
    return scores[0]["rouge-l"]["f"]  # Using ROUGE-L F1 score

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_reference", methods=["POST"])
def generate_reference():
    data = request.json
    task = data.get("task")
    text = data.get("text")

    if not task or not text:
        return jsonify({"error": "Invalid input"}), 400

    if task == "summarization":
        prompt = f"Summarize the following text: {text}"
    elif task == "translation":
        source_lang = data.get("sourceLang")
        target_lang = data.get("targetLang")
        if not source_lang or not target_lang:
            return jsonify({"error": "Missing language inputs"}), 400
        prompt = f"Translate from {source_lang} to {target_lang}: {text}"
    elif task == "qa":
        prompt = f"Answer the following question: {text}"
    else:
        return jsonify({"error": "Invalid task"}), 400

    response = model.generate_content(prompt)
    reference_output = response.text

    return jsonify({"reference": reference_output})

@app.route("/evaluate_output", methods=["POST"])
def evaluate_output():
    data = request.json
    reference = data.get("reference")
    user_output = data.get("user_output")

    if not reference or not user_output:
        return jsonify({"error": "Invalid input"}), 400

    # Calculate ROUGE Score
    rouge_score = calculate_rouge(reference, user_output)

    return jsonify({"rouge_score": rouge_score})

if __name__ == "__main__":
    app.run(debug=True)
