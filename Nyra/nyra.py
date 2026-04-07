import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import os
import random
import pyautogui
import requests
import platform
import psutil
import pyjokes

ASSISTANT_NAME = "Nyra"
USER_NAME = "Neha"

# ---------------- ENGINE ----------------
engine = pyttsx3.init()

def setup_engine():
    engine.setProperty('rate', 170)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

setup_engine()

# ---------------- SPEAK ----------------
def speak(text):
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()

# ---------------- GREETING ----------------
def wishme():
    hour = datetime.datetime.now().hour

    if hour < 12:
        greet = "Good morning"
    elif hour < 18:
        greet = "Good afternoon"
    else:
        greet = "Good evening"

    speak(f"Hello {USER_NAME}, {greet}")
    speak(f"I am {ASSISTANT_NAME}. How can I help you today?")

# ---------------- COMMAND ----------------
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
        except:
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in").lower()
        print("You said:", query)
        return query

    except:
        speak("Sorry, I didn't catch that")
        return None

# ---------------- FEATURES ----------------

def tell_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time}")

def tell_date():
    now = datetime.datetime.now()
    speak(f"Today is {now.day} {now.strftime('%B')} {now.year}")

# 🎬 YOUTUBE HANDLER (SMART)
def handle_youtube(query):
    if "open youtube" in query:
        speak("Opening YouTube")
        wb.open("https://www.youtube.com")

    elif "on youtube" in query or "youtube" in query:
        search = query.replace("play", "").replace("search", "").replace("on youtube", "").replace("youtube", "").strip()
        if search:
            speak(f"Searching {search} on YouTube")
            wb.open(f"https://www.youtube.com/results?search_query={search}")
        else:
            speak("Opening YouTube")
            wb.open("https://www.youtube.com")

# 🔍 GOOGLE SEARCH
def google_search(query):
    speak(f"Searching Google for {query}")
    wb.open(f"https://www.google.com/search?q={query}")

# 💻 OPEN APP
def open_app(query):
    app_name = query.replace("open", "").strip()

    if "notepad" in app_name:
        os.system("notepad")

    elif "calculator" in app_name:
        os.system("calc")

    elif "chrome" in app_name:
        os.system("start chrome")

    else:
        try:
            os.system(app_name)
        except:
            speak("App not found, searching on Google")
            google_search(app_name)

# 📸 SCREENSHOT
def screenshot():
    try:
        img = pyautogui.screenshot()
        path = os.path.expanduser("~\\Pictures\\screenshot.png")
        img.save(path)
        speak("Screenshot taken")
    except:
        speak("Unable to take screenshot")

# 🖥 SYSTEM INFO
def system_info():
    uname = platform.uname()
    speak(f"System is {uname.system}")
    battery = psutil.sensors_battery()
    if battery:
        speak(f"Battery is at {battery.percent} percent")

# 💬 SMART REPLY
def smart_reply(query):

    if "how are you" in query:
        return "I am doing great Neha"

    elif "your name" in query:
        return f"My name is {ASSISTANT_NAME}"

    elif "hello" in query:
        return "Hello Neha"

    elif "joke" in query:
        return pyjokes.get_joke()

    else:
        speak("I don't know that, searching on Google")
        google_search(query)
        return None

# ---------------- MAIN ----------------
if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()

        if query is None:
            continue

        print("Command:", query)

        # 🎬 YOUTUBE PRIORITY
        if "youtube" in query:
            handle_youtube(query)

        # 🔍 GOOGLE
        elif "search" in query or "google" in query:
            google_search(query.replace("search", "").replace("google", ""))

        # 💻 OPEN APP
        elif "open" in query:
            open_app(query)

        # ⏰ TIME/DATE
        elif "time" in query:
            tell_time()

        elif "date" in query:
            tell_date()

        # 📸 SCREENSHOT
        elif "screenshot" in query:
            screenshot()

        # 🖥 SYSTEM
        elif "system info" in query or "battery" in query:
            system_info()

        # ❌ EXIT
        elif "exit" in query or "stop" in query:
            speak(f"Bye {USER_NAME}")
            break

        # 💬 FALLBACK
        else:
            response = smart_reply(query)
            if response:
                speak(response)