module.exports = function(io) {
// collaboration sessions
// record all the participants in each session
// so that server can send changes to all participants in a session
var collaborations = {};

var socketIdTSessionId = {};
io.on('connection', (socket) => {
// get sessionId
	var sessionId = socket.handshake.query['sessionId'];
	socketIdTSessionId[socket.id] = sessionId;

	if (!(sessionId in collaborations)) {
		collaborations[sessionId] = {
			'participants': []
		};
	}
	collaborations[sessionId]['participants'].push(socket.id);
// socket event listeners
// delta is the change info
// it records the row and cloumn of the changes
	socket.on('change', delta => {
// log, easy for debuging
		console.log("change " + socketIdTSessionId[socket.id] + " " + delta);
// get session id based on socket.id
		let sessionId = socketIdTSessionId[socket.id];
		if (sessionId in collaborations) {
// get all participants on this session
			let participants = collaborations[sessionId]['participants'];
// send changes to all participants
			for (let i = 0; i < participants.length; i++) {
// skip the one who created this change
				if (socket.id != participants[i]) {
					io.to(participants[i]).emit("change", delta);
				}
			}
			} else {
				console.log("could not tie socket id to any collaboration");
			}
		})
	})
}