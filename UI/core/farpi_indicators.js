class FarPiLED extends FarPiElement {
    setup() {
        this.source = this.getAttribute("source");
        this.label = this.innerText;
        this.innerHTML =
            `<div class="btn btn-outline btn-primary w-full toggle_switch flex space-x-4 no-animation">
                <input type="radio" class="radio radio-primary" />
                <span class="label">${this.label}</span>
            </div>`
        this.onclick = this.onclick_handler
        console.log('FarPiLED added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let led_element = this.getElementsByTagName("input")[0];

        led_element.checked = newValue[this.source].state;
    }
}

class FarPiGaugeRound extends FarPiElement {
    setup() {
        this.value = 0;
        this.units = "V";
        this.source = this.getAttribute("source");
        this.label = this.innerText;
        this.innerHTML =
            `<div class="grid place-items-center">
                <span class="radial-progress text-primary border-primary" style="--value:0;">${this.value}</span>
                <span class="label">${this.label}</span>
            </div>`
        this.onclick = this.onclick_handler
        console.log('FarPiLED added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let gauge_element = this.getElementsByClassName("radial-progress")[0];
        this.value = (newValue[this.source]["state"]*100.0).toFixed(1);

        gauge_element.style = `--value:${this.value}`;
        gauge_element.innerText = `${this.value}${this.units}`
    }
}


customElements.define('farpi-led', FarPiLED);
customElements.define('farpi-guage-round', FarPiGaugeRound);
