import cv2
import face_recognition
import sys
import mysql.connector
from PIL import Image
import io
import numpy as np

def load_known_faces():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="attendance_system"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, photo FROM users")
    known_face_encodings = []
    known_face_names = []
    for user_id, name, photo in cursor:
        image = Image.open(io.BytesIO(photo))
        img_np = np.array(image)
        encoding = face_recognition.face_encodings(img_np)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)
    conn.close()
    return known_face_encodings, known_face_names

def mark_attendance(name, date):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="attendance_system"
    )
    cursor = conn.cursor()
    user_id_query = "SELECT id FROM users WHERE name = %s"
    cursor.execute(user_id_query, (name,))
    user_id = cursor.fetchone()[0]
    insert_attendance_query = "INSERT INTO attendance (user_id, date, status) VALUES (%s, %s, %s)"
    cursor.execute(insert_attendance_query, (user_id, date, 'present'))
    conn.commit()
    conn.close()

def main(date):
    known_face_encodings, known_face_names = load_known_faces()

    img = cv2.imread('uploads/captured.png')
    rgb_img = img[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            mark_attendance(name, date)

        print(f"Attended: {name}")

if _name_ == "_main_":
    date = sys.argv[1]
    main(date)