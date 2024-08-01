#Packet Structure - (Mode, Parameters) 
import json

MANUAL_MODE = 1
ALT_MODE    = 2
AUTO_MODE    = 3
LAND        = 4
TELEMETRY   = 5
TUNE_PID    = 6

#################################################################################################
#Create packet for the manual mode---------------------------------------------------------------
#################################################################################################
def setManual(thrust, roll, pitch, yaw_rate):
    
    packet = {
        "M":MANUAL_MODE,
        "T":thrust,
        "R":roll,
        "P":pitch,
        "Y":yaw_rate 
        }

    packet = json.dumps(packet)
    return packet.encode()

#################################################################################################
#Create packet for the altitude hold mode--------------------------------------------------------
#################################################################################################
def altHold(height, roll, pitch, yaw_rate):
    
    packet = {
        "M":ALT_MODE,
        "H":round(height,1),
        "R":round(roll),
        "P":round(pitch),
        "Y":round(yaw_rate) 
        }

    packet = json.dumps(packet)
    return packet.encode()

#################################################################################################
#Create packet for the position hold mode--------------------------------------------------------
#################################################################################################
def posHold(height, vx, vy, yaw_rate):
    
    packet = {
        "M":AUTO_MODE,
        "H":height,
        "VX":vx,
        "VY":vy,
        "Y":yaw_rate 
        }

    packet = json.dumps(packet)
    return packet.encode()

#################################################################################################
#Create packet for the linear movements----------------------------------------------------------
#################################################################################################
def linearMovement(set_vel, duration, direction):
    
    packet = {
        "M":AUTO_MODE,
        "Command":3,
        "Dir":direction,
        "Vel":set_vel,
        "Time":duration 
        }

    packet = json.dumps(packet)
    return packet.encode()

#################################################################################################
#Create packet for the rotational movements----------------------------------------------------------
#################################################################################################
def rotationalMovement(angle, direction):
    
    packet = {
        "M":AUTO_MODE,
        "Command":4,
        "Dir":direction,
        "Angle":angle 
        }

    packet = json.dumps(packet)
    return packet.encode()

#################################################################################################
#Create packet for auto takeoff mode-------------------------------------------------------------
#################################################################################################
def takeoff(height = 0.5):
    packet = {
        "M":AUTO_MODE,
        "Command":1,
        "H": height
    }
    packet = json.dumps(packet)
    return packet.encode()

#################################################################################################
#Create packet for auto land mode----------------------------------------------------------------
#################################################################################################
def land():
    packet = {
        "M":AUTO_MODE,
        "Command":2
        }

    packet = json.dumps(packet)
    return packet.encode()

#################################################################################################
#Create packet for change PID--------------------------------------------------------------------
#################################################################################################
def setPID(ID, KP, KI, KD):
    
    packet = {
        "M":TUNE_PID,
        "ID":ID,
        "KP":KP,
        "KI":KI,
        "KD":KD 
        }

    packet = json.dumps(packet)
    return packet.encode()


