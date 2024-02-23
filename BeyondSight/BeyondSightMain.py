import multiprocessing as mp

import BeyondSightFunctions as bsf
import BeyondSightProcesses as bsp


# CONSTANTS
# titles
LEFTCAM = "Left Eye"
LEFTFILE = "Left Eye.txt"
RIGHTCAM = "Right Eye"
RIGHTFILE = "Right Eye.txt"
DISTANCEFILE = "Distance.txt"


# MAIN PROG
def Main():

    # Camera and Frame Constants
    widthFrame = 640  # working at width 
    heightFrame = 480  # working at height q

    cameraFOV_r = 70
    cameraFOV_l = 52
    distance_cameras = 0.26  # 26 cm


    configFile = r"C:\Users\umerz\OneDrive\Desktop\Study\NED\Final Year Project\PythonProject"\
                 r"\.cvlib\object_detection\yolo\yolov3\yolov4_new.cfg"
    weightsFile = r"C:\Users\umerz\OneDrive\Desktop\Study\NED\Final Year Project\PythonProject"\
                  r"\.cvlib\object_detection\yolo\yolov3\yolov4.weights"
    #net = cv.dnn.readNet(configFile, weightsFile)

    classesFile = r"C:\Users\umerz\OneDrive\Desktop\Study\NED\Final Year Project\PythonProject"\
                  r"\.cvlib\object_detection\yolo\yolov3\yolov3_classes.txt"
    with open(classesFile, 'r') as f:
        classes = f.read().splitlines()



    procL = mp.Process(target=bsp.FrameRead, args=(LEFTCAM, 0, widthFrame, heightFrame,
                                               classes, cameraFOV_l,
                                               configFile, weightsFile
                                               ))
    procR = mp.Process(target=bsp.FrameRead, args=(RIGHTCAM, 1, widthFrame, heightFrame,
                                               classes, cameraFOV_r,
                                               configFile, weightsFile
                                               ))
    
    procD = mp.Process(target=bsp.ProcessData, args=(distance_cameras, RIGHTFILE, LEFTFILE, DISTANCEFILE))

    procL.start()
    procR.start()
    procD.start()
    

    procL.join()
    procR.join()
    
    procD.terminate()
    
    bsf.DeleteFile("Distance.txt")
    bsf.DeleteFile("Left Eye.txt")
    bsf.DeleteFile("Right Eye.txt")


# IF MASTER
if __name__ == "__main__":
    Main()


