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

class FarPiGauge extends FarPiElement {
    setup() {
        this.value = 0;

        this.units = this.getAttribute("units");
        if(!this.units) this.units = "";

        // If no scale attribute is provided, assume the value is in the range 0-1, convert to percentage
        this.scale = this.getAttribute("scale");
        if(this.scale){
            this.scale = parseFloat(this.scale);
        } else {
            this.scale = 100.0;
        }

        // Maximum value the gauge will show. Any value over this is ignored
        this.max = this.getAttribute("max");
        if(this.max){
            this.max = parseFloat(this.max);
        } else {
            this.max = 100.0;
        }

        // Handle X.Y notation
        this.source = this.getAttribute("source");
        let source_parts = this.source.split(".");
        if(source_parts.length > 1){
            this.source = source_parts[0];
            this.param = source_parts[1];
        } else {
            this.param = "state";
        }

        this.label = this.innerHTML;

        this.innerHTML =
            `<div class="flex w-64 pr-5">
                <span class="text-primary p-2">${this.label}</span>
                <span class="text-primary p-2 w-full">
                    <progress class="progress progress-primary h-2" max="${this.max}"></progress>
                </span>
                <span class="text-primary p-2">${this.value}</span>
            </div>`
        this.onclick = this.onclick_handler
        console.log('FarPiGaugeRound added to page - ' + this.source);
    }

    farPiUpdate(newValue) {

        this.value = (newValue[this.source][this.param]*this.scale).toFixed(1);
        let gauge_element = this.getElementsByTagName("progress")[0];
        gauge_element.setAttribute("value", this.value);

        let gauge_element_text = this.getElementsByTagName("span")[2];
        gauge_element_text.innerText = `${this.value}${this.units}`
    }
}


class FarPiGaugeRound extends FarPiElement {
    setup() {
        this.value = 0;

        this.units = this.getAttribute("units");
        if(!this.units) this.units = "";

        // If no scale attribute is provided, assume the value is in the range 0-1, convert to percentage
        this.scale = this.getAttribute("scale");
        if(this.scale){
            this.scale = parseFloat(this.scale);
        } else {
            this.scale = 100.0;
        }

        // Handle X.Y notation
        this.source = this.getAttribute("source");
        let source_parts = this.source.split(".");
        if(source_parts.length > 1){
            this.source = source_parts[0];
            this.param = source_parts[1];
        } else {
            this.param = "state";
        }

        this.label = this.innerText;

        this.innerHTML =
            `<div class="grid grid-rows-1 justify-items-center place-content-center rounded-lg border border-panel p-5 bg-base-100">
                <span class="radial-progress text-primary border-4 border-neutral-800 bg-neutral-800" style="--value:0;">${this.value}</span>
                <span class="label p-0">${this.label}</span>
            </div>`
        this.onclick = this.onclick_handler
        console.log('FarPiGaugeRound added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let gauge_element = this.getElementsByClassName("radial-progress")[0];
        this.value = (newValue[this.source][this.param]*this.scale).toFixed(1);

        gauge_element.style = `--value:${this.value}`;
        gauge_element.innerText = `${this.value}${this.units}`
    }
}


class FarPiMiniGauge extends FarPiElement {
    setup() {
        this.value = 0;

        this.units = this.getAttribute("units");
        if(!this.units) this.units = "";

        // If no scale attribute is provided, assume the value is in the range 0-1, convert to percentage
        this.scale = this.getAttribute("scale");
        if(this.scale){
            this.scale = parseFloat(this.scale);
        } else {
            this.scale = 100.0;
        }

        // Handle X.Y notation
        this.source = this.getAttribute("source");
        let source_parts = this.source.split(".");
        if(source_parts.length > 1){
            this.source = source_parts[0];
            this.param = source_parts[1];
        } else {
            this.param = "state";
        }

        this.label = this.innerText;

        this.innerHTML =
            `<div class="grid grid-rows-1 justify-items-center place-content-center p-1 ">
                <span class="radial-progress text-primary border-1 border-neutral-800 bg-neutral-800" style="--value:0;"></span>
            </div>`
        this.onclick = this.onclick_handler
        console.log('FarPiGaugeRound added to page - ' + this.source);
    }

    farPiUpdate(newValue) {
        let gauge_element = this.getElementsByClassName("radial-progress")[0];
        this.value = (newValue[this.source][this.param]*this.scale).toFixed(1);

        gauge_element.style = `--value:${this.value}; --size:3rem; --thickness:5px`;
    }
}



customElements.define('farpi-led', FarPiLED);
customElements.define('farpi-gauge', FarPiGauge);
customElements.define('farpi-gauge-round', FarPiGaugeRound);
customElements.define('farpi-mini-gauge', FarPiMiniGauge);
