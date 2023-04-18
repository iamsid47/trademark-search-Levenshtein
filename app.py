from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    ai_response = generate_ai_response(user_message)

    return jsonify({'response': ai_response})

def generate_ai_response(user_message):
    openai.api_key = os.getenv('OPEN_AI_API')
    prompt = f'User: {user_message}\nAI:'

    response = openai.ChatCompletion.create(
        #model='davinci:ft-personal-2023-04-10-18-29-12',  
        model='gpt-4',  
        #messages=prompt,
        messages=[{"role": "user", "content": str(prompt)}],
        temperature=0.7     
    )

    ai_response = response.choices[0]['message']['content']

    return ai_response

if __name__ == '__main__':
    app.run(debug=True)
