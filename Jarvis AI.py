import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import requests
import time
from googletrans import Translator


engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour=int(datetime.datetime.now().hour) 
    # this function returns current date and time as datetime object(if hour is 14 it will return 14hour)
    if hour>=0 and hour<12:
        speak("Good Morning !")

    elif hour>=12 and hour<18:
        speak("Good Afternoon !")

    else:
        speak("Good Evening !")    

    speak("Jarvis here! How may I help you ")  

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en')
        print("User said:",query )

    except Exception as e:
        print("Can't understand, say that again please ")
        return "None"
    
    return query

#For sending Emails
def send_email(to, content): #content is email message body
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo() #Sends the "EHLO" (Extended Hello) command to the SMTP server to identify the client
    server.starttls() #This ensures that the email content and credentials are transmitted securely
    server.login('your email', 'your password')
    server.sendmail('your email',to,content)
    server.close()

#For Spotify 
def play_song(song_name):
    query = song_name.replace(" ", "+")
    url = f"https://open.spotify.com/search/{query}"   
    webbrowser.open(url)

# For Weather
def get_weather(city_name):
    api_key="insert weather API here"   
    base_url="http://api.openweathermap.org/data/2.5/weather?"
    # creating complete URL
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric" #units=metric for temperature in celsius
    
    # Fetch the weather data
    response = requests.get(complete_url) #sends a get request to API
    data = response.json()  # Convert response to JSON

    if data["cod"] != "404": #will check cod key in json, anything other than 404 means valid weather data exists
        main = data["main"]  #contains temp and humidity details
        weather_desc = data["weather"][0]["description"] #weather brief description   # 0 is the index of first item in weather list 
        temp = main["temp"] #curr temp in celsis
        humidity = main["humidity"] #curr humidity percentage
        
        # creating a weather report string
        weather_report = (
            f"The weather in {city_name} is currently {weather_desc} "
            f"with a temperature of {temp}°C and a humidity of {humidity}%."
        )
        return weather_report
    else:
        return f"Sorry, I couldn't find the weather information for {city_name}."

def speak_weather(city_name, speak):
    weather = get_weather(city_name)
    speak(weather)        

#For Youtube
def play_video(video_name):
    query=video_name.replace(" ", '+')
    url=f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)

#For Google
def search(g_search):
    query=g_search.replace(" ", "+")
    url=f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
   
#For Calculator
def get_number(prompt):
    speak(prompt)
    while True:
        number = takeCommand()
        try:
            return float(number)
        except ValueError:
            speak("That doesn't seem to be a valid number, Please say it again")


def get_operator():
    speak("Please say the operator you want to use.")
    while True:
        operator = takeCommand().lower()
        if operator in ["plus", "addition", "add", "+"]:
            return "+"
        elif operator in ["minus", "subtraction", "subtract", "-"]:
            return "-"
        elif operator in ["multiply", "multiplication", "times", "*"]:
            return "*"
        elif operator in ["divide", "division", "divided by","divides", "/"]:
            return "/"
        else:
            speak("Invalid operator. Please say it again.")

def calculator():
    speak("Welcome to the voice calculator")
    first_number = get_number("Please say the first number.")
    second_number = get_number("Please say the second number.")
    operator = get_operator()

    if operator == "+":
        result = first_number + second_number
    elif operator == "-":
        result = first_number - second_number
    elif operator == "*":
        result = first_number * second_number
    elif operator == "/":
        if second_number == 0:
            speak("Division by zero is not allowed.")
            print("Division by zero is not allowed.")
            return
        result = first_number / second_number

    speak(f"The result of {first_number} {operator} {second_number} is {result}")
    print(f"The result of {first_number} {operator} {second_number} is {result}")

#For Stopwatch
def start_stopwatch():
    speak("Stopwatch started. Say 'stop' to stop the stopwatch.")
    start_time = time.time()
    
    while True:
        command = takeCommand()  
        if 'stop' in command.lower():
            elapsed_time = time.time() - start_time
            mins, secs = divmod(elapsed_time, 60)
            speak(f"Stopwatch stopped. Total time: {int(mins)} minutes and {int(secs)} seconds.")
            break
        

#For Files 
def open_file(file_name):
    """Function to open a file by name."""
    file_paths = {
        "notepad": "C:\\Windows\\System32\\notepad.exe",
        "calculator": "C:\\Windows\\System32\\calc.exe",
        "python project": "D:\\Python Stats Project\\project.py",
        "word document": "C:\\Users\\SAMSUNG\\Downloads",
        "proposal": "C:\\Users\\SAMSUNG\\Downloads",
        "movies ": "C:\\Users\\SAMSUNG\\OneDrive\\Documents\\Websites"
    }

    file_path = file_paths.get(file_name)
    if file_path and os.path.exists(file_path):
        os.startfile(file_path)
        speak(f"Opening {file_name}")
    else:
        speak(f"Sorry, I couldn't find the file {file_name}.")
        print(f"File '{file_name}' not found.")

    file_path = file_paths.get(file_name)
    if file_path and os.path.exists(file_path):
        os.startfile(file_path)
        speak(f"Opening {file_name}")
    else:
        speak(f"Sorry, I couldn't find the file {file_name}.")

# For Translation
def translate_text(text, dest_language): #'text' is text to be translated and 'dest_language' is in which para is translated 
 
    translator = Translator() #Translator() object is provided by googletrans library
    try:
        translated = translator.translate(text, dest=dest_language)  #this line uses the translator tool to translate the input text into a language you choose
        return translated.text  #this access text property of translated object, which contains translated version of input text 
    except Exception as e:
        speak("Sorry, I couldn't translate the text.")
        print("Translation error:", e)
        return None

if __name__=="__main__":
    wishme()
    while True:
        query=takeCommand().lower()
        if 'exit' in query.lower():
            speak("Goodbye")
            break
        
        if 'wikipedia' in query:
            speak("Searching wikipedia...")
            query = query.replace("wikipedia", "")
            # to focus on main word and dont focus on 'wikipedia',otherwise it will start explaining wikipedia
            results=wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")   

        elif 'open google' in query:
            webbrowser.open("google.com")  

        elif 'open spotify' in query:
            webbrowser.open("spotify.com")

        elif 'open whatsapp' in query:
            webbrowser.open("whatsapp.com")      

        elif 'open yahoo' in query:
            webbrowser.open("yahoo.com")
        
        elif 'open github' in query:
            webbrowser.open("github.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")    

        elif 'open student portal' in query:
            webbrowser.open("portals.au.edu.pk/students/")   

        elif 'open gmail' in query:
            webbrowser.open("gmail.com")            
        
        elif 'play music' in query:
            music_dir = 'path of any music directory' 
            songs = os.listdir(music_dir)
            random_song = random.choice(songs)
            os.startfile(os.path.join(music_dir, random_song)) 
        
        elif 'time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, time is {strtime}")

        elif 'open code' in query:
            codepath="C:\\Users\\SAMSUNG\\AppData\\Local\\Programs\\\Microsoft VS Code\\\Code.exe"    
            os.startfile(codepath)

        elif 'open word' in query:
            wordpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            os.startfile(wordpath)  

        elif 'open excel' in query:
            excelpath="C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
            os.startfile(excelpath)    

        elif 'email to [someone]' in query:
            try:
                speak("What should I say ?")
                content = takeCommand()  #takecommand() captures users voice input
                to="email address that you want to send mail to"
                send_email(to,content)
                speak("Email has been sent!")

            except Exception as e:
                print(e)
                speak("Sorry, I'm not able to send this email")       

            except Exception as e:
                print(e)
                speak("Sorry, I'm not able to send this email")          

            except Exception as e:
                print(e)
                speak("Sorry, I'm not able to send this email")           

        elif 'play spotify' in query:
            speak("Which song should I play?")
            song_name = takeCommand()
            play_song(song_name)  

        elif 'tell weather' in query:
            speak("Which city's weather would you like to know?")
            city_name = takeCommand()  
            speak_weather(city_name, speak)

        elif 'play youtube' in query:
            speak("Which video should I play?")
            video_name = takeCommand()
            play_video(video_name)

        elif 'search on google' in query:
            speak("What do you want to search?")
            search_bar=takeCommand()
            search(search_bar)    

        elif 'calculator' in query:
            calculator()   

        elif 'open file' in query:
            speak("What file would you like to open?")
            file_name = takeCommand()
            if file_name:
                open_file(file_name)     

        elif 'start stopwatch' in query:
            start_stopwatch()    
        
        elif 'translate' in query:
            speak("What text would you like me to translate?")
            text_to_translate = takeCommand()
            if text_to_translate == "None":
                continue
            speak("Which language should I translate it to?")
            language = takeCommand().lower()
            language_mapping = {
                "french": "fr",
                "spanish": "es",
                "german": "de",
                "italian": "it",
                "hindi": "hi",
                "arabic": "ar",
                "chinese": "zh-cn",
                "japanese": "ja",
                "russian": "ru",
            }
            dest_language = language_mapping.get(language, None)  #Takes the user-provided language name and retrieves the corresponding language code from the language_mapping dictionary
            if not dest_language:
                speak("Sorry, I don't recognize that language.")
                continue
            translated_text = translate_text(text_to_translate, dest_language)
            if translated_text:
                speak(f"The translation is: {translated_text}")
                print(f"Translated text: {translated_text}")
