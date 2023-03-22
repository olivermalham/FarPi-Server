
class FarPiNavbar extends FarPiElement {
    setup() {
        this.logo = this.getAttribute("logo");
        this.label = this.innerText;
        this.innerHTML =
            `<div class="navbar bg-primary text-neutral-content h-20">
                <div class="flex-1">
                    <img src="${this.logo}" alt="${this.logo} Logo" class="h-20 p-2"/>
                </div>
                ${this.innerHTML}
            </div>`;
    }
}
customElements.define('farpi-navbar', FarPiNavbar);


class FarPiNavbarButton extends FarPiElement {
    setup() {
        this.logo = this.getAttribute("logo");
        this.innerHTML =
            `<button class="btn">
                ${this.innerHTML}
            </button>`;
        // <div class="flex items-center justify-center bg-base-100 text-primary border border-2 border-neutral p-1 mr-3 rounded-xl w-28 h-12 items-center">
    }
}
customElements.define('farpi-navbar-button', FarPiNavbarButton);


class FarPiTabList extends FarPiElement {
    // Tab headers
    setup() {
        this.innerHTML =
            `<div class="tabs tabs-boxed mr-3">
                ${this.innerHTML}
            </div>`;
    }
}
customElements.define('farpi-tab-list', FarPiTabList);


class FarPiTab extends FarPiElement {
    // Container for the contents of each tab
    setup() {
        this.classList.add("pr-3");
        this.innerHTML =
            `<div class="flex items-center justify-center text-neutral border border-2 border-neutral p-1 rounded-xl w-12 h-12 items-center">
                <div class="text-neutral inline-block h-6 w-6 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" role="status">
                    
                </div>
            </div>`;
    }
}
customElements.define('farpi-tab', FarPiTab);
