import cv2
from gpiozero import LED
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
dirPin = 11
stepPin = 13
rev_buttonPin = 15
for_buttonPin = 16
cam_buttonPin = 18 #enables/disables camera mode

GPIO.setup(stepPin, GPIO.OUT)
GPIO.output(stepPin, GPIO.LOW)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(rev_buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(for_buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cam_buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
rev_buttonState = 0
for_buttonState = 0
cam_buttonState = 0
waitSecs = 1
cam_mode = False #false for disabled cam, true for enabled cam
# Load the pre-trained Haar Cascade classifier for face detection
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Start video capture from the default webcam (usually at index 0)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    
    rev_buttonState = GPIO.input(rev_buttonPin)
    #print("revState: ",rev_buttonState,"\n")
    for_buttonState = GPIO.input(for_buttonPin)
    #print("forState: ",for_buttonState,"\n")
    cam_buttonState = GPIO.input(cam_buttonPin)
    #print("camState: ",cam_buttonState,"\n")
    if (cam_buttonState == GPIO.LOW):
        time.sleep(0.1) #debounce
        cam_mode = not(cam_mode) #flip cam mode
        print("Cam Mode:",cam_mode)
        while (cam_buttonState == GPIO.LOW):
            cam_buttonState = GPIO.input(cam_buttonPin) #wait until button stops being held
        time.sleep(0.1)

    dirbuttonPressed = rev_buttonState == GPIO.LOW or for_buttonState == GPIO.LOW

    if (dirbuttonPressed and not(cam_mode)): #if using buttons
        if (rev_buttonState == GPIO.LOW): #motor reverse
            GPIO.output(dirPin, GPIO.HIGH)
            GPIO.output(stepPin, GPIO.HIGH)
            time.sleep(0.0005)
            GPIO.output(stepPin, GPIO.LOW)
            time.sleep(0.0005)
        elif (for_buttonState == GPIO.LOW): #motor forward
            GPIO.output(dirPin, GPIO.LOW)
            GPIO.output(stepPin, GPIO.HIGH)
            time.sleep(0.0005)
            GPIO.output(stepPin, GPIO.LOW)
            time.sleep(0.0005)
    elif (cam_mode): #not using buttons
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
        if (len(faces) == 0): #turn hat off
            print("NO FACE FOUND")
            start = time.time()
            curr = time.time()
            GPIO.output(dirPin, GPIO.LOW)
            while ((curr - start) < waitSecs): #activates for 3 seconds
                GPIO.output(stepPin, GPIO.HIGH)
                time.sleep(0.0005)
                GPIO.output(stepPin, GPIO.LOW)
                time.sleep(0.0005)
                curr = time.time()
        else:
            print("FACE FOUND!")
            GPIO.output(stepPin, GPIO.LOW)
            


    # Display the frame with the detected faces
    #cv2.imshow('Real-Time Face Detection', frame)

    # Press 'q' to exit the webcam view
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
