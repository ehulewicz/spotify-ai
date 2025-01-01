from flask import Blueprint, request, jsonify
from services import GPTService
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Instantiate the GPT client globally
gpt_client = GPTService(api_key=os.getenv("OPENAI_API_KEY"))

# Create the Flask Blueprint
gpt = Blueprint("gpt", __name__)

@gpt.route("/", methods=["POST"])
def chat():
    try:
        # Get the user"s message from the request
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "Message is empty"}), 400

        # Define the messages for GPT
        messages = [
            {"role": "system", "content": "You are working for SpotifyAI."},
            {"role": "user", "content": user_message}
        ]

        # Get GPT response using the client
        gpt_response = gpt_client.get_response(model="gpt-4o-mini", messages=messages)

        return jsonify({"response": gpt_response})

    except Exception as e:
        # Handle and return errors
        return jsonify({"error": str(e)}), 500