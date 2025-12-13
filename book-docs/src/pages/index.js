import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import ModuleCards from '@site/src/components/ModuleCards';
import ValueProposition from '@site/src/components/ValueProposition';
import WhatYouWillLearn from '@site/src/components/WhatYouWillLearn';
import LearningJourney from '@site/src/components/LearningJourney';

import Heading from '@theme/Heading';
import styles from './index.module.css';

/**
 * HomepageHeader - Impressive hero section with animated gradient
 * Features:
 * - Animated purple gradient background
 * - Large, bold headline with gradient text effect
 * - Compelling subheadline
 * - Dual CTAs: "Get Started" and "Explore Modules"
 * - Fade-in animations for all content
 */
function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroBanner, 'hero-gradient')}>
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>
          {siteConfig.title}
        </Heading>
        <p className={styles.heroSubtitle}>
          Master humanoid robotics from ROS 2 fundamentals to Vision-Language-Action systems. Learn with hands-on exercises, real-world examples, and an AI-powered assistant.
        </p>
        <div className={styles.heroButtons}>
          <Link
            className={clsx(styles.btnPrimaryCta, 'btn-primary-cta')}
            to="/docs/fundamentals/what-is-physical-ai">
            Get Started
          </Link>
          <Link
            className={clsx(styles.btnSecondaryCta, 'btn-secondary-cta')}
            to="#modules">
            Explore Modules ↓
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="Master AI-powered humanoid robotics with hands-on learning, practical exercises, and an AI-powered chat assistant. Learn ROS 2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action systems.">
      <HomepageHeader />
      <main>
        <WhatYouWillLearn />
        <LearningJourney />
        <section id="modules">
          <ModuleCards />
        </section>
        <ValueProposition />
      </main>
    </Layout>
  );
}
