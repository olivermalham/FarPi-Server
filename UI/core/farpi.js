class FarPi extends HTMLElement {

    // State attribute is populated by JSON decoding server response
    state = {}

    // Web-socket connection to the server
    socket = undefined

    // Send a message back to the server
    sendMsg() {
        this.socket.send(document.getElementById('msg').value);
    }

    action(target, args) {
        this.socket.send("{\"action\":\"" + target + "\", \"parameters\":{" + args + "}}");
    }

    // Opens a websocket connection to the server, sets up the message handler and finds and configures all
    // FarPi elements in the DOM
    connectedCallback() {
        setTimeout(() => {
            let address = this.getAttribute("server");
            this.socket = new WebSocket(address);
            console.log("FarPi connected to " + address);

            // Assumes there is only one farpi-root element, any more will be ignored
            let farpiRoot = document.getElementsByTagName("farpi-root")[0];

            // Get all elements with the _farPiComponent class, automatically added by FarPiElement
            this.socket.farpiControls = farpiRoot.getElementsByClassName("_farPiComponent");

            // Attach the this FarPi instance to all of the FarPiElements
            for (let i = 0; i < this.socket.farpiControls.length; i++) {
                this.socket.farpiControls[i]._farpi = this;
            }

            this.socket.onmessage = function (e) {
                // Remember: "this" refers to the socket, NOT the FarPi object!
                let state = JSON.parse(e.data);
                for (let i = 0; i < this.farpiControls.length; i++) {
                    this.farpiControls[i].farPiUpdate(state);
                }
            }
        });
    }
}
customElements.define('farpi-root', FarPi);

class FarPiElement extends HTMLElement {
    // Base class for FarPi elements.
    connectedCallback() {
        // Add classname to make it easy to find all FarPi components
        this.className = this.className + " _farPiComponent";
        this.source = this.getAttribute("source");
        setTimeout(() => this.setup());
    }

    setup() {
        // Setup code run once the DOM is fully constructed
    }

    farPiUpdate(newValue) {
        // Called every time we receive a state update from the server
    }

    action(action, args){
        // Utility function for RPC calls back to the server
        this._farpi.action(this.source + "." + action, args);
    }
}


class FarPiHeartBeat extends FarPiElement {
    // Simple active connection indicator
    setup() {
        this.style_on = "";
        this.style_off = "badge-outline";
        this.classList.add("badge", "badge-outline");
        this.label = this.innerText;
        this.innerHTML =
            `<div>${this.label}</div>`
    }

    farPiUpdate(newValue) {
        if (newValue["cycle"] % 2) {
            // this.classList.add(this.style_on);
            this.classList.remove(this.style_off);
        } else {
            // this.classList.remove(this.style_on);
            this.classList.add(this.style_off);
        }
    }
}
customElements.define('farpi-heartbeat', FarPiHeartBeat);


class FarPiPanel extends FarPiElement {
    // Very basic custom component to create a control panel - just a DaisyUI card really
    setup() {
        this.classList.add("card", "card-bordered", "border-panel", "shadow-xl", "bg-neutral", "text-neutral-content");
    }

}
customElements.define('farpi-panel', FarPiPanel);
