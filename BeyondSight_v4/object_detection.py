import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from tts import speak
from utils import get_center, get_location

class ObjectDetector:
    def __init__(self, size=(640, 480)):
        self.size = size
        self.yolo = YOLO("yolov8n.pt")
        self.previous_objects = {}

    def detect_objects(self, img):
        img_resized = cv.resize(img, self.size)
        results = self.yolo.predict(img_resized, show=True, conf=0.7)
        current_objects = {}

        annotator = Annotator(img_resized)
        for result in results:
            boxes = result.boxes

            for box in boxes:
                boxBoundary = box.xyxy[0]
                boxClass = box.cls
                objName = self.yolo.names[int(boxClass)]
                center = get_center(boxBoundary)
                location = get_location(center, self.size[0], self.size[1])

                if objName in current_objects:
                    current_objects[objName].append(location)
                else:
                    current_objects[objName] = [location]

        new_objects = {k: v for k, v in current_objects.items() if k not in self.previous_objects or len(v) != len(self.previous_objects.get(k, []))}

        for obj, locations in new_objects.items():
            count = len(locations)
            if count > 1:
                speak(f"{count} {obj}s Detected")
                location_counts = {"Right": 0, "Left": 0, "Center": 0}
                for location in locations:
                    location_counts[location] += 1

                for location, count in location_counts.items():
                    if count > 0:
                        speak(f"{count} at {location}")
            else:
                speak(f"{obj} at {locations[0]}")

        self.previous_objects = current_objects

# Example usage:
# detector = ObjectDetector()
# frame = cv.imread('image.jpg')  # Example image path
# detector.detect_objects(frame)
