from openai import OpenAI

class GPTService:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key is empty")
        self.client = OpenAI(api_key=api_key)
    
    def get_response(self, model, messages):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error with OpenAI API: {str(e)}")