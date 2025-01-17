# Bit_Sindri_Hackathon
# Smart Quality Vision Testing System

This project is a Smart Quality Vision Testing System that uses computer vision and OCR to analyze video frames from a camera feed. The system consists of a frontend built with Streamlit and a backend built with Flask.

## Features

- Real-time video feed from a camera
- Object detection using YOLOv8
- Optical Character Recognition (OCR) using Tesseract
- Display of processed video frames with detected objects and text

## Requirements

- Python 3.7+
- Streamlit
- OpenCV
- Flask
- Flask-CORS
- Requests
- PIL (Pillow)
- NumPy
- Tesseract-OCR
- YOLOv8 (Ultralytics)

## Installation

1. Clone the repository:

   ```sh
   git clone 

   ```markdown
# SmartVision Project Setup Guide

## Steps to Set Up the Project

### 1. Create and Activate a Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Install the Required Packages
```bash
pip install -r requirements.txt
```

### 3. Download and Install Tesseract-OCR
- Download Tesseract-OCR from [here](https://github.com/tesseract-ocr/tesseract).
- Follow the installation instructions for your operating system.

### 4. Update the Tesseract Executable Path
- Open `SmartVision.py`.
- Update the `tesseract_cmd` variable with the path to the Tesseract executable.
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'PATH_TO_TESSERACT_EXECUTABLE'
  ```
  Replace `PATH_TO_TESSERACT_EXECUTABLE` with the actual path where Tesseract is installed.

### 5. Download YOLOv8 Model Weights
- Download the YOLOv8 model weights from the [official repository](https://github.com/ultralytics/ultralytics).
- Place the downloaded weights file in the project directory.

---

## Usage Instructions

### 1. Start the Flask Backend
```bash
python app.py
```

### 2. Start the Streamlit Frontend
```bash
streamlit run frontend.py
```

### 3. Access the Application
- Open your web browser and navigate to [http://localhost:8501](http://localhost:8501) to use the Streamlit app.

---

## File Structure
```
SmartVision/
│
├── app.py                   # Flask backend
├── frontend.py              # Streamlit frontend
├── requirements.txt         # Required Python packages
├── SmartVision.py           # Main application logic
├── yolov8_weights.pt        # YOLOv8 model weights
├── static/                  # Static files (CSS, JS, images, etc.)
├── templates/               # HTML templates for the Flask app
└── README.md                # Project documentation
```
```