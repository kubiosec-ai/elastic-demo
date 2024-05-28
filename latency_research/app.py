from flask import Flask, jsonify
from elasticapm.contrib.flask import ElasticAPM
import openai
import os

app = Flask(__name__)

app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'FlaskApp',
    'SECRET_TOKEN': '',
    'SERVER_URL': 'http://localhost:8200'
}

apm = ElasticAPM(app)

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    apm.capture_message('hello, world!')
    return "Hello World!"

@app.route('/quote2')
def quote2():
    try:
        response = openai.Completion.create(
            engine="davinci-002",
            prompt="Tell me a joke.",
            max_tokens=250,
            temperature=1
        )
        joke = response.choices[0].text.strip()
        return jsonify(joke=joke)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/quote35')
def quote35():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Tell me a joke."}
            ],
            max_tokens=250,
            temperature=1,
        )
        joke = response.choices[0].message['content'].strip()
        return jsonify(joke=joke)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/quote4')
def quote4():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Tell me a joke."}
            ],
            max_tokens=250,
            temperature=1
        )
        joke = response.choices[0].message['content'].strip()
        return jsonify(joke=joke)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/quote4o')
def quote4o():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Tell me a joke."}
            ],
            max_tokens=250,
            temperature=1
        )
        joke = response.choices[0].message['content'].strip()
        return jsonify(joke=joke)
    except Exception as e:
        return jsonify(error=str(e)), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
