import cv2 as cv
import numpy as np
import csv
from datetime import datetime
import face_recognition
import math
import os, sys
#finding the confidence of the face

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)
    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


#creating object from our cv module
video_capture = cv.VideoCapture(0)
if not video_capture.isOpened():
    sys.exit("Video source not found")
#getting and encoding specimen 
#getting and encoding specimen pictures




known_face_encodings= []
known_face_names = []
for image in os.listdir('faces'):
    face_image = face_recognition.load_image_file(f'faces/{image}')
    face_encoding = face_recognition.face_encodings(face_image)[0]
    if face_encoding:
        known_face_encodings.append(face_encoding)
        known_face_names.append(image)




#creating family name list

family = known_face_names.copy()

#creating necesasary varaibles

face_locations = []
face_encodings = []
face_names = []
check = True

#getting exact date and time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
print(current_date)


#creating new csv files
f = open(f'{current_date}.csv', 'w+', newline = '',encoding='utf-8') 
#creating an object used to write to csv files
inwrtiter =csv.writer(f)



while True:
    #extracting data from the video camera
    _,frame = video_capture.read()
    #decreasing the size of the pictures coming from the camera by a ratio of 0.25
    small_frame = cv.resize(frame,(0,0),fx=0.25,fy=0.25)
    #changing image to rgb
    rgb_small_frame = small_frame[:,:,::-1]
    
    
    if check:
        #check if there is a face in the frame and encode
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names =[]
        for face_encoding  in face_encodings:
            
            #check if face encoding matches any known encoding
            matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
            name = ''
            face_distance = face_recognition.face_distance(known_face_encodings,face_encoding)
            #cheching the best probability
            
        
            best_match_index = np.argmin(face_distance)
            confidence = face_confidence(face_distance[best_match_index])
            if matches[best_match_index]:
                name= known_face_names[best_match_index]
            #Entering name to csv file
            face_names.append(f'{name} ({confidence})')
            print(face_names)
            if name in known_face_names:
                if name in family:
                    print(name)
                    #to avoid redundancy
                    family.remove(name)
                    current_time =now.strftime("%Y-%m-%d")
                    #write down to file
                    inwrtiter.writerow([name,current_time])

    for(top, right, bottom, left), name in zip(face_locations,face_names):
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
f.close()
