#importing necessary modules
import cv2 as cv
import numpy as np
import csv
from datetime import datetime
import face_recognition


#creating object from our cv module
video_capture = cv.VideoCapture(0)

#ggetting and encoding specimen 
#getting and encoding specimen pictures
testament_image = face_recognition.load_image_file(r'C:\Users\USER\Pictures\ADOBE RESOURCES\Camera Roll\testament.jpg')
testament_encodings = face_recognition.face_encodings(testament_image)
if len(testament_encodings) > 0:
    testament_encoding = testament_encodings[0]

nifise_image = face_recognition.load_image_file(r'C:\Users\USER\OneDrive - COVENANT UNIVERSITY\PICS FROM PHONE\nifise.jpg')
nifise_encodings = face_recognition.face_encodings(nifise_image)
if len(nifise_encodings) > 0:
    nifise_encoding = nifise_encodings[0]

ini_image = face_recognition.load_image_file(r'C:\Users\USER\OneDrive - COVENANT UNIVERSITY\PICS FROM PHONE\ini.jpg')
ini_encodings = face_recognition.face_encodings(ini_image)
if len(ini_encodings) > 0:
    ini_encoding = ini_encodings[0]

daddy_image = face_recognition.load_image_file(r'C:\Users\USER\OneDrive - COVENANT UNIVERSITY\PICS FROM PHONE\daddy.jpg')
daddy_encodings = face_recognition.face_encodings(daddy_image)
if len(daddy_encodings) > 0:
    daddy_encoding = daddy_encodings[0]

bill_clinton_image = face_recognition.load_image_file(r'C:\Users\USER\Pictures\FACE_RECOGNITIO_PICS\bill_clinton.jpg')
bill_clinton_encodings = face_recognition.face_encodings(bill_clinton_image)
if len(bill_clinton_encodings) > 0:
    bill_clinton_encoding = bill_clinton_encodings[0]

#creating list for created encodings
known_face_encodings =[
    nifise_encoding,
    ini_encoding,
    testament_encoding,
    bill_clinton_encoding]




#creating list for known_face names
known_face_names =[
    'testament',
    'nifise',
    'ini',
    'daddy'

]

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
            print(best_match_index)
            if matches[best_match_index]:
                name= known_face_names[best_match_index]
            #Entering name to csv file
            face_names.append(name)
            if name in known_face_names:
                if name in family:
                    print(name)
                    #to avoid redundancy
                    family.remove(name)
                    current_time =now.strftime("%Y-%m-%d")
                    #write down to file
                    inwrtiter.writerow([name,current_time])

    cv.imshow('family attendance system', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

#release camera
video_capture.release()
#destroy all windows
cv.destroyAllWindows()
f.close()
