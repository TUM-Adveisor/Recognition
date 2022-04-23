import time
import speech_recognition as sr



def callback(recognizer, audio):
    global text
    try:
        text = recognizer.recognize_google(audio, language="de-AT", show_all=True)
        print(text)
    except sr.UnknownValueError:
        print("Wth did you say?")
        # Call speech recognition function again
    except sr.RequestError:
        print("Internet problems!")

r = sr.Recognizer()
m = sr.Microphone()
#print(sr.Microphone.list_microphone_names()) list of audio input
with m as source: #change default with device_index= of previous list
    r.adjust_for_ambient_noise(source, duration=0.5)
    print("Start speaking:")
stop_listening = r.listen_in_background(m, callback)
time.sleep(8)
stop_listening(wait_for_stop=False)
if "text" in globals():
  print("exists")
else:
    print("Something went wrong!")



#Start: 'Befehl'
#To-do: get confidence levels > 0.9, otherwise search alternatives for key words set from names
# König, Dame, Läufer, Turm, Springer, Bauer
# If confidence level too low --> ask "Did you say "..."?"