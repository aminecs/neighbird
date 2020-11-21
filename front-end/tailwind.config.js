module.exports = {
  purge: ['./components/**/*.{js,jsx,ts,tsx}', './pages/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      screens: {
        tablet: { max: '800px' },
        // => @media (max-width: 800px) { ... }

        smallTablet: { max: '600px' },
        // => @media (max-width: 600px) { ... }

        phone: { max: '450px' },
        // => @media (max-width: 350px) { ... }
      },
    },
  },
  variants: {
    // ...
    borderWidth: ['responsive'],
    borderWidth: ['responsive', 'hover', 'focus'],
    margin: ['responsive', 'hover', 'focus'],
    scale: ['responsive', 'hover', 'focus', 'active', 'group-hover'],
  },
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  corePlugins: {
    preflight: false,
  },
};
