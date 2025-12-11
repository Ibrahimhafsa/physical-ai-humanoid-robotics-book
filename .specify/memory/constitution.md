# AI & Physical Robotics Book Constitution

<!--
Sync Impact Report (v1.0.0 → v1.0.0)
=================================
- Initial constitution creation
- 6 core principles established
- 2 additional constraint sections added
- Governance framework defined
- Docusaurus content standards integrated
- No prior version; baseline establishment
-->

## Purpose

This constitution governs the **AI & Physical Robotics Book** project—an instructional resource designed to teach Physical AI, embodied intelligence, and humanoid robotics to beginners and intermediate learners using Docusaurus.

**Primary Goals:**
- Teach foundational concepts in physical AI and embodied intelligence
- Provide practical, engineering-focused instruction in humanoid robotics
- Create a clear, accessible learning path from beginner to intermediate
- Enable reproducible, testable examples and code samples
- Maintain high accuracy and safety standards in robotics guidance

## Core Principles

### I. Education-First Design

Every content piece—chapters, examples, diagrams, and code—must serve learner understanding. Prioritize clarity and accessibility for beginners; avoid jargon without explanation. Measure success by student comprehension, not feature completeness.

**Non-negotiable rules:**
- Concepts explained before use; prerequisites explicitly stated
- Real examples precede abstract theory
- Diagrams and visualizations mandatory for spatial/mechanical concepts
- Code samples must be runnable and include clear comments

**Rationale:** Effective instruction requires intentional architecture. Beginners lack domain knowledge; clarity enables learning momentum.

### II. Practical, Engineering-Focused Content

Content must ground theory in real physical systems. Every principle connects to actual hardware, simulation, or deployable code. Avoid purely theoretical chapters without practical application.

**Non-negotiable rules:**
- Robotics concepts tied to sim-to-real scenarios or real hardware
- Code samples run on standard platforms (Python 3.9+, ROS 2, simulator SDKs)
- Experiments and labs include success criteria and debugging guidance
- Performance/resource tradeoffs discussed (compute, power, latency)

**Rationale:** Physical AI is hardware-reality-bounded. Practical grounding teaches students actual constraints and trade-offs.

### III. Content Accuracy & Safety (Critical)

Robotics guidance carries safety implications. All technical content must be verified, and safety warnings must be explicit and prominent. Inaccuracy can cause harm.

**Non-negotiable rules:**
- Safety warnings precede any potentially hazardous operation (mechanical, electrical, control)
- Claims about hardware capabilities verified against datasheets or published benchmarks
- Control algorithms reviewed by domain experts before publication
- Deprecation/changes tracked; outdated guidance explicitly marked
- No hardcoded credentials, API keys, or tokens in examples

**Rationale:** Robotics learners will build and deploy systems. Incorrect guidance causes injury or system failure.

### IV. Docusaurus Standards & Consistency

All content is authored in Markdown and published via Docusaurus. Consistent structure and metadata ensure navigation, searchability, and maintainability.

**Non-negotiable rules:**
- All chapters organized under `docs/` with `.md` extension
- Metadata: frontmatter YAML (title, description, sidebar_position, tags) on every doc
- Cross-references use Docusaurus link syntax (e.g., `/docs/chapter-name`)
- Code blocks tagged with language; long blocks (>30 lines) extracted to example files
- Images stored in `docs/assets/` with descriptive filenames
- Sidebar navigation configured in `sidebars.js`; auto-discovery avoided

**Rationale:** Docusaurus consistency enables automatic generation of ToC, search, versioning, and multi-language support.

### V. Testable, Reproducible Examples

Every code example must be runnable and verifiable. Provide setup instructions, dependencies, and success criteria. Outdated examples break trust.

**Non-negotiable rules:**
- Code examples specify Python version, dependencies (in requirements.txt), and tested environments
- Multi-file examples organized in `examples/<chapter-slug>/` with README explaining setup
- Simulations include expected output or log excerpts for verification
- Deprecation notices added for outdated frameworks/libraries (e.g., ROS 1 vs. ROS 2)
- CI/linting configured to catch syntax errors in code blocks

**Rationale:** Learners trust hands-on examples. Broken code erodes credibility and wastes learning time.

### VI. Iterative Improvement & Community Feedback

Content is never "final." Feedback mechanisms (comments, issues, PRs) enable ongoing refinement. Track learner pain points and update accordingly.

**Non-negotiable rules:**
- Public issues/discussions enabled for typos, clarifications, and errors
- Contribution guidelines in `CONTRIBUTING.md` for community PRs
- Quarterly review of high-traffic chapters and feedback
- Version history maintained in `CHANGELOG.md`; major updates noted
- Versioned documentation enabled in Docusaurus for historical reference

**Rationale:** Learning materials improve with real-world use. Community feedback identifies gaps and errors faster than internal review.

## Content Organization & File Structure

**Directory Layout:**

```
docs/
├── intro.md                           # Welcome, learning path
├── 01-fundamentals/                   # Part I: Concepts
│   ├── what-is-physical-ai.md
│   ├── embodied-intelligence.md
│   └── ...
├── 02-humanoid-robotics/              # Part II: Humanoid systems
│   ├── anatomy-actuators.md
│   ├── kinematics-dynamics.md
│   └── ...
├── 03-control-simulation/             # Part III: Control & simulation
│   ├── feedback-control.md
│   ├── sim-frameworks.md
│   └── ...
├── 04-learning-ai/                    # Part IV: Learning & AI
│   ├── imitation-learning.md
│   ├── reinforcement-learning.md
│   └── ...
└── assets/                            # Images, diagrams, schematics
    ├── diagrams/
    ├── schematics/
    └── photos/

examples/
├── chapter-01-intro/                  # Runnable code samples
│   ├── README.md
│   ├── requirements.txt
│   └── *.py
├── chapter-02-kinematics/
│   └── ...
└── ...

sidebars.js                            # Docusaurus navigation config
docusaurus.config.js                   # Site configuration
CHANGELOG.md                           # Version history
CONTRIBUTING.md                        # Contribution guidelines
```

**File Naming Rules:**
- Filenames lowercase, hyphenated (e.g., `what-is-physical-ai.md`)
- Chapter files prefixed with order (e.g., `01-`, `02-`) for clarity
- Examples in `examples/<chapter-slug>/` with matching chapter reference

## Code Quality & Development Standards

### Language & Framework Requirements

- **Primary**: Python 3.9+ (robotics standard; accessible for learners)
- **Simulation**: CoppeliaSim, PyBullet, or Gazebo (open-source preference)
- **Robotics Middleware**: ROS 2 (Humble or LTS releases)
- **Supporting**: C++ for performance-critical sections (with Python bindings)
- **Visualization**: Matplotlib, RViz, or web-based (Three.js) for diagrams

### Code Review & Testing

- All code examples reviewed for correctness and security before merge
- Examples tested against stated environment (OS, Python version, dependencies)
- No external secrets or API keys in example code; use `.env` files with `.env.example` template
- Linting: `pylint` or `flake8` for Python; C++ adheres to ROS style guide

### Documentation in Code

- Functions/classes: docstring with purpose, parameters, return type, example usage
- Complex algorithms: inline comments explaining mathematical or control logic
- Safety-critical sections: `# WARNING:` comment block with implications
- Deprecations: `# DEPRECATED: use X instead` with migration note

## Safety & Accuracy Guidelines

### Hardware & Control Safety

- **Mechanical**: Warn about pinch points, high-speed motion, tool-like appendages
- **Electrical**: Note voltage/current hazards; ground requirements
- **Control**: Unstable controllers can cause oscillation/runaway; testing prerequisites stated
- **Simulation Gaps**: Explicitly note where simulation differs from reality (friction, timing, latency)

### Content Verification Process

1. **Initial Draft**: Author writes content with references to sources
2. **Technical Review**: Domain expert reviews for accuracy (roboticist, controls engineer, AI researcher)
3. **Learner Testing**: (Optional for critical content) Test with 1-2 learners; note confusion points
4. **Publish & Monitor**: Collect feedback; issue/PR for corrections
5. **Quarterly Audit**: Review high-traffic chapters for deprecations or corrections

### Source Attribution

- Academic papers: full citation (DOI when available)
- Hardware datasheets: product name, version, link
- Open-source code: license and repository link
- Simulation tools: version used for examples

## Governance

### Constitution Authority

This constitution supersedes all prior practices and informal agreements. All development, content creation, and decision-making must align with these principles. Violations are grounds for review and revision.

### Amendment Process

1. **Proposal**: Issue or PR proposing amendment with rationale
2. **Justification**: Explain why current principle(s) insufficient or outdated
3. **Impact**: List affected processes, files, and team practices
4. **Approval**: Unanimous consensus on amendment; if blocked, escalate to project lead
5. **Implementation**: Migrate all dependent artifacts (specs, tasks, existing chapters)
6. **Documentation**: Version bump, CHANGELOG entry, PHR record

### Versioning Policy

- **MAJOR** (e.g., 1.0.0 → 2.0.0): Principle removal, redefinition, or governance restructure
- **MINOR** (e.g., 1.0.0 → 1.1.0): New principle added, section expanded, material guidance change
- **PATCH** (e.g., 1.0.0 → 1.0.1): Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review

- **Quarterly**: Review new chapters/examples against constitution principles
- **Per-PR**: Maintainers verify content meets education, safety, and Docusaurus standards
- **Annual**: Full audit of deprecated guidance, technology shifts, and learner feedback trends

### Role & Tools

- **Claude Code (Agent)**: Primary implementer; executes spec-driven development, maintains artifacts, enforces principles
- **Project Lead**: Arbitrates amendment disputes; approves major version changes
- **Domain Experts**: Review technical accuracy and safety claims
- **Community**: Submits issues/PRs for corrections and improvements

**Version**: 1.0.0 | **Ratified**: 2025-12-11 | **Last Amended**: 2025-12-11
