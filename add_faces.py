from pathlib import Path
import pickle

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
FACES_FILE = DATA_DIR / "faces_data.pkl"
NAMES_FILE = DATA_DIR / "names.pkl"
CASCADE_FILE = DATA_DIR / "haarcascade_frontalface_default.xml"

SAMPLE_COUNT = 30   # ← reduced from 100; 30 is plenty for KNN


def main() -> None:
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        raise RuntimeError("Could not open webcam.")

    facedetect = cv2.CascadeClassifier(str(CASCADE_FILE))
    if facedetect.empty():
        raise RuntimeError(f"Could not load cascade file: {CASCADE_FILE}")

    faces_data = []
    i = 0

    name = input("Enter Your Name: ").strip()
    if not name:
        raise ValueError("Name cannot be empty.")

    print(f"Collecting {SAMPLE_COUNT} face samples — look at the camera...")

    while True:
        ret, frame = video.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            crop_img = frame[y:y + h, x:x + w, :]
            resized_img = cv2.resize(crop_img, (50, 50))
            if len(faces_data) < SAMPLE_COUNT and i % 5 == 0:
                faces_data.append(resized_img)
            i += 1

            # Progress bar drawn on frame
            progress = len(faces_data) / SAMPLE_COUNT
            bar_w = 300
            filled = int(bar_w * progress)
            cv2.rectangle(frame, (30, 30), (30 + bar_w, 58), (40, 40, 40), -1)
            cv2.rectangle(frame, (30, 30), (30 + filled, 58), (50, 200, 120), -1)
            cv2.putText(frame, f"Samples: {len(faces_data)}/{SAMPLE_COUNT}",
                        (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 200, 120), 2)

        cv2.imshow("Add Face — press Q to cancel", frame)
        k = cv2.waitKey(1)
        if k == ord('q') or len(faces_data) == SAMPLE_COUNT:
            break

    video.release()
    cv2.destroyAllWindows()

    collected = len(faces_data)
    if collected < SAMPLE_COUNT:
        print(f"Only collected {collected} samples. Try again with better lighting.")
        return

    print(f"Done! Saving {collected} samples for '{name}'...")

    faces_data = np.asarray(faces_data).reshape(SAMPLE_COUNT, -1)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save names
    if not NAMES_FILE.exists():
        names = [name] * SAMPLE_COUNT
    else:
        with open(NAMES_FILE, 'rb') as f:
            names = pickle.load(f)
        names = list(names) + [name] * SAMPLE_COUNT

    with open(NAMES_FILE, 'wb') as f:
        pickle.dump(names, f)

    # Save faces
    if not FACES_FILE.exists():
        with open(FACES_FILE, 'wb') as f:
            pickle.dump(faces_data, f)
    else:
        with open(FACES_FILE, 'rb') as f:
            existing = pickle.load(f)
        faces_data = np.append(existing, faces_data, axis=0)
        with open(FACES_FILE, 'wb') as f:
            pickle.dump(faces_data, f)

    print(f"'{name}' registered successfully!")


if __name__ == "__main__":
    main()
