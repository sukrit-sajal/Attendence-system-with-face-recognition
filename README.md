# Attendence-system-with-face-recognition
1. Introduction
The management of student attendance in educational institutions has traditionally relied on manual methods, involving cumbersome paperwork and physical signatures. These conventional systems are not only time-consuming but also prone to errors and inefficiencies. Teachers and administrative staff often face challenges in maintaining accurate records, dealing with issues such as absenteeism, and managing discrepancies in attendance logs. The manual approach also requires significant administrative effort to track and report attendance, which can detract from the focus on educational activities.

As technology continues to advance, there is a growing need to modernize traditional administrative processes. Manual attendance systems are increasingly viewed as outdated and inadequate in the context of digital transformation. The shift towards digital solutions is essential for improving accuracy, efficiency, and reliability in attendance management.

In response to these challenges, this paper proposes the implementation of a Facial Recognition Attendance System. This digital solution leverages advanced face detection and recognition technologies to automate the attendance process. By integrating a camera-based system with facial recognition algorithms, the proposed solution aims to replace traditional methods with a more accurate, efficient, and user-friendly approach. The system eliminates the need for physical paperwork and manual record-keeping, providing a streamlined process for tracking student attendance.

The primary objective of this facial recognition system is to enhance the accuracy and efficiency of attendance management. It offers a modern alternative to outdated practices by capturing and verifying student identities in real-time, thus ensuring that attendance records are accurate and up-to-date. The system also provides a digital signature to each attendance entry, which adds an additional layer of reliability and reduces the potential for fraudulent or erroneous entries. By adopting this digital solution, educational institutions can significantly reduce administrative burdens and improve the overall management of student attendance.


3. Methodology
This section outlines the methodology employed in developing the Facial Recognition Attendance System. The approach combines face detection and recognition technologies to automate the student attendance process efficiently.

3.1 System Architecture
Hardware Setup:

Camera: A standard webcam is used to capture real-time video feeds. The camera is positioned to cover the intended area where students will be detected.
Computer: A computer with sufficient processing power is required to run the face detection and recognition algorithms in real-time.
Software Components:

Programming Language: Python is used for its extensive libraries and ease of integration with computer vision and machine learning tools.
Libraries:
OpenCV: Used for face detection and image processing.
face_recognition: Utilized for face recognition and encoding.
sqlite3: Manages the SQLite database for storing attendance records.
pickle: Handles loading and saving of face encodings.
3.2 Face Detection and Recognition
Face Detection:

Haar Cascade Classifier: The system employs the Haar Cascade Classifier from OpenCV to detect faces in the video feed. The classifier is loaded from an XML file containing pre-trained data on face detection.
Region of Interest (ROI): A circular region is defined within the camera's field of view to focus face detection and reduce the computational load. Pixels outside this region are masked to improve detection accuracy.
Face Recognition:

Encoding Faces: The face_recognition library is used to extract face encodings from detected faces. Each encoding represents a unique numerical vector of facial features.
Comparing Encodings: The system compares these encodings with a database of known faces using the compare_faces method. The best match is determined based on face distances calculated by face_distance.
3.3 Attendance Management
Database Setup:

SQLite Database: The system uses an SQLite database to store student information and attendance records. A table is created for each day’s attendance, with a unique name based on the current date.
Table Structure: Each table has two columns—reg_no_last_three_digits for storing the last three digits of the student’s registration number, and status to indicate the attendance status.
Attendance Recording:

Face Recognition Results: For each detected face, the system queries the database to find the corresponding registration number. If a match is found, the attendance is recorded as "Present" in the relevant table.
Data Insertion: If the student’s registration number is not already present in the table for the current date, it is inserted with the status "Present."
3.4 Implementation Workflow
Initialization: The Haar Cascade Classifier is loaded, and face encodings are loaded from a saved file. A connection to the SQLite database is established.
Video Capture: The webcam begins capturing video frames in real-time.
Frame Processing:
Frames are converted to grayscale to facilitate face detection.
A circular mask is applied to exclude irrelevant areas.
Faces within the defined region are detected and their encodings are computed.
Face Matching and Attendance: Each detected face is compared with known encodings. If a match is found, the attendance is updated in the database.
Display and Termination: The results are displayed on the screen with bounding boxes around detected faces and names. The system continues running until manually stopped.
This methodology ensures a robust and automated approach to student attendance, leveraging modern facial recognition technology to replace outdated manual systems.

How to Run the Code
Follow the steps below to set up and run the project:

Prerequisites
Ensure you have Python installed on your system.

Setup Instructions
Create the Images Directory

Inside the project folder, create a directory named images.
Install Dependencies

Run the following command to install the required modules:
pip install -r requirements.txt
Create the Database

Execute database_creation.py to generate the database. The database will be created based on the images stored in the images directory.
To add student images manually, create a folder inside images with the format:
"studentname_registrationnumber"
Example: JohnDoe_123456
Place the student's image inside this folder.

Start the Web Server
Once the database is created, run the following command to start the web server:
#python code.py
The server should now be running and accessible via your browser.

