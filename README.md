# 📸 Attendify – Face Recognition Based Attendance System

**Attendify** is a lightweight and efficient attendance tracking system that uses **face recognition** via an **ESP32-CAM module** and Python backend. Designed for classrooms and labs, it automates the attendance process by identifying students’ faces and marking their presence in an Excel file.

---

## 🧠 Key Features

- 👁️ **Face Detection & Recognition**
  - Uses Python with OpenCV and a pre-trained LBPH face recognizer.
  - Matches live camera feed with stored facial data.
  
- 📷 **ESP32-CAM Integration**
  - Captures real-time face images wirelessly and sends them for processing.
  
- 🗃️ **MySQL Database**
  - Stores registered student face data and metadata for secure matching.
  
- ✅ **Automated Attendance Marking**
  - On successful face match, attendance is marked automatically in an Excel sheet using Pandas.
  
- 📊 **Excel Report Generation**
  - Generates daily attendance logs for easy access and records.

---

## 🛠️ Tech Stack

- **Hardware**: ESP32-CAM Module
- **Languages**: Python (OpenCV, Pandas, MySQL Connector)
- **Database**: MySQL (for image metadata and user records)
- **Output**: Excel (.xlsx) files for attendance

---

## ⚙️ Setup & Usage

1. **Connect and configure ESP32-CAM** to stream images.
2. **Run Python script** to:
   - Capture and decode image feed.
   - Detect face using OpenCV.
   - Match with stored MySQL face data.
3. **Mark attendance** in the Excel sheet if face is recognized.

---

## 📌 Future Enhancements

- Add GUI for manual overrides or reports.
- Integrate SMS/email alerts to students/parents.
- Migrate to cloud for centralized multi-classroom tracking.

---

## 📁 Project Structure

```
├── attendance.py         # Main face recognition and marking script
├── db_config.sql         # SQL schema for student face data
├── /dataset              # Stored face images for training
├── /models               # Trained recognizer model
├── attendance.xlsx       # Generated attendance sheet
└── esp32-cam-config/     # Firmware and setup guide
```

---

## 🧪 Status

✅ Functional prototype tested in real classroom conditions with over 90% recognition accuracy under controlled lighting.

---
