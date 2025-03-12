from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import subprocess
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the Keras model
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

# Function to get the most frequent prediction
def get_most_frequent_prediction(predictions):
    unique, counts = np.unique(predictions, return_counts=True)
    return unique[np.argmax(counts)]

# List to store predictions over 5 seconds
predictions = []

# Start time for the 5-second detection window
start_time = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Resize and preprocess the image
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Predict using the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # Append the predicted class to the list
    predictions.append(class_name)

    # Display the prediction on the frame
    cv2.putText(frame, f"Class: {class_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Confidence: {confidence_score:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Webcam", frame)

    # Check if 5 seconds have passed
    if time.time() - start_time >= 5:
        # Get the most frequent prediction over the last 5 seconds
        most_frequent_class = get_most_frequent_prediction(predictions)
        print(f"Most frequent class over 5 seconds: {most_frequent_class}")

        # Extract the numeric part of the class name
        class_number = most_frequent_class.split()[0]  # Splits "0 politic" into ["0", "politic"] and takes the first part

        # Take action based on the most frequent prediction
        if class_number == "0":  # Compare with "0"
            print("You are not allowed to enter.")
            cap.release()
            cv2.destroyAllWindows()
        elif class_number == "1":  # Compare with "1"
            print("Access granted! Launching Pygame script...")

            # Release the camera and close the OpenCV window
            cap.release()
            cv2.destroyAllWindows()

            # Launch the Pygame script
            try:
                subprocess.run(["python", "logic.py"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error launching Pygame script: {e}")

            break  # Exit the loop after launching the Pygame script

        # Reset for the next 5-second window
        predictions = []
        start_time = time.time()

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window (if not already done)
if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()