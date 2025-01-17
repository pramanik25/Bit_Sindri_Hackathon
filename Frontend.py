import streamlit as st
import cv2
from PIL import Image
import numpy as np

st.title("Smart Quality Vision Testing System")
st.sidebar.title("Settings")

camera = cv2.VideoCapture(0)

def check_food_quality(frame):
    quality = "Good"
    cv2.putText(frame, f"Quality: {quality}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame, quality

if st.button("Start Camera", key="start_camera"):
    st.text("Camera is running. Close Streamlit session to stop.")
    while True:
        ret, frame = camera.read()
        if not ret:
            st.error("Failed to fetch camera feed.")
            break
        
        frame = cv2.flip(frame, 1)
        frame, quality = check_food_quality(frame)
        st.write(f"Food Quality: {quality}")
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(rgb_frame, channels="RGB")

        if st.button("Stop Camera", key="stop_camera"):
            break

camera.release()
cv2.destroyAllWindows()
