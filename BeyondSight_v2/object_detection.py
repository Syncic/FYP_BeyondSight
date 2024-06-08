import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from tts import speak
from utils import get_center, get_location

class ObjectDetector:
    def __init__(self, size=(640, 360)):
        self.size = size
        self.yolo = YOLO("yolov8n.pt")
        self.previous_objects = set()

    def detect_objects(self, img):
        img_resized = cv.resize(img, self.size)
        results = self.yolo.predict(img_resized, show=True, conf=0.7)
        current_objects = {}

        for result in results:
            annotator = Annotator(img_resized)
            boxes = result.boxes

            for box in boxes:
                boxBoundary = box.xyxy[0]
                boxClass = box.cls
                objName = self.yolo.names[int(boxClass)]
                center = get_center(boxBoundary)
                location = get_location(center, self.size[0], self.size[1])

                if objName in current_objects:
                    current_objects[objName] += 1
                else:
                    current_objects[objName] = 1

        new_objects = {k: v for k, v in current_objects.items() if k not in self.previous_objects or v != self.previous_objects.get(k, 0)}

        for obj, count in new_objects.items():
            if count > 1:
                speak(f"{count} {obj}s Detected")
                location_counts = {"Right": 0, "Left": 0, "Center": 0}
                for box in boxes:
                    boxClass = box.cls
                    objName = self.yolo.names[int(boxClass)]
                    if objName == obj:
                        center = get_center(box.xyxy[0])
                        location = get_location(center, self.size[0], self.size[1])
                        location_counts[location] += 1

                for location, count in location_counts.items():
                    if count > 0:
                        speak(f"{count} at {location}")
            else:
                for box in boxes:
                    boxClass = box.cls
                    objName = self.yolo.names[int(boxClass)]
                    if objName == obj:
                        center = get_center(box.xyxy[0])
                        location = get_location(center, self.size[0], self.size[1])
                        speak(f" {objName} at {location}")

        self.previous_objects = current_objects
