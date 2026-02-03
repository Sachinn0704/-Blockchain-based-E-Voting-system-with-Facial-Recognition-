# Blockchain‑based E‑Voting System with Facial Recognition

A secure electronic voting system that uses **facial recognition** to authenticate voters and a structured backend flow to record and count votes reliably.  
The goal is to make the voting process **more secure, transparent, and auditable** than traditional web‑based voting systems.

---

## 🔍 Project Overview

Modern e‑voting platforms face three major challenges:

1. **Identity fraud** – the same person voting multiple times or unauthorized users voting.
2. **Result tampering** – votes can be altered or deleted if stored insecurely.
3. **Lack of transparency** – it is hard to verify if results are genuine.

This project addresses these issues by:

- Using **face recognition** to verify voter identity before allowing a vote.
- Storing vote records in a persistent file (`Votes.csv`) for auditing and recounting.
- Structuring the system into clear stages: **registration**, **authentication**, **voting**, and **result analysis**.

Although this implementation uses local files (CSV and pickle), the architecture is designed so it can later be extended to use databases or blockchain ledgers.

---

## 🧱 Tech Stack

**Language**

- Python 3.x

**Core Libraries / Concepts**

- OpenCV – for capturing images from the webcam and performing facial recognition.
- NumPy – for numerical operations (used under the hood by face processing).
- CSV / standard library – for managing `Votes.csv` and file I/O.
- Pickle – for serializing and loading face encodings and associated names.

**Files & Assets**

- `add_faces.py` – Script to register voters and capture their face data.
- `give_vote.py` – Script to authenticate voters via face recognition and record their votes.
- `faces_data.pkl` – Serialized facial feature encodings of all registered voters.
- `names.pkl` – Serialized list of voter names/IDs aligned with `faces_data.pkl`.
- `Votes.csv` – Stores vote records (e.g., voter identifier, candidate, timestamp).
- `background.png` – Background image used in the user interface or display frame.
- `requirement.txt` / `requirements.txt` – Python dependency list.
- `LICENSE` – License for the project.
- `README.md` – Project documentation.

---

## 📁 Repository Structure

```text
.
├── LICENSE              # License for this project
├── README.md            # Main project documentation (this file)
├── Votes.csv            # Persistent storage of votes (CSV format)
├── add_faces.py         # Script to enroll/register new voters' faces
├── background.png       # UI background for display / overlay
├── faces_data.pkl       # Serialized facial encodings for registered voters
├── give_vote.py         # Script to authenticate voters and record votes
├── names.pkl            # Serialized names/IDs corresponding to faces_data.pkl
├── requirement.txt      # Dependency list (may be an older version)
└── requirement.txt      # Dependency list (final version; rename to requirements.txt)
