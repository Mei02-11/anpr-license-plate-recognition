import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import mysql.connector
from datetime import datetime
from gpiozero import Servo, LED, Buzzer
from time import sleep

servo = Servo(17)
servo.value = None

led_waiting = LED(12)
led_waiting.off()

led_error = LED(26)
led_error.off()

def recognition(timestamp):
    conn = mysql.connector.connect(
        host="localhost",
        database="car_rental",
        user="root",
        password="YOUR_PASSWORD"
    )

    led_waiting.on()

    img = cv2.imread(f"{timestamp}.jpg")

    # Show original image
    image2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image2)
    plt.show()

    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray, cmap='gray')
    plt.show()

    # Filter
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    plt.imshow(bfilter, cmap='gray')
    plt.show()

    # Edge detection
    edged = cv2.Canny(bfilter, 30, 200)
    plt.imshow(edged, cmap='gray')
    plt.show()

    # Find contours
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    if location is None:
        print("No license plate found!")
        error_light()
        return

    # Masking
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
    plt.show()

    # Crop
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    plt.imshow(cropped_image, cmap='gray')
    plt.show()

    # OCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    if result != []:
        text = result[0][-2]

        cursor = conn.cursor()
        query = "SELECT * FROM car WHERE vehicle_plate = %s"
        cursor.execute(query, (text,))
        resultplate = cursor.fetchone()

        if resultplate:
            led_waiting.off()
            print(text)
            print("Valid user carplate")

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_query = "INSERT INTO entry_record (vehicle_plate, entry_time) VALUES (%s, %s)"
            cursor.execute(insert_query, (text, current_time))
            conn.commit()

            print("Current time inserted successfully")
            gate_open()
        else:
            error_warning()
            print(text)
            print("Invalid user carplate")

        cursor.close()
        conn.close()

        # Draw result
        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(
            img,
            text=text,
            org=(location[0][0][0], location[1][0][1] + 60),
            fontFace=font,
            fontScale=1,
            color=(0, 255, 0),
            thickness=2
        )

        res = cv2.rectangle(
            img,
            tuple(location[0][0]),
            tuple(location[2][0]),
            (0, 255, 0),
            3
        )

        plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        plt.show()

    else:
        error_light()
        print("Cannot recognize character!")

def gate_open():
    servo.value = 0.2
    sleep(1)
    servo.value = None

    sleep(10)

    servo.value = -1
    sleep(1)
    servo.value = None


def error_light():
    led_waiting.off()
    led_error.on()
    sleep(5)
    led_error.off()


def error_warning():
    led_waiting.off()
    led_error.on()
    sleep(5)
    led_error.off()