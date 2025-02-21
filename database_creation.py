import os
import cv2
from imutils import paths
import face_recognition
import pickle
import sqlite3

# get paths of each file in the folder named Images
# Images here contains my data(folders of various persons)
imagePaths = list(paths.list_images(r"D:\projectattend\images"))
knownEncodings = []
knownNames = []

# Open a connection to the SQLite database (create one if not exists)
conn = sqlite3.connect("student_database.db")
cursor = conn.cursor()

# Create a table to store student information with the last three digits of reg_no as the primary key
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        reg_no_last_three_digits TEXT PRIMARY KEY,
        name TEXT,
        reg_no TEXT UNIQUE
    )
""")

# Commit changes and close the connection
conn.commit()
conn.close()

# Loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
    # Check if the current item is a file
    if os.path.isfile(imagePath):
        # extract the person name, registration number from the image path
        path_parts = imagePath.split(os.path.sep)
        
        # Ensure that there are at least two parts after splitting
        if len(path_parts) >= 2:
            # Get the second-to-last element
            second_to_last = path_parts[-2]
            
            # Check if there is an underscore in the second-to-last element
            if "_" in second_to_last:
                try:
                    # Split the second-to-last element using underscore
                    name, reg_no = second_to_last.rsplit("_", 1)

                    # Extract the last three digits of the registration number
                    reg_no_last_three_digits = reg_no[-3:]
                except ValueError:                                                        
                    print(f"Error: Unable to split path: {imagePath}")
                    continue

                # load the input image and convert it from BGR (OpenCV ordering)
                # to dlib ordering (RGB)
                image = cv2.imread(imagePath)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Use Face_recognition to locate faces
                boxes = face_recognition.face_locations(rgb, model='hog')

                # compute the facial embedding for the face
                encodings = face_recognition.face_encodings(rgb, boxes)

                # Open a connection to the SQLite database
                conn = sqlite3.connect("student_database.db")
                cursor = conn.cursor()

                # Insert student information into the database
                cursor.execute("INSERT OR IGNORE INTO students (reg_no_last_three_digits, name, reg_no) VALUES (?, ?, ?)",
                               (reg_no_last_three_digits, name, reg_no))

                # Commit changes and close the connection
                conn.commit()
                conn.close()

                # loop over the encodings
                for encoding in encodings:
                    knownEncodings.append(encoding)
                    knownNames.append(name)

            else:
                print(f"Error: Underscore not found in path: {imagePath}")
        else:
            print(f"Error: Not enough parts in path: {imagePath}")
    else:
        print(f"Skipping directory: {imagePath}")

# save encodings along with their names in dictionary data
data = {"encodings": knownEncodings, "names": knownNames}

# use pickle to save data into a file for later use
f = open("face_enc", "wb")
f.write(pickle.dumps(data))
f.close()



