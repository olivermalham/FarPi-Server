/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        '../js/**/*.{html,js}',
        '../../core/**/*.{html,js}',
        '../../HUD/**/*.{html,js}',
        '../index.html',],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: ["light", "dark", "cupcake",
            {
                squirt: {
                    ...require('daisyui/src/colors/themes')['[data-theme=black]'],
                    'border-color': 'rgba(211, 211, 211, 0.2)',
                    'primary': '#ffffff',
                    'secondary': '#ffffff',
                    'neutral': '#ffffff',
                    'progress-primary': '#ffffff',
                }
            }
        ],
    },
}