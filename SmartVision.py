from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import pytesseract
from ultralytics import YOLO
import base64

app = Flask(__name__)
CORS(app)

# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'D:/Program Files/Tesseract-OCR/tesseract.exe'  # For Windows

# Load YOLOv8 models
object_model = YOLO("yolov8s.pt")

# Load class names for object detection
object_class_names = object_model.names

# Preprocess image
def pre_proc_img(image):
    img = cv2.resize(image, (100, 100))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Draw bounding boxes and labels for objects and logos
def draw_boxes(frame, results, class_names, color):
    h, w, _ = frame.shape
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()  
        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            
            if confidence > 0.5:
                x1, y1, x2, y2 = map(int, box)
                label = f'{class_names[int(class_id)]}: {confidence:.2f}'
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
    return frame

# Perform OCR
def perform_ocr(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray).strip()
    return text

# Overlay detected text on the frame
def overlay_text(frame, text):
    
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)
    cv2.rectangle(frame, (10, 30 - text_height - baseline), (10 + text_width, 30 + baseline), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
    return frame

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        file = request.files['frame']
        npimg = np.fromfile(file, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Perform object detection
        object_results = object_model(frame)
        frame = draw_boxes(frame, object_results, object_class_names, (0, 255, 0))
        
        # Perform OCR
        text = perform_ocr(frame)
        frame = overlay_text(frame, text)

        _, img_encoded = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        response = {
            'frame': img_base64,
            'text': text
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)