# Imports
import time
import importlib.util

# If script is running on the Raspberry Pi, we'll import RPi.GPIO
# If script is running on Windows for development reasons, we'll import FakeRPi.GPIO
# FakeRPi: https://github.com/sn4k3/FakeRPi
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO


### Tweakable constants
# Responsiveness - This controls a buffer time between motion control commands, when sent to the controller
delayBetweenCommands:int = 0.01 # seconds
# PWM Frequency
pwmFreq = 50 # Hz

### Global speed variables
# These store individual current speed for the motors, and they get sent to the controller when calling setSpeeds()
speedLeft:int = 0 # percent
speedRight:int = 0 # percent

### Global pin variables
# These store pin numbers for the high and low pins connected to the motors through the controller
# They get sent to the controller when calling setPins()
pinHighL = -1
pinLowL = -1
pinHighR = -1
pinLowR = -1
pinPwmL = -1
pinPwmR = -1
pwmL = None
pwmR = None

def setSpeeds():
    # Sends global speeds to motor controller
    # DOES NOT ACCEPT ARGUMETS, speed must be set using one of the motion control functions
    global speedLeft, speedRight, delayBetweenCommands
    pwmL.ChangeDutyCycle(speedLeft)
    print("[PWM] Left speed: " + speedLeft + "%")
    pwmR.ChangeDutyCycle(speedRight)
    print("[PWM] Right speed: " + speedRight + "%")
    time.sleep(delayBetweenCommands)

def stop():
    # Completly freeze in place
    global speedLeft, speedRight
    speedLeft = 0
    speedRight = 0
    setSpeeds()

def goForward(speed:int = 100):
    # Full-speed forward movement, unless a speed is given
    # Both motors will be set to the same speed
    global speedLeft, speedRight
    speedLeft = speed
    speedRight = speed
    setSpeeds()

def goBackwards(speed:int = 100):
    # Full-speed backwards movement, unless a speed is given
    # Both motors will be set to the same speed
    # Global speeds will be set to the local -speed, since we'll be going backwards
    global speedLeft, speedRight
    speedLeft = -speed
    speedRight = -speed
    setSpeeds()

def manevra(speedL:int = 0, speedR:int = 0):
    # Custom speed maneuver for both motors
    # Speeds default to 0
    # Can specify individual speeds for one or both motors, positive for forward movement and negative for backward movement
    global speedLeft, speedRight
    speedLeft = speedL
    speedRight = speedR
    setSpeeds()

def manevraL(speed:int = 0):
    # Custom speed maneuver LEFT motor
    # Speed defaults to 0
    # Adresses
    global speedLeft
    speedLeft = speed
    setSpeeds()

def setup():
    global pwmL, pwmR
    GPIO.setmode(GPIO.BOARD)
    print("GPIO pin mode was set to GPIO.BOARD")
    GPIO.setup(pinHighL, GPIO.OUT)
    print("Using pin " + str(pinHighL) + "as GPIO.OUT")
    GPIO.setup(pinLowL, GPIO.OUT)
    print("Using pin " + str(pinLowR) + "as GPIO.OUT")
    GPIO.setup(pinHighR, GPIO.OUT)
    print("Using pin " + str(pinHighR) + "as GPIO.OUT")
    GPIO.setup(pinLowR, GPIO.OUT)
    print("Using pin " + str(pinLowR) + "as GPIO.OUT")
    GPIO.setup(pinPwmL, GPIO.OUT)
    print("Using pin " + str(pinPwmL) + "as GPIO.OUT")
    GPIO.setup(pinPwmR, GPIO.OUT)
    print("Using pin " + str(pinPwmR) + "as GPIO.OUT")
    pwmL = GPIO.PWM(pinPwmL, pwmFreq)
    print("Initiated PWM instance on pin " + pinPwmL)
    pwmR = GPIO.PWM(pinPwmR, pwmFreq)
    print("Initiated PWM instance on pin " + pinPwmR)
    pwmL.start(0)
    print("[PWM] Left speed: 0%")
    pwmR.start(0)
    print("[PWM] Right speed: 0%")
    print("GPIO setup complete!")

def reset():
    GPIO.cleanup()
    setup()

#############################
### Execution begins here ###
#############################

reset() # If the process gets killed in the middle of something, motors might still be rolling, so this resets whatever the robot is doing
time.sleep(1) # Let's wait a second so the GPIO setup has some leeway to complete