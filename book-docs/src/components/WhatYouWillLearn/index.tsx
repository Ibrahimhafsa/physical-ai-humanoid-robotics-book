/**
 * WhatYouWillLearn Component - Enhanced Learning Skills Section
 * Displays a grid of key skills and concepts learners will acquire
 * with enhanced visual design, badges, and interactive animations
 */

import styles from './styles.module.css';

interface Skill {
  id: string;
  icon: string;
  title: string;
  description: string;
  category: string;
}

const SKILLS: Skill[] = [
  {
    id: 'ros2-mastery',
    icon: '⚙️',
    title: 'ROS 2 Mastery',
    description: 'Build sophisticated robot systems with middleware architecture, node communication, and distributed systems.',
    category: 'Core Framework',
  },
  
  {
    id: 'computer-vision',
    icon: '📷',
    title: 'Computer Vision',
    description: 'Implement perception systems with deep learning models for object detection, tracking, and scene understanding.',
    category: 'AI Systems',
  },
  
  {
    id: 'ai-integration',
    icon: '🤖',
    title: 'AI Integration',
    description: 'Deploy deep learning, reinforcement learning, and large language models on robotic hardware.',
    category: 'Advanced AI',
  },
  {
    id: 'production-deployment',
    icon: '🚀',
    title: 'Production Deployment',
    description: 'Learn real-world best practices: testing, containerization, monitoring, and continuous integration.',
    category: 'DevOps',
  },
];

/**
 * WhatYouWillLearn - Enhanced showcase of key skills
 * Features:
 * - 3-column grid on desktop, 2 on tablet, 1 on mobile
 * - Animated skill category badges
 * - Interactive icons with glow effects
 * - Gradient borders and depth effects
 * - Smooth fade-in animations on page load
 * - Professional hover animations
 */
export default function WhatYouWillLearn(): JSX.Element {
  return (
    <section className={styles.skillsSection}>
      <div className={styles.backgroundDecoration}></div>
      <div className="container">
        <div className={styles.sectionHeader}>
          <div className={styles.headerBadge}>Master Essential Skills</div>
          <h2 className={styles.sectionTitle}>What You'll Learn</h2>
          <p className={styles.sectionSubtitle}>
            Master the essential skills and concepts needed for modern robotics and AI integration
          </p>
        </div>

        <div className={styles.skillsGrid}>
          {SKILLS.map((skill, idx) => (
            <div
              key={skill.id}
              className={styles.skillCard}
              style={{ animationDelay: `${idx * 0.08}s` }}
            >
              <div className={styles.cardGradientBorder}></div>
              <div className={styles.skillCategory}>{skill.category}</div>
              <div className={styles.iconWrapper}>
                <div className={styles.skillIcon}>{skill.icon}</div>
                <div className={styles.iconGlow}></div>
              </div>
              <h3 className={styles.skillTitle}>{skill.title}</h3>
              <p className={styles.skillDescription}>{skill.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
