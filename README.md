# Blockchain E-Voting System with Face Recognition

A Python-based electronic voting prototype that combines voter face recognition with structured vote recording. The project is organized around voter registration, identity verification, voting, and result analysis.

## Project Summary

The system is designed to reduce duplicate or unauthorized voting by verifying a voter's face before a vote is recorded. Registered face data is serialized locally, while vote records are stored in `Votes.csv` for persistence and basic auditing.

> Note: despite the repository name, the current implementation described by the available project files uses local CSV/pickle storage. A blockchain ledger is not present in the current file-based workflow.

## Main Components

- `add_faces.py` — registers voters and captures face data.
- `give_vote.py` — performs face-based authentication and records votes.
- `faces_data.pkl` — serialized facial feature data.
- `names.pkl` — voter names/IDs aligned with the face data.
- `Votes.csv` — stored voting records.
- `background.png` — interface/display asset.
- `requirement.txt` — Python dependency list.

## Technology Stack

- Python 3.x
- OpenCV for webcam capture and face recognition
- NumPy for numerical processing
- CSV and Python standard-library file handling
- Pickle for local serialization

## How It Works

1. Register a voter and capture facial data with `add_faces.py`.
2. Store the generated face encodings and voter identifiers locally.
3. Start the voting workflow with `give_vote.py`.
4. Authenticate the voter using the captured face.
5. Record the vote in `Votes.csv`.
6. Use the stored records for result review or analysis.

## How to Run

### 1. Install dependencies

```bash
pip install -r requirement.txt
```

### 2. Register voters

```bash
python add_faces.py
```

Follow the prompts to capture the required face data.

### 3. Run the voting application

```bash
python give_vote.py
```

A working webcam is required for face capture and verification.

## Project Structure

```text
.
├── LICENSE
├── README.md
├── Votes.csv
├── add_faces.py
├── background.png
├── faces_data.pkl
├── give_vote.py
├── names.pkl
└── requirement.txt
```

## Key Learning Outcomes

- Computer-vision based authentication
- Python file and data handling
- Basic voter-verification workflow design
- Separation of registration, authentication, voting, and analysis stages

## Future Improvements

- Replace local files with a database
- Add a real blockchain ledger or smart-contract layer
- Encrypt sensitive voter data
- Add role-based administration and stronger audit controls
- Add automated tests and deployment documentation
