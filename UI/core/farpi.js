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

            // Attach this FarPi instance to all the FarPiElements
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

            this.socket.onclose = function (e) {
                let heartbeat = document.getElementsByTagName("farpi-heartbeat")[0];
                heartbeat.disconnected();
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
        this.classList.add("pr-3");
        this.label = this.innerText;
        this.innerHTML =
            `<div class="flex items-center justify-center text-neutral border border-2 border-neutral p-1 rounded-xl w-12 h-12 items-center">
                <div class="text-neutral inline-block h-6 w-6 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" role="status">
                    
                </div>
            </div>`
    }

    disconnected() {
        let spinner = this.getElementsByClassName("animate-spin")[0];
        if(spinner){
            spinner.classList.remove("animate-spin")
        }
        this.innerHTML = `
            <div class="flex items-center justify-center text-neutral border border-2 border-neutral p-1 rounded-xl w-12 h-12 items-center text-5xl">
                    &CircleTimes;
            </div>`
    }
}
customElements.define('farpi-heartbeat', FarPiHeartBeat);


class FarPiPanel extends FarPiElement {
    // Very basic custom component to create a control panel - just a DaisyUI card really
    setup() {
        this.classList.add("card", "card-bordered", "border-panel", "shadow-xl", "bg-neutral", "text-neutral-content", "backdrop-blur", "bg-white/10");
    }

}
customElements.define('farpi-panel', FarPiPanel);
