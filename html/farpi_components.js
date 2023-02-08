// Create a class for the element
class FarPiSwitch extends HTMLElement {
  // TODO:
  //  - Refactor into a FarPiElement base class
  //  - Figure out how to do the action calls to the server
  //  - Refactor codebase to make it easy for FarPi app settings to select UI to serve
  //  - Get Tailwind and Daisy CSS libraries added to make it pretty

  constructor() {
    // Always call super first in constructor
    super();
    this.source = null;
    console.log('FarPiSwitch constructed.');
  }

  connectedCallback() {
    this.className = this.className + " _farPiComponent";
    this.source = this.getAttribute("source");
    this.label = this.getAttribute("label");
    this.innerHTML =
        `<div class="LED interactive">
          <span class="toggle_switch"><span class="toggle_indicator">&nbsp;</span></span>
          <span class="label">${this.label}</span>
        </div>`
    this.onclick = this.onclick_handler
    console.log('FarPiSwitch added to page.' + this.source);
  }

  disconnectedCallback() {
    console.log('FarPiSwitch removed from page.');
  }

  adoptedCallback() {
    console.log('FarPiSwitch moved to new page.');
  }

  attributeChangedCallback(name, oldValue, newValue) {
    console.log('FarPiSwitch attributes changed.');
  }

  farpiUpdate(newValue){
    let switch_element = this.getElementsByClassName("toggle_switch")[0];
    let switch_indicator = this.getElementsByClassName("toggle_indicator")[0];

    if(newValue[this.source].state){
      switch_element.classList.add("toggle_switch_on", "on_glow");
      switch_indicator.classList.add("toggle_on");
    } else {
      switch_element.classList.remove("toggle_switch_on", "on_glow");
      switch_indicator.classList.remove("toggle_on");
    }
  }

  onclick_handler(event){
    // FIXME: For some reason specifying onclick directly doesn't work?
    console.log(`Onclick called for ${this.source}`);
    this.farpi.action(this.source, "");
  }
}

// Create a class for the element
class FarPiHeartBeat extends HTMLElement {

  constructor() {
    // Always call super first in constructor
    super();
    this.source = null;
    console.log('FarPiHeartBeat constructed.');
  }

  connectedCallback() {
    this.className = this.className + " _farPiComponent";
    this.innerHTML =
        `<div class="HeartBeat" id="HeartBeat">- FarPi -</div>`
    console.log('FarPiHeartBeat added to page.' + this.source);
  }

  farpiUpdate(newValue){
    if(newValue["cycle"] % 2){
      this.children[0].classList.toggle("HeartBeatGlow");
    }
  }
}

customElements.define('farpi-switch', FarPiSwitch);
customElements.define('farpi-heartbeat', FarPiHeartBeat);