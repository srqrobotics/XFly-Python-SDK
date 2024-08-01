import commander
import communicator
import time
import keyboard
import sys
import handGesture2

commander.verifyByLED()

# keyboard.keyboardController(70,20)

# handGesture2.handGestureController(40,20)

commander.takeoff(0.6)
# communicator.packetMonitor(40)
commander.goForward(0.2, 4)
commander.goForward(0.15, 1)
commander.goForward(0.15, 3)
# communicator.packetMonitor(4)
# commander.goLeft(0.2, 5)
#time.sleep(2)
# commander.goBackward(0.15, 4)
# communicator.packetMonitor(4)
#commander.goRight(0.15, 3)
# commander.land()

sys.exit()


