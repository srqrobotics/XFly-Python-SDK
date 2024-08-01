import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import commander
import sys
import numpy as np

def handGestureController(angle, yaw_rate):
    frame_width = 1280
    frame_height = 720

    line1_start_point = (0, 0)
    line1_end_point = (frame_width, frame_height)

    line2_start_point = (0, frame_height)
    line2_end_point = (frame_width, 0)

    dash_length = 20
    gap_length = 10

    slope1 = (line1_end_point[1] - line1_start_point[1]) / (line1_end_point[0] - line1_start_point[0])
    intercept1 = line1_start_point[1] - slope1 * line1_start_point[0]

    slope2 = (line2_end_point[1] - line2_start_point[1]) / (line2_end_point[0] - line2_start_point[0])
    intercept2 = line2_start_point[1] - slope2 * line2_start_point[0]

    hand_on_section = 0

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    detector = HandDetector(maxHands = 1)

    # drone parameters
    height = 0.1
    roll_set  = 0
    pitch_set = 0
    yaw_set   = 0

    currentTime = 0
    previousTime = 0



    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Draw diagonal lines
        for i in range(0, int(np.sqrt((line1_end_point[0] - line1_start_point[0])**2 + (line1_end_point[1] - line1_start_point[1])**2)), dash_length + gap_length):
            x1 = int(line1_start_point[0] + i * np.cos(np.arctan(slope1)))
            y1 = int(line1_start_point[1] + i * np.sin(np.arctan(slope1)))
            x2 = int(line1_start_point[0] + (i + dash_length) * np.cos(np.arctan(slope1)))
            y2 = int(line1_start_point[1] + (i + dash_length) * np.sin(np.arctan(slope1)))
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

        
        for i in range(0, int(np.sqrt((line2_end_point[0] - line2_start_point[0])**2 + (line2_end_point[1] - line2_start_point[1])**2)), dash_length + gap_length):
            x1 = int(line2_start_point[0] + i * np.cos(np.arctan(slope2)))
            y1 = int(line2_start_point[1] + i * np.sin(np.arctan(slope2)))
            x2 = int(line2_start_point[0] + (i + dash_length) * np.cos(np.arctan(slope2)))
            y2 = int(line2_start_point[1] + (i + dash_length) * np.sin(np.arctan(slope2)))
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

        # hands, frame = detector.findHands(frame, flipType = False)
        hands, frame = detector.findHands(frame)
        if not hands:
            # print("Nothing")
            cv2.putText(frame, "not detected", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            pitch_set = 0 
            roll_set = 0
            yaw_set = 0
            height = 0.1
            
        else:           
            # first hand
            hand = hands[0]

            # determine hand position on frame window
            handCenter = hand['center']
            line1_y = slope1 * handCenter[0] + intercept1
            line2_y = slope2 * handCenter[0] + intercept2

            if handCenter[1] < line1_y and handCenter[1] < line2_y:
                hand_on_section = 1
            elif handCenter[1] > line1_y and handCenter[1] > line2_y:                
                hand_on_section = 2
            elif handCenter[1] > line1_y and handCenter[1] < line2_y:
                hand_on_section = 3
            elif handCenter[1] < line1_y and handCenter[1] > line2_y:
                hand_on_section = 4
            else:
                hand_on_section = 0
            # print(hand_on_section)

            # detect finger positions
            fingers = detector.fingersUp(hand)
            # print(fingers[0], fingers[1], fingers[2], fingers[3], fingers[4])

            #go up
            if(fingers[0] == 1 and 
               fingers[1] == 0 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 0):
                # print("go up")
                cv2.putText(frame, "go up", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                # height = height + 0.1
                height = 0.5
                if (height > 1.0):
                    height = 1.0
                height = round(height,1)
                pitch_set = 0 
                roll_set = 0
                yaw_set = 0

            #go down
            if(fingers[0] == 0 and 
               fingers[1] == 0 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 1):
                # print("go down")
                cv2.putText(frame, "go down", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                # height = height - 0.1
                height = 0.1
                if (height < 0.0):
                    height = 0.0
                height = round(height,1)
                pitch_set = 0 
                roll_set = 0
                yaw_set = 0

            #go down off
            if(fingers[0] == 1 and 
               fingers[1] == 0 and 
               fingers[2] == 0 and 
               fingers[3] == 0 and 
               fingers[4] == 1):
                # print("go down")
                cv2.putText(frame, "go down off", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                # height = height - 0.1
                height = 0.0
                if (height < 0.0):
                    height = 0.0
                height = round(height,1)
                pitch_set = 0 
                roll_set = 0
                yaw_set = 0

            #go forward
            if(fingers[0] == 1 and 
               fingers[1] == 1 and 
               fingers[2] == 1 and 
               fingers[3] == 1 and 
               fingers[4] == 1 and
               hand_on_section == 1):
                # print("go forward")
                cv2.putText(frame, "go forward", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                pitch_set = -angle
                roll_set = 0
                yaw_set = 0
                
            #go backward
            if(fingers[0] == 1 and 
               fingers[1] == 1 and 
               fingers[2] == 1 and 
               fingers[3] == 1 and 
               fingers[4] == 1 and
               hand_on_section == 2):
                # print("go backward")
                cv2.putText(frame, "go backward", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                pitch_set = angle
                roll_set = 0
                yaw_set = 0
                
            #go left
            if(fingers[0] == 1 and 
               fingers[1] == 1 and 
               fingers[2] == 1 and 
               fingers[3] == 1 and 
               fingers[4] == 1 and
               hand_on_section == 3):
                # print("go left")
                cv2.putText(frame, "go left", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                roll_set = -angle
                pitch_set = 0 
                yaw_set = 0
                
            #go right
            if(fingers[0] == 1 and 
               fingers[1] == 1 and 
               fingers[2] == 1 and 
               fingers[3] == 1 and 
               fingers[4] == 1 and
               hand_on_section == 4):
                # print("go right")
                cv2.putText(frame, "go right", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                roll_set = angle
                pitch_set = 0 
                yaw_set = 0

        currentTime = time.time()
        fps = int(1/(currentTime - previousTime))
        previousTime = currentTime

        cv2.putText(frame, str(fps), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

        #send the command
        commander.altitudeHoldFlying(height, roll_set, pitch_set, yaw_set)
        # commander.positionHoldFlying(height, roll_set, pitch_set, yaw_set)
        print(height, roll_set, pitch_set, yaw_set)
        time.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()
    return