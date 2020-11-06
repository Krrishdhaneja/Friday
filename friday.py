from googlesearch import *
import pyttsx3
import webbrowser
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
import requests
import json
import time

api_key = "e7bcb44e803e558ca3b74aaf5a37b41c"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

engine = pyttsx3.init('sapi5')

client = wolframalpha.Client('EV3UUJ-ET9UTALAH3')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    print('Computer: ' + audio)
    engine.say(audio)
    engine.runAndWait()


def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if 0 <= currentH < 12:
        speak('Good Morning! , sir')

    if 12 <= currentH < 18:
        speak('Good Afternoon! , sir')

    if currentH >= 18 and currentH != 0:
        speak('Good Evening! , sir')


greetMe()

speak('what can I do for you , sir')


def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
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

        if 'open youtube' in query or 'open YouTube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.com')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif 'open github' in query:
            speak('okay')
            webbrowser.open('www.github.com')

        elif "what\'s up" in query or 'how are you friday' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!',
                      'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif "hey friday" in query:
            # speak(greetMe())
            help = ["what can i do for you , sir", "how can i help you"]
            speak(random.choice(help))

        elif 'search' in query or 'do a search' in query:
            speak('what should I search for ?  sir')
            search1 = myCommand()
            chrome_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe %s'
            for url in search(search1, tld="co.in", num=1, stop=1, pause=2):
                webbrowser.open("https://google.com/search?q=%s" % search1)
            speak('done , sir')

        elif "do calculations" in query or 'do some calculations' in query:
            speak("ok , sir")
            speak("which is the first number")
            num1 = myCommand()
            num11 = float(num1)
            speak("which is the second number")
            num2 = myCommand()
            num22 = float(num2)
            speak('which operator')
            q = myCommand()
            if 'minus' in q or 'Minus' in q or '-' in q:
                print(num11 - num22)
            elif 'plus' in q or 'Plus' in q or '+' in q:
                print(num11 + num22)
            elif 'multiply' in q or 'Multiply' or 'x' in q or '*' in q:
                print(num11 * num22)
            elif 'divide' in q or 'Divide' in q or '/' in q:
                print(num11 / num22)

        elif 'nothing' in query or 'abort' in query or 'stop' in query or 'no' in query:
            speak('okay')
            speak('Bye Sir, have a good day.')
            sys.exit()

        elif 'hello' in query:
            speak('Hello Sir')

        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            sys.exit()

        elif 'what\'s the time' in query:
            hours = str(datetime.datetime.now().hour)
            minutes = str(datetime.datetime.now().minute)
            speak('it is ' + hours + ' : ' + minutes)

        elif "make a list" in query:
            speak("ok sir")
            list3 = str(input("what is the item:"))
            speak("things added")

        elif "add items in my list" in query:
            speak("ok sir")
            list2 = str(input("what is the new item:"))
            speak("things added")

        elif 'repeat me' in query or 'repeat what i say' in query:
            speak('what should i repeat ?')
            repeat = myCommand()
            speak(repeat)

        elif 'change your voice' in query:
            engine.setProperty('voice', voices[1].id)
            speak("Is this voice ok ? speak yes or no")
            voice1 = myCommand()
            if "yes" in voice1:
                speak('ok , sir')
            if 'no' in voice1:
                speak('changing the voice ....')
                engine.setProperty('voice', voices[0].id)
                speak('voice changed')

        elif 'change your voice to male' in query:
            engine.setProperty('voice', voices[1].id)
            speak("Is this voice ok ? speak yes or no")
            voice3 = myCommand()
            if "yes" in voice3:
                speak('ok , sir')
            if 'no' in voice3:
                speak('changing the voice ....')
                engine.setProperty('voice', voices[0].id)
                speak('voice changed')

        elif 'change your voice to female' in query:
            engine.setProperty('voice', voices[0].id)
            speak("Is this voice ok ? speak yes or no")
            voice4 = myCommand()
            if "yes" in voice4:
                speak('ok , sir')
            if 'no' in voice4:
                speak('changing the voice ....')
                engine.setProperty('voice', voices[1].id)
                speak('voice changed')

        elif 'what\'s the weather like today' in query or 'what is the weather outside' in query:
            speak('of which city you want to know the weather of')
            city_name = myCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature (in Celsius): " +
                      str(current_temperature - 273) +
                      "\n atmospheric pressure (in hPa unit): " +
                      str(current_pressure) +
                      "\n humidity (in percentage): " +
                      str(current_humidity) +
                      "\n description: " +
                      str(weather_description))
            else:
                print(" City Not Found ")





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
