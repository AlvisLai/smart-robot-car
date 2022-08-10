import cv2
import camera
from Stepper import Stepper
from turnMotor import turnMotor
import RPi.GPIO as GPIO
#import servo
import time
import threading

# initializing variables
control_pin = [5, 6, 13, 26]
turn_pin = [24,21,20,16]
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initializing camera and wheels
video = cv2.VideoCapture(0)
back_wheels = Stepper(control_pin, GPIO)
back_wheels.setup()
front_wheels = turnMotor(turn_pin, GPIO)
front_wheels.setup()

def move():
    while True:
        back_wheels.move(5)
        
def clean():
    GPIO.output(23,True)
    for pin in turn_pin:
        GPIO.output(pin,True)

if __name__ == "__main__":
    back_wheel = threading.Thread(target=move)
    back_wheel.start()
    
    while True:
        success, frame = video.read()  # getting video frame
        frame = cv2.resize(frame, (480, 240))  # resizing the frame
        curve = camera.detect_lane(frame)  # detecting the lane and curve rate

        temp = 90 + curve
        # limiting angles
        #if temp >= 150: temp = 150
        #if temp <= 0: temp = 30
        print("temp",temp)
        #check direction
        turnLeft = temp < 90
        #servo.front_wheel.angle = temp
        front_wheels.turn(turnLeft)
        time.sleep(0.01)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            clean()
            break