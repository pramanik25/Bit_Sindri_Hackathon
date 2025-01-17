import React from 'react';
import Camera from './components/Camera';
import Settings from './components/Settings';
import './styles.css';

function App() {
    return (
        <div className="App">
            <h1>Smart Quality Vision Testing System</h1>
            <Settings />
            <Camera />
        </div>
    );
}

export default App;