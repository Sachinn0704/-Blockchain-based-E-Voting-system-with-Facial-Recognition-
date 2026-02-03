# Blockchain‑based E‑Voting System with Facial Recognition

A secure electronic voting system that uses **facial recognition** for voter authentication and **tamper‑resistant storage** of votes.  
This project demonstrates my focus on **backend logic, security, and identity verification**, which aligns closely with what a company like **Omnimise** cares about: trust, fraud‑prevention, and reliable user identity.

---

## 🔍 Project Overview

Traditional e‑voting systems are vulnerable to identity fraud, multiple voting, and result tampering.  
This project addresses these problems by combining:

- **Face recognition** to ensure that only legitimate voters can vote.
- A structured backend flow to **record and count votes reliably**.
- Persistent files (`faces_data.pkl`, `names.pkl`, `Votes.csv`) to maintain voter features, labels, and vote history.

The system is implemented entirely in **Python**, with a simple local UI (using OpenCV windows and a background image) and CSV‑based storage for vote counts.

---

## 🧱 Tech Stack

- **Language:** Python  
- **Computer Vision:** OpenCV  
- **Data / Storage:**  
  - `faces_data.pkl` — serialized facial feature vectors  
  - `names.pkl` — serialized voter labels/names  
  - `Votes.csv` — CSV file to store vote records / counts  
- **Other Assets:**  
  - `background.png` — UI background / overlay image  
- **Environment / Dependencies:** listed in `requirement.txt`

---

## 📁 Repository Structure

```text
.
├── LICENSE              # License file
├── README.md            # Project documentation
├── Votes.csv            # Vote records or tally data (CSV)
├── add_faces.py         # Script to register new voters and capture face data
├── give_vote.py         # Main voting script (authenticate & record votes)
├── background.png       # Background image used in the UI
├── faces_data.pkl       # Serialized facial encodings/features
├── names.pkl            # Serialized mapping of face data to voter names/IDs
├── requirement.txt      # Python dependencies (typo version)
└── requirement.txt      # Python dependencies (final version; use this one)

