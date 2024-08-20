import os
import textwrap
import speech_recognition as sr
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QMessageBox
)
from IPython.display import display
from IPython.display import Markdown
import nltk
from rake_nltk import Rake
import random
import google.generativeai as genai

# Make sure to download nltk resources if you haven't already
nltk.download('punkt')
nltk.download('stopwords')

GENAI_API_KEY = 'AIzaSyAhd6hBehgK4QRMrnGgukT1VZKSoDqNETk'
genai.configure(api_key=GENAI_API_KEY)

def to_markdown(text):
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def extract_keywords(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    keyword_phrases = rake.get_ranked_phrases()
    return keyword_phrases[:5]

def transcribe_from_microphone(duration=10):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak for the next few seconds:")
        audio = r.listen(source, timeout=duration)

        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error from speech recognition service; {e}")
        return ""

def generate_notes_gui():
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle('Note Generation')

    layout = QVBoxLayout()

    transcription_label = QLabel('Transcription:')
    layout.addWidget(transcription_label)

    transcription_text = QTextEdit()
    layout.addWidget(transcription_text)

    def generate_notes_from_audio():
        transcription = transcribe_from_microphone()
        if transcription:
            transcription_text.setText(transcription)

    audio_button = QPushButton('Transcribe Audio')
    audio_button.clicked.connect(generate_notes_from_audio)
    layout.addWidget(audio_button)

    generate_button = QPushButton('Generate Notes')
    layout.addWidget(generate_button)

    def generate_notes():
        transcription = transcription_text.toPlainText()
        if transcription:
            keywords = extract_keywords(transcription)

            notes_prompt = f"Generate notes focusing on these keywords: {', '.join(keywords)}"
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(notes_prompt)

            notes_label.setText("Notes:")
            notes_text.setText(response.text)
            notes_text.show()

    generate_button.clicked.connect(generate_notes)

    notes_label = QLabel('')
    layout.addWidget(notes_label)

    notes_text = QTextEdit()
    notes_text.setReadOnly(True)
    layout.addWidget(notes_text)

    window.setLayout(layout)
    window.show()

    app.exec_()

def ask_question_gui(notes):
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle('Question Generation')

    layout = QVBoxLayout()

    question_label = QLabel('Question:')
    layout.addWidget(question_label)

    question_text = QTextEdit()
    layout.addWidget(question_text)

    def generate_question():
        question = question_text.toPlainText()
        if question:
            model = genai.GenerativeModel('gemini-pro')
            question_prompt = f"Generate an answer to the question: {question}"
            response = model.generate_content(question_prompt)

            answer_label.setText("Answer:")
            answer_text.setText(response.text)
            answer_text.show()

    generate_button = QPushButton('Generate Answer')
    generate_button.clicked.connect(generate_question)
    layout.addWidget(generate_button)

    answer_label = QLabel('')
    layout.addWidget(answer_label)

    answer_text = QTextEdit()
    answer_text.setReadOnly(True)
    layout.addWidget(answer_text)

    window.setLayout(layout)
    window.show()

    app.exec_()

def main():
    while True:
        generate_notes_gui()

        questions_feedback = input("Do you have any questions regarding the notes? (y/n): ")
        if questions_feedback.lower() == 'y':
            notes = input("Enter the notes: ")
            ask_question_gui(notes)

        feedback = input("Are you happy with the notes? (y/n): ")
        if feedback.lower() == 'n':
            generate_again = input("Do you want to generate notes again? (y/n): ")
            if generate_again.lower() != 'y':
                break
            continue

        question_option = input("Do you want a question related to the notes? (y/n): ")
        if question_option.lower() == 'y':
            notes = input("Enter the notes: ")
            ask_question_gui(notes)

        another_question = input("Do you want another question? (y/n): ")
        if another_question.lower() != 'y':
            break

if __name__ == "__main__":
    main()
