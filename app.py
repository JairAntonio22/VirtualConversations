
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

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
answer = 'https://mostlamedia.blob.core.windows.net/media/media1.mp4'


@app.route('/', methods=['GET', 'POST'])
def main():
    global answer

    if request.method == 'POST':
        question = request.form['question']
        answer = get_answer(question)

        print(f'Q: {question}')
        print(f'A: {answer}')

        return redirect('/')
    else:
        return render_template('index.jinja', video_src=answer)
