import commander
import pygame, time
from pygame.locals import *
import sys


def keyboardController(angle, yaw_rate):
    height = 0.1
    roll_set  = 0
    pitch_set = 0
    yaw_set   = 0

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Pygame Keyboard Test')
    pygame.mouse.set_visible(0)

    while(1):

        for event in pygame.event.get():
            #go forward
            if (event.type == KEYDOWN and event.key == pygame.K_UP):
                pitch_set = -angle
            if (event.type == KEYUP and event.key == pygame.K_UP):
                pitch_set = 0   

            #go backward
            if (event.type == KEYDOWN and event.key == pygame.K_DOWN):
                pitch_set = angle
            if (event.type == KEYUP and event.key == pygame.K_DOWN):
                pitch_set = 0

            #go left
            if (event.type == KEYDOWN and event.key == pygame.K_LEFT):
                roll_set = -angle
            if (event.type == KEYUP and event.key == pygame.K_LEFT):
                roll_set = 0

            #go right
            if (event.type == KEYDOWN and event.key == pygame.K_RIGHT):
                roll_set = angle
            if (event.type == KEYUP and event.key == pygame.K_RIGHT):
                roll_set = 0 

            #turn right
            if (event.type == KEYDOWN and event.key == pygame.K_d):
                yaw_set = yaw_rate
            if (event.type == KEYUP and event.key == pygame.K_d):
                yaw_set = 0

            #turn left
            if (event.type == KEYDOWN and event.key == pygame.K_a):
                yaw_set = -yaw_rate
            if (event.type == KEYUP and event.key == pygame.K_a):
                yaw_set = 0

            #go up
            if (event.type == KEYDOWN and event.key == pygame.K_w):
                height = height + 0.1
                if (height > 2.0):
                    height = 2.0
                height = round(height,1)

            #go down
            if (event.type == KEYDOWN and event.key == pygame.K_s):
                height = height - 0.1
                if (height < 0.0):
                    height = 0.0
                height = round(height,1)
            
            #exit   
            if (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        #send the command
        commander.altitudeHoldFlying(height, roll_set, pitch_set, yaw_set)
        time.sleep(0.05)
    return

