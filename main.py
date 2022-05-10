import json

from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

with open(".secrets.json") as secret_file:
    secrets = json.load(secret_file)

endpoint = secrets["qa"]["endpoint"]
credential = AzureKeyCredential(secrets["qa"]["key"])
knowledge_base = secrets["qa"]["project-name"]
deployment = secrets["qa"]["deployment"]

def main():
    while True:
        question = input("Q: ")

        with QuestionAnsweringClient(endpoint, credential) as client:
            output = client.get_answers(
                question = question,
                project_name = knowledge_base,
                deployment_name = deployment
            )

        print(f"A: {output.answers[0].answer}")

if __name__ == '__main__':
    main()
