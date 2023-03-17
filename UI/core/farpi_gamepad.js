class FarPiGamepad extends FarPiElement {
    setup() {
        this.sample_period = this.getAttribute("period");
        this.label = this.innerText;
        this.classList.add("bg-base-100", "rounded-lg", "border", "border-panel", "p-5")

        this.innerHTML =
            `<div>gamepad</div>
            <div class="flex justify-center w-full">
              <kbd class="btn btn-primary text-xl" id="up">&#9650</kbd>
            </div>
            <div class="flex justify-center gap-24 w-full">
              <kbd class="btn btn-primary text-xl" id="left">&#9668</kbd>
              <kbd class="btn btn-primary text-xl" id="right">&#9658</kbd>
            </div>
            <div class="flex justify-center w-full">
              <kbd class="btn btn-primary text-xl" id="down">&#9660</kbd>
            </div>`

        console.log('FarPiGamepad added to page');

        if ('GamepadEvent' in window) {
          window.addEventListener("gamepadconnected", this.connect_handler);
          window.addEventListener("gamepaddisconnected", this.disconnect_handler);

        }
        window.setInterval(this.gamepad_handler, this.sample_period);
    }

    connect_handler(){
      console.log("Gamepad connected");
      this.gamepads = navigator.getGamepads();
      console.log(this.gamepads);
    }

    disconnect_handler(){
      console.log("Gamepad disconnected");
    }

    farPiUpdate(newValue) {
    }

    gamepad_handler(event) {
        for(let gamepad in this.gamepads){
            console.log(this.gamepads[gamepad]);
        }
    }
}
customElements.define('farpi-gamepad', FarPiGamepad);
