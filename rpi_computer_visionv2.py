import cv2
from gpiozero import LED
import RPi.GPIO as GPIO
import time
GPI.setmode(GPIO.BOARD)
dirPin = 11
stepPin = 13
rev_buttonPin = 15
for_buttonPin = 16

GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(rev_buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(for_buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
rev_buttonState = 0
for_buttonState = 0
# Load the pre-trained Haar Cascade classifier for face detection
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Start video capture from the default webcam (usually at index 0)
cap = cv2.VideoCapture(0)
led = LED(17)
led.off()
# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Convert the frame to grayscale (Haar Cascade works on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    #for (x, y, w, h) in faces:
     #   cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    rev_buttonState = GPIO.input(rev_buttonPin)
    if (rev_buttonState == GPIO.LOW): 
        GPIO.output(dirPin, GPIO.HIGH)
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(stepPin, GPIO.LOW)
        time.sleep(0.5)
    
    for_buttonState = GPIO.input(for_buttonPin)
    if (for_buttonState == GPIO.LOW):
        GPIO.output(dirPin, GPIO.LOW)
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(stepPin, GPIO.LOW)
        time.sleep(0.5)
    '''
    if len(faces) == 0:
        #led.off()
        GPIO.output(stepPin, GPIO.LOW)

    else:
        #led.on()
        GPIO.output(dirPin, GPIO.LOW)
        GPIO.output(stepPin, GPIO.LOW)
        print("FACE FOUND!")'''
    # Display the frame with the detected faces
    #cv2.imshow('Real-Time Face Detection', frame)

    # Press 'q' to exit the webcam view
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
