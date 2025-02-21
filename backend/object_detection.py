import torch
from PIL import Image
import cv2
import numpy as np
import base64
from custom_utils import calculate_distance, infer_region

# Load YOLO model for object detection
model_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
model_yolo.conf = 0.1  # Lower confidence threshold
model_yolo.iou = 0.3   # Lower IOU threshold

def detect_objects_in_image(image_file):
    try:
        # Open and validate the image
        image = Image.open(image_file)
        image.verify()  # Verify if it's a valid image
        image = Image.open(image_file)  # Reopen for processing
        image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to OpenCV format

        results = model_yolo(image_cv2)
        objects = []
        for obj in results.xyxy[0]:
            label = model_yolo.names[int(obj[-1])]
            confidence = float(obj[4])  # Confidence score
            x_min, y_min, x_max, y_max = map(int, obj[:4])  # Bounding box coordinates

            # Draw bounding box
            cv2.rectangle(image_cv2, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(image_cv2, f"{label} {confidence:.2f}", (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            position = {
                "x_center": (x_min + x_max) // 2,
                "y_center": (y_min + y_max) // 2,
                "width": x_max - x_min,
                "height": y_max - y_min
            }
            objects.append({"name": label, "confidence": confidence, "position": position})

        # Calculate distances between objects
        for i, obj1 in enumerate(objects):
            obj1["nearby"] = []
            for j, obj2 in enumerate(objects):
                if i != j:  # Don't compare the object with itself
                    distance = calculate_distance(obj1, obj2)
                    if distance < 500:  # Arbitrary threshold for "nearby"
                        obj1["nearby"].append(obj2["name"])

        # Convert the annotated image to Base64
        _, buffer = cv2.imencode('.jpg', image_cv2)
        annotated_image_base64 = base64.b64encode(buffer).decode('utf-8')

        return objects, annotated_image_base64

    except Exception as e:
        print("Error processing image:", str(e))
        return {"error": "Error processing image", "details": str(e)}, None