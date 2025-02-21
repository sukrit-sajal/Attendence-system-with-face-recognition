import cv2
import os
import sqlite3
import pickle
import numpy as np
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify, Response
from flask_bcrypt import Bcrypt
import face_recognition

app = Flask(__name__, static_folder='D:/projectattend/static')
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = bcrypt.generate_password_hash('admin123').decode('utf-8')

# Load the known faces and embeddings saved in the file
data = pickle.loads(open('face_enc', "rb").read())

# Find path of xml file containing haarcascade file
cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_default.xml"
# Load the haarcascade in the cascade classifier
faceCascade = cv2.CascadeClassifier(cascPathface)

# Open a connection to the SQLite database
conn = sqlite3.connect("student_database.db")
cursor = conn.cursor()

# Set the center and radius of the circular region
circle_center = (300, 200)  # Example center coordinates
circle_radius = 150

print("Streaming started")

# Open the video capture


# camera_start function to handle live streaming and attendance marking
def camera_start():
    # Open the video capture
    video_capture = cv2.VideoCapture(0)
    
    # Check if the video capture is successfully opened
    if not video_capture.isOpened():
        print("Error: Could not open video device.")
        return

    while True:
        ret, frame = video_capture.read()
        
        # Check if frame is valid
        if not ret or frame is None:
            print("Error: Failed to capture frame from camera.")
            continue  # Skip this frame and try again

        frame = cv2.flip(frame, 1) 

        # Circular masking logic
        distances = np.sqrt((np.arange(frame.shape[0])[:, None] - circle_center[1]) ** 2 +
                            (np.arange(frame.shape[1]) - circle_center[0]) ** 2)
        mask = distances > circle_radius
        frame[mask] = 0

        # Detect faces in the frame
        faces = faceCascade.detectMultiScale(frame,
                                            scaleFactor=1.1,
                                            minNeighbors=8,
                                            minSize=(60, 60),
                                            flags=cv2.CASCADE_SCALE_IMAGE)

        # Convert frame to RGB for face recognition
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            face_distances = face_recognition.face_distance(data["encodings"], encoding)
            best_match_index = np.argmin(face_distances)
            probability = 1 - face_distances[best_match_index]

            name = "Unknown"
            if matches[best_match_index] and probability >= 0.55:
                name = data["names"][best_match_index]
            names.append(name)

        # Open database connection for attendance marking
        conn = sqlite3.connect("student_database.db")
        cursor = conn.cursor()

        for ((x, y, w, h), name) in zip(faces, names):
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            current_date_column_name = f"col_{date.today().isoformat().replace('-', '_')}"
            cursor.execute(f"PRAGMA table_info(attendance)")
            columns = cursor.fetchall()
            
            # Check if column for today's date exists; add if necessary
            if not any(column[1] == current_date_column_name for column in columns):
                cursor.execute(f"ALTER TABLE attendance ADD COLUMN {current_date_column_name} TEXT DEFAULT 'Absent'")

            # Update or insert attendance
            if name != "Unknown":
                cursor.execute(f"""
                    INSERT OR REPLACE INTO attendance (reg_no_last_three_digits, {current_date_column_name})
                    VALUES (?, 'Present')
                """, (name,))
                print(f"Attendance marked/updated for {name} with probability {probability:.2f}")
            else:
                print("Face not recognized, attendance not marked.")

            # Annotate frame with name and recognition probability
            cv2.putText(frame, f"{name} ({int(probability * 100)}%)", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        
        # Draw a circle for the masking region
        cv2.circle(frame, circle_center, circle_radius, (255, 0, 0), 2)
        
        # Commit database changes
        conn.commit()
        conn.close()

        # Prepare frame for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release the video capture device after the loop ends
    video_capture.release()

    
# Flask routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and bcrypt.check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html', error=None)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('D:/projectattend/static', path)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/attendance')
def attendance():
    conn = sqlite3.connect("student_database.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(attendance)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    cursor.execute("SELECT * FROM attendance")
    record2 = cursor.fetchall()
    conn.close()
    return render_template('attendance.html', record2=record2, column_names=column_names)

@app.route('/database')
def database():
    conn = sqlite3.connect("student_database.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    record1 = cursor.fetchall()
    return render_template('database.html', record1=record1)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/video_capture')
def video_capture():
    return Response(camera_start(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/close_camera', methods=['POST'])
def close_camera():
    global stop_camera
    stop_camera = True
    return '', 204

@app.route('/student_recognized')
def student_recognized():
    return jsonify({"message": f"student recognized successfully!"})

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        print("Redirecting to login")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        reg_no = request.form['registration']
        image = request.files['image']

        first_name = name.split()[0]
        folder_name = f"{name}_{reg_no}"
        os.makedirs(os.path.join("D:/projectattend/images", folder_name), exist_ok=True)
        image_path = os.path.join("D:/projectattend/images", folder_name, f"{first_name}.jpg")
        image.save(image_path)
        reg_no_last_three_digits = reg_no[-3:]

        conn = sqlite3.connect('student_database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (reg_no_last_three_digits , name, reg_no) VALUES (?, ?, ?)",
                       (reg_no_last_three_digits, name, reg_no))
        conn.commit()
        conn.close()

        return jsonify({"message": "Student added successfully!"})

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False,host='0.0.0.0', port=5050)
    