class FarPiSwitch extends FarPiElement {
    // TODO:
    //  - Refactor codebase to make it easy for FarPi app settings to select UI to serve
    //  - Get Tailwind and Daisy CSS libraries added to make it pretty

    setup() {
        this.source = this.getAttribute("source");
        this.label = this.innerText; //this.getAttribute("label");
        this.innerHTML =
            `<div class="LED interactive">
                <span class="toggle_switch"><span class="toggle_indicator">&nbsp;</span></span>
                <span class="label">${this.label}</span>
            </div>`
        this.onclick = this.onclick_handler
        console.log('FarPiSwitch added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let switch_element = this.getElementsByClassName("toggle_switch")[0];
        let switch_indicator = this.getElementsByClassName("toggle_indicator")[0];

        if (newValue[this.source].state) {
            switch_element.classList.add("toggle_switch_on", "on_glow");
            switch_indicator.classList.add("toggle_on");
        } else {
            switch_element.classList.remove("toggle_switch_on", "on_glow");
            switch_indicator.classList.remove("toggle_on");
        }
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
            `<div class="LED interactive">
                <span class="LED_indicator">&nbsp;</span>
                <span class="label">${this.label}</span>
            </div>`
        this.onmousedown = this.onmousedown_handler;
        this.onmouseup = this.onmouseup_handler;
        this.ontouchstart = this.onmousedown_handler;
        this.ontouchend = this.onmouseup_handler;
        console.log('FarPiButton added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let switch_indicator = this.getElementsByClassName("LED_indicator")[0];

        if (newValue[this.source].state) {
            switch_indicator.classList.add("LED_on", "on_glow");
        } else {
            switch_indicator.classList.remove("LED_on", "on_glow");
        }
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