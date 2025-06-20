import cv2
import numpy as np
import os
from datetime import datetime , timedelta
import face_recognition
# from PIL import ImageGrab

path = r'C:\Users\athar\Downloads\ATTENDANCE (1)\image_folder'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

import winsound  # For playing beep sound (works on Windows)
from datetime import datetime, timedelta

# Dictionary to track the last time attendance was marked
lastAttendanceTime = {}

def markAttendance(name):
    with open('attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []

        # Process the current attendance data
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        now = datetime.now()
        date = now.date()
        dtString = now.strftime('%H:%M:%S')

        # If the name is already in the list, check the last attendance time
        if name in lastAttendanceTime:
            last_time = lastAttendanceTime[name]

            # Check if the last attendance was more than an hour ago
            if datetime.now() - last_time > timedelta(hours=1):
                # Update the last attendance time and mark attendance
                lastAttendanceTime[name] = datetime.now()
                f.writelines(f'\n{name},{dtString},{date}')
                print(f"Attendance marked for {name}")  # Acknowledgment message
                winsound.Beep(1000, 500)  # Beep sound for 500ms at 1000Hz
                return True  # Attendance marked, return True
        else:
            # If the name is not in the list, mark attendance for the first time
            lastAttendanceTime[name] = datetime.now()
            f.writelines(f'\n{name},{dtString},{date}')
            print(f"Attendance marked for {name}")  # Acknowledgment message
            winsound.Beep(1000, 500)  # Beep sound for 500ms at 1000Hz
            return True  # Attendance marked, return True

    return False  # Attendance not marked, return False


# Initialize the webcam and face recognition process
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            # Check if attendance is marked and print the name only once
            if markAttendance(name):
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Webcam', img)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break
cv2.destroyAllWindows()
