/**
 * ValueProposition Component - Enhanced "Why This Book" Section
 * Displays the key benefits and features of the book with visual enhancements
 * Features improved visual hierarchy, animations, and interactive elements
 */

import styles from './styles.module.css';

interface Proposition {
  id: string;
  icon: string;
  title: string;
  description: string;
  badge: string;
  features?: string[];
}

const VALUE_PROPOSITIONS: Proposition[] = [
  {
    id: 'hands-on',
    icon: '🎓',
    title: 'Hands-On Learning',
    description: 'Practical exercises, real-world examples, and interactive code snippets help you master robotics concepts through doing.',
    badge: 'Learn by Doing',
    features: ['Interactive Labs', 'Code Examples', 'Real Projects'],
  },
  {
    id: 'ai-assistant',
    icon: '🤖',
    title: 'AI-Powered Assistant',
    description: 'Built-in RAG chat widget provides instant Q&A about book content, making learning faster and more intuitive.',
    badge: 'Chat Anytime',
    features: ['24/7 Available', 'RAG-Enabled', 'Instant Answers'],
  },
  {
    id: 'comprehensive',
    icon: '📚',
    title: 'Comprehensive Coverage',
    description: 'From ROS 2 basics to advanced Vision-Language-Action systems, covering all essential topics in one place.',
    badge: 'Complete Path',
    features: ['5 Core Modules', 'Advanced Topics', 'Best Practices'],
  },
  {
    id: 'production',
    icon: '🚀',
    title: 'Production-Ready Tools',
    description: 'Learn industry-standard tools: ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language models used in real robotics.',
    badge: 'Industry Standard',
    features: ['Professional Tools', 'Real Applications', 'Career Ready'],
  },
];

/**
 * ValueProposition - Enhanced showcase of the 4 key benefits
 * Features:
 * - 2x2 grid on desktop, 1 column on mobile
 * - Animated icons with floating effects
 * - Visual badges for each proposition
 * - Gradient borders and depth effects
 * - Feature highlights within cards
 */
export default function ValueProposition(): JSX.Element {
  return (
    <section className={styles.valuePropSection}>
      <div className={styles.backgroundDecoration}></div>
      <div className="container">
        <div className={styles.sectionHeader}>
          <div className={styles.headerBadge}>Why Choose This Book?</div>
          <h2 className={styles.sectionTitle}>Why This Book?</h2>
          <p className={styles.sectionSubtitle}>
            Everything you need to master AI-powered humanoid robotics
          </p>
        </div>

        <div className={styles.propGrid}>
          {VALUE_PROPOSITIONS.map((prop, idx) => (
            <div
              key={prop.id}
              className={styles.propCard}
              style={{ animationDelay: `${idx * 0.1}s` }}
            >
              <div className={styles.cardGradientBorder}></div>
              <div className={styles.propBadge}>{prop.badge}</div>
              <div className={styles.iconWrapper}>
                <div className={styles.propIcon}>{prop.icon}</div>
                <div className={styles.iconGlow}></div>
              </div>
              <h3 className={styles.propTitle}>{prop.title}</h3>
              <p className={styles.propDescription}>{prop.description}</p>
              {prop.features && (
                <div className={styles.featuresList}>
                  {prop.features.map((feature, i) => (
                    <span key={i} className={styles.featureBadge}>
                      {feature}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
