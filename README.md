# Face Recognition Attendance System

## Overview
This project implements a face recognition-based attendance system using Python. It captures video from the webcam, recognizes known faces, and marks attendance by recording the recognized names and timestamps in a text file.

## Features
- Real-time face recognition using a webcam.
- Attendance marking with timestamp recording.
- GUI interface using Tkinter.
- Saves attendance records in `attendance.txt`.

## Requirements
- Python 3.x
- OpenCV
- face_recognition
- Tkinter (comes with Python)

## Installation
1. Install required Python packages:
   ```bash
   pip install opencv-python face_recognition
   ```
   
2. Ensure Tkinter is installed (it usually comes with Python).

## Directory Structure
```
project_directory/
├── E:/MYPIC.png/     # Directory containing known images (JPEG format)
├── attendance.txt    # File where attendance records will be saved
├── attendance_system.py    # Main script file
```

## Usage
1. **Place known images**: Place the images of known individuals in the `E:/MYPIC.png/` directory. The filenames (without extensions) will be used as the names for recognition.

2. **Run the script**:
   ```bash
   python attendance_system.py
   ```

3. The application will open a window showing the video feed from the webcam. Recognized faces will be marked with a green rectangle and their names will be displayed. Unrecognized faces will be marked with a red rectangle.

4. Attendance will be recorded in the `attendance.txt` file with the format:
   ```
   Name,Timestamp
   ```

## Code Explanation

### Importing Libraries
The script starts by importing necessary libraries:
```python
import cv2
import face_recognition
import tkinter as tk
import os
from datetime import datetime
```

### Setting Up Tkinter Window
A Tkinter window is created to display the video feed:
```python
window = tk.Tk()
label = tk.Label(window)
label.pack()
button_close = tk.Button(window, text="Close", command=close_window)
button_close.pack()
```

### Loading Known Images
Images of known individuals are loaded, and their face encodings are computed:
```python
known_images_dir = "E:/MYPIC.png"
known_encodings = []
known_names = []
for filename in os.listdir(known_images_dir):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        known_image_path = os.path.join(known_images_dir, filename)
        known_image = face_recognition.load_image_file(known_image_path)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        known_encodings.append(known_encoding)
        known_names.append(filename.split(".")[0])
```

### Initializing Video Capture
The video capture from the webcam is initialized:
```python
video_capture = cv2.VideoCapture(0)
```

### Face Comparison and Attendance Marking
Functions to compare faces and mark attendance are defined:
```python
def compare_faces(known_encodings, face_encoding):
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    threshold = 0.6
    matches = [distance <= threshold for distance in distances]
    return matches

def mark_attendance(name):
    timestamp = datetime.now()
    if name not in marked_names:
        marked_names.append(name)
        with open("attendance.txt", "a") as file:
            file.write(f"{name},{timestamp}\n")
```

### Video Streaming and Face Recognition
The main function to capture video frames, recognize faces, and display the video feed in the Tkinter window:
```python
def video_stream(window):
    ret, frame = video_capture.read()
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = compare_faces(known_encodings, face_encoding)
        if any(matches):
            name = known_names[matches.index(True)]
            mark_attendance(name)
        top, right, bottom, left = face_location
        color = (0, 255, 0) if any(matches) else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        for match, name in zip(matches, known_names):
            if match:
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = tk.PhotoImage(data=cv2.imencode('.png', frame_rgb)[1].tobytes())
    label.config(image=img)
    label.image = img
    if window.winfo_exists():
        window.after(1, video_stream, window)
```

### Starting the Video Stream
The video stream is started and the Tkinter event loop is run:
```python
video_stream(window)
window.mainloop()
video_capture.release()
```

## Notes
- Adjust the `video_capture` index if using a different camera.
- Modify the threshold value in the `compare_faces` function if needed to adjust recognition accuracy.

## License
This project is licensed under the MIT License.