import cv2
import re
from Simple_facerec import SimpleFacerec

# Encode faces from a folderexit
sfr = SimpleFacerec()
sfr.load_encoding_images("C:/random_path_to_img")

# Load Camera
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        # Remove numbers from the name
        name = re.sub(r'[^a-zA-Z ]', '', name)

        cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 3)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("successfull..")
        break

cap.release()
cv2.destroyAllWindows()