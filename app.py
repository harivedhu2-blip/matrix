from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# 🔥 Groq AI (API KEY from environment)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return "🚀 AI Backend Running Successfully"

@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    brand = data.get("brand", "").strip()
    content_type = data.get("contentType", "").strip()
    tone = data.get("tone", "").strip()
    audience = data.get("audience", "").strip()
    cta = data.get("cta", "").strip()
    custom_prompt = data.get("customPrompt", "").strip()
    topic = data.get("topic", "").strip()

    # 🔥 Defaults (if empty)
    if not tone:
        tone = "Friendly"
    if not content_type:
        content_type = "General Content"

    # 🔥 Build Prompt
    prompt = f"""
You are an expert AI marketing assistant.

Generate high-quality content.

### Inputs:
Brand: {brand if brand else "Not specified"}
Platform: {content_type}
Tone: {tone}
Audience: {audience if audience else "General audience"}
CTA: {cta if cta else "Not specified"}
Topic: {topic if topic else "General"}

Extra Instructions:
{custom_prompt if custom_prompt else "None"}

### Rules:
- Do NOT ask questions
- If something is missing, infer it
- Make it engaging and professional
- Always include CTA naturally

### Output:
Create complete ready-to-use content.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict AI marketing agent that always follows instructions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=600
        )

        result_text = response.choices[0].message.content

        return jsonify({
            "output": result_text
        })

    except Exception as e:
        return jsonify({
            "output": f"❌ Error: {str(e)}"
        }), 500


# 🔥 IMPORTANT: Render Fix
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
