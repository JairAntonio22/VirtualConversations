
''' ===== Secrets ===== '''

import json
from azure.core.credentials import AzureKeyCredential

with open(".secrets.json") as secret_file:
    secrets = json.load(secret_file)

ENDPOINT = secrets["qa"]["endpoint"]
CREDENTIAL = AzureKeyCredential(secrets["qa"]["key"])
KNOWLEDGE_BASE = secrets["qa"]["project-name"]
DEPLOYMENT = secrets["qa"]["deployment"]


''' ===== Azure Language Service Connection ===== '''

from azure.ai.language.questionanswering import QuestionAnsweringClient

def get_answer(question):
    with QuestionAnsweringClient(ENDPOINT, CREDENTIAL) as client:
        output = client.get_answers(
            question = question,
            project_name = KNOWLEDGE_BASE,
            deployment_name = DEPLOYMENT
        )

    return output.answers[0].answer


''' ===== Web Server ===== '''

import os
from flask import (
    Flask, render_template, request, redirect
)

UPLOAD_FOLDER = 'test'
answer = secrets['init-video']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/text', methods=['POST'])
def text():
    global answer

    if 'question' in request.form:
        question = request.form['question']
        answer = get_answer(question)

    return redirect('/')



@app.route('/audio', methods=['POST'])
def audio():
    if 'audio' in request.files:
        audio = request.files['audio']

        if audio.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
            audio.save(filepath)

    return redirect('/')


@app.route('/')
def main():
    return render_template('index.jinja', video_src=answer)
