module.exports = {
    content: [
        '../../templates/**/*.html',
        './templates/**/*.html',

        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            keyframes: {
                // Tu rebote de “typing-dot”
                bounceDot: {
                '0%, 80%, 100%': { transform: 'translateY(0)' },
                '40%':           { transform: 'translateY(-10px)' },
                },
                // El “ping” para el punto de estado
                pingCustom: {
                '0%':   { transform: 'scale(1); opacity: 1' },
                '75%,100%': { transform: 'scale(2); opacity: 0' },
                },
            },
            animation: {
                // Animaciones typing-dot
                'bounce-dot':         'bounceDot 1.2s infinite',
                'bounce-dot-delay-1': 'bounceDot 1.2s infinite 0.2s',
                'bounce-dot-delay-2': 'bounceDot 1.2s infinite 0.4s',
                // Animación ping para status-dot
                'ping-custom':        'pingCustom 1s cubic-bezier(0,0,0.2,1) infinite',
            },
            height: {
            'screen-minus-16': 'calc(100dvh - 64px)',
            },
        },
    },

    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
