const express = require('express');
const app = express();
const path = require('path');
const indexRouter = require('./routes/index');
const restRouter = require('./routes/rest');

var http = require('http');
var socketIO = require('socket.io');
var io = socketIO();
var editorSocketService = require('./services/editorSocketService')(io);

const mongoose = require('mongoose');
mongoose.connect('mongodb://parrow:Ly19930518!@ds111492.mlab.com:11492/parrow');

app.use('/api/v1',restRouter);

app.use(express.static(path.join(__dirname, '../public')));

const server = http.createServer(app);
io.attach(server);
server.listen(3000);
server.on('listening',function(){
	console.log('App listening on port 3000');
});

app.use((req,res)=>{
	res.sendFile('index.html', {root:path.join(__dirname, '../public')});
})