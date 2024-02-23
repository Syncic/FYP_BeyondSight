import cv2 as cv
import numpy as np
import time
from collections import deque

import BeyondSightFunctions as bsf
import BeyondSightTextToSpeech as bss
from BeyondSightTextRecognition import pic_to_text 


# PROCESSES
def FrameRead(title, camIdx, widthFrame, heightFrame, classesOD, cameraFOV,
              configFile, weightsFile
              ):
    net = cv.dnn.readNet(configFile, weightsFile)

    cap = cv.VideoCapture(camIdx)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, widthFrame)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, heightFrame)

    centerFrameX = widthFrame / 2
    centerFrameY = heightFrame / 2

    while True:
        ret, frame = cap.read()
        cv.imshow(title, frame)
        height, width = frame.shape[:-1]

        blob = cv.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), True, False)

        net.setInput(blob)

        output_layers_names = net.getUnconnectedOutLayersNames()
        layer_outputs = net.forward(output_layers_names)

        detected_objects = []
        angle_objects = []


        for output in layer_outputs:
            for index, detection in enumerate(output):
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    label = str(classesOD[class_id])
                    confidence_percent = str(round(confidence * 100, 2))
                    detected_objects.append(label)

                    x = int(detection[0] * width)
                    x_coord = x - centerFrameX
                    y = int(detection[1] * height)
                    y_coord = y - centerFrameY
                    angle_objects.insert(index, int((cameraFOV / 2) * (x_coord / (widthFrame / 2))))

        bsf.WriteFile(f"{title}.txt", detected_objects, angle_objects)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv.waitKey(1) == ord('p'):
            pic_to_text()

    cap.release()
    cv.destroyAllWindows()


def ProcessData(distance_cameras: int, rightFile: str, leftFile: str, distFile: str):
    
    previous_detections = deque(maxlen=5)       # for TTS of new detections
    
    while True:
        try:
            detected_objects_r, angle_object_r = bsf.ReadFile(rightFile)
            detected_objects_l, angle_object_l = bsf.ReadFile(leftFile)
        except:
            detected_objects_r = []
            detected_objects_l = [] 
            angle_object_l = []
            angle_object_r = []
        
        detected_objects_both = []
        dist_objects = []
        angle_both_l = []
        angle_both_r = []
        
        
        if  len(detected_objects_r) > 0 and len(detected_objects_l) > 0:
            # proper array creation for distance calculation
            
            # creating arrays that have suitable data for further processing
            # detected_objects, angle_both_l and angle_both_r will have same indices
            for i, detection_l in enumerate(detected_objects_l):
                for j,detection_r in enumerate(detected_objects_r):     # checking if an object is detected by both cams
                    if detection_l == detection_r:
                        detected_objects_both.append(detection_l)
                        angle_both_l.append(angle_object_l[i])
                        angle_both_r.append(angle_object_r[j])
                        break
            
            # declaring new lists to use temporarily
            new_detected_objects_both = []                  
            new_angle_both_l = []
            new_angle_both_r = []
            
            j = 0
            for index, det in enumerate(detected_objects_both):
                if (index == 0) or (det != detected_objects_both[0]):
                    new_detected_objects_both.insert(j, det)
                    new_angle_both_r.insert(j, angle_both_r[index])
                    new_angle_both_l.insert(j, angle_both_l[index])
                    j += 1
                    continue
                
            
            # Updating the original lists
            detected_objects_both = new_detected_objects_both
            angle_both_l = new_angle_both_l
            angle_both_r = new_angle_both_r
            
            for index, detection in enumerate(detected_objects_both):
                dist_objects.insert(index, 
                                    bsf.calculate_distance(
                                                            index, angle_both_l, angle_both_r, 
                                                            angle_object_l, angle_object_r, 
                                                            distance_cameras
                                                            ))
                
        #setting new and old detections
        current_detections = set(detected_objects_both)
        new_detections = current_detections - set(previous_detections)
        previous_detections = detected_objects_both
        
        # speaking out text for detection
        for index, detection in enumerate(new_detections):
            direction = bsf.AngleClassification(angle_both_l[index], angle_both_r[index])
            speakText = f"{detection} detected at distance {dist_objects[index]} meters in {direction} of you"
            bss.speak(speakText)
                
        bsf.WriteFile("Distance.txt", detected_objects_both, dist_objects)
        detected_objects_both, dist_objects = bsf.ReadFile(distFile)
        print(f"Detected: {detected_objects_both}\nDistance: {dist_objects}")
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(2)