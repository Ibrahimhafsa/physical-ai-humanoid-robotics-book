// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI & Humanoid Robotics TextBook',
  tagline: 'From Basics to Advanced',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://ai-physical-robotics-book.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'ai-physical-robotics', // Usually your GitHub org/user name.
  projectName: 'ai-physical-robotics-book', // Usually your repo name.

  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/ai-physical-robotics/ai-physical-robotics-book/tree/main/',
          remarkPlugins: [
            require('remark-gfm'),
          ],
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl:
            'https://github.com/ai-physical-robotics/ai-physical-robotics-book/tree/main/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  headTags: [
    {
      tagName: 'script',
      innerHTML: `
      window.__RAG_API_URL__ = "${process.env.DOCUSAURUS_API_URL || 'http://localhost:8000'}";
      console.log('[RAG CONFIG] API URL injected:', window.__RAG_API_URL__);
    `,
    },
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'AI & Physical Robotics',
        logo: {
          alt: 'Robotics Book Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'dropdown',
            label: 'Modules',
            position: 'left',
            items: [
              {
                label: '🤖 ROS 2 - Robotics Nervous System',
                to: '/docs/humanoid-robotics/ros2-architecture',
              },
              {
                label: '🎮 Digital Twin - Gazebo & Unity',
                to: '/docs/digital-twin/simulation-fundamentals',
              },
              {
                label: '🧠 NVIDIA Isaac - AI Brain',
                to: '/docs/ai-brain/nvidia-isaac-overview',
              },
              {
                label: '👁️ Vision-Language-Action',
                to: '/docs/vla/multimodal-learning',
              },
            ],
          },
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            label: 'Get Started',
            to: '/docs/fundamentals/what-is-physical-ai',
            position: 'left',
            className: 'navbar-cta-button',
          },
          {
            href: 'https://github.com/ai-physical-robotics/ai-physical-robotics-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Issues',
                href: 'https://github.com/ai-physical-robotics/ai-physical-robotics-book/issues',
              },
              {
                label: 'Discussions',
                href: 'https://github.com/ai-physical-robotics/ai-physical-robotics-book/discussions',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/ai-physical-robotics/ai-physical-robotics-book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AI & Physical Robotics. Built with Docusaurus. Created by HAFSA IBRAHIM`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
