import streamlit as st
import cv2
from PIL import Image
import numpy as np
import requests
import base64
import time

st.title("Smart Quality Vision Testing System")
st.sidebar.title("Settings")

camera = cv2.VideoCapture(0)

def check_food_quality(frame):
    _, img_encoded = cv2.imencode('.jpg', frame)
    try:
        response = requests.post('http://localhost:5000/process_frame', files={'frame': img_encoded.tobytes()})
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        img_base64 = data['frame']
        img_bytes = base64.b64decode(img_base64)
        frame = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        quality = data['text']
        return frame, quality
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the backend: {e}")
        return frame, "Error"
    except ValueError as e:
        st.error(f"Error decoding JSON: {e}")
        return frame, "Error"

def run_camera():
    frame_placeholder = st.empty()  # Placeholder for the video frame
    stop_button_key = 0  # Initialize a unique key for the stop button
    while True:
        ret, frame = camera.read()
        if not ret:
            st.error("Failed to fetch camera feed.")
            break
        
        frame = cv2.flip(frame, 1)
        frame, quality = check_food_quality(frame)
        st.write(f"Food Quality: {quality}")
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(rgb_frame, channels="RGB")

        if st.button("Stop Camera", key=f"stop_camera_{stop_button_key}"):
            break
        stop_button_key += 1  # Increment the key to ensure uniqueness

        time.sleep(1/24)  # 24 FPS
    
if st.button("Start Camera", key="start_camera"):
    st.text("Camera is running. Close Streamlit session to stop.")
    run_camera()

camera.release()
cv2.destroyAllWindows()