let FarPi = {
    // Send a message back to the server
    sendMsg: function() {
        this.socket.send(document.getElementById('msg').value);
    },

    action: function(target, arguments) {
        this.socket.send("{\"action\":\""+target+"\", \"parameters\":{"+arguments+"}}");
    },

    // Called when the page is loaded. Opens a websocket connection to the server
    // and registers the callback to handle the returned server state.
    onLoad: function(target) {
        const address = "ws://" + location.hostname + ":" + location.port + "/" + target;
        console.log("Connecting to "+address)
        this.socket = new WebSocket(address);
        this.socket.onmessage = function(e) {
            FarPi.state = JSON.parse(e.data);
            FarPi.heartbeat();
            for(let i in FarPi._callbacks){
                FarPi._callbacks[i]();
            }
        };
    },

    // Private list of call back functions that get called whenever the state gets refreshed by the server
    _callbacks: [],
    registerCallback: function(callback){
        this._callbacks.push(callback);
    },

    heartbeat: function(){
        let heartbeat_element = document.getElementById("HeartBeat");
        if(FarPi.state["cycle"] % 2){
            heartbeat_element.classList.toggle("HeartBeatGlow");
        }
    },

    trap_context: function() {
        event = window.event;
        event.preventDefault();
        return true;
    },

    // State attribute is populated by JSON decoding server response
    state: {},

    // Web-socket connection to the server
    socket: undefined
}
