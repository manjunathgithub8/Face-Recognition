import dlib
import cv2
import time

def haar(name):
    st=time.time()
    classifier = cv2.CascadeClassifier('/content/frontal_face.xml')
    img = cv2.imread(name)
    faces = classifier.detectMultiScale(img)
    ft=time.time()-st
    print('haar',ft)
    
    for result in faces:
        x, y, w, h = result
        x1, y1 = x + w, y + h
        cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)
    cv2_imshow(img)
            
def hog(name):
    st=time.time()
    detector = dlib.get_frontal_face_detector()
    img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 1)
    print('hog',time.time()-st)
    for result in faces:
        x = result.left()
        y = result.top()
        x1 = result.right()
        y1 = result.bottom()
        cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)
    cv2_imshow(img)

    

name='/content/ppl4.jpg'
hog(name)
haar(name)
