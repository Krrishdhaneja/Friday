import ast
import urllib.parse
import pyttsx3
import webbrowser
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import sys
import requests

weather_api_key = "undefined"
wolframalpha_api_key = "undefined"

try:
    f = open("api_config.txt", "r")
    for i in f.readlines():
        if i.startswith("weather_api_key"):
            weather_api_key = i[i.index("=") + 1:].strip()
        if i.startswith("wolframalpha_api_key"):
            wolframalpha_api_key = i[i.index("=") + 1:].strip()
    f.close()

except FileNotFoundError:
    print("Error: api_config.txt not found. Please create this file and add your API keys there")

base_url = "http://api.openweathermap.org/data/2.5/weather?"

client = wolframalpha.Client(wolframalpha_api_key)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

message_callback = None
last_message_not_understood = False


def speak(audio, only_print=False):
    audio = str(audio)  # some parsers return other types then string

    if message_callback is not None:
        message_callback.emit(audio)
    else:
        print('Computer: ' + audio)

    if not only_print:
        engine.say(audio)
        engine.runAndWait()


# don't use this function directly inside user_input_parser
def listen_microphone(fallback=True):
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')

    except (sr.UnknownValueError, OSError):
        if not fallback:
            return

        speak('Sorry sir! I didn\'t get that! Try typing the command!')

        try:
            query = str(input('Command: '))
        except EOFError:
            speak('Sorry sir! Seams like you have neither a microphone nor a console that supports input!')
            query = "exit"  # only happens in ci tests which doesn't support inputs

    return query


def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if 0 <= currentH < 12:
        return 'Good Morning! , sir'
    elif currentH < 18:
        return 'Good Afternoon! , sir'
    else:
        return 'Good Evening! , sir'


def parser_return(output_text, current_topic="", computer_again=False):
    return output_text, current_topic, computer_again


def user_input_parser(query, current_topic, callback=None):
    global message_callback, last_message_not_understood
    message_callback = callback

    query = query.lower()

    if current_topic == "greet":
        speak(greetMe())
        speak('what can I do for you, sir?')
        return

    elif query == "" and not last_message_not_understood:
        last_message_not_understood = True
        speak('Sorry sir! I didn\'t get that! Please try again...')
        return current_topic

    elif query == "":
        return current_topic

    else:
        last_message_not_understood = False

    ####################################################################
    #       current_topic checks are starting here...                  #
    ####################################################################

    if current_topic == "search":
        webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote(query, safe=''))
        speak('done , sir')

    elif current_topic == "calc: firstnum":
        speak("which is the second number?")
        return "calc: " + query

    elif current_topic.startswith("calc: "):
        try:
            nums = {"num1": float(current_topic[current_topic.index(" "):].strip()), "num2": float(query)}
            speak('which operator?')
            return "calc_end: " + str(nums)
        except ValueError:
            speak('At least one of the numbers doesn\'t seam to be a string. So again, what is the first number?')
            return "calc: firstnum"

    elif current_topic.startswith("calc_end: "):
        nums = ast.literal_eval(current_topic[current_topic.index(" "):].strip())

        if 'minus' in query or '-' in query:
            speak(nums["num1"] - nums["num2"])
        elif 'plus' in query or '+' in query:
            speak(nums["num1"] + nums["num2"])
        elif 'multiply' in query or 'x' in query or '*' in query:
            speak(nums["num1"] * nums["num2"])
        elif 'divide' in query or '/' in query:
            speak(nums["num1"] / nums["num2"])

    elif current_topic == "repeat":
        speak(query)

    elif current_topic == "weather":
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + query
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
                  str(round(current_temperature - 273.15, 1)) +
                  "\n atmospheric pressure (in hPa unit): " +
                  str(current_pressure) +
                  "\n humidity (in percentage): " +
                  str(current_humidity) +
                  "\n description: " +
                  str(weather_description))
        else:
            speak("Sorry, I couldn't find the city!")

    ####################################################################
    #     some more current_topic checks maybe here...                 #
    #     other parsing after that... (always continue with elif!)     #
    ####################################################################

    elif 'open youtube' in query:
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
        return "search"

    elif "calculations" in query:
        speak("ok , sir")
        speak("which is the first number?")
        return "calc: firstnum"


    elif 'nothing' in query or 'abort' in query or 'stop' in query or 'no' in query or 'exit' in query:
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

    # elif "make a list" in query:
    #     speak("ok sir")
    #     list3 = str(input("what is the item:"))  # not the right way to go anymore - we have to think of something else
    #     speak("things added")
    #
    # elif "add items in my list" in query:
    #     speak("ok sir")
    #     list2 = str(input("what is the new item:"))  # not the right way to go anymore - we have to think of something else
    #     speak("things added")

    elif 'repeat me' in query or 'repeat what i say' in query:
        speak('what should i repeat ?')
        return "repeat"

    # elif 'change your voice' in query:
    #     engine.setProperty('voice', voices[0].id)
    #     speak("Is this voice ok ? speak yes or no")
    #     voice1 = myCommand()  # not allowed anymore - please use current_topic to break it up in multiple parsing steps
    #     if "yes" in voice1:
    #         speak('ok , sir')
    #     if 'no' in voice1:
    #         speak('changing the voice ....')
    #         engine.setProperty('voice', voices[0].id)
    #         speak('voice changed')
    #
    # elif 'change your voice to male' in query:
    #     engine.setProperty('voice', voices[0].id)
    #     speak("Is this voice ok ? speak yes or no")
    #     voice3 = myCommand()  # not allowed anymore - please use current_topic to break it up in multiple parsing steps
    #     if "yes" in voice3:
    #         speak('ok , sir')
    #     if 'no' in voice3:
    #         speak('changing the voice ....')
    #         engine.setProperty('voice', voices[0].id)
    #         speak('voice changed')
    #
    # elif 'change your voice to female' in query:
    #     engine.setProperty('voice', voices[1].id)
    #     speak("Is this voice ok ? speak yes or no")
    #     voice4 = myCommand()  # not allowed anymore - please use current_topic to break it up in multiple parsing steps
    #     if "yes" in voice4:
    #         speak('ok , sir')
    #     if 'no' in voice4:
    #         speak('changing the voice ....')
    #         engine.setProperty('voice', voices[1].id)
    #         speak('voice changed')

    elif 'what\'s the weather like today' in query or 'what is the weather outside' in query:
        speak('of which city you want to know the weather of')
        return "weather"


    # elif 'make a new file' in query:
    #     speak('please enter the file name')
    #     file_name = str(input('File name:'))  # not the right way to go anymore - we have to think of something else
    #     open(file_name, "w+")
    #
    # elif "delete a file" in query:
    #     speak("please , write the full path of the file")
    #     file_to_delete = str(input('Write the full path of the file to delete : '))  # not the right way to go anymore - we have to think of something else
    #     os.remove(file_to_delete)

    elif "yes" in query:
        speak('ok , sir')

    else:
        speak('Searching...')
        try:
            try:
                res = client.query(query)
                results = next(res.results).text
                # speak('Got it.')
                speak(' - WOLFRAM-ALPHA says - ', only_print=True)
                speak(results)

            except:
                results = wikipedia.summary(query, sentences=2)
                # speak('Got it.')
                speak(' - WIKIPEDIA says - ', only_print=True)
                speak(results)

        except:
            webbrowser.open('https://www.google.com/search?q=' + urllib.parse.quote(query, safe=''))

    speak('Anything else that i can do for you?')


if __name__ == '__main__':

    currentTopic = "greet"
    text = ""

    while True:
        currentTopic = user_input_parser(text, currentTopic)
        if currentTopic is None:
            currentTopic = ""
        text = listen_microphone()
