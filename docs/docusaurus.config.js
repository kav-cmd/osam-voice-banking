module.exports = {
  title: 'OSAM Voice Banking',
  tagline: 'Voice-enabled accessible banking for India in Hindi, Tamil & English',
  url: 'https://osam-voice-banking.onrender.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'kav-cmd',
  projectName: 'osam-voice-banking',
  themeConfig: {
    navbar: {
      title: 'OSAM',
      items: [
        { to: '/docs/intro', label: 'Docs', position: 'left' },
        { to: '/docs/api', label: 'API', position: 'left' },
        { to: '/docs/accessibility', label: 'Accessibility', position: 'left' },
        {
          href: 'https://github.com/kav-cmd/osam-voice-banking',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        { title: 'Docs', items: [{ label: 'Getting Started', to: '/docs/intro' }] },
        { title: 'Community', items: [{ label: 'RBI Innovation Hub', href: 'https://rbihub.in' }] },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} RBI Innovation Hub. Built for public good.`,
    },
  },
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        theme: { customCss: require.resolve('./src/css/custom.css') },
      },
    ],
  ],
};
