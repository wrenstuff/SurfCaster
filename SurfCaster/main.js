const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let flaskProcess;

function startFlask() {
    // Points to the Python script that starts the Flask server
    flaskProcess = spawn('python', ['app.py']);
}

app.on('ready', () => {
    startFlask();
    let win = new BrowserWindow({
        width: 800,
        height: 600,
    });
    // Point to flask server
    win.loadURL('http://localhost:5000');
});

app.on('window-all-closed', () => {
    // backend shutdown
    if (flaskProcess) flaskProcess.kill();
    app.quit();
});