from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('.env')

# GPT Client Wrapper
class GPTClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key is empty")
        self.client = OpenAI(api_key=api_key)
    
    def get_response(self, model, messages):
        """
        This function does smth
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error with OpenAI API: {str(e)}")

# Instantiate the GPT client globally
gpt_client = GPTClient(api_key=os.getenv('OPENAI_API_KEY'))

# Create the Flask Blueprint
gpt = Blueprint('gpt', __name__)

@gpt.route('/', methods=['POST'])
def chat():
    try:
        # Get the user's message from the request
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({'error': 'Message is empty'}), 400

        # Define the messages for GPT
        messages = [
            {"role": "system", "content": "You are working for SpotifyAI."},
            {"role": "user", "content": user_message}
        ]

        # Get GPT response using the client
        gpt_response = gpt_client.get_response(model='gpt-4o-mini', messages=messages)

        return jsonify({'response': gpt_response})

    except Exception as e:
        # Handle and return errors
        return jsonify({'error': str(e)}), 500