class FarPiLED extends FarPiElement {
    setup() {
        this.source = this.getAttribute("source");
        this.label = this.innerText;
        this.innerHTML =
            `<div class="LED" id="LED_{{pin}}_{{_id}}">
                <span class="LED_indicator">&nbsp;</span>
                <span class="label">${this.label}</span>
            </div>`
        this.onclick = this.onclick_handler
        console.log('FarPiLED added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let led_element = this.getElementsByClassName("LED_indicator")[0];

        if (newValue[this.source].state) {
            led_element.classList.add("LED_on", "on_glow");
        } else {
            led_element.classList.remove("LED_on", "on_glow");
        }
    }
}

customElements.define('farpi-led', FarPiLED);

