import cv2
import numpy as np
import face_recognition
from PIL import Image,ExifTags
import pandas as pd
import eel
import threading
from datetime import datetime
import encode
import pydb

cap=False

name_list=[]

def get_data(names,facestr):
    global known_face_names,known_face_encodings
    known_face_names=names
    known_face_encodings=encode.imgdecode(facestr)
    



def camera():
    global cap,known_face_names,known_face_encodings
    global video_capture 
    video_capture = cv2.VideoCapture(0)
    (grabbed, frame) = video_capture.read()


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    
    while cap:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            #print(len(face_encodings))
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                maintain_list(name)
                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            if name=='Unknown':
                colortuple=(0,0,255)
            else:
                colortuple=(0,255,25)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), colortuple, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('img',frame)
        

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

@eel.expose
def StartCamera():
    global cap
    if cap==False:
        cap=True
        t1 = threading.Thread(target=camera)
        t1.daemon = True
        t1.start()
        print('End--')


@eel.expose
def maintain_list(name):
    global name_list
    if len(name_list)>=10:
        name_list.pop(-1)
    if (name not in name_list) and (name != "Unknown"):
        curr_time = datetime.now()
        curr_clock = curr_time.strftime("%H:%M") 
        name_list.insert(0,name)
        pydb.todaylist(name,curr_clock)
        eel.returned_face(name_list)
        print(name,curr_clock)



'''--------- Main ------------'''
t1 = threading.Thread(target=camera)
t1.daemon = True