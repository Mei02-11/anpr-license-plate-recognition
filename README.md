# Automatic Number Plate Recognition (ANPR)
This project implements an Automatic Number Plate Recognition (ANPR) system using OpenCV and EasyOCR.

## Features
- Detect vehicle license plates from images
- Extract plate number using EasyOCR
- Validate plate against MySQL database
- Automatically open gate using servo motor
- Motion detection using PIR sensor

## Tech Stack
- Python
- OpenCV
- EasyOCR
- Raspberry Pi (Picamera, PIR sensor, servo)
- MySQL

## System Workflow
1. Motion detected by PIR sensor
2. Camera captures image
3. Image processing using OpenCV
4. Plate recognition using OCR
5. Validation with database
6. Gate opens if valid

## Sample output
Original Photo 


## References
This project was inspired by online tutorials (https://youtu.be/NApYP_5wlKY?si=9U2-o-Kt6NUelfOO) for license plate detection using OpenCV and EasyOCR. 

The system was extended with:
- Raspberry Pi integration
- Motion sensor trigger and gate control
- Database validation using MySQL
