const electron = require('electron')
const remote = require('electron').remote
const { app, BrowserWindow, protocol, net} = electron;
const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');
const { performance } = require('perf_hooks');
const path = require('path')
const url = require('url')
var util = require('util');

app.on('ready', () => {
	initwindow();
    initticketserver();
})

var bwin

async function initwindow() {
	 bwin = new BrowserWindow({
		width: 1366,
		height: 728,
		show: false,
			webPreferences: {
			    nodeIntegration:true,
				allowRunningInsecureContent: true
			}
	})

	protocol.interceptFileProtocol('file', (request, callback) => {
    const url = request.url.substr(7)    /* all urls start with 'file://' */
    callback({ path: path.normalize(`${__dirname}/${url}`) })
  }, (err) => {
    if (err) console.error('Failed to register protocol')
  })

	bwin.loadURL(url.format({
    pathname: 'index.html',    /* Attention here: origin is path.join(__dirname, 'index.html') */
    protocol: 'file',
    slashes: true
  }))


	bwin.on('close', function(e){
		window = null;
	});

};

function callAgent(args) {
            return new Promise(resolve => {
                bwin.webContents.send('bpd',args);
                electron.ipcMain.on('bpd-reply', (event, result) => {
                    resolve(result);
                })
            });
        }

function initticketserver(){
    bankExpressApp = express();
    let port = '7000';
    let address = '209.182.216.166';

    console.log('Bank server listening on port: ' + port);
    bankExpressApp.set('port', port);
    bankExpressApp.set('address', address);
    bankExpressApp.use(bodyParser.json());
    bankExpressApp.use(bodyParser.urlencoded({ extended: true }));

    bankExpressApp.get('/akamai', async function(req, res) {
        let foo = await callAgent([url.parse(req.url,true).query.abck, url.parse(req.url,true).query.url])
        res.send(String(foo));
    });

    bankServer = bankExpressApp.listen(bankExpressApp.get('port'), bankExpressApp.get('address'));
}


