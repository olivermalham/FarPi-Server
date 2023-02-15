class FarPiMessageBox extends FarPiElement {
    setup() {
        this.source = this.getAttribute("source");
        this.label = this.innerText;
        this.innerHTML =
            `<textarea readonly class="textarea textarea-bordered MessageBox w-full h-[16rem]"></textarea>`
        this.onclick = this.onclick_handler
        console.log('FarPiLED added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let messageBox = this.getElementsByClassName("MessageBox")[0];

        if(newValue["message"].length > 0){
            messageBox.value = messageBox.value + newValue["message"] + "\n";
            messageBox.scrollTop = messageBox.scrollHeight;
        }
    }
}

class FarPiConsole extends FarPiElement {
    setup() {
        this.source = this.getAttribute("source");
        this.buffer = ""
        this.commandLine = ""

        this.innerHTML =
            `<div class="form-control">
                <label class="label">
                    <textarea readonly class="textarea textarea-bordered">${this.buffer}</textarea>
                </label>
                <label class="input-group input-group-vertical">
                    <span>Email</span>
                    <input type="text" placeholder="info@site.com" class="CommandLine input input-bordered" />
                </label>
            </div>`
        console.log('FarPiConsole added to page');
        this.onkeydown = this.onenter_handler;
    }

    farPiUpdate(newValue) {
        let messageBox = this.getElementsByClassName("MessageBox")[0];
        let commandLine = this.getElementsByClassName("CommandLine")[0];

        if(newValue["message"].length > 0){
            messageBox.value = messageBox.value + newValue["message"] + "\n";
            messageBox.scrollTop = messageBox.scrollHeight;
        }

        if (newValue.message) {
            this.buffer = this.buffer + "Marvin > " + newValue.message + "\n";
            messageBox.value = this.buffer;
            messageBox.scrollTop = messageBox.scrollHeight;
        }
        if (newValue.error) {
            this.buffer = this.buffer + "ERROR > " + newValue.error + "\n";
            messageBox.value = this.buffer;
            messageBox.scrollTop = messageBox.scrollHeight;
        }
    }

    onenter_handler(event){
        if(event.key === "Enter") {
            let commandLine = this.getElementsByClassName("CommandLine")[0];
            this.action("action_command", `"command": "${commandLine.value}"`);
            commandLine.value = "";
        }
    }
}


customElements.define('farpi-message', FarPiMessageBox);
customElements.define('farpi-console', FarPiConsole);