'use strict';

let { app, BrowserWindow } = require('electron');

app.on('ready', function() {
    let mainWindow = new BrowserWindow({
        webPrefrences: {
            nodeIntegration : true
    }});
    mainWindow.setMenu(null);
    mainWindow.loadURL('file://' + __dirname + '/app/index.html');
    mainWindow.webContents.openDevTools()
});