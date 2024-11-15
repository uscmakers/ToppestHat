import cv2
from gpiozero import LED
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
    if len(faces) == 0:
        led.off()
    else:
        led.on()
        print("FACE FOUND!")
    # Display the frame with the detected faces
    #cv2.imshow('Real-Time Face Detection', frame)

    # Press 'q' to exit the webcam view
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
