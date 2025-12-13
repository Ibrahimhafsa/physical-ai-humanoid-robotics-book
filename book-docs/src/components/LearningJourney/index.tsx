/**
 * LearningJourney Component
 * Interactive timeline showing the learning progression through the book
 * with visual indicators and smooth animations
 */

import styles from './styles.module.css';

interface JourneyStep {
  id: string;
  phase: string;
  title: string;
  description: string;
  icon: string;
}

const JOURNEY_STEPS: JourneyStep[] = [
  {
    id: 'phase1',
    phase: '01',
    title: 'Fundamentals',
    description: 'Understand the core concepts of physical AI, robotics, and how systems interact.',
    icon: '📖',
  },
  {
    id: 'phase2',
    phase: '02',
    title: 'ROS 2 & Architecture',
    description: 'Master the Robot Operating System 2, middleware patterns, and distributed communication.',
    icon: '⚙️',
  },
  {
    id: 'phase3',
    phase: '03',
    title: 'Digital Twins & Simulation',
    description: 'Build realistic simulations using Gazebo and Unity for safe robot development.',
    icon: '🎮',
  },
  {
    id: 'phase4',
    phase: '04',
    title: 'AI & Perception',
    description: 'Implement computer vision, deep learning, and intelligent decision-making systems.',
    icon: '🧠',
  },
  {
    id: 'phase5',
    phase: '05',
    title: 'Advanced Integration',
    description: 'Deploy production systems using Vision-Language-Action models and reinforcement learning.',
    icon: '🚀',
  },
];

/**
 * LearningJourney - Displays the 5-phase learning progression
 * Features:
 * - Vertical timeline on desktop, linear on mobile
 * - Alternating left-right layout for visual interest
 * - Smooth animations with staggered entrance
 * - Phase indicators with icons
 * - Responsive and accessible design
 */
export default function LearningJourney(): JSX.Element {
  return (
    <section className={styles.journeySection}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Your Learning Journey</h2>
          <p className={styles.sectionSubtitle}>
            A structured path from basics to advanced robotics mastery
          </p>
        </div>

        <div className={styles.timeline}>
          {JOURNEY_STEPS.map((step, idx) => (
            <div key={step.id} className={`${styles.timelineItem} ${idx % 2 === 0 ? styles.left : styles.right}`}>
              <div className={styles.timelineMarker}>
                <div className={styles.markerIcon}>{step.icon}</div>
                <div className={styles.markerPhase}>{step.phase}</div>
              </div>
              <div className={styles.timelineContent}>
                <h3 className={styles.stepTitle}>{step.title}</h3>
                <p className={styles.stepDescription}>{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
