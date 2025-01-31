# Face Recognition Attendance System

This project is a face recognition-based attendance system that uses real-time video capture to identify individuals and mark their attendance. It leverages the `face_recognition` library for face detection and recognition, and it provides a user-friendly interface for adding new faces to the database.

---

## Features

- **Real-Time Face Recognition**: Detects and recognizes faces in real-time using a webcam.
- **Attendance Logging**: Logs attendance in a CSV file with timestamps.
- **Dynamic Database**: Allows adding new faces to the database during runtime.
- **Text-to-Speech Feedback**: Provides audio feedback using `pyttsx3`.
- **User Interaction**: Supports voice and text input for adding new faces.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/face-recognition-attendance.git
   cd face-recognition-attendance
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the script**:
   ```bash
   python face_recognition_attendance.py
   ```

---

## How It Works

1. **Initialization**:
   - The system loads known face encodings from the `faces` directory.
   - It initializes the webcam for real-time face detection.

2. **Face Recognition**:
   - Captures video frames and detects faces.
   - Compares detected faces with known face encodings.
   - If a match is found, it logs the attendance in a CSV file.

3. **Adding New Faces**:
   - If an unknown face is detected, the system prompts the user to add the face to the database.
   - The user can provide a name, and the system captures an image of the face for future recognition.

4. **Attendance Logging**:
   - Attendance is logged in a CSV file named with the current date (e.g., `2023-10-01.csv`).
   - Each entry includes the name of the individual and the timestamp.

---

## File Structure

```
face-recognition-attendance/
├── faces/                     # Directory containing known face images
├── face_recognition_attendance.py  # Main script for face recognition and attendance logging
├── requirements.txt           # List of dependencies
└── README.md                  # Project documentation
```

---

## Dependencies

- Python 3.8+
- `opencv-python` for video capture and image processing
- `face_recognition` for face detection and recognition
- `pyttsx3` for text-to-speech feedback
- `numpy` for numerical operations
- `speech_recognition` for voice input (optional)

---

## Usage

1. **Start the System**:
   - Run the script to start the face recognition system.
   - The system will initialize and load known faces from the `faces` directory.

2. **Real-Time Recognition**:
   - The webcam will activate, and the system will start detecting and recognizing faces.
   - Recognized faces will be logged in the attendance CSV file.

3. **Adding New Faces**:
   - If an unknown face is detected, the system will prompt you to add the face to the database.
   - Follow the on-screen instructions to capture and save the new face.

4. **Exit the System**:
   - Press `q` to exit the system and close the webcam.

---

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Build and use your own face recognition attendance system with ease! 🚀📷
