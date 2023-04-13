from flask import Flask, request, jsonify
import openai
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    ai_response = generate_ai_response(user_message)

    return jsonify({'response': ai_response})

def generate_ai_response(user_message):
    openai.api_key = 'API HERE'
    prompt = f'User: {user_message}\nAI:'

    response = openai.Completion.create(
        model='davinci:ft-personal-2023-04-10-18-29-12',  
        prompt=prompt,
        max_tokens=40,
     
    )

    ai_response = response.choices[0].text.strip()

    return ai_response

if __name__ == '__main__':
    app.run(debug=True)
