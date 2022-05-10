
''' ===== Secrets ===== '''

import json
from azure.core.credentials import AzureKeyCredential

with open(".secrets.json") as secret_file:
    secrets = json.load(secret_file)

ENDPOINT = secrets["qa"]["endpoint"]
CREDENTIAL = AzureKeyCredential(secrets["qa"]["key"])
KNOWLEDGE_BASE = secrets["qa"]["project-name"]
DEPLOYMENT = secrets["qa"]["deployment"]



''' ===== Azure Language Server ===== '''

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

from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return '<p> Hello, World! </p>'
