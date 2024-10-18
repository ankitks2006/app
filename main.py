# import pyttsx3
# import speech_recognition as sr
# import urllib.parse
# import time
# import webbrowser
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.clock import mainthread
# import threading

# class VoiceApp(App):
#     def build(self):
#         self.listening = False
#         self.layout = BoxLayout(orientation='vertical', padding=10)

#         self.label = Label(text="Voice Assistant", font_size=24)
#         self.layout.add_widget(self.label)

#         self.text_output = TextInput(text="", readonly=True, size_hint=(1, 0.4))
#         self.layout.add_widget(self.text_output)

#         self.start_button = Button(text="Start Listening", size_hint=(1, 0.2))
#         self.start_button.bind(on_press=self.start_listening)
#         self.layout.add_widget(self.start_button)

#         self.stop_button = Button(text="Stop", size_hint=(1, 0.2))
#         self.stop_button.bind(on_press=self.stop_listening)
#         self.layout.add_widget(self.stop_button)

#         self.exit_button = Button(text="Exit", size_hint=(1, 0.2))
#         self.exit_button.bind(on_press=self.stop)
#         self.layout.add_widget(self.exit_button)

#         return self.layout

#     @mainthread
#     def append_text(self, message):
#         self.text_output.text += f"{message}\n"

#     def start_listening(self, instance):
#         if not self.listening:
#             self.listening = True
#             self.append_text("Starting to listen...")
#             threading.Thread(target=self.run_voice_commands).start()

#     def stop_listening(self, instance):
#         self.listening = False
#         self.append_text("Stopped listening.")

#     def run_voice_commands(self):
#         self.speechtx("How can I help you?")
#         recognizer = sr.Recognizer()
#         while self.listening:
#             with sr.Microphone() as source:
#                 recognizer.adjust_for_ambient_noise(source)
#                 audio = recognizer.listen(source)
#                 try:
#                     data1 = recognizer.recognize_google(audio).lower()
#                     self.append_text(f"Heard: {data1}")
#                     if "stop" in data1:
#                         self.speechtx("Goodbye!")
#                         self.listening = False
#                     elif "song" in data1:
#                         self.speechtx("What song would you like to play?")
#                         song_request = recognizer.listen(source)
#                         song_request = recognizer.recognize_google(song_request).lower()
#                         self.speechtx(f"Searching YouTube for {song_request}.")
#                         query_encoded = urllib.parse.quote(song_request)
#                         webbrowser.open(f"https://www.youtube.com/results?search_query={query_encoded}")
#                     elif "github" in data1:
#                         webbrowser.open("https://github.com/")
#                     elif "youtube" in data1:
#                         self.speechtx("What would you like to search for on YouTube?")
#                         search_query = recognizer.listen(source)
#                         search_query = recognizer.recognize_google(search_query).lower()
#                         query_encoded = urllib.parse.quote(search_query)
#                         webbrowser.open(f"https://www.youtube.com/results?search_query={query_encoded}")
#                     elif "search" in data1:
#                         self.speechtx("What would you like to search for on Google?")
#                         search_query = recognizer.listen(source)
#                         search_query = recognizer.recognize_google(search_query).lower()
#                         query_encoded = urllib.parse.quote(search_query)
#                         webbrowser.open(f"https://www.google.com/search?q={query_encoded}")
#                     else:
#                         self.speechtx("Sorry, I didn't understand that command.")
#                 except sr.UnknownValueError:
#                     self.append_text("Sorry, I didn't understand that.")
    
#     def speechtx(self, text):
#         engine = pyttsx3.init()
#         voices = engine.getProperty('voices')
#         engine.setProperty('voice', voices[1].id)  # Female voice
#         engine.setProperty('rate', 150)  # Adjust speaking speed
#         engine.say(text)
#         engine.runAndWait()

# if __name__ == '__main__':
#     VoiceApp().run()

import pyttsx3
import speech_recognition as sr
import urllib.parse
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread
import threading

class VoiceApp(App):
    def build(self):
        self.listening = False
        self.layout = BoxLayout(orientation='vertical', padding=10)

        self.label = Label(text="Voice Assistant", font_size=24)
        self.layout.add_widget(self.label)

        self.text_output = TextInput(text="", readonly=True, size_hint=(1, 0.4))
        self.layout.add_widget(self.text_output)

        self.start_button = Button(text="Start Listening", size_hint=(1, 0.2))
        self.start_button.bind(on_press=self.start_listening)
        self.layout.add_widget(self.start_button)

        self.stop_button = Button(text="Stop Listening", size_hint=(1, 0.2))
        self.stop_button.bind(on_press=self.stop_listening)
        self.layout.add_widget(self.stop_button)

        self.exit_button = Button(text="Exit", size_hint=(1, 0.2))
        self.exit_button.bind(on_press=self.stop)
        self.layout.add_widget(self.exit_button)

        return self.layout

    @mainthread
    def append_text(self, message):
        self.text_output.text += f"{message}\n"

    def start_listening(self, instance):
        if not self.listening:
            self.listening = True
            self.append_text("Starting to listen...")
            threading.Thread(target=self.run_voice_commands, daemon=True).start()

    def stop_listening(self, instance):
        self.listening = False
        self.append_text("Stopped listening.")

    def run_voice_commands(self):
        self.speechtx("How can I help you?")
        recognizer = sr.Recognizer()
        
        while self.listening:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                self.append_text("Listening...")
                
                try:
                    audio = recognizer.listen(source)
                    data1 = recognizer.recognize_google(audio).lower()
                    self.append_text(f"Heard: {data1}")
                    self.process_command(data1)
                except sr.UnknownValueError:
                    self.append_text("Sorry, I didn't understand that.")
                except sr.RequestError as e:
                    self.append_text(f"Could not request results; {e}")
                except Exception as e:
                    self.append_text(f"An error occurred: {e}")

    def process_command(self, command):
        if "stop" in command:
            self.speechtx("Goodbye!")
            self.listening = False
        elif "song" in command:
            self.speechtx("What song would you like to play?")
            song_request = self.listen_for_response()
               
            if song_request:
                self.speechtx(f"Searching YouTube for {song_request}.")
                query_encoded = urllib.parse.quote(song_request)
                webbrowser.open(f"https://www.youtube.com/results?search_query={query_encoded}")
        elif "github" in command:
            webbrowser.open("https://github.com/")
        elif "youtube" in command:
            self.speechtx("What would you like to search for on YouTube?")
            search_query = self.listen_for_response()
            if search_query:
                query_encoded = urllib.parse.quote(search_query)
                webbrowser.open(f"https://www.youtube.com/results?search_query={query_encoded}")
        elif "search" in command:
            self.speechtx("What would you like to search for on Google?")
            search_query = self.listen_for_response()
            if search_query:
                query_encoded = urllib.parse.quote(search_query)
                webbrowser.open(f"https://www.google.com/search?q={query_encoded}")
        else:
            self.speechtx("Sorry, I didn't understand that command.")

    def listen_for_response(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5)  # Adding timeout for response
                return recognizer.recognize_google(audio).lower()
            except (sr.UnknownValueError, sr.RequestError):
                self.append_text("Sorry, I didn't catch that.")
                return None

    def speechtx(self, text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Female voice
        engine.setProperty('rate', 150)  # Adjust speaking speed
        engine.say(text)
        engine.runAndWait()

if __name__ == '__main__':
    VoiceApp().run()
