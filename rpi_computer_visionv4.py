import cv2
from gpiozero import LED
import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BOARD)
dirPin = 11 #2
stepPin = 13 #3
rev_buttonPin = 15 #8
for_buttonPin = 16 #9
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

# Load the pre-trained Haar Cascade classifier for face detection
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Start video capture from the default webcam (usually at index 0)
cap = cv2.VideoCapture(0)
len_faces = 0
cam_mode = False #false for disabled cam, true for enabled cam


# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

def thread_1(): #cam thread
    global cam_mode
    global len_faces
    while (True):
        
        if (cam_mode):
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Convert the frame to grayscale (Haar Cascade works on grayscale images)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            len_faces = len(faces)
            if (len_faces == 0):
                print("NO FACE FOUND")
            else:
                print("FACE FOUND!")

def thread_2(): #motor thread
    global cam_mode
    global len_faces
    while (True):
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
                microsecond_delay(500)
                GPIO.output(stepPin, GPIO.LOW)
                microsecond_delay(500)
            elif (for_buttonState == GPIO.LOW): #motor forward
                GPIO.output(dirPin, GPIO.LOW)
                GPIO.output(stepPin, GPIO.HIGH)
                microsecond_delay(500)
                GPIO.output(stepPin, GPIO.LOW)
                microsecond_delay(500)
        elif (cam_mode): #not using buttons
            if (len_faces == 0): #turn hat off
                
                GPIO.output(dirPin, GPIO.LOW)
                GPIO.output(stepPin, GPIO.HIGH)
                microsecond_delay(500)
                GPIO.output(stepPin, GPIO.LOW)
                microsecond_delay(500)
            else:
                GPIO.output(stepPin, GPIO.LOW)
                

cam_thread = threading.Thread(target=thread_1)
cam_thread.start()

motor_thread = threading.Thread(target=thread_2)
motor_thread.start()

def microsecond_delay(microseconds):
    start_time = time.perf_counter_ns()
    target_time = start_time + microseconds * 1000  # Convert microseconds to nanoseconds

    while time.perf_counter_ns() < target_time:
        pass