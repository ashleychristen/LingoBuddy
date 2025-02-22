import cv2
from deepface import DeepFace
import tensorflow as tf
print("TensorFlow version:", tf.__version__)  # Add this to verify TensorFlow is working

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

def get_emotion(frame):
    """
    Analyze a frame and return the dominant emotion detected.
    Returns None if no face/emotion is detected.
    """
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, silent=True)
        # Extract just the emotion value
        emotion = result[0]['dominant_emotion']
        print(f"{emotion}")  # Debug print to see what we're getting
        return emotion
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print for errors
        return None


def analyze_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = rgb_frame[y:y + h, x:x + w]

        # Get emotion using the new function
        emotion = get_emotion(face_roi)
        
        if emotion:
            # Draw rectangle around face and label with predicted emotion
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Real-time Emotion Detection', frame)


def get_curr_emotion():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = rgb_frame[y:y + h, x:x + w]

        # Get emotion using the new function
        emotion = get_emotion(face_roi)

        if emotion:
            return emotion
        
    return "Neutral"


def start_video():
    # Start capturing video
    global cap
    cap = cv2.VideoCapture(0)


def end_video():
    # Release the capture and close all windows
    global cap
    cap.release()
    cv2.destroyAllWindows()


def main():
    start_video()

    while True:
        analyze_frame()

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    end_video()


if __name__ == "__main__":
    main()
