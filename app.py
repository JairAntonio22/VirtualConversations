
''' ===== Secrets ===== '''

import json
from azure.core.credentials import AzureKeyCredential


with open('.secrets.json') as secret_file:
    secrets = json.load(secret_file)


# Language service
QA_ENDPOINT = secrets['qa']['endpoint']
QA_KEY = AzureKeyCredential(secrets['qa']['key'])
QA_PROJECT = secrets['qa']['project-name']
QA_DEPLOYMENT = secrets['qa']['deployment']

# Language service
STT_KEY = secrets['stt']['key']
STT_REGION = secrets['stt']['region']


''' ===== Azure Language Service Connection ===== '''

from azure.ai.language.questionanswering import QuestionAnsweringClient

def get_answer(question):
    with QuestionAnsweringClient(QA_ENDPOINT, QA_KEY) as client:
        output = client.get_answers(
            question = question,
            project_name = QA_PROJECT,
            deployment_name = QA_DEPLOYMENT
        )

    return output.answers[0].answer


''' ===== Azure Speech Service Connection ===== '''

from azure.cognitiveservices.speech import (
    SpeechConfig, audio, SpeechRecognizer, ResultReason, CancellationReason
)

def recognize(filename):
    speech_config = SpeechConfig(subscription = STT_KEY, region=STT_REGION)
    speech_config.speech_recognition_language = 'es-MX'
    audio_config = audio.AudioConfig(filename=filename)

    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = recognizer.recognize_once_async().get()

    if result.reason == ResultReason.RecognizedSpeech:
        print(f'Recognized: {result.text}')
        return result.text

    elif result.reason == ResultReason.NoMatch:
        print(f'No speech could be recognized: {result.no_match_details}')
        return ''

    elif result.reason == ResultReason.Canceled:
        details = result.details

        print(f'Speech Recognition canceled: {details.reason}')

        if details.reason == CancellationReason.Error:
            print(f'Error details: {details.error_details}')

        return ''


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
def handle_text():
    global answer

    if 'question' in request.form:
        question = request.form['question']
        answer = get_answer(question)

    return redirect('/')


@app.route('/audio', methods=['POST'])
def handle_audio():
    global answer
    if 'audio' in request.files:
        audio = request.files['audio']

        if audio.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
            audio.save(filepath)
            os.system('ffmpeg -y -i test/recording.ogg test/recording.wav')
            question = recognize('test/recording.wav')
            answer = get_answer(question)

    return redirect('/')


@app.route('/')
def main():
    return render_template('index.jinja', video_src=answer)
