import tkinter as tk
import pyttsx3
import threading
import time
import speech_recognition as sr
import pygame
from modules.local_chat import get_local_response  


engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.5)  


def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("background.mp3")  
    pygame.mixer.music.set_volume(0.2)  
    pygame.mixer.music.play(-1)


root = tk.Tk()
root.title("JARVIS - ULTRA FINAL BEAST MODE")
root.attributes("-fullscreen", True)
root.configure(bg="#121212")

canvas = tk.Canvas(root, width=400, height=400, bg="#121212", highlightthickness=0)
canvas.place(relx=0.5, rely=0.5, anchor="center")

circle = canvas.create_oval(50, 50, 350, 350, fill="#000000", outline="#00BFFF", width=5)
label = canvas.create_text(200, 200, text="JARVIS", fill="#ffffff", font=("Consolas", 28, "bold"))

is_speaking = False


def animate_core():
    grow = True
    while is_speaking:
        coords = (40, 40, 360, 360) if grow else (50, 50, 350, 350)
        color = "#FFFFFF" if grow else "#FFFFFF"
        canvas.coords(circle, *coords)
        canvas.itemconfig(circle, outline=color)
        canvas.itemconfig(label, fill=color)
        grow = not grow
        root.update()
        time.sleep(0.12)
    canvas.coords(circle, 50, 50, 350, 350)
    canvas.itemconfig(circle, outline="#ffffff")
    canvas.itemconfig(label, fill="#ffffff")
    root.update()


def speak_jarvis(text):
    global is_speaking
    is_speaking = True
    threading.Thread(target=animate_core, daemon=True).start()
    engine.say(text)
    engine.runAndWait()
    is_speaking = False


root.bind("<Escape>", lambda e: root.destroy())


def listen_loop():
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except:
        speak_jarvis("Microphone not found.")
        return

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    speak_jarvis("Ultra Final Mode online, Tony.")
    while True:
        with mic as source:
            try:
                print("🎤 Listening...")
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                print("✅ You said:", command)

                if command.lower() in ["exit", "shutdown"]:
                    speak_jarvis("Powering down.")
                    root.destroy()
                    break

                response = get_local_response(command)
                if not response:
                    response = "I don't have an answer for that."
                speak_jarvis(response)

            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print("❌ Error:", e)
                speak_jarvis("I didn't catch that.")

def keyboard_input():
    while True:
        cmd = input("🧠 Type: ")
        if cmd.lower() in ["exit", "shutdown"]:
            speak_jarvis("Shutting down.")
            root.destroy()
            break
        response = get_local_response(cmd)
        speak_jarvis(response if response else "I don't have an answer for that.")


threading.Thread(target=play_music, daemon=True).start()
threading.Thread(target=listen_loop, daemon=True).start()
threading.Thread(target=keyboard_input, daemon=True).start()

root.mainloop()
