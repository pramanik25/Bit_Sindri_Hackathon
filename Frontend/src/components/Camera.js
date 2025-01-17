import React, { useRef, useState } from 'react';

const Camera = () => {
    const videoRef = useRef(null);
    const [quality, setQuality] = useState('Waiting for input...');
    const [processedImage, setProcessedImage] = useState(null);
    const [isCameraOn, setIsCameraOn] = useState(false);

    const checkFoodQuality = async (imageBlob) => {
        try {
            const response = await fetch('http://localhost:5000/process_frame', {
                method: 'POST',
                body: imageBlob,
            });

            if (!response.ok) {
                throw new Error('Failed to process frame');
            }

            // Get the food quality text from response headers
            const qualityText = response.headers.get('Food-Quality');

            // Convert binary response to a Blob and create a URL
            const imageBlob = await response.blob();
            const imageUrl = URL.createObjectURL(imageBlob);

            // Update state with the image and quality text
            setProcessedImage(imageUrl);
            setQuality(qualityText || 'Unknown');
        } catch (error) {
            console.error('Error:', error);
            setQuality('Error');
        }
    };

    const startCamera = () => {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
                setIsCameraOn(true);

                videoRef.current.onloadedmetadata = () => {
                    processVideo();
                };
            })
            .catch((error) => {
                console.error('Error accessing the camera:', error);
            });
    };

    const processVideo = () => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');

        // Set canvas dimensions to match the video element
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;

        const interval = setInterval(() => {
            if (isCameraOn) {
                context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

                canvas.toBlob(async (blob) => {
                    if (blob) {
                        const formData = new FormData();
                        formData.append('frame', blob);
                        await checkFoodQuality(formData);
                    }
                }, 'image/jpeg');
            } else {
                clearInterval(interval);
            }
        }, 1000 / 24); // Capture frames at 24 FPS
    };

    const stopCamera = () => {
        setIsCameraOn(false);
        const stream = videoRef.current.srcObject;
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach((track) => track.stop());
        }
        videoRef.current.srcObject = null;
    };

    return (
        <div>
            <h1>Smart Quality Vision Testing System</h1>
            <video ref={videoRef} width="640" height="480" />
            <div>
                <button onClick={startCamera}>Start Camera</button>
                <button onClick={stopCamera}>Stop Camera</button>
            </div>
            {processedImage && <img src={processedImage} alt="Processed Frame" />}
            <p>Food Quality: {quality}</p>
        </div>
    );
};

export default Camera;
