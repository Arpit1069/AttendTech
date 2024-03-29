import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'images'
images = []
personname = []
mylist = os.listdir(path)
print(mylist)
for cu_img in mylist:
    current_Img = cv2.imread(f'{path}/{cu_img}')
    images.append(current_Img)
    personname.append(os.path.splitext(cu_img)[0])
print(personname)
    
def faceencodings(images):
    encodelist = []
    for cu_img in mylist:
       img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       encode = face_recognition.face_encodings(img)[0]
       encodelist.append(encode)
    return encodelist



print(faceencodings(images))
encodelistknown = faceencodings(images)
print("All encodings complete!!!!")

def attendance(name):
    with open('attendance.csv','r+') as f:
     myDataList = f.readlines()
     nameList = []
     for line in myDataList:
         entry = line.split(',')
         nameList.append(entry[0])

     if name not in nameList:
            time_now = datetime.now()
            tstr = time_now.strftime('%H:%M:%S')
            dstr = time_now.strftime('%d/%m%/%Y')
            f.writelines(f'{name},{tstr},{dstr}')   

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame, (0,0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(faces)
    encodesCurrentFrame = face_recognition.face_encodings(faces,facesCurrentFrame)

    for encodeface, faceloc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodelistknown, encodeface)
        faceDis = face_recognition.face_distance(encodelistknown, encodeface)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personname[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(frame, (x1,y2-35),(x2,y2),(0,255,0), cv2.filled)
            cv2.putText(frame, name,(x1 + 6, y2 - 6),cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255), 2)
            attendance(name)

    cv2.imshow("Camera", frame)
    if cv2.waitKey(10) == 13:
        break
cap.release()
cv2.destoryAllWindows()