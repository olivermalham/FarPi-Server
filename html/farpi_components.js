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
    this.innerHTML =
        `<div class="LED interactive">
          <span class="toggle_switch"><span class="toggle_indicator">&nbsp;</span></span>
          <span class="label">${this.source}</span>
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
    console.log(`FarPiSwitch ${this.source} update called ${newValue[this.source]}`);
  }

  onclick_handler(event){
    // FIXME: For some reason specifying onclick directly doesn't work?
    console.log(`Onclick called for ${this.source}`);
  }
}

customElements.define('farpi-switch', FarPiSwitch);