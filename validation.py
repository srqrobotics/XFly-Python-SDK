PID_TYPES = {'Roll', 'Pitch', 'Yaw', 'YawRate', 'AltHoldRate', 'AltHold'}

def thrust(thrust):
    if (type(thrust) == int):
        if (thrust<0 or thrust>100):
            print("Thrust should be between 0-100")
            return 0
        else:
            return 1
    else:
        print ("Thrust should be an Integer")
        return 0


def euler(angle):
    if (type(angle) == int):
        if (angle<-80 or angle>80):
            print("Roll and Pitch should be between -30 and +30")
            return 0
        else:
            return 1
    else:
        print ("Roll and Pitch should be Integers")
        return 0


def yawRate(yawRate):
    if (type(yawRate) == int):
        if (yawRate<-100 or yawRate>100):
            print("Yaw Rate should be between -100 and 100")
            return 0
        else:
            return 1
    else:
        print ("Yaw Rate should be an Integer")
        return 0


def height(height):
    if (type(height) == float):
        if (height<0.0 or height>2.0):
            print("Height should be between 0.1-1.5")
            return 0
        else:
            return 1
    else:
        print ("Height should be a Float")
        return 0


def positiveFloat(number):
    if (type(number) == float and number > 0.0):
        return 1
    else:
        print("PID value must be a positive float")
        return 0

def pidType(type):
    if (type in PID_TYPES):
        return 1
    else:
        print("Invalid PID Type")
        return 0

def movementVelocity(vel):
    if (type(vel) == float or type(vel) == int):
        return 1
    else:
        print("Velocity value should be a number")
        return 0