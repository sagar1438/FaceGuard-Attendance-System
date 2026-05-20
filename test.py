from pathlib import Path
import csv
import os
import pickle
import time
from datetime import datetime

import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from win32com.client import Dispatch


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
ATTENDANCE_DIR = ROOT / "Attendance"
CASCADE_FILE = DATA_DIR / "haarcascade_frontalface_default.xml"
FACES_FILE = DATA_DIR / "faces_data.pkl"
NAMES_FILE = DATA_DIR / "names.pkl"


def speak(text: str) -> None:
    voice = Dispatch("SAPI.SpVoice")
    voice.Speak(text)


def main() -> None:
    ATTENDANCE_DIR.mkdir(parents=True, exist_ok=True)

    video = cv2.VideoCapture(0)
    if not video.isOpened():
        raise RuntimeError("Could not open webcam.")

    facedetect = cv2.CascadeClassifier(str(CASCADE_FILE))
    if facedetect.empty():
        raise RuntimeError(f"Could not load cascade file: {CASCADE_FILE}")

    with open(NAMES_FILE, 'rb') as w:
        labels = pickle.load(w)
    with open(FACES_FILE, 'rb') as f:
        faces = pickle.load(f)

    faces = np.asarray(faces)
    labels = list(labels)

    print('Shape of Faces matrix --> ', faces.shape)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)

    img_background = cv2.imread(str(ROOT / "background.png"))
    if img_background is None:
        raise RuntimeError("Could not load background.png")

    col_names = ['NAME', 'TIME']
    attendance = None

    while True:
        ret, frame = video.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_found = facedetect.detectMultiScale(gray, 1.3, 5)

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        attendance_file = ATTENDANCE_DIR / f"Attendance_{date}.csv"
        exist = attendance_file.is_file()

        for (x, y, w, h) in faces_found:
            crop_img = frame[y:y + h, x:x + w, :]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            output = knn.predict(resized_img)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, str(output[0]), (x, y - 15),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            attendance = [str(output[0]), str(timestamp)]

        img_background[162:162 + 480, 55:55 + 640] = frame
        cv2.imshow("Frame", img_background)
        k = cv2.waitKey(1)

        if k == ord('o') and attendance is not None:
            speak("Attendance Taken..")
            time.sleep(2)
            if exist:
                with open(attendance_file, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(attendance)
            else:
                with open(attendance_file, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(col_names)
                    writer.writerow(attendance)

        if k == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
