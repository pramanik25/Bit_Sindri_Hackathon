import React, { useEffect, useRef, useState } from 'react';

const Camera = () => {
    const videoRef = useRef(null);
    const [quality, setQuality] = useState('Waiting for input...');
    const [isCameraOn, setIsCameraOn] = useState(false);

    const checkFoodQuality = async (imageData) => {
        try {
            const response = await fetch('http://localhost:5000/process_frame', {
                method: 'POST',
                body: imageData,
                headers: {
                    'Content-Type': 'application/octet-stream',
                },
            });
            const data = await response.json();
            const imgBase64 = data.frame;
            const qualityText = data.text;
            setQuality(qualityText);
            return imgBase64;
        } catch (error) {
            console.error('Error connecting to the backend:', error);
            setQuality('Error');
        }
    };

    const startCamera = () => {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
                setIsCameraOn(true);
                processVideo(stream);
            })
            .catch((error) => {
                console.error('Error accessing the camera:', error);
            });
    };

    const processVideo = (stream) => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        const interval = setInterval(() => {
            if (isCameraOn) {
                context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
                canvas.toBlob(async (blob) => {
                    const imageData = new FormData();
                    imageData.append('frame', blob);
                    await checkFoodQuality(imageData);
                }, 'image/jpeg');
            } else {
                clearInterval(interval);
            }
        }, 1000 / 24); // 24 FPS
    };

    const stopCamera = () => {
        setIsCameraOn(false);
        const stream = videoRef.current.srcObject;
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
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
            <p>Food Quality: {quality}</p>
        </div>
    );
};

export default Camera;