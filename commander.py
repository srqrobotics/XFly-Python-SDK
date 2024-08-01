import packetGenerator as packet
import communicator
import validation
import time
#################################################################################################
#Fly in the full manual mode--------------------------------------------------------------------
#################################################################################################
def manualModeFlying(thrust, roll, pitch, yaw_rate):
    a = validation.thrust(thrust)
    b = validation.euler(roll)
    c = validation.euler(pitch)
    d = validation.euler(yaw_rate)

    dataValidated = a and b and c and d

    if (dataValidated):
        dataPacket = packet.setManual(thrust, roll, pitch, yaw_rate)
        communicator.transmit(dataPacket)
        return 1

    else:
        return 0

#################################################################################################
#Fly in the alt hold mode--------------------------------------------------------------------
#################################################################################################
def altitudeHoldFlying(set_height, roll, pitch, yaw_rate):
    a = validation.height(set_height)
    b = validation.euler(roll)
    c = validation.euler(pitch)
    d = validation.euler(yaw_rate)

    dataValidated = a and b and c and d

    if (dataValidated):
        dataPacket = packet.altHold(set_height, roll, pitch, yaw_rate)
        communicator.transmit(dataPacket)
        return 1

    else:
        return 0
    
#################################################################################################

#################################################################################################
def positionHoldFlying(set_height, roll, pitch, yaw_rate):
    a = validation.height(set_height)
    b = validation.euler(roll)
    c = validation.euler(pitch)
    d = validation.euler(yaw_rate)

    dataValidated = a and b and c and d

    if (dataValidated):
        dataPacket = packet.posHold(set_height, roll, pitch, yaw_rate)
        communicator.transmit(dataPacket)
        return 1

    else:
        return 0

#################################################################################################
#Automatic Takeoff-------------------------------------------------------------------------------
#################################################################################################
def takeoff(set_height = 0.5):
    a = validation.height(set_height)

    dataValidated = a

    if (dataValidated):
        dataPacket = packet.takeoff(set_height)
        communicator.transmit(dataPacket)
        confirmed = communicator.getMsgConfirmation()
        if (confirmed):
            print("Takeoff Initiated")
        #confirmed = communicator.getActionConfirmation()

        if (confirmed):
            print("Takeoff Successful")
            return 1
        else:
            print("Takeoff Failed!")
            return 0

    else:
        return 0

#################################################################################################
#Set Height-------------------------------------------------------------------------------
#################################################################################################
def setHeight(set_height = 0.5):
    a = validation.height(set_height)

    dataValidated = a

    if (dataValidated):
        dataPacket = packet.takeoff(set_height)
        communicator.transmit(dataPacket)
        return 1
        #confirmed = communicator.getMsgConfirmation()
        #if (confirmed):
        #    print("Height Adjust Initiated")
        #confirmed = communicator.getActionConfirmation()

        #if (confirmed):
        #    print("Height Adjust Successful")
        #    return 1
        #else:
        #    print("Height Adjust Failed!")
        #    return 0
    else:
        return 0

#################################################################################################
#Automatic Land----------------------------------------------------------------------------------
#################################################################################################
def land():
    dataPacket = packet.land()
    communicator.transmit(dataPacket)
    confirmed = communicator.getMsgConfirmation()
    if (confirmed):
        print("Land Initiated")
    confirmed = communicator.getActionConfirmation()

    if (confirmed):
        print("Land Successful")
        return 1
    else:
        print("Land Failed!")
        return 0    

#################################################################################################
#Linear movements--------------------------------------------------------------------------------
#################################################################################################
def goForward(set_vel = 0.2, set_time = 1.0):
    movementConstructor(set_vel, set_time, 'F')

def goBackward(set_vel = 0.2, set_time = 1.0):
    movementConstructor(set_vel, set_time, 'B')

def goLeft(set_vel = 0.2, set_time = 1.0):
    movementConstructor(set_vel, set_time, 'L')

def goRight(set_vel = 0.2, set_time = 1.0):
    movementConstructor(set_vel, set_time, 'R')

def movementConstructor(set_vel, set_time, direction):
    a = validation.movementVelocity(set_vel)

    dataValidated = a

    if (dataValidated):
        if   (set_vel  <  0.0):   set_vel = 0.0
        elif (set_vel  >  0.5):   set_vel = 0.5
        if   (set_time <  0.0):  set_time = 0.0
        elif (set_time > 10.0):  set_time = 10.0

        dataPacket = packet.linearMovement(set_vel, set_time, direction)
        communicator.transmit(dataPacket)
        #confirmed = communicator.getMsgConfirmation()
        #if (confirmed):
        #    print("Movement Initiated")
        #confirmed = getTimeConfirmation(set_time)

        #if (confirmed):
        #    print("Movement Successful")
        #    return 1
        #else:
        #    print("Movement Failed!")
        #    return 0

    else:
        return 0

#################################################################################################
#Rotational Movement--------------------------------------------------------------------------------
#################################################################################################
def rotateLeft(angle):
    rotationConstructor(angle, 'L')

def rotateRight(angle):
    rotationConstructor(angle, 'R')

def rotationConstructor(angle, direction):
    a = True

    dataValidated = a

    if (dataValidated):
        dataPacket = packet.rotationalMovement(angle, direction)
        communicator.transmit(dataPacket)
        #confirmed = communicator.getMsgConfirmation()
        #if (confirmed):
        #    print("Movement Initiated")
        confirmed = getTimeConfirmation()

        if (confirmed):
            print("Movement Successful")
            return 1
        else:
            print("Movement Failed!")
            return 0

    else:
        return 0

#################################################################################################
#Set PID values----------------------------------------------------------------------------------
#################################################################################################
def setPID(type, KP, KI, KD):
    a = validation.positiveFloat(KP)
    b = validation.positiveFloat(KI)
    c = validation.positiveFloat(KD)
    d = validation.pidType(type)
    dataValidated = a and b and c and d

    if (dataValidated):
        dataPacket = packet.setPID(type, KP, KI, KD)
        communicator.transmit(dataPacket)
        
        confirmed = communicator.setMsgConfirmation()
        #confirmed = 1
        if (confirmed):
            print("PID Set Successfull")
            return 1
        else:
            print("PID Set Failed")
            return 0

    else:
        return 0


def getTimeConfirmation(task_time = 3.0):
    start_time = time.time()
    while(time.time() - start_time < task_time):
        a = 1
    return 1





def verifyByLED():
    dataPacket = packet.verifyByLED()
    communicator.transmit(dataPacket)
    return 1