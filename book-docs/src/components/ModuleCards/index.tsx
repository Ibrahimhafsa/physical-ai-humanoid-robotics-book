/**
 * ModuleCards Component - Premium Learning Modules Section
 * Displays the 4 main learning modules with advanced visual design
 * Features numbered badges, progress indicators, and premium animations
 */

import Link from '@docusaurus/Link';
import styles from './styles.module.css';

interface Module {
  id: string;
  number: number;
  icon: string;
  title: string;
  description: string;
  chapters: number;
  link: string;
  color: string;
}

const MODULES: Module[] = [
  {
    id: 'ros2',
    number: 1,
    icon: '⚙️',
    title: 'ROS 2 - Robotics Nervous System',
    description: 'Master ROS 2 architecture, nodes, topics, control systems, and navigation fundamentals.',
    chapters: 5,
    link: '/docs/humanoid-robotics/ros2-architecture',
    color: 'module-1',
  },
  {
    id: 'digital-twin',
    number: 2,
    icon: '🎮',
    title: 'Digital Twin - Gazebo & Unity',
    description: 'Build realistic simulations with Gazebo and Unity for safe robot testing and development.',
    chapters: 4,
    link: '/docs/digital-twin/simulation-fundamentals',
    color: 'module-2',
  },
  {
    id: 'isaac',
    number: 3,
    icon: '🧠',
    title: 'NVIDIA Isaac - AI Robot Brain',
    description: 'Implement computer vision, deep learning, and reinforcement learning for intelligent robots.',
    chapters: 4,
    link: '/docs/ai-brain/nvidia-isaac-overview',
    color: 'module-3',
  },
  {
    id: 'vla',
    number: 4,
    icon: '👁️',
    title: 'Vision-Language-Action (VLA)',
    description: 'Integrate vision, language, and action for advanced robot intelligence and natural interaction.',
    chapters: 1,
    link: '/docs/vla/multimodal-learning',
    color: 'module-4',
  },
];

/**
 * ModuleCards - Premium showcase of 4 learning modules
 * Features:
 * - Numbered module badges (1-4) with unique colors
 * - Large emoji icons with glow effects
 * - Chapter progress indicators
 * - 2x2 grid on desktop, 1 column on mobile
 * - Premium hover animations with lift and glow
 * - Interactive "Start Learning" CTA button
 * - Responsive design across all devices
 */
export default function ModuleCards(): JSX.Element {
  return (
    <section className={styles.modulesSection}>
      <div className={styles.backgroundDecoration}></div>
      <div className="container">
        <div className={styles.sectionHeader}>
          <div className={styles.headerBadge}>Structured Learning Path</div>
          <h2 className={styles.sectionTitle}>Learning Modules</h2>
          <p className={styles.sectionSubtitle}>
            Master the 4-module backbone of Physical AI and Humanoid Robotics
          </p>
        </div>

        <div className={styles.modulesGrid}>
          {MODULES.map((module) => (
            <div
              key={module.id}
              className={`${styles.moduleCard} ${styles[module.color]}`}
              style={{ animationDelay: `${module.number * 0.1}s` }}
            >
              <div className={styles.cardGradientBorder}></div>
              <div className={styles.moduleNumber}>{module.number}</div>
              <div className={styles.iconWrapper}>
                <div className={styles.moduleIcon}>{module.icon}</div>
                <div className={styles.iconGlow}></div>
              </div>
              <h3 className={styles.moduleTitle}>{module.title}</h3>
              <p className={styles.moduleDescription}>{module.description}</p>
              <div className={styles.progressBar}>
                <div className={styles.progressFill}></div>
              </div>
              <span className={styles.moduleBadge}>{module.chapters} Chapters</span>
              <Link to={module.link} className={styles.moduleCTA}>
                Start Learning →
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
