import cv2
import numpy as np
from ultralytics import YOLO
import os
import uuid
import time

from typing import Tuple

class PersonDetector:
    def __init__(self):
        start_time = time.time()
        self.net = cv2.dnn.readNet("./checkpoints/yolov3.weights", "./checkpoints/yolov3.cfg")

        # Warm up step to avoid the first inference taking longer
        # Read image
        image = cv2.imread("./assets/3.jpg")
        if image is None:
            raise ValueError("Could not load image")

        # Get image dimensions
        (height, width) = image.shape[:2]

        # Define the neural network input
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)

        # Perform forward propagation
        output_layer_names = self.net.getUnconnectedOutLayersNames()
        output_layers = self.net.forward(output_layer_names)

        # Initialize lists to hold boxes, confidences, and (if needed) class IDs
        boxes = []
        confidences = []

        # Loop over the output layers
        for output in output_layers:
            # Loop over the detections in each output
            for detection in output:
                # Extract the scores, class ID, and confidence of the current detection
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Only consider 'person' detections (class_id == 0) with high confidence
                if class_id == 0 and confidence > 0.5:
                    # Scale the bounding box coordinates back relative to the image size
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Calculate the top-left corner of the bounding box
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # Append box and confidence to the lists
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))

        # Apply Non-Maximum Suppression to filter out overlapping boxes
        indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

        # Draw bounding boxes for the detections that remain after NMS
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Save the visualized image with a unique name
            filename = f"{uuid.uuid4().hex}.jpg"
            save_path = os.path.join("static", filename)
        
        print("Init and Warm-up complete in", time.time() - start_time, "seconds")


    def detect(self, image_path: str) -> Tuple[str, int]:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")

        # Get image dimensions
        (height, width) = image.shape[:2]

        # Define the neural network input
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)

        # Perform forward propagation
        output_layer_names = self.net.getUnconnectedOutLayersNames()
        output_layers = self.net.forward(output_layer_names)

        # Initialize lists to hold boxes, confidences, and (if needed) class IDs
        boxes = []
        confidences = []

        # Loop over the output layers
        for output in output_layers:
            # Loop over the detections in each output
            for detection in output:
                # Extract the scores, class ID, and confidence of the current detection
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Only consider 'person' detections (class_id == 0) with high confidence
                if class_id == 0 and confidence > 0.5:
                    # Scale the bounding box coordinates back relative to the image size
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Calculate the top-left corner of the bounding box
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # Append box and confidence to the lists
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))

        # Apply Non-Maximum Suppression to filter out overlapping boxes
        indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

        # Draw bounding boxes for the detections that remain after NMS
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Save the visualized image with a unique name
            filename = f"{uuid.uuid4().hex}.jpg"
            save_path = os.path.join("static", filename)
            cv2.imwrite(save_path, image)

        return save_path, len(indices)
    
class PersonDetectorV2:
    def __init__(self):
        start_time = time.time()

        # Load YOLO model
        self.model = YOLO("./checkpoints/yolo11n.pt", task="detect")

        # Warm up step to avoid the first inference taking longer
        image = "./assets/3.jpg"

        # Perform inference
        results = self.model(image, classes=[0])

        # # Save the image with bounding boxes
        # results[0].save()

        # # Print the number of detected objects
        # print(len(results[0].boxes))
        
        print("Init and Warm-up complete in", time.time() - start_time, "seconds")


    def detect(self, image_path: str) -> Tuple[str, int]:
        # Read image

        # Perform inference
        results = self.model(image_path, classes=[0])
        
        filename = f"{uuid.uuid4().hex}.jpg"
        save_path = os.path.join("static", filename)

        # Save the image with bounding boxes
        results[0].save(save_path)
        

        return save_path, len(results[0].boxes)