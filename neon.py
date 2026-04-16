import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

print("Initializing engine...")

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
print("Available voices:")
for i, v in enumerate(voices):
    print(i, v.id)

engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)


def speak(audio):
    print("\nAssistant:", audio)
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    print("Current hour:", hour)

    if 0 <= hour < 12:
        speak("Good Morning, how can I help you")
    elif 12 <= hour < 18:
        speak("Good Afternoon, how can I help you")
    else:
        speak("Good Evening, how can I help you")


def list_microphones():
    print("Microphones available:")
    for i, mic in enumerate(sr.Microphone.list_microphone_names()):
        print(i, mic)


def takeCommand():
    print("\nCalling takeCommand()")

    r = sr.Recognizer()

    list_microphones()

    try:
        with sr.Microphone() as source:
            print("Using default microphone")
            print("Adjusting for noise...")
            r.adjust_for_ambient_noise(source, duration=1)

            print("Listening now...")
            audio = r.listen(source)

            print("Audio captured")

    except Exception as e:
        print("Microphone error:", e)
        return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User:", query)
        return query.lower()

    except sr.UnknownValueError:
        print("Could not understand audio")
        return None

    except sr.RequestError as e:
        print("API error:", e)
        return None

    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    print("Starting assistant...")

    wishMe()

    while True:
        print("\nWaiting for next command...")

        query = takeCommand()

        if query is None:
            print("No input detected, trying again")
            continue

        print("Final command:", query)

        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("wikipedia", "")

            try:
                page = wikipedia.page(query)
                content = page.content.split('\n')[0:3]
                content = ' '.join(content)

                print("Wikipedia result:", content)
                speak(content)

            except Exception as e:
                print("Wikipedia error:", e)
                speak("Sorry, not found")

        elif 'youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'music' in query:
            speak("Opening music")
            webbrowser.open("https://music.youtube.com")

        elif 'whatsapp' in query:
            speak("Opening WhatsApp")
            webbrowser.open("https://web.whatsapp.com")

        elif 'notepad' in query:
            speak("Opening Notepad")
            os.startfile("notepad.exe")

        elif 'chrome' in query:
            speak("Opening Chrome")
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

        elif 'code' in query:
            speak("Opening VS Code")
            os.startfile("C:\\Users\\Harsh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

        elif 'cmd' in query or 'command prompt' in query:
            speak("Opening command prompt")
            os.startfile("C:\\Windows\\System32\\cmd.exe")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print("Time:", strTime)
            speak(f"The time is {strTime}")

        elif 'exit' in query or 'stop' in query:
            speak("Goodbye")
            print("Exiting program")
            break

        else:
            print("Command not matched")
            speak("I did not understand")
