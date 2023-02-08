class FarPi extends HTMLElement {

    // State attribute is populated by JSON decoding server response
    state = {}

    // Web-socket connection to the server
    socket = undefined

    // Private list of call back functions that get called whenever the state gets refreshed by the server
    _callbacks = []

    // Send a message back to the server
    sendMsg() {
        this.socket.send(document.getElementById('msg').value);
    }

    action(target, args) {
        this.socket.send("{\"action\":\""+target+"\", \"parameters\":{"+args+"}}");
    }

    trap_context() {
        event = window.event;
        event.preventDefault();
        return true;
    }

    // Called when the page is loaded. Opens a websocket connection to the server
    // and registers the callback to handle the returned server state.
    connectedCallback() {
        let address = this.getAttribute("server");
        this.socket = new WebSocket(address);
        console.log("FarPi connected to "+address);

        // Assumes there is only one farpi-root element, any more will be ignored
        let farpiRoot = document.getElementsByTagName("farpi-root")[0];

        // Get all elements with the _farPiComponent class, automatically added by FarPi webcomponents
        this.socket.farpiControls = farpiRoot.getElementsByClassName("_farPiComponent");

        for(let i = 0; i < this.socket.farpiControls.length; i++) {
            this.socket.farpiControls[i].farpi = this;
        }

        this.socket.onmessage = function(e) {
            // Remember: "this" refers to the socket, NOT the FarPi object!
            let state = JSON.parse(e.data);
            for(let i = 0; i < this.farpiControls.length; i++) {
                this.farpiControls[i].farpiUpdate(state);
            }
        }
    }
}

customElements.define('farpi-root', FarPi);