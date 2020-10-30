import pyttsx3
import webbrowser
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys

engine = pyttsx3.init('sapi5')

client = wolframalpha.Client('your_client_id')

voices = engine.getProperty('voices')
engine.setProperty('voice' ,voices[0].id)

def speak(audio):
    print('Computer: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning! , sir')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon! , sir')

    if currentH >= 18 and currentH !=0:
        speak('Good Evening! , sir')

greetMe()

#speak("what\'s the password")
#k=str(input("password:"))
#if "your_password" in k:
#    speak("welcome back ,  sir")
#else:
#    sys.exit()


speak('what can i do for you , sir')

def myCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold =  0.3
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query


if __name__ == '__main__':

    while True:

        query = myCommand()
        query = query.lower()

        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif "do calculations" in query:
            speak("ok , sir")
            speak("which is the first number")
            d=int(input("first number:"))
            speak("which is the second number")
            t=int(input("second number:"))
            speak("and which operator")
            k=str(input("operator:"))
            if "+" in k:
              print(d+t)
            if "-" in k:
              print(d-t)
            if "x" in k:
              print(d*t)
            if "/" in k:
              print(d/t)
            if "^" in k:
              print(d**t)


        elif 'nothing' in query or 'abort' in query or 'stop' in query or 'no' in query:
            speak('okay')
            speak('Bye Sir, have a good day.')
            sys.exit()

        elif 'hello' in query:
            speak('Hello Sir')

        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            sys.exit()

        elif "change your voice" in query:
            os.startfile('jarvis.py')
            sys.exit

        elif "make a list" in query:
            speak("ok sir")
            k = str(input("what is the item:"))
            speak("things added")

        elif "add items in my list" in query:
            speak("ok sir")
            d=str(input("what is the new item:"))
            speak("things added")

        elif "what\'s in my list" in query or "what is in my list" in query:
            speak("now telling list items")




        else:
            query = query
            speak('Searching...')
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak('WOLFRAM-ALPHA says - ')
                    speak('Got it.')
                    speak(results)

                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak('WIKIPEDIA says - ')
                    speak(results)

            except:
                webbrowser.open('www.google.com')

        speak('anything else that i can do for you , sir')
        if "yes" in query:
            speak('ok , sir')
        elif "no" in query:
            speak("ok sir . have a good day")
            sys.exit
