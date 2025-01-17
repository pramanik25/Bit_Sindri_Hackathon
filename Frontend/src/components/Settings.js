import React from 'react';

const Settings = () => {
    return (
        <div className="settings">
            <h2>Settings</h2>
            <label>
                Camera Resolution:
                <select>
                    <option value="640x480">640x480</option>
                    <option value="1280x720">1280x720</option>
                    <option value="1920x1080">1920x1080</option>
                </select>
            </label>
            <br />
            <label>
                Quality Threshold:
                <input type="number" min="0" max="100" defaultValue="75" />
            </label>
            <br />
            <button onClick={() => alert('Settings saved!')}>Save Settings</button>
        </div>
    );
};

export default Settings;