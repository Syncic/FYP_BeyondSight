import os
import json
import math

PI = math.pi


# FUNCTIONS
# File Functions
def WriteFile(fileName: str, data1: list, data2: list):
    try:
        with open(fileName, 'w') as file:
            # If the file exists, replace its content with JSON representation of the two lists
            file.write(json.dumps(data1) + '\n' + json.dumps(data2))
    except FileNotFoundError:
        # If the file doesn't exist, create it and add the JSON representation of the two lists
        with open(fileName, 'w') as file:
            file.write(json.dumps(data1) + '\n' + json.dumps(data2))


def DeleteFile(fileName: str):
    try:
        # Attempt to remove the file
        os.remove(fileName)
        print(f"File {fileName} deleted successfully")
    except FileNotFoundError:
        print(f"File {fileName} not found, cannot delete.")


def ReadFile(fileName: str):
    try:
        # Attempt to open the file for reading
        with open(fileName, 'r') as file:
            # Read the content of the file and load it as a JSON object
            content = file.read()

            # Split the content into two parts using a line break
            lines = content.split('\n')

            # Load each part as a JSON object
            data1 = json.loads(lines[0])
            data2 = json.loads(lines[1])

            return data1, data2
    except FileNotFoundError:
        print(f"File {fileName} not found, cannot read.")
        return [],[]

# calculating distance
def calculate_distance(det_index : int, 
                       angle_both_l, angle_both_r, 
                       angle_object_l, angle_object_r, 
                       distance_cameras
                       ):
    
    centerpoint = distance_cameras / 2
    
    # calculating angles needed for measurement
    theta_l = math.radians(90 - angle_both_l[det_index])
    theta_r = math.radians(90 + angle_both_r[det_index])
    angle_cam_object = PI - theta_r - theta_l

    # object between the two cameras
    if (angle_object_l[det_index] >= 0 and angle_object_r[det_index] <= 0):     
        # calculating distances needed
        dist_rcam_ml = distance_cameras * math.sin(theta_l)

        try:
            dist_object_rcam = dist_rcam_ml / math.sin(angle_cam_object)
        except:
            dist_object_rcam = 0
        dist_straight_object = dist_object_rcam * math.sin(theta_r)
        dist_straight_rcam = dist_object_rcam * math.cos(theta_r)

        # distance from center of cameras to straight line of object
        dist_straight_center = centerpoint - dist_straight_rcam

        # distance to object from center point
        dist_to_object = math.sqrt(dist_straight_object ** 2 + dist_straight_center ** 2)
        dist_to_object = round(dist_to_object, 2)
        return dist_to_object
    
    # object right to both cameras
    elif (angle_object_l[det_index] >= 0 and angle_object_r[det_index] >= 0):   
        # calculating distances needed
        dist_rcam_ml = distance_cameras * math.sin(theta_l)

        try:
            dist_object_rcam = dist_rcam_ml / math.sin(angle_cam_object)
        except:
            dist_object_rcam = 0
        dist_straight_object = dist_object_rcam * math.sin(PI - theta_r)
        dist_straight_rcam = dist_object_rcam * math.cos(PI - theta_r)

        # distance from center of cameras to straight line of object
        dist_straight_center = centerpoint + dist_straight_rcam

        # distance to object from center point
        dist_to_object = math.sqrt(dist_straight_object ** 2 + dist_straight_center ** 2)
        dist_to_object = round(dist_to_object, 2)
        return dist_to_object
    
    # object left to both cameras
    elif (angle_object_l[det_index] <= 0 and angle_object_r[det_index] <= 0):   
        # calculating distances needed
        dist_lcam_mr = distance_cameras * math.sin(theta_r)

        try:
            dist_object_lcam = dist_rcam_ml / math.sin(angle_cam_object)
        except:
            dist_object_lcam = 0
        dist_straight_object = dist_object_lcam * math.sin(PI - theta_l)
        dist_straight_lcam = dist_object_lcam * math.cos(PI - theta_l)

        # distance from center of cameras to straight line of object
        dist_straight_center = centerpoint + dist_straight_lcam

        # distance to object from center point
        dist_to_object = math.sqrt(dist_straight_object ** 2 + dist_straight_center ** 2)
        dist_to_object = round(dist_to_object, 2)
        return dist_to_object
    
    # return  None if no valid case was found
    else:
        return 'undefined'