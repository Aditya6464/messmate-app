/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './core/templates/**/*.html',
        './templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                primary: '#3B82F6',
                secondary: '#8B5CF6',
                success: '#10B981',
                danger: '#EF4444',
                warning: '#F59E0B',
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
