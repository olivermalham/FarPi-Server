class FarPiSwitch extends FarPiElement {
    // TODO:
    //  - Rewrite the component HTML to use DaisyUI and tailwind

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


customElements.define('farpi-switch', FarPiSwitch);
customElements.define('farpi-button', FarPiButton);