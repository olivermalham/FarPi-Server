class FarPiSwitch extends FarPiElement {
    setup() {
        this.source = this.getAttribute("source");
        this.label = this.innerText;
        this.innerHTML =
            `<div class="btn btn-primary w-full toggle_switch flex space-x-4">
                <input type="checkbox" class="toggle toggle-primary bg-primary-content" />
                <span class="label">${this.label}</span>
            </div>`
        this.onclick = this.onclick_handler
        console.log('FarPiSwitch added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let switch_indicator = this.getElementsByTagName("input")[0];

        switch_indicator.checked = newValue[this.source].state;
    }

    onclick_handler(event) {
        this.action("action_toggle", "");
    }
}
customElements.define('farpi-switch', FarPiSwitch);


class FarPiButton extends FarPiElement {
    setup() {
        this.source = this.getAttribute("source");
        this.label = this.innerText;

        this.innerHTML =
            `<div class="btn btn-primary w-full">
                <span class="label" class="bg-primary-content">${this.label}</span>
            </div>`
        this.onmousedown = this.onmousedown_handler;
        this.onmouseup = this.onmouseup_handler;
        this.ontouchstart = this.onmousedown_handler;
        this.ontouchend = this.onmouseup_handler;
        console.log('FarPiButton added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
    }

    onmousedown_handler(event) {
        event.preventDefault();
        this.action("action_set", '"value":1');
        console.log('FarPiButton down - ' + this.source);
    }

    onmouseup_handler(event) {
        event.preventDefault();
        this.action("action_set", '"value":0');
        console.log('FarPiButton up - ' + this.source);
    }
}
customElements.define('farpi-button', FarPiButton);


class FarPiKeypad extends FarPiElement {
    setup() {
        this.source = this.getAttribute("source");
        this.label = this.innerText;

        this.innerHTML =
            `<div class="flex justify-center w-full">
              <kbd class="btn btn-primary text-xl" id="up">&#9650</kbd>
            </div>
            <div class="flex justify-center gap-24 w-full">
              <kbd class="btn btn-primary text-xl" id="left">&#9668</kbd>
              <kbd class="btn btn-primary text-xl" id="right">&#9658</kbd>
            </div>
            <div class="flex justify-center w-full">
              <kbd class="btn btn-primary text-xl" id="down">&#9660</kbd>
            </div>`
        this.onmousedown = this.onmousedown_handler;
        this.onmouseup = this.onmouseup_handler;
        this.ontouchstart = this.onmousedown_handler;
        this.ontouchend = this.onmouseup_handler;
        console.log('FarPiKeypad added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
    }

    onmousedown_handler(event) {
        event.preventDefault();
        this.action("action_set", '"value":1');
        console.log('FarPiKeypad down - ' + this.source);
    }

    onmouseup_handler(event) {
        event.preventDefault();
        this.action("action_set", '"value":0');
        console.log('FarPiKeypad up - ' + this.source);
    }
}
customElements.define('farpi-keypad', FarPiKeypad);
