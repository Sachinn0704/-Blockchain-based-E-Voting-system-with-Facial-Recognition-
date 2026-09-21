from sklearn.neighbors import KNeighborsClassifier

import csv
import os
import pickle
import time
from datetime import datetime

import cv2
import numpy as np
from win32com.client import Dispatch

DATA_DIR = "data"
VOTES_FILE = "Votes.csv"
CAMERA_INDEX = 0
MIN_FACE_MATCH_CONFIDENCE = 0.6
COL_NAMES = ["NAME", "VOTE", "DATE", "TIME"]
VOTE_OPTIONS = {
    ord("1"): "BJP",
    ord("2"): "CONGRESS",
    ord("3"): "AAP",
    ord("4"): "NOTA",
}


def speak(message):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(message)


def load_pickle(filename):
    with open(os.path.join(DATA_DIR, filename), "rb") as file:
        return pickle.load(file)


def is_voter_recorded(rows, voter_id):
    """Return True when a data row already contains the voter identifier."""
    return any(row and row[0] == voter_id for row in rows)


def check_if_exists(value):
    """Return True when the voter identifier already has a recorded vote.

    Existing vote files may be headerless, while newly created files include
    a header. Handle both formats so the first real vote is never skipped.
    """
    if not os.path.isfile(VOTES_FILE):
        return False

    with open(VOTES_FILE, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    if rows and rows[0] == COL_NAMES:
        rows = rows[1:]

    return is_voter_recorded(rows, value)


def record_vote(voter_id, vote):
    """Append a vote and create the CSV header when the file is new."""
    file_exists = os.path.isfile(VOTES_FILE)
    now = datetime.now()
    row = [
        voter_id,
        vote,
        now.strftime("%d-%m-%Y"),
        now.strftime("%H:%M-%S"),
    ]

    with open(VOTES_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(COL_NAMES)
        writer.writerow(row)


def load_classifier():
    labels = load_pickle("names.pkl")
    faces = np.asarray(load_pickle("faces_data.pkl"))

    if len(labels) != len(faces) or len(faces) == 0:
        raise ValueError("Face data and voter labels must contain the same non-zero number of samples.")

    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(faces, labels)
    return classifier


def predict_voter(classifier, face_image):
    """Return a voter ID only when the classifier is sufficiently confident."""
    probabilities = classifier.predict_proba(face_image)[0]
    best_index = int(np.argmax(probabilities))
    confidence = float(probabilities[best_index])

    if confidence < MIN_FACE_MATCH_CONFIDENCE:
        return None

    return str(classifier.classes_[best_index])


def get_vote_choice(key):
    """Translate a keyboard key into a configured candidate choice."""
    return VOTE_OPTIONS.get(key)


def main():
    if not os.path.isdir(DATA_DIR):
        raise FileNotFoundError("The data directory is missing. Run add_faces.py first.")

    knn = load_classifier()
    video = cv2.VideoCapture(CAMERA_INDEX)
    facedetect = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    img_background = cv2.imread("background.png")

    if not video.isOpened():
        raise RuntimeError("Unable to open the webcam.")
    if img_background is None:
        raise FileNotFoundError("background.png could not be loaded.")

    try:
        while True:
            ret, frame = video.read()
            if not ret:
                print("Unable to read a frame from the webcam.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)
            voter_id = None

            for (x, y, w, h) in faces:
                crop_img = frame[y:y + h, x:x + w]
                resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                voter_id = predict_voter(knn, resized_img)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
                cv2.putText(
                    frame,
                    voter_id or "Unknown",
                    (x, y - 15),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    1,
                )

            img_background[370:370 + 480, 225:225 + 640] = frame
            cv2.imshow("frame", img_background)
            key = cv2.waitKey(1) & 0xFF

            if voter_id is None:
                if key == ord("q"):
                    break
                continue

            if check_if_exists(voter_id):
                speak("YOU HAVE ALREADY VOTED")
                break

            vote = get_vote_choice(key)
            if vote:
                record_vote(voter_id, vote)
                speak("YOUR VOTE HAS BEEN RECORDED")
                time.sleep(2)
                speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
                break

            if key == ord("q"):
                break
    finally:
        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
