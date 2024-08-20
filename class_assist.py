import speech_recognition as sr
import wikipedia
import datetime

def listen_and_identify_keywords():
    """Listens to audio input and identifies computer science keywords."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, timeout=10)  # Set a timeout for listening

    try:
        recognized_results = r.recognize_google(audio, show_all=True)
        text = recognized_results['alternative'][0]['transcript']
        print("You said: " + text)
        return text.lower()

    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Error fetching results from Google Speech Recognition service; {0}".format(e))
        return ""

def create_notes(keywords):
    """Creates notes based on identified computer science keywords."""
    if not keywords:
        print("No computer science keywords found in your speech.")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notes = f"**Learning with NLP Notes** ({timestamp})\n"

    all_keywords = ["algorithm", "data structure", "artificial intelligence",
                    "programming languages", "machine learning", "data mining",
                    "big data", "cloud computing", "cybersecurity", "internet of things",
                    "software engineering", "computer vision", "natural language processing",
                    "robotics", "virtual reality", "augmented reality", "blockchain", "cryptography"]

    # Check if the input method is audio
    if len(keywords.split()) == 1:
        # Treat the entire recognized text as a single keyword
        keyword = keywords.strip()
        if keyword in all_keywords:
            try:
                summary = wikipedia.summary(keyword, sentences=2)
                notes += f"- **{keyword.capitalize()}**: {summary}\n"
            except wikipedia.exceptions.PageError:
                print(f"Wikipedia summary unavailable for: {keyword}")
                notes += f"- **{keyword.capitalize()}**: (Wikipedia summary unavailable)\n"
        else:
            print(f"Keyword '{keyword}' not found in the list of computer science keywords.")
    else:
        # Split the recognized text into words
        for keyword in keywords.split():
            if keyword in all_keywords  :
                try:
                    summary = wikipedia.summary(keyword, sentences=2)
                    notes += f"- **{keyword.capitalize()}**: {summary}\n"
                except wikipedia.exceptions.PageError:
                    print(f"Wikipedia summary unavailable for: {keyword}")
                    notes += f"- **{keyword.capitalize()}**: (Wikipedia summary unavailable)\n"
        # N-grams for more phrases
        bigrams = [b for b in zip(keywords.split(), keywords.split()[1:])]
        for bigram in bigrams:
            phrase = " ".join(bigram)
            if phrase in all_keywords:
                try:
                    summary = wikipedia.summary(phrase, sentences=2)
                    notes += f"- **{phrase.capitalize()}**: {summary}\n"
                except wikipedia.exceptions.PageError:
                    print(f"Wikipedia summary unavailable for: {phrase}")
                    notes += f"- **{phrase.capitalize()}**: (Wikipedia summary unavailable)\n"

    print("Notes created:")
    print(notes)

def main():
    """Runs the main program loop."""
    while True:
        input_method = input("Choose input method (1: audio, 2: text): ")
        if input_method == "1":
            identified_keywords = listen_and_identify_keywords()
            create_notes(identified_keywords)
        elif input_method == "2":
            text = input("Write your text here: ")
            create_notes(text)
        else:
            print("Invalid input method. Please choose 1 for audio or 2 for paste notes.")
            continue

        choice = input("Listen/Write again? (y/n): ").lower()
        if choice != 'y':
            break

if __name__ == "__main__":
    main()
