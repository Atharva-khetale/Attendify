import cv2
import numpy as np
import face_recognition
import mysql.connector
import os
import winsound
from datetime import datetime, timedelta
from tkinter import *
import pandas as pd
from tkinter import messagebox
from tkinter import ttk

cap=cv2.VideoCapture(0)
# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",  # Change if necessary
    user="root",  # Your MySQL username
    password="QWEASD",  # Your MySQL password
    database="attendance_system"  # Name of the database you created
)

cursor = conn.cursor()

# Initialize global variables
encodeListKnown = []
classNames = []
lastAttendanceTime = {}


# GUI Functions
def load_student_data(college, year, division):
    global encodeListKnown, classNames
    query = "SELECT name, photo_path FROM students WHERE college=%s AND year=%s AND division=%s"
    cursor.execute(query, (college, year, division))
    student_data = cursor.fetchall()
    images = []
    classNames = []

    for name, photo_path in student_data:
        # Add print to debug the path
        print(f"Attempting to load image for {name} from {photo_path}")

        # Make sure the path doesn't have extra quotes
        if '"' in photo_path:
            photo_path = photo_path.replace('"', '')

        if os.path.exists(photo_path):
            img = cv2.imread(photo_path)
            images.append(img)
            classNames.append(name)
        else:
            print(f"File not found: {photo_path}")
            messagebox.showerror("Error", f"Image file not found for {name} at {photo_path}")

    if images:
        encodeListKnown = findEncodings(images)
    else:
        messagebox.showerror("Error", "No images were loaded successfully.")


def findEncodings(images):
    encodeList = []
    for img in images:
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Only convert if img is valid
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        else:
            print("Warning: One of the images could not be loaded.")
    return encodeList


def markAttendance(name):
    showname()
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')

    path = r'C:\Users\athar\Downloads\ATTENDANCE (1)'
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []

        # Process the current attendance data
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        # If the name is already in the list, check the last attendance time
        if name in lastAttendanceTime:
            last_time = lastAttendanceTime[name]

            # Check if the last attendance was more than an hour ago
            if datetime.now() - last_time > timedelta(minutes=1):
                # Update the last attendance time and mark attendance
                lastAttendanceTime[name] = datetime.now()
                f.writelines(f'\n{name},{dtString}')
                print(f"Attendance marked for {name}")  # Acknowledgment message
                winsound.Beep(1000, 500)  # Beep sound for 500ms at 1000Hz
                return True  # Attendance marked, return True
        else:
            # If the name is not in the list, mark attendance for the first time
            lastAttendanceTime[name] = datetime.now()
            f.writelines(f'\n{name},{dtString}')
            print(f"Attendance marked for {name}")  # Acknowledgment message
            winsound.Beep(1000, 500)  # Beep sound for 500ms at 1000Hz
            return True  # Attendance marked, return True

    return False  # Attendance not marked, return False

def showname():
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
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


def start_face_recognition():

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

                if markAttendance(name):
                    showname()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()


def on_submit():
    college = college_var.get()
    year = year_var.get()
    division = div_var.get()

    if not college or not year or not division:
        messagebox.showerror("Error", "Please select all options")
        return

    load_student_data(college, year, division)
    start_face_recognition()


# GUI Design
root = Tk()
root.title("College Attendance System")
root.geometry("400x300")

college_var = StringVar()
year_var = StringVar()
div_var = StringVar()

Label(root, text="College").grid(row=0, column=0, padx=10, pady=10)
college_entry = Entry(root, textvariable=college_var)
college_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Year").grid(row=1, column=0, padx=10, pady=10)
year_entry = Entry(root, textvariable=year_var)
year_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Division").grid(row=2, column=0, padx=10, pady=10)
div_entry = Entry(root, textvariable=div_var)
div_entry.grid(row=2, column=1, padx=10, pady=10)

Button(root, text="Start Attendance", command=on_submit).grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()
