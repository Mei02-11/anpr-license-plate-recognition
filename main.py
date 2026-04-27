from picamera2 import Picamera2, Preview
from time import sleep
from gpiozero import MotionSensor, LED, Servo
from datetime import datetime
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import mysql.connector
import recognition

# Sensors and camera setup
pir = MotionSensor(4)
led = LED(25)
led.off()

camera = Picamera2()
camera_config = camera.create_still_configuration(
    main={"size": (1920, 1080)},
    lores={"size": (640, 480)},
    display="lores"
)
camera.configure(camera_config)
camera.start()

def capture():
    led.on()
    save_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    sleep(2)
    led.off()

    camera.capture_file(f"{save_timestamp}.jpg")
    p1_e2_withTest3.recognition(save_timestamp)

# Main loop
while True:
    pir.wait_for_motion()
    capture()