import speech_recognition as sr
import time
from database import save_recording,connect_to_db, setup_db, read_recording,last_n_recording, delete_recording 

def command_process(command_text,text):
    command1 = "start recording"
    command2 = "stop recording"
    # Check if the trigger word is detected
    if command1 in command_text.lower():
        print("Recording started...")
        return "start"
    elif command2 in command_text.lower():
        print("recording stopped")
        save_recording(text)
        return "stop"
    

    
def listen():
    r = sr.Recognizer()
    text = ""
    with sr.Microphone() as source:
        print("Listening for command...")
        start_time = time.time()
        time_limit = 30
        start_mode = None
        while True:
            if time.time() - start_time > time_limit:
                print(f"time limit of {time_limit} seconds has been passed. ")
                command_text = "Stop recording"
                command_process(command_text,text)
                return

            audio = r.listen(source)  
            
            try:
                command_text = r.recognize_google(audio)
                command = command_process(command_text,text)
                if command == "start":
                    start_mode = 1

                elif command == "stop":
                    return
                
                elif start_mode:
                    text +=" "+ command_text
                    print("the recorded text is: ", text)

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error: {0}".format(e))

# conn = connect_to_db()
# setup_db()
listen()
# read_recording()
# delete_recording(conn, 1)
read_recording()
# last_n_recording(2)