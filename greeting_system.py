import cv2 as cv
import numpy as np
import csv
import pyttsx3
from datetime import datetime
import face_recognition
import math
import os, sys
import pyttsx3
import speech_recognition as sp
import time
import sys
def load_animation():
    
    #animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    animation = animation * 3
    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

def snap_picture(image_name, video_capture):
    cam = cv.VideoCapture(0)
    while True:
        ret,frame = cam.read()

        if not ret:
            print('failed to grab frame')
            break
        cv.imshow('test', frame)

        k = cv.waitKey(1)
        
        if k%256 == 32:
            img_name = 'faces/{image_name}.png'
            cv2.imwrite(image_name,frame)
            computer_say('screenshot_taken')
            computer_say('please wait a few minute for it to encode your face')
            encode_image(answer)
            computer_say('Your face has been successfully added to the database')
            break
        




#initiate pyttsx3
engine = pyttsx3.init()
#initialize recognitiom
rec = sp.Recognizer()
#initialize microphone
my_micro = sp.Microphone(device_index=0)
#finding the confidence of the face
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)
    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class  FaceRecognition:
    known_face_encodings= []
    known_face_names = []
    face_locations = []
    face_encodings = []
    face_names = []
    check = True
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    family= []
    f= None
    inwriter = None
    not_done = False
    def __init__(self) :
        self.computer_say('We are working on your images,please wait...')
        while not self.not_done:
            load_animation()
            self.encode_face()
        self.computer_say('your camera will be activated soon')
        

    def computer_say(self, sentence):
        engine.setProperty('volume',1)
        voices = engine.getProperty('voices')
        print(voices)
        engine.setProperty('voice', voices[0].id)
        engine.say(sentence)
        engine.runAndWait()
       
    def computer_listen(self,source):
        print('listening...')
        audio = rec.listen(source)
        answer = rec.recognize_google(audio)
        return answer
    def encode_face(self):

        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            if face_recognition.face_encodings(face_image):
                face_encoding = face_recognition.face_encodings(face_image)[0]
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(image)
            else:
                os.remove(f'faces/{image}')
            self.not_done = True
    def encode_image(self,image):
        face_image = face_recognition.load_image_file(f'faces/{image}.png')
        if face_recognition.face_encodings(face_image):
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(f'faces/{image}.png')
        else:
            os.remove(image)
            

    def run_recognition(self):
        self.f = open(f'{self.current_date}.csv', 'w+', newline = '',encoding='utf-8') 
        self.inwriter =csv.writer(self.f)
        self.family = self.known_face_names.copy()
        video_capture = cv.VideoCapture(0)
        if not video_capture.isOpened():
            sys.exit("Video source not found")
        while True:
            #extracting data from the video camera
            _,frame = video_capture.read()
            #decreasing the size of the pictures coming from the camera by a ratio of 0.25
            small_frame = cv.resize(frame,(0,0),fx=0.25,fy=0.25)
            #changing image to rgb
            rgb_small_frame = small_frame[:,:,::-1]
            
            
            if self.check:
                #check if there is a face in the frame and encode
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame,self.face_locations)
                self.face_names =[]
                for face_encoding  in self.face_encodings:
                    
                    #check if face encoding matches any known encoding
                    matches = face_recognition.compare_faces(self.known_face_encodings,face_encoding)
                    name = ''
                    face_distance = face_recognition.face_distance(self.known_face_encodings,face_encoding)
                    #cheching the best probability
                    
                
                    best_match_index = np.argmin(face_distance)
                    confidence = face_confidence(face_distance[best_match_index])
                    if matches[best_match_index]:
                        name= self.known_face_names[best_match_index]
                        self.face_names.append(f'{name} ({confidence})')
                    else:
                        video_capture.release()
                        cv.destroyAllWindows()
                        self.computer_say('Image not in database,Would you like to add your image to the database yes or np')
                        # answer = self.computer_listen(source)
                        answer = input('yes or no? ')
                        if answer == 'yes':
                            self.computer_say('what is your name')
                            # answer = self.computer_listen(source)
                            answer = input('Input your name ?   ')
                            self.computer_say('please station your head to show  your face  unless picture won\'t be stored')
                            cam = cv.VideoCapture(0)
                            while True:
                                ret,frames = cam.read()
                                if not ret:
                                    print('failed to grab frame')
                                    break
                                cv.imshow('test', frames)
                                k = cv.waitKey(1)
                                if k%256 == 32:
                                    img_name = f'faces/{answer}.png'
                                    cv.imwrite(img_name,frame)
                                    self.computer_say('screenshot_taken')
                                    self.computer_say('please wait a few minute for it to encode your face')
                                    self.encode_image(answer)
                                    self.computer_say('Your face has been successfully added to the database')
                                    cam.release()
                                    cv.destroyAllWindows()
                                    self.run_recognition()
                                    break
                                    
                        elif answer == 'no':
                            self.computer_say('you wont be able to use this system')
                            sys.exit()
                            print('life')
                


                        
                    if name in self.known_face_names:
                        if name in self.family:
                            self.computer_say(f'{name} is  in the class')
                            #to avoid redundancy
                            self.family.remove(name)
                            current_time =self.now.strftime("%H-%M-%S")
                            #write down to file
                            self.inwriter.writerow([name,current_time])
            #add rectangle and name over face
            for(top, right, bottom, left), name in zip(self.face_locations,self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                cv.rectangle(frame,(left,top), (right,bottom),(0,0,255),2)
                cv.rectangle(frame,(left,bottom-35), (right,bottom),(0,0,255),-1)
                cv.putText(frame,name, (left+6,bottom - 6),cv.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
            

            cv.imshow('family attendance system', frame)
            if cv.waitKey(1)  == ord('q'):
                break

        #release camera
        video_capture.release()
        #destroy all windows
        cv.destroyAllWindows()
        self.f.close()





if __name__ == "__main__":
    fr = FaceRecognition()
    fr.run_recognition()



