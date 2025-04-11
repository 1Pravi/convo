from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini AI API
API_KEY = "AIzaSyB335UzzSBBxHj94igOEAThkn_G_uFP9UY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start_conversation():
    start_prompt = "Start a friendly conversation about an interesting topic, like AI benefits."
    response = model.generate_content(start_prompt)
    ai_response = response.text.strip()
    
    conversation_history.append(("AI", ai_response))
    return jsonify({"ai_response": ai_response})

@app.route("/process", methods=["POST"])
def process_speech():
    data = request.get_json()
    user_input = data["user_input"]
    conversation_history.append(("User", user_input))

    # AI should provide short, informative answers before asking a question
    ai_prompt = f"""
    Act like a friendly conversation partner who helps improve spoken English.
    - If the user asks a question, **first give a short, clear answer**.
    - Then, **ask a related question** to keep the conversation going.
    - If the user doesn’t know something, **explain briefly in 1-2 sentences before asking a follow-up**.
    - Keep responses short and engaging.

    Example:
    - User: "What AI models are best for fine-tuning?"
    - AI: "GPT, BERT, and LLaMA are great for fine-tuning! Have you worked with any AI models before?"
    
    Here’s the conversation so far:
    {conversation_history}

    Respond in a **helpful, friendly, and concise way**.
    """

    response = model.generate_content(ai_prompt)
    ai_response = response.text.strip()

    conversation_history.append(("AI", ai_response))
    return jsonify({"ai_response": ai_response})



@app.route("/continue")
def continue_conversation():
    full_context = "\n".join([f"{speaker}: {message}" for speaker, message in conversation_history])
    continue_prompt = f"The user has paused. Continue the conversation naturally based on this history:\n\n{full_context}"
    
    response = model.generate_content(continue_prompt)
    ai_response = response.text.strip()
    
    conversation_history.append(("AI", ai_response))
    return jsonify({"ai_response": ai_response})

@app.route("/feedback")
def get_feedback():
    conversation_text = "\n".join([f"{speaker}: {message}" for speaker, message in conversation_history])
    feedback_prompt = f'''Analyze the following conversation and provide feedback on the user's communication skills:\n\n{conversation_text}
      Include ratings (out of 10) for the following areas:

    1. Clarity & Pace
    2. Pauses & Fillers
    3. Grammatical Accuracy
    4. Vocabulary Range
    5. Word Choice & Precision
    6. Fluency & Flow
    7. Coherence & Organization
    8. Ability to Express Ideas
    9. Communication Style
    10. Listening Skills
    11. Adaptability

    Then, summarize must be in the following format:
    - **Suggestions to improve:** (1 sentence only)
    - **Weakness:** (1 sentence only)
    - **Strength:** (1 sentence only)
    - **Tips and tricks:** (1 sentence only) '''
    
    response = model.generate_content(feedback_prompt)
    feedback = response.text.strip()

    return jsonify({"feedback": feedback})

if __name__ == "__main__":
    app.run(debug=True)
