import google.generativeai as genai
import os
import textwrap
import speech_recognition as sr
from IPython.display import display
from IPython.display import Markdown
import nltk
from rake_nltk import Rake
import random

nltk.download('punkt')
nltk.download('stopwords')

def to_markdown(text):
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def extract_keywords(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    keyword_phrases = rake.get_ranked_phrases()
    return keyword_phrases[:5]

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text

    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None

    except sr.RequestError as e:
        print("Sorry, an error occurred. Please try again later.")
        return None

def generate_notes():
    transcription = listen()
    if transcription:
        keywords = extract_keywords(transcription)

        print("Keywords:")
        print(*keywords, sep='\n')

        notes_prompt = f"Generate notes focusing on these keywords: {', '.join(keywords)}"
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(notes_prompt)

        print("Notes:")
        print(response.text)
        display(to_markdown(response.text))
    return transcription

def ask_question(input_method):
    if input_method == 'microphone':
        user_question = listen()
    else:
        user_question = input("Ask your question: ")

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_question)

    print("Answer:")
    print(response.text)

def generate_question(notes):
    model = genai.GenerativeModel('gemini-pro')
    question_prompt = f"Generate a question related to the notes: {notes}"
    response = model.generate_content(question_prompt)

    print("Question:")
    print(response.text)
    return response.text

def generate_answer(question):
    model = genai.GenerativeModel('gemini-pro')
    answer_prompt = f"Generate an answer to the question: {question}"
    response = model.generate_content(answer_prompt)

    print("Answer:")
    print(response.text)

def get_input_method():
    """Asks the user how they want to provide input"""
    while True:
        choice = input("How would you like to input your notes?\n(1) Microphone\n(2) Text\nChoice: ")
        if choice == '1' or choice.lower() == 'microphone':
            return 'microphone'
        elif choice == '2' or choice.lower() == 'text':
            return 'text'
        else:
            print("Invalid choice. Please select 1 or 2.")

def process_notes():
    notes = input("Enter your notes: ")
    model = genai.GenerativeModel('gemini-pro')

    summarize_prompt = f"write short notes on these notes:\n{notes}"
    response = model.generate_content(summarize_prompt)

    print("Summary:")
    display(response.text)

    return notes

def process_questions(transcript):
    questions_feedback = input("Do you have any questions regarding the notes? (y/n): ").lower()
    if questions_feedback == 'y':
        question_input_method = input(
            "How would you like to ask your question?\n(1) Microphone\n(2) Text\nChoice: ").lower()
        if question_input_method == '1' or question_input_method == 'microphone':
            ask_question('microphone')
        elif question_input_method == '2' or question_input_method == 'text':
            ask_question('text')
        else:
            print("Invalid choice. Please select 1 or 2.")

# Retrieve API Key from Environment Variable
GOOGLE_API_KEY = 'AIzaSyAhd6hBehgK4QRMrnGgukT1VZKSoDqNETk'
genai.configure(api_key=GOOGLE_API_KEY)

# Main loop
if __name__ == "__main__":
    input_method = get_input_method()
    while True:
        if input_method == 'microphone':
            transcript = generate_notes()
        elif input_method == 'text':
            transcript = process_notes()

        if not transcript:
            continue

        process_questions(transcript)

        feedback = input("Are you happy with the notes? (y/n): ").lower()
        if feedback != 'y':
            generate_again = input("Do you want to generate notes again? (y/n): ").lower()
            if generate_again != 'y':
                break
            else:
                continue

        question_option = input("Do you want a question related to the notes? (y/n): ").lower()
        if question_option != 'y':
            break

        generated_question = generate_question(transcript)

        answer_option = input("Do you want to see the answer to the question? (y/n): ").lower()
        if answer_option == 'y':
            generate_answer(generated_question)

        another_question = input("Do you want another question? (y/n): ").lower()
        if another_question != 'y':
            break


        generated_question = generate_question(transcript)

        answer_option = input("Do you want to see the answer to the question? (y/n): ").lower()
        if answer_option == 'y':
            generate_answer(generated_question)

        another_question = input("Do you want another question? (y/n): ").lower()
        if another_question != 'y':
            break
