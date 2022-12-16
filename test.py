import pyttsx3
import speech_recognition as sp
import cv2

import sys
engine = pyttsx3.init()
check = True
#initialize recognition
rec = sp.Recognizer()
cam = cv2.VideoCapture(0)
#device index
my_micro = sp.Microphone(device_index=0)


with my_micro as source:
    engine.say('Your image is not in database, will you like to add, yes or no')
    engine.runAndWait()
    print('listening...')
    audio = rec.listen(source) 
    answer = rec.recognize_google(audio)
    if answer == 'yes':
        engine.say('what is your name')
        engine.runAndWait()
        print('listening...')
        audio = rec.listen(source) 
        answer = rec.recognize_google(audio)
        engine.say('please station your head to take your picture')
        engine.runAndWait()
        while True:
            ret,frame = cam.read()

            if not ret:
                print('failed to grab frame')
                break
            cv2.imshow('test', frame)

            k = cv2.waitKey(1)
            if k %2567 == 27:
                
                print('Escape hit, closing the app')
                break
            if k%256 == 32:
                img_name = 'faces/answer.png'
                cv2.imwrite(img_name,frame)
                print('screenshot_taken')
                break
    elif answer == 'no':
        engine.say('You wont be able to use this system')
        engine.runAndWait()
        sys.exit()
        print('life')


