import face_recognition
import cv2
import os
import glob
import numpy as np
import pickle

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25

    def save_encodings(self, file_path):
        """Save the known face encodings and names to a file."""
        with open(file_path, 'wb') as f:
            pickle.dump((self.known_face_encodings, self.known_face_names), f)
        print(f"Encodings saved to {file_path}")

    def load_encodings(self, file_path):
        """Load face encodings and names from a file if it exists."""
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                self.known_face_encodings, self.known_face_names = pickle.load(f)
            print(f"Encodings loaded from {file_path}")
        else:
            print("Encoding file not found. Please ensure the file path is correct.")

    def load_encoding_images(self, images_path, encodings_file='encodings.pkl'):
        """
        Load face encoding images from a directory or from a saved encodings file.
        :param images_path: Path to the images directory.
        :param encodings_file: Path to the encodings file.
        """
        if os.path.exists(encodings_file):
            self.load_encodings(encodings_file)
        else:
            image_files = glob.glob(os.path.join(images_path, "*.*"))
            print(f"{len(image_files)} encoding images found.")

            for img_path in image_files:
                img = cv2.imread(img_path)
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                basename = os.path.basename(img_path)
                filename, _ = os.path.splitext(basename)

                encodings = face_recognition.face_encodings(rgb_img)
                if encodings:
                    img_encoding = encodings[0]
                    self.known_face_encodings.append(img_encoding)
                    self.known_face_names.append(filename)
                else:
                    print(f"No face found in {img_path}")

            print("Encoding images loaded")
            self.save_encodings(encodings_file)

    def detect_known_faces(self, frame):
        """
        Detect known faces in the given frame.
        :param frame: Frame in which to detect faces.
        :return: List of face locations and corresponding face names.
        """
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        face_locations = (np.array(face_locations) / self.frame_resizing).astype(int)
        return face_locations, face_names

# Example usage:
# sfr = SimpleFacerec()
# sfr.load_encoding_images(images_path="path/to/images")
# frame = cv2.imread("path/to/frame.jpg")
# locations, names = sfr.detect_known_faces(frame)
# print(locations, names)

