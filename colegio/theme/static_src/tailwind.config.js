module.exports = {
    content: [
        '../templates/**/*.html',

        '../../templates/**/*.html',

        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            keyframes: {
            'pulse-soft': {
                '0%, 100%': { transform: 'scale(1)', opacity: '0.5' },
                '50%': { transform: 'scale(1.4)', opacity: '0.1' },
            },
            'typing': {
                '0%, 80%, 100%': { transform: 'translateY(0)' },
                '40%': { transform: 'translateY(-6px)' }
            },
            'fade': {
                '0%': { opacity: 0 },
                '100%': { opacity: 1 },
            }
            },
            animation: {
            'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            'typing-bounce': 'typing 1.2s infinite',
            'fade-in': 'fade 0.5s ease-in-out',
            'pulse-soft': 'pulse-soft 2s ease-in-out infinite',
            }
        },
    },

    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
