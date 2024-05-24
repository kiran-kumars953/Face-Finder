import cv2
import face_recognition
import tkinter as tk
import os
from datetime import datetime

# Create a window using tkinter
window = tk.Tk()

# Load the known images and their encodings
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

# Initialize video capture
video_capture = cv2.VideoCapture(0)  # Change the index if using a different camera

# Create a label to display the video feed
label = tk.Label(window)
label.pack()

# Maintain a list of marked names
marked_names = []


def close_window():
    video_capture.release()
    window.destroy()


# Create a button to close the window
button_close = tk.Button(window, text="Close", command=close_window)
button_close.pack()


def compare_faces(known_encodings, face_encoding):
    # Calculate the Euclidean distance between the known encodings and current face encoding
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    threshold = 0.6

    matches = [distance <= threshold for distance in distances]
    return matches


def mark_attendance(name):
    timestamp = datetime.now()
    if name not in marked_names:  # Check if attendance is already marked
        marked_names.append(name)  # Add the name to marked names
        with open("attendance.txt", "a") as file:
            file.write(f"{name},{timestamp}\n")
        print(f"Attendance marked for {name} at {timestamp}")
    # close_window()  # Remove this line to keep the window open after marking attendance


def video_stream(window):
    ret, frame = video_capture.read()

    # Find faces and their encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Iterate over each face found in the current frame
    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare the current face encoding with the known face encodings
        matches = compare_faces(known_encodings, face_encoding)

        # Check if any of the known faces match the current face
        if any(matches):
            name = known_names[matches.index(True)]
            mark_attendance(name)

        # Draw a rectangle around the face
        top, right, bottom, left = face_location
        color = (0, 255, 0) if any(matches) else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Display the name of the matched person(s)
        for match, name in zip(matches, known_names):
            if match:
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Convert the frame to RGB for displaying in tkinter
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create an image from the frame
    img = tk.PhotoImage(data=cv2.imencode('.png', frame_rgb)[1].tobytes())

    # Update the label with the new image
    label.config(image=img)
    label.image = img

    if window.winfo_exists():
        # Schedule the next video frame
        window.after(1, video_stream, window)


# Start the video stream
video_stream(window)

# Run the tkinter event loop
window.mainloop()

# Release video capture
video_capture.release()
