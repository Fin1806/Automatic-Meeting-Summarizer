from flask import Flask, render_template, request, jsonify
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import torch
import re

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_PATH = "pegasus_mixed_finetuned"

print("Loading model...")

tokenizer = PegasusTokenizer.from_pretrained(MODEL_PATH)

model = PegasusForConditionalGeneration.from_pretrained(
    MODEL_PATH
).to(device)

model.eval()

print("Model loaded.")


def clean_transcript(text):
    """Remove extra whitespace from transcript"""
    text = str(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def summarize_pegasus(text, tokenizer, model, device="cuda"):
    """
    Generate summary using Pegasus
    """

    # Clean transcript
    text = clean_transcript(text)

    # Tokenize
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    ).to(device)

    generate_kwargs = {
        "max_length": 256,
        "min_length": 50,

        "num_beams": 8,

        "length_penalty": 1.5,
        "repetition_penalty": 1.5,
        "no_repeat_ngram_size": 3,

        "early_stopping": True,
        "do_sample": True,

        "temperature": 0.7,
        "top_p": 0.9,
    }
    
    # Generate summary
    with torch.no_grad():
        summary_ids = model.generate(
            **inputs,
            **generate_kwargs
        )

    # Decode
    summary_text = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return summary_text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():

    transcript = request.json["text"]

    summary = summarize_pegasus(
        transcript,
        tokenizer,
        model,
        device
    )

    return jsonify({
        "summary": summary
    })

# for hosting
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=7860)

# local host
if __name__ == "__main__":
    app.run(debug=True)