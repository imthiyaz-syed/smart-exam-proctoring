# 🎓 ProctoGuard: AI-Driven Secure Online Examination System With Behavioural Analysis

## 📌 Overview

ProctoGuard is an AI-powered online examination system designed to ensure exam integrity through real-time monitoring and intelligent analysis. The system uses computer vision and machine learning techniques to detect suspicious activities such as mobile phone usage, multiple persons in the frame, and abnormal behavior during exams.

It integrates **Flask (backend)**, **MySQL (database)**, and **YOLOv8 (object detection)** to provide a secure and automated proctoring solution.

---

## 🚀 Key Features

### 🔐 Authentication & User Management

* Student and Faculty Registration
* Secure Login System
* Face Recognition-based Student Verification

### 🧠 AI-Based Proctoring

* Real-time webcam monitoring
* Detection of:

  * 📱 Mobile phone usage
  * 👥 Multiple persons in frame
  * 🚫 Absence of candidate
* Head movement tracking
* Cheating flag generation

### 📝 Examination Module

* Create and manage exams
* Random question generation
* AI-based MCQ generation (Gemini API)
* Online test interface

### 📊 Results & Evaluation

* Automatic answer evaluation
* Stores results in MySQL database
* Tracks:

  * Correct answers
  * Total questions
  * Cheating status

## 🔴 Live Monitoring & Auto-Logout Feature

The system includes a **real-time monitoring mechanism** to detect suspicious head movements during the examination.

### 📡 Live Monitoring

* Continuous webcam-based monitoring is performed during the exam.
* The AI model analyzes candidate behavior in real time.
* Detects:

  * Head looking down
  * Absence of candidate
  * Abnormal posture

### ⚠️ Look-Down Detection

* If the candidate looks **down continuously for a few seconds**, it is considered suspicious behavior.
* A counter-based mechanism is used to avoid false positives.

### 🚨 Auto Logout / Exam Termination

* If the system detects prolonged suspicious behavior:

  * The exam is automatically terminated
  * The user is redirected to the home page
  * A warning message is displayed

### 🔁 Warning Mechanism

* Instead of immediate termination, the system can:

  * Issue warnings (1st and final warning)
  * Terminate exam after multiple violations

### 🏗️ System Architecture

The system follows a multi-layer architecture integrating frontend, backend, AI module, and database:

* **Frontend Layer (HTML/CSS/JS)**
  Provides user interface for students and faculty to interact with the system.

* **Backend Layer (Flask)**
  Handles authentication, exam logic, result processing, and API communication.

* **AI Proctoring Module (YOLO + OpenCV)**
  Processes webcam input to detect:

  * Mobile phone usage
  * Multiple persons
  * Head movement and behavior

* **Database Layer (MySQL)**
  Stores user data, exam questions, responses, and results.

* **External Services**

  * Email system for notifications
  * Gemini API for MCQ generation

### 🔄 Data Flow

User → Flask → AI Module → Database → Result → UI

### 🔄 System Workflow

The system follows a structured workflow during the examination process:

1. **User Login**

   * Student logs in with credentials and face verification

2. **Exam Initialization**

   * Questions are loaded from the database
   * Webcam monitoring starts

3. **Live Monitoring**

   * AI continuously analyzes webcam feed
   * Detects suspicious activities

4. **Behavior Analysis**

   * Checks for:

     * Looking down
     * Multiple persons
     * Phone usage

5. **Violation Handling**

   * Warning system activated
   * If violations exceed threshold → exam terminated

6. **Exam Submission**

   * Answers collected and evaluated

7. **Result Processing**

   * Marks calculated
   * Cheating status stored

8. **Result Display**

   * Student views results
   * Faculty can monitor reports

---

### 🎯 Decision Logic

```text
IF cheating detected:
    increase violation count

IF violation > threshold:
    terminate exam

ELSE:
    continue exam
```


### 🧠 Working Logic

```text
Start Monitoring
   ↓
Detect Head Position
   ↓
If "Down" detected repeatedly
   ↓
Increase violation counter
   ↓
If threshold exceeded
   → Terminate exam / Logout user
```

### 🎯 Purpose

This feature ensures:

* Candidates remain attentive during exams
* Prevents cheating via hidden materials (looking down)
* Enhances overall exam security

---

## ⚠️ Note

* Current implementation uses **bounding box-based estimation** for head movement.
* Accuracy depends on webcam quality and lighting conditions.
* Future improvements can include:

  * Eye gaze tracking
  * Face landmark detection (MediaPipe)
  * Advanced behavioral analysis


### 📧 Notification System

* Email alerts for registration and results
* Cheating alerts to faculty (optional)

### ⛓️ Blockchain Integration (Optional)

* Secure storage of final results using blockchain logic

---

## 🛠️ Technologies Used

| Technology            | Purpose           |
| --------------------- | ----------------- |
| Python                | Core programming  |
| Flask                 | Backend framework |
| MySQL                 | Database          |
| OpenCV                | Face detection    |
| YOLOv8 (Ultralytics)  | Object detection  |
| Scikit-learn          | Label encoding    |
| HTML, CSS, JavaScript | Frontend          |
| Gemini API            | MCQ generation    |

---

## 📂 Project Structure

```
project/
│
├── app.py                  # Main Flask application
├── yolo_webcam.py          # AI proctoring module
├── logic.py                # Blockchain / logic functions
├── templates/              # HTML templates
├── static/                 # CSS, JS, assets
├── TrainingImage/          # Face dataset
├── Trained_Model/          # Face recognition model
├── label_encoder.pkl       # Label encoder
├── requirements.txt        # Dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone https://github.com/imthiyaz-syed/smart-exam-proctoring.git
cd proctoguard
```

### 2️⃣ Create Virtual Environment

```
python -m venv env
env\Scripts\activate
```

### 3️⃣ Install Dependencies

```
python -m pip install -r requirements.txt
```

### 4️⃣ Setup Database

* Create MySQL database: `face_biometric`
* Create required tables:

  * user_registration
  * faculty_registration
  * qsn_ans
  * exam_paper
  * results
  * finalresults

### 5️⃣ Run Application

```
python app.py
```

---

## 🎯 System Workflow

1. Student logs in using credentials and face recognition
2. Exam begins with real-time webcam monitoring
3. YOLO model detects objects (phone, person, etc.)
4. System identifies suspicious behavior
5. On submission:

   * Answers are evaluated
   * Cheating status is recorded
   * Results are stored in the database

---

## 👨‍💻 Team Members

| S.No | Roll Number | Name                 |
| ---- | ----------- | -------------------- |
| 1    | 22W51A0573  | R.S. Mohammed Arshad |
| 2    | 22W51A0590  | Syed Imthiyaz        |
| 3    | 22W51A0592  | S. Sameera           |
| 4    | 22W51A0598  | V. Roshni            |

---

## 👥 Team Contributions

* **Syed Imthiyaz**
  Implemented **backend logic and database integration** using Python (Flask) and MySQL, including authentication, exam workflow, and result processing.

* **V. Roshni**
  Developed the **frontend interface** using HTML, CSS, and JavaScript, ensuring a responsive and user-friendly design.

* **S. Sameera**
  Built the **AI proctoring module**, including face detection and real-time monitoring using OpenCV and YOLO.

* **R.S. Mohammed Arshad**
  Handled **testing, integration, and documentation**, ensuring system reliability and proper validation.

---

## 🧑‍🏫 Project Supervisor

* **Mrs. P. Sumithra, M.Tech**
  Assistant Professor, Department of Computer Science & Engineering

---

## 🏫 Institution

**Viswam Engineering College**
Affiliated to JNTUA, Ananthapuramu
Department of Computer Science & Engineering

---

## ⚠️ Limitations

* Basic head movement detection (not eye tracking)
* No browser/tab switching detection
* No audio-based monitoring
* Performance depends on webcam quality

---

## 🔮 Future Enhancements

* 👁️ Eye gaze tracking
* 🌐 Browser activity monitoring
* 🔊 Audio-based cheating detection
* 📊 Real-time admin dashboard
* 🤖 Advanced behavior analysis using AI

---

## 📜 License

This project is developed for academic purposes only.

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
