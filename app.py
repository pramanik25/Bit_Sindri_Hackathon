import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from keras.src.saving.saving_api import load_model
import pytesseract
from torchvision.models import mobilenet_v2
import torch

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'D:/Program Files/Tesseract-OCR/tesseract.exe'

# Load models
object_model = YOLO("yolov8s.pt")
logo_model = YOLO("logo.pt")
fresh_model = load_model('rottenvsfresh.h5')

# Load class names
object_class_names = object_model.names
logo_class_names = logo_model.names

def print_fresh(res):
    if res < 0.10:
        return "FRESH", (0, 255, 0)  # Green
    elif 0.10 <= res < 0.35:
        return "MEDIUM FRESH", (0, 255, 255)  # Yellow
    else:
        return "NOT FRESH", (0, 0, 255)  # Red

def pre_proc_img(image):
    img = cv2.resize(image, (100, 100))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def evaluate_rotten_vs_fresh(image):
    prediction = fresh_model.predict(pre_proc_img(image))
    return prediction[0][0]

def draw_boxes(frame, results, class_names, color):
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
                if class_names[int(class_id)] in ['apple', 'banana', 'orange']:
                    crop_img = frame[y1:y2, x1:x2]
                    freshness_score = evaluate_rotten_vs_fresh(crop_img)
                    freshness_label, freshness_color = print_fresh(freshness_score)
                    cv2.putText(frame, freshness_label, (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, freshness_color, 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), freshness_color, 2)
    return frame


def perform_ocr(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray).strip()
    st.write(f"Text: {text}")  # Debugging information
    return text

# Streamlit UI
st.title("EyeFicient: Smart Vision Quality Testing System")

# Add mode selection
mode = st.radio("Select Mode", ("Image Upload", "Live Camera Feed"))

if mode == "Image Upload":
    st.write("Upload an image to analyze.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Convert uploaded file to OpenCV format
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Object detection
        object_results = object_model(frame)
        frame_with_objects = draw_boxes(frame.copy(), object_results, object_class_names, (255, 255, 255))

        # Logo detection
        logo_results = logo_model(frame)
        frame_with_logos = draw_boxes(frame_with_objects.copy(), logo_results, logo_class_names, (255, 0, 0))

        # OCR
        detected_text = perform_ocr(frame_with_logos)
        st.subheader("Detected Text (OCR)")
        st.write(detected_text)

        st.image(cv2.cvtColor(frame_with_logos, cv2.COLOR_BGR2RGB), caption='Processed Image', use_container_width=True)

elif mode == "Live Camera Feed":
    st.write("Analyzing live camera feed. Press 'Q' to exit.")

    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    stframe = st.empty()  # Streamlit frame for displaying the video

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Unable to access the camera. Check your device.")
            break

        # Object detection
        object_results = object_model(frame)
        frame_with_objects = draw_boxes(frame.copy(), object_results, object_class_names, (255, 255, 255))

        # Logo detection
        logo_results = logo_model(frame)
        frame_with_logos = draw_boxes(frame_with_objects.copy(), logo_results, logo_class_names, (255, 0, 0))

        # OCR
        detected_text = perform_ocr(frame_with_logos)
        stframe.text(f"Detected Text: {detected_text}")

        # Display video frame
        stframe.image(cv2.cvtColor(frame_with_logos, cv2.COLOR_BGR2RGB), use_container_width=True)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
