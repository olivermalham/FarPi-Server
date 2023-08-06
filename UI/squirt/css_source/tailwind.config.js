/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        '../js/**/*.{html,js}',
        '../../core/**/*.{html,js}',
        '../index.html',],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: [
            {
                halloween: {
                    ...require('daisyui/src/colors/themes')['[data-theme=halloween]'],
                    '.border-panel': {
                        'border-color': 'rgba(211, 211, 211, 0.2)',
                    },
                }
            }
        ],
    },
}
