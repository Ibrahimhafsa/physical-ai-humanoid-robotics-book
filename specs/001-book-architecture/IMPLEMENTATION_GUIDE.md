# Implementation Guide: Book Architecture & Content Structure

**Date**: 2025-12-11
**Status**: Ready for Development
**Target**: Phase 1 & Phase 2 Execution

This guide provides concrete implementation examples for the AI & Physical Robotics Book using Docusaurus v3.

---

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Chapter Markdown Template](#chapter-markdown-template)
3. [Docusaurus Configuration](#docusaurus-configuration)
4. [Sidebar Configuration](#sidebar-configuration)
5. [React/TypeScript Components](#reacttypescript-components)
6. [JSON Schemas](#json-schemas)
7. [Example Module Setup](#example-module-setup)
8. [Code Examples Integration](#code-examples-integration)

---

## Directory Structure

### Complete Project Layout

```
humanoid-robotics/ai-physical-robotics-book/
├── docs/                                    # Content chapters
│   ├── intro.md                             # Book introduction and learning path
│   ├── 01-fundamentals/                     # Module 1: Concepts (3-4 chapters)
│   │   ├── _category_.json                  # Module category config
│   │   ├── what-is-physical-ai.md           # Chapter 1
│   │   ├── embodied-intelligence.md         # Chapter 2
│   │   ├── basics-of-robotics.md            # Chapter 3
│   │   └── assets/                          # Module 1 diagrams
│   │       ├── what-is-physical-ai/
│   │       │   ├── physical-ai-diagram.svg
│   │       │   └── embodiment-flowchart.png
│   │       ├── embodied-intelligence/
│   │       └── basics-of-robotics/
│   │
│   ├── 02-humanoid-robotics/                # Module 2: ROS 2 (4-5 chapters)
│   │   ├── _category_.json
│   │   ├── ros2-architecture.md             # Chapter 1
│   │   ├── nodes-and-topics.md              # Chapter 2
│   │   ├── robot-control-basics.md          # Chapter 3
│   │   ├── kinematics-and-dynamics.md       # Chapter 4
│   │   ├── navigation-and-planning.md       # Chapter 5
│   │   └── assets/
│   │       ├── ros2-architecture/
│   │       ├── nodes-and-topics/
│   │       ├── robot-control-basics/
│   │       ├── kinematics-and-dynamics/
│   │       └── navigation-and-planning/
│   │
│   ├── 03-digital-twin/                     # Module 3: Digital Twin (4 chapters)
│   │   ├── _category_.json
│   │   ├── simulation-fundamentals.md
│   │   ├── gazebo-setup-tutorial.md
│   │   ├── unity-robotics-intro.md
│   │   ├── physics-simulation.md
│   │   └── assets/
│   │
│   ├── 04-ai-brain/                         # Module 4: NVIDIA Isaac (4 chapters)
│   │   ├── _category_.json
│   │   ├── nvidia-isaac-overview.md
│   │   ├── computer-vision-basics.md
│   │   ├── deep-learning-robotics.md
│   │   ├── reinforcement-learning.md
│   │   └── assets/
│   │
│   ├── 05-vla/                              # Module 5: VLA (3 chapters)
│   │   ├── _category_.json
│   │   ├── multimodal-learning.md
│   │   ├── language-grounding.md
│   │   ├── end-to-end-robotics.md
│   │   └── assets/
│   │
│   └── assets/                              # Shared assets
│       ├── diagrams/
│       ├── schematics/
│       └── photos/
│
├── examples/                                # Code examples
│   ├── chapter-01-physical-ai/
│   │   ├── README.md                        # Setup and run instructions
│   │   ├── requirements.txt                 # Python dependencies
│   │   ├── simple_simulation.py             # Example code
│   │   └── expected_output.txt              # Expected console output
│   │
│   ├── chapter-02-ros2-basics/
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── ros2_node_example.py
│   │   └── expected_output.txt
│   │
│   ├── capstone-module-1/
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── integration_test.py
│   │   └── expected_output.txt
│   │
│   └── ... (more examples for each chapter and capstone)
│
├── src/                                     # React/TypeScript components
│   ├── components/
│   │   ├── LearningObjectives.tsx           # Learning objectives component
│   │   ├── PrerequisiteCard.tsx             # Prerequisite warning component
│   │   ├── NextChapterButton.tsx            # Navigation component
│   │   ├── CodeTabs.tsx                     # Code block tabs
│   │   ├── DeprecationBanner.tsx            # Version deprecation warning
│   │   └── ProgressIndicator.tsx            # Learning progress tracker
│   │
│   ├── types/
│   │   ├── chapter.ts                       # TypeScript interfaces
│   │   └── module.ts
│   │
│   └── styles/
│       ├── components.css                   # Component styling
│       └── book-theme.css                   # Custom theme
│
├── .github/
│   ├── workflows/
│   │   ├── validate-book.yml                # Docusaurus build validation
│   │   ├── validate-examples.yml            # Python linting + execution
│   │   ├── deploy-to-pages.yml              # GitHub Pages deployment
│   │   └── check-links.yml                  # Link validation
│   │
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── correction.md
│       ├── feedback.md
│       └── feature_request.md
│
├── .specify/
│   ├── templates/
│   │   ├── chapter-template.md              # Chapter authoring template
│   │   ├── code-example-template.py         # Code example template
│   │   ├── exercise-template.md             # Exercise template
│   │   └── capstone-template.md             # Capstone project template
│   │
│   ├── scripts/
│   │   ├── validate-frontmatter.sh          # Frontmatter YAML validation
│   │   ├── validate-custom-path.sh          # Custom learning path validation
│   │   └── generate-custom-path.sh          # Custom path generator
│   │
│   └── memory/
│       └── constitution.md                  # Project governance
│
├── docusaurus.config.js                     # Main Docusaurus configuration
├── sidebars.js                              # Sidebar navigation (auto-generated)
├── package.json                             # Node.js dependencies
├── tsconfig.json                            # TypeScript configuration
├── .eslintrc.json                           # ESLint configuration
├── .prettierrc.json                         # Prettier configuration
├── .gitignore                               # Git ignore patterns
├── CONTRIBUTING.md                          # Contributor guidelines
├── CHANGELOG.md                             # Version history
├── LICENSE                                  # Project license
├── README.md                                # Repository overview
├── ENVIRONMENT.md                           # Environment setup
├── AUTHORING_GUIDE.md                       # Author guidelines
├── PREREQUISITES.md                         # Learning path matrix
├── SIDEBAR.md                               # Sidebar structure documentation
└── i18n/                                    # Internationalization
    ├── en/
    │   └── docusaurus.json                  # English translations
    ├── es/
    │   └── docusaurus.json                  # Spanish (placeholder)
    └── zh/
        └── docusaurus.json                  # Chinese (placeholder)
```

---

## Chapter Markdown Template

### File: `.specify/templates/chapter-template.md`

```markdown
---
title: "Chapter Title: Brief Descriptive Title"
description: "One-sentence description of what learners will understand after this chapter"
sidebar_position: 1
tags: ["ROS 2", "robotics", "architecture"]
module: "humanoid-robotics"
estimated_time: "120 minutes"
prerequisites: ["01-fundamentals/basics-of-robotics"]
difficulty_level: "beginner"
authors: ["Author Name"]
last_updated: "2025-12-11"
---

# Chapter Title: Brief Descriptive Title

:::info
**Estimated Time**: 120 minutes | **Difficulty**: Beginner | **Status**: Draft
:::

## Learning Objectives

After completing this chapter, learners will be able to:

- **Understand** the core concepts of [topic]
- **Explain** how [concept] relates to [related topic]
- **Implement** a basic [system/component] using [tools/frameworks]
- **Troubleshoot** common issues with [topic]

:::warning
**Prerequisites Required**: Ensure you have completed [prerequisite chapter] before starting this chapter. You should understand [specific prerequisite knowledge].
:::

---

## Lesson Content

### What is [Topic]?

[Clear explanation of the concept, starting with real-world examples before abstract theory]

Real example: [Concrete example from robotics or simulation]

### Key Concepts

- **Concept 1**: Definition and significance
- **Concept 2**: How it relates to Concept 1
- **Concept 3**: Practical applications

:::tip
**Pro Tip**: [Helpful hint based on common learner questions]
:::

### Why This Matters

[Explanation of relevance to physical AI, robotics, or learning objectives]

---

## Code Examples

This section includes working code examples demonstrating the concepts above.

:::note
All code examples are tested and runnable. See the [examples folder](../../examples/chapter-slug/) for complete setup instructions.
:::

### Example 1: [Brief Description]

```python
# File: examples/chapter-slug/example1.py
# Description: [What this example demonstrates]
# Environment: Python 3.9+, Ubuntu 20.04, ROS 2 Humble

import sys

def main():
    """Main function demonstrating [concept]"""
    print("Hello, Robotics!")

if __name__ == "__main__":
    main()
```

**Expected Output:**
```
Hello, Robotics!
```

**Run This Example:**
```bash
cd examples/chapter-slug
pip install -r requirements.txt
python example1.py
```

### Example 2: [Brief Description]

[Similar structure for second code example]

---

## Exercises

Complete these exercises to reinforce your understanding.

### Exercise 1: [Exercise Title] (Beginner, 20 minutes)

**Learning Objective**: Practice implementing [concept]

**Task Description:**
Modify the code example above to [specific modification]. Your implementation should:
- Input: [What the learner needs to provide]
- Output: [Expected output or behavior]
- Acceptance Criteria:
  - [ ] Code runs without errors
  - [ ] Output matches expected behavior
  - [ ] Code is commented explaining key steps

**Hints:**
- Start by reviewing Example 1
- Look for the [specific part] to modify
- Test with [test case] to verify your solution

---

### Exercise 2: [Exercise Title] (Intermediate, 45 minutes)

[Similar structure for more complex exercise]

---

### Exercise 3: [Exercise Title] (Advanced, 60 minutes)

[Similar structure for advanced exercise]

---

## Capstone Guidance

This chapter contributes to the Module Capstone Project: "[Capstone Name]"

**Concepts from this chapter used in the capstone:**
- [Concept 1]: Used for [specific purpose]
- [Concept 2]: Required for [specific component]

**Next Steps After This Chapter:**
- Complete the exercises above
- Review the prerequisites for [Next Chapter]
- Consider how [concept] applies to [related module]

---

## Safety Warnings

:::danger
**SAFETY ALERT**: If this chapter covers mechanical/electrical/control systems:

**Mechanical Hazards:**
- [Specific hazard] - Risk: [injury type]
- Mitigation: [safety measure]

**Electrical Hazards:**
- [Specific hazard] - Risk: [shock/fire/etc]
- Mitigation: [safety measure]

**Control System Hazards:**
- [Specific hazard] - Risk: [unintended movement/damage]
- Mitigation: [safety measure and testing procedures]

**Simulation Differences:**
- This chapter uses [simulator name], which differs from real hardware in:
  - Friction model: [difference]
  - Latency: [difference]
  - Sensor accuracy: [difference]
:::

---

## References & Attribution

### Academic Papers
- [Author et al., "Paper Title"](https://doi.org/xxxx.xxxx) - Published in [Journal/Conference]

### Hardware Datasheets
- [Robot/Component Name](link-to-datasheet) - Version [X.X]

### Software Documentation
- [Library/Framework Name](link-to-docs) - Version [X.X]

### Open-Source Code
- [Code Repository](link-to-repo) - License: [MIT/GPL/etc]

---

## Troubleshooting

### Common Issue 1: [Error Message]

**Cause:** [Why this happens]

**Solution:**
1. Check [first step]
2. Verify [second step]
3. Run [diagnostic command]

---

### Common Issue 2: [Another Common Problem]

[Similar structure]

---

## What's Next?

You've completed **[Chapter Name]**. Next, you're ready for:

:::tip
**Recommended**: [Next Chapter Name] - Estimated time: [X] minutes

**Alternative Path**: [Alternative Chapter] if you're interested in [topic]

**Prerequisites for Next Chapter**: You should understand [concepts from this chapter]
:::

---

## Feedback

We'd love to hear from you! If you found errors, unclear explanations, or have suggestions:

- [Report an Issue](link-to-github-issues)
- [Join the Discussion](link-to-discussions)
- [Contribute a Fix](link-to-contributing)

---

## Progress Tracking

```
Module: [Module Name]
Chapter: [Chapter Number] of [Total Chapters]
Estimated Progress: [X]% of module
```
```

---

## Code Example Template

### File: `.specify/templates/code-example-template.py`

```python
"""
================================================================================
Code Example: [Example Title]
================================================================================

Description:
    This example demonstrates [what it teaches], showing how to [what it does].

Chapter:
    [Module Number]/[Chapter Name] - [Chapter Title]
    Link: ../../docs/[module-slug]/[chapter-slug].md

Environment:
    - Python Version: 3.9+
    - OS: Ubuntu 20.04 LTS (or macOS 12+, Windows 10+)
    - ROS 2: Humble (or Foxy, Iron as applicable)
    - Simulators: PyBullet 3.2+, Gazebo Harmonic
    - Dependencies: See requirements.txt

Tested On:
    ✓ Ubuntu 20.04 + Python 3.10 + ROS 2 Humble
    ✓ macOS 12 + Python 3.11
    ✗ Windows 10 (WSL2 recommended)

Setup Instructions:
    1. Navigate to examples/chapter-slug/
    2. Install dependencies: pip install -r requirements.txt
    3. Run example: python code-example-template.py
    4. Expected output: See EXPECTED_OUTPUT section below

Expected Output:
    [Paste expected console output here]

Troubleshooting:
    Q: I get ImportError for [module]
    A: Install missing dependency: pip install [module]

    Q: [Common issue]
    A: [Solution]

================================================================================
"""

import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ExampleClass:
    """
    Example class demonstrating [concept].

    Attributes:
        param1 (str): Description of parameter 1
        param2 (int): Description of parameter 2
    """

    def __init__(self, param1: str, param2: int):
        """Initialize the example class.

        Args:
            param1: First parameter
            param2: Second parameter

        Raises:
            ValueError: If param2 is negative
        """
        if param2 < 0:
            raise ValueError("param2 must be non-negative")

        self.param1 = param1
        self.param2 = param2
        logger.info(f"ExampleClass initialized with param1={param1}, param2={param2}")

    def demonstrate_concept(self) -> str:
        """
        Demonstrate the main concept of this example.

        Returns:
            str: Result of the demonstration
        """
        logger.debug("Starting concept demonstration")
        result = f"{self.param1} with value {self.param2}"
        logger.info(f"Demonstration complete: {result}")
        return result


def main():
    """
    Main execution function.

    This function:
    1. Creates an instance of ExampleClass
    2. Calls the demonstration method
    3. Prints the result
    """
    try:
        # Step 1: Create instance
        logger.info("Creating ExampleClass instance...")
        example = ExampleClass("demo", 42)

        # Step 2: Run demonstration
        logger.info("Running demonstration...")
        result = example.demonstrate_concept()

        # Step 3: Print results
        print(f"\n=== RESULT ===")
        print(f"Output: {result}")
        print(f"Success: True\n")

        return 0

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        print(f"\n=== ERROR ===")
        print(f"Error: {e}\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
```

---

## Exercise Template

### File: `.specify/templates/exercise-template.md`

```markdown
# Exercise: [Exercise Title]

**Difficulty**: Beginner | **Time**: 15 minutes | **Learning Objective**: [Objective]

## Background

[Context and why this exercise is important]

## Task Description

You need to [specific task]. Your implementation should:

### Input
```python
# You'll be given:
input_data = [...]
```

### Expected Output
```python
# Your code should produce:
output = [...]
```

### Acceptance Criteria

- [ ] Code executes without errors
- [ ] Output matches expected result
- [ ] Code includes comments explaining key steps
- [ ] Time limit: [X] minutes

## Hints

Start with Example 2 from the lesson. Look for the part where [concept]. Test your changes with [test case].

## Solution Template

```python
def solve_exercise(input_data):
    """Your solution here"""
    result = None
    # TODO: Implement solution
    return result

# Test your solution
if __name__ == "__main__":
    test_input = [...]
    result = solve_exercise(test_input)
    print(f"Result: {result}")
```

## Verification

Run your solution:
```bash
python your_solution.py
```

Compare your output with the expected output. If they match, exercise complete!

## Next Steps

- [ ] Solution runs without errors
- [ ] Output matches expected
- [ ] Code is well-commented
- [ ] Ready for next exercise
```

---

## Docusaurus Configuration

### File: `docusaurus.config.js`

```javascript
// @ts-check
// `@type` JSDoc annotations allow better IDE support

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI & Physical Robotics Book',
  tagline: 'Learn Physical AI, Embodied Intelligence, and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/ai-physical-robotics-book/',

  // GitHub pages deployment config.
  organizationName: 'your-username',
  projectName: 'ai-physical-robotics-book',
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'zh'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      es: {
        label: 'Español',
        direction: 'ltr',
      },
      zh: {
        label: '中文',
        direction: 'ltr',
      },
    },
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-username/ai-physical-robotics-book/tree/main/',
          // Enable versions
          lastVersion: 'current',
          versions: {
            current: {
              label: 'main (unstable)',
            },
          },
        },
        blog: false, // Disable blog
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your own image
      image: 'img/book-social-card.jpg',
      navbar: {
        title: '🤖 AI & Robotics Book',
        logo: {
          alt: 'Book Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'bookSidebar',
            position: 'left',
            label: 'Learn',
          },
          {
            href: 'https://github.com/your-username/ai-physical-robotics-book',
            label: 'GitHub',
            position: 'right',
          },
          {
            type: 'localeDropdown',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Modules',
            items: [
              {
                label: 'Fundamentals',
                to: '/docs/intro',
              },
              {
                label: 'ROS 2',
                to: '/docs/02-humanoid-robotics/ros2-architecture',
              },
              {
                label: 'Digital Twin',
                to: '/docs/03-digital-twin/simulation-fundamentals',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Discussions',
                href: 'https://github.com/your-username/ai-physical-robotics-book/discussions',
              },
              {
                label: 'Report Issues',
                href: 'https://github.com/your-username/ai-physical-robotics-book/issues',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Contributing',
                to: '/CONTRIBUTING',
              },
              {
                label: 'License',
                href: 'https://github.com/your-username/ai-physical-robotics-book/blob/main/LICENSE',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AI & Physical Robotics Contributors. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['bash', 'python', 'yaml', 'json'],
      },
      // Search configuration
      algolia: {
        // The application ID provided by Algolia
        appId: 'YOUR_ALGOLIA_APP_ID',

        // Public API key: it is safe to commit it
        apiKey: 'YOUR_ALGOLIA_API_KEY',

        indexName: 'ai-robotics-book',

        // Optional: see doc section below
        contextualSearch: true,

        // Optional: Specify domains where the docs should be searchable;
        // otherwise the current domain is used
        searchPagePath: 'search',
      },
    }),

  plugins: [
    [
      'docusaurus-auto-sidebar',
      {
        ignoreIndex: true,
      },
    ],
  ],

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
};

module.exports = config;
```

---

## Sidebar Configuration

### File: `sidebars.js`

```javascript
/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a set of docs in the sidebar
 - provide next/previous navigation

 The sidebars can be generated from the file structure automatically with the
 `docusaurus-auto-sidebar` plugin.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  bookSidebar: [
    {
      type: 'ref',
      id: 'intro',
    },
    {
      type: 'category',
      label: '01 Fundamentals: Concepts',
      items: [
        'fundamentals/what-is-physical-ai',
        'fundamentals/embodied-intelligence',
        'fundamentals/basics-of-robotics',
      ],
    },
    {
      type: 'category',
      label: '02 Humanoid Robotics: ROS 2',
      items: [
        'humanoid-robotics/ros2-architecture',
        'humanoid-robotics/nodes-and-topics',
        'humanoid-robotics/robot-control-basics',
        'humanoid-robotics/kinematics-and-dynamics',
        'humanoid-robotics/navigation-and-planning',
      ],
    },
    {
      type: 'category',
      label: '03 Digital Twin: Gazebo & Unity',
      items: [
        'digital-twin/simulation-fundamentals',
        'digital-twin/gazebo-setup-tutorial',
        'digital-twin/unity-robotics-intro',
        'digital-twin/physics-simulation',
      ],
    },
    {
      type: 'category',
      label: '04 AI Brain: NVIDIA Isaac',
      items: [
        'ai-brain/nvidia-isaac-overview',
        'ai-brain/computer-vision-basics',
        'ai-brain/deep-learning-robotics',
        'ai-brain/reinforcement-learning',
      ],
    },
    {
      type: 'category',
      label: '05 VLA: Vision-Language-Action',
      items: [
        'vla/multimodal-learning',
        'vla/language-grounding',
        'vla/end-to-end-robotics',
      ],
    },
  ],
};

module.exports = sidebars;
```

---

## React/TypeScript Components

### Learning Objectives Component

**File: `src/components/LearningObjectives.tsx`**

```typescript
import React from 'react';
import styles from './LearningObjectives.module.css';

interface LearningObjectivesProps {
  objectives: string[];
  className?: string;
}

export default function LearningObjectives({
  objectives,
  className = '',
}: LearningObjectivesProps): JSX.Element {
  return (
    <div className={`${styles.container} ${className}`}>
      <h3 className={styles.title}>📚 Learning Objectives</h3>
      <ul className={styles.list}>
        {objectives.map((objective, index) => (
          <li key={index} className={styles.item}>
            <span className={styles.bullet}>✓</span>
            {objective}
          </li>
        ))}
      </ul>
      <p className={styles.subtitle}>
        After completing this chapter, you will be able to understand and apply these concepts.
      </p>
    </div>
  );
}
```

**CSS Module: `src/components/LearningObjectives.module.css`**

```css
.container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-left: 5px solid #667eea;
  border-radius: 8px;
  padding: 20px 24px;
  margin: 20px 0;
  color: white;
}

.title {
  margin: 0 0 12px 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0 0 12px 0;
}

.item {
  margin: 8px 0;
  display: flex;
  align-items: flex-start;
  line-height: 1.6;
}

.bullet {
  margin-right: 10px;
  font-weight: bold;
  flex-shrink: 0;
}

.subtitle {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
}
```

### Prerequisite Card Component

**File: `src/components/PrerequisiteCard.tsx`**

```typescript
import React from 'react';
import Link from '@docusaurus/Link';
import styles from './PrerequisiteCard.module.css';

interface PrerequisiteCardProps {
  prerequisites: Array<{
    title: string;
    path: string;
    description: string;
  }>;
  className?: string;
}

export default function PrerequisiteCard({
  prerequisites,
  className = '',
}: PrerequisiteCardProps): JSX.Element {
  if (prerequisites.length === 0) {
    return <></>;
  }

  return (
    <div className={`${styles.container} ${className}`}>
      <div className={styles.header}>
        <span className={styles.icon}>⚠️</span>
        <h3 className={styles.title}>Prerequisites Required</h3>
      </div>
      <p className={styles.description}>
        Make sure you've completed these chapters before starting:
      </p>
      <ul className={styles.list}>
        {prerequisites.map((prereq, index) => (
          <li key={index} className={styles.item}>
            <Link to={prereq.path} className={styles.link}>
              {prereq.title}
            </Link>
            <p className={styles.itemDescription}>{prereq.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Next Chapter Button Component

**File: `src/components/NextChapterButton.tsx`**

```typescript
import React from 'react';
import Link from '@docusaurus/Link';
import styles from './NextChapterButton.module.css';

interface NextChapterProps {
  nextChapterPath: string;
  nextChapterTitle: string;
  currentChapter: string;
  estimatedTime?: number;
}

export default function NextChapterButton({
  nextChapterPath,
  nextChapterTitle,
  currentChapter,
  estimatedTime = 120,
}: NextChapterProps): JSX.Element {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <p className={styles.label}>You've completed {currentChapter}</p>
        <h3 className={styles.nextTitle}>What's Next?</h3>
        <p className={styles.description}>
          Continue your learning journey with the next chapter. Estimated time: {estimatedTime} minutes.
        </p>
      </div>
      <Link to={nextChapterPath} className={styles.button}>
        <span className={styles.buttonText}>{nextChapterTitle}</span>
        <span className={styles.arrow}>→</span>
      </Link>
    </div>
  );
}
```

### Code Tabs Component

**File: `src/components/CodeTabs.tsx`**

```typescript
import React from 'react';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';

interface CodeExample {
  language: string;
  label: string;
  code: string;
}

interface CodeTabsProps {
  examples: CodeExample[];
  title?: string;
}

export default function CodeTabs({
  examples,
  title = 'Code Examples',
}: CodeTabsProps): JSX.Element {
  return (
    <div>
      {title && <h3>{title}</h3>}
      <Tabs>
        {examples.map((example, index) => (
          <TabItem key={index} value={example.language} label={example.label}>
            <CodeBlock language={example.language}>
              {example.code}
            </CodeBlock>
          </TabItem>
        ))}
      </Tabs>
    </div>
  );
}
```

---

## JSON Schemas

### Chapter Frontmatter Schema

**File: `specs/001-book-architecture/contracts/chapter-schema.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Book Chapter Schema",
  "description": "Schema for chapter frontmatter YAML validation",
  "type": "object",
  "required": [
    "title",
    "description",
    "sidebar_position",
    "tags",
    "module",
    "estimated_time",
    "difficulty_level"
  ],
  "properties": {
    "title": {
      "type": "string",
      "description": "Chapter title with optional subtitle",
      "minLength": 5,
      "maxLength": 100,
      "pattern": "^[A-Z][^:]*: [A-Z].*$"
    },
    "description": {
      "type": "string",
      "description": "One-sentence description of chapter content",
      "minLength": 10,
      "maxLength": 200
    },
    "sidebar_position": {
      "type": "integer",
      "description": "Order within module (1, 2, 3, etc.)",
      "minimum": 1,
      "maximum": 10
    },
    "tags": {
      "type": "array",
      "description": "Tags for categorization and search",
      "items": {
        "type": "string"
      },
      "minItems": 1,
      "maxItems": 5
    },
    "module": {
      "type": "string",
      "description": "Module identifier",
      "enum": [
        "fundamentals",
        "humanoid-robotics",
        "digital-twin",
        "ai-brain",
        "vla"
      ]
    },
    "estimated_time": {
      "type": "string",
      "description": "Estimated reading and exercise time",
      "pattern": "^[0-9]+ (minutes|hours)$"
    },
    "difficulty_level": {
      "type": "string",
      "description": "Difficulty level for learners",
      "enum": ["beginner", "intermediate", "advanced"]
    },
    "prerequisites": {
      "type": "array",
      "description": "Required prior chapters",
      "items": {
        "type": "string",
        "pattern": "^[0-9]{2}-[a-z-]+/[a-z-]+$"
      }
    },
    "authors": {
      "type": "array",
      "description": "Chapter authors",
      "items": {
        "type": "string"
      }
    },
    "last_updated": {
      "type": "string",
      "description": "Last update date",
      "format": "date"
    }
  }
}
```

### Module Configuration Schema

**File: `specs/001-book-architecture/contracts/module-schema.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Book Module Schema",
  "description": "Schema for module configuration",
  "type": "object",
  "required": ["id", "title", "description", "chapters"],
  "properties": {
    "id": {
      "type": "string",
      "enum": [
        "01-fundamentals",
        "02-humanoid-robotics",
        "03-digital-twin",
        "04-ai-brain",
        "05-vla"
      ]
    },
    "title": {
      "type": "string",
      "description": "Module title"
    },
    "description": {
      "type": "string",
      "description": "Module overview"
    },
    "estimated_hours": {
      "type": "number",
      "description": "Total estimated hours for module"
    },
    "chapters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title"],
        "properties": {
          "id": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "slug": {
            "type": "string"
          }
        }
      }
    },
    "capstone_project": {
      "type": "object",
      "required": ["title", "description"],
      "properties": {
        "title": {
          "type": "string"
        },
        "description": {
          "type": "string"
        }
      }
    }
  }
}
```

---

## Example Module Setup

### Module 1: Fundamentals (`_category_.json`)

**File: `docs/01-fundamentals/_category_.json`**

```json
{
  "label": "01 Fundamentals: Concepts",
  "position": 1,
  "collapsed": false,
  "collapsible": true,
  "description": "Build your foundation in Physical AI and robotics fundamentals. Start here if you're new to the field."
}
```

### Example Chapter Structure

**File: `docs/01-fundamentals/what-is-physical-ai.md`**

```markdown
---
title: "What is Physical AI: Understanding Embodied Intelligence"
description: "Learn the fundamental concepts of Physical AI and why embodied systems differ from traditional AI"
sidebar_position: 1
tags: ["physical-ai", "embodied-intelligence", "fundamentals"]
module: "fundamentals"
estimated_time: "90 minutes"
prerequisites: []
difficulty_level: "beginner"
authors: ["Book Team"]
last_updated: "2025-12-11"
---

import LearningObjectives from '@site/src/components/LearningObjectives';
import PrerequisiteCard from '@site/src/components/PrerequisiteCard';
import CodeTabs from '@site/src/components/CodeTabs';

<LearningObjectives objectives={[
  "Define Physical AI and embodied intelligence",
  "Understand how physical constraints shape intelligence",
  "Recognize the differences between simulated and real-world systems",
  "Identify applications of Physical AI in robotics"
]} />

<PrerequisiteCard prerequisites={[]} />

## What is Physical AI?

Physical AI refers to intelligent systems that interact with and learn from the physical world...

[Rest of chapter content]
```

---

## Code Examples Integration

### Example: Python Requirements File

**File: `examples/chapter-02-ros2-basics/requirements.txt`**

```
# ROS 2 dependencies for ROS 2 Basics chapter examples
# Python 3.9+

# ROS 2 client library
rclpy==0.13.4

# ROS 2 message types
geometry-msgs==0.13.0
std-msgs==0.13.0

# Utilities
numpy==1.24.3
pyyaml==6.0

# Testing
pytest==7.3.1
pytest-cov==4.1.0

# Development tools
pylint==2.17.4
black==23.3.0
```

### Example: Code Block with Execution

**In a chapter markdown file:**

```markdown
## Example: Creating a ROS 2 Node

```python
# File: examples/chapter-02-ros2-basics/ros2_node_example.py
# Python 3.9+, ROS 2 Humble

import rclpy
from rclpy.node import Node

class SimpleNode(Node):
    def __init__(self):
        super().__init__('simple_node')
        self.get_logger().info('Node created!')

def main(args=None):
    rclpy.init(args=args)
    node = SimpleNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run this example:**

```bash
cd examples/chapter-02-ros2-basics
pip install -r requirements.txt
python ros2_node_example.py
```

**Expected output:**

```
[INFO] [simple_node]: Node created!
```
```

---

## Summary

This implementation guide provides:

✅ **Complete directory structure** for 5 modules with 15-20 chapters
✅ **Chapter markdown template** with all required sections
✅ **Docusaurus v3 configuration** with versioning and i18n
✅ **React/TypeScript components** for interactive learning
✅ **JSON schemas** for metadata validation
✅ **Code example organization** with Python setup
✅ **Exercise and capstone templates** for learner practice

Use these templates and examples as references when implementing Phase 1 & Phase 2 of the task list. Each file shows the exact structure, format, and content expected for the book project.

