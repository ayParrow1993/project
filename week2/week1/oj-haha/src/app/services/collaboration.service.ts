import { Injectable } from '@angular/core';

declare var io: any;

@Injectable({
  providedIn: 'root'
})
export class CollaborationService {
	collaborationSocket: any;
  constructor() { }
  init(editor: any, sessionId: string): void {
	this.collaborationSocket = io(window.location.origin, {query:'sessionId=' + sessionId});
// handler the changes send from server.
	this.collaborationSocket.on("change", (delta: string) => {
		console.log('collabration: editor changes by ' + delta);
		delta = JSON.parse(delta); // delta is json format
		editor.lastAppliedChange = delta;
// apply the changes on editor
		editor.getSession().getDocument().applyDeltas([delta]);
		});
	}
// emit event to make changes and inform server and other
	
	change(delta: string): void {
// emit "change" event
		this.collaborationSocket.emit("change", delta);
	}
}
