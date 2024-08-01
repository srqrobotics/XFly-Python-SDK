import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import commander
import sys

def handGestureController(angle, yaw_rate):
    height = 0.1
    roll_set  = 0
    pitch_set = 0
    yaw_set   = 0

    currentTime = 0
    previousTime = 0

    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands = 1)

    while True:
        ret, frame = cap.read()
        # frame = cv2.flip(frame, 1)

        # hands, frame = detector.findHands(frame, flipType = False)
        hands, frame = detector.findHands(frame)
        if not hands:
            # print("Nothing")
            cv2.putText(frame, "not detected", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            pitch_set = 0 
            roll_set = 0
            yaw_set = 0
            height = 0.0


        else:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            # print(fingers[0], fingers[1], fingers[2], fingers[3], fingers[4])

            #go up
            if(fingers[0] == 1 and 
               fingers[1] == 1 and 
               fingers[2] == 1 and 
               fingers[3] == 1 and 
               fingers[4] == 1):
                # print("go up")
                cv2.putText(frame, "go up", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                height = height + 0.1
                if (height > 2.0):
                    height = 2.0
                height = round(height,1)
                pitch_set = 0 
                roll_set = 0
                yaw_set = 0

            #go down
            if(fingers[0] == 0 and 
               fingers[1] == 0 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 0):
                # print("go down")
                cv2.putText(frame, "go down", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                height = height - 0.1
                if (height < 0.0):
                    height = 0.0
                height = round(height,1)
                pitch_set = 0 
                roll_set = 0
                yaw_set = 0

            #go forward
            if(fingers[0] == 0 and 
               fingers[1] == 1 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 0):
                # print("go forward")
                cv2.putText(frame, "go forward", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                pitch_set = -angle
                roll_set = 0
                yaw_set = 0
                
            #go backward
            if(fingers[0] == 1 and 
               fingers[1] == 1 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 0):
                # print("go backward")
                cv2.putText(frame, "go backward", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                pitch_set = angle
                roll_set = 0
                yaw_set = 0
                
            #go left
            if(fingers[0] == 1 and 
               fingers[1] == 0 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 0):
                # print("go left")
                cv2.putText(frame, "go left", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                roll_set = -angle
                pitch_set = 0 
                yaw_set = 0
                
            #go right
            if(fingers[0] == 0 and 
               fingers[1] == 0 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 1):
                # print("go right")
                cv2.putText(frame, "go right", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                roll_set = angle
                pitch_set = 0 
                yaw_set = 0
                
            #turn left
            if(fingers[0] == 1 and 
               fingers[1] == 1 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 1):
                # print("turn left")
                cv2.putText(frame, "turn left", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                yaw_set = -yaw_rate
                pitch_set = 0 
                roll_set = 0
                
            #turn right
            if(fingers[0] == 0 and 
               fingers[1] == 1 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 1):
                # print("turn right")
                cv2.putText(frame, "turn right", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                yaw_set = yaw_rate
                pitch_set = 0 
                roll_set = 0

        currentTime = time.time()
        fps = int(1/(currentTime - previousTime))
        previousTime = currentTime

        cv2.putText(frame, str(fps), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

        #send the command
        commander.altitudeHoldFlying(height, roll_set, pitch_set, yaw_set)
        print(height, roll_set, pitch_set, yaw_set)
        time.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()
    return