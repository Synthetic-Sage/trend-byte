module.exports = {
  content: ["./public/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        primary: '#33FF00', 
        background: '#050505',
        surface: '#050505',
        textMain: '#33FF00',
        textMuted: '#1A3D1A'
      },
      animation: {
        'flicker': 'flicker 0.15s infinite',
        'cursor': 'cursor .75s step-end infinite'
      },
      keyframes: {
        flicker: {
          '0%': { opacity: '0.98' },
          '50%': { opacity: '1' },
          '100%': { opacity: '0.99' }
        },
        cursor: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
