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


def check_if_exists(value):
    """Return True when the voter identifier already has a recorded vote."""
    if not os.path.isfile(VOTES_FILE):
        return False

    with open(VOTES_FILE, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        return any(row and row[0] == value for row in reader)


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
            output = None

            for (x, y, w, h) in faces:
                crop_img = frame[y:y + h, x:x + w]
                resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                output = knn.predict(resized_img)
                voter_id = str(output[0])

                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
                cv2.putText(
                    frame,
                    voter_id,
                    (x, y - 15),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    1,
                )

            img_background[370:370 + 480, 225:225 + 640] = frame
            cv2.imshow("frame", img_background)
            key = cv2.waitKey(1) & 0xFF

            if output is None:
                if key == ord("q"):
                    break
                continue

            voter_id = str(output[0])
            if check_if_exists(voter_id):
                speak("YOU HAVE ALREADY VOTED")
                break

            if key in VOTE_OPTIONS:
                vote = VOTE_OPTIONS[key]
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
