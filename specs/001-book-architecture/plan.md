# Implementation Plan: Book Architecture & Content Structure

**Branch**: `001-book-architecture` | **Date**: 2025-12-11 | **Spec**: [specs/001-book-architecture/spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-book-architecture/spec.md`

## Summary

Implement a 4-module robotics book architecture using Docusaurus v3 with a structured content model, auto-generated navigation, versioning support, and internationalization. The plan progresses through environment setup, Docusaurus configuration, content structure creation, authoring guidelines, testing infrastructure, deployment, and final reporting.

**Technical Approach**:
- Docusaurus v3+ for publication (auto-sidebar generation, versioning, i18n)
- Markdown + YAML frontmatter for content (standardized metadata)
- Python 3.9+ and ROS 2 Humble for code examples
- GitHub Pages for hosting (auto-deploy on main branch)
- GitHub Actions CI/CD for linting, validation, and build verification
- MDX components for interactive content (code tabs, admonitions, prompts)

## Technical Context

**Language/Version**: Markdown (content), JavaScript/TypeScript (Docusaurus config), Python 3.9+ (code examples)

**Primary Dependencies**:
- Docusaurus v3.x (publication platform)
- Node.js 18+ (build tool)
- Python 3.9+ (code examples)
- ROS 2 Humble (robotics examples)
- Gazebo Harmonic, CoppeliaSim 4.7+, PyBullet 3.2+ (simulators)
- `flake8` / `pylint` (Python linting)

**Storage**: Markdown files in `docs/` and `examples/` directories (GitHub repo), versioned via git tags

**Testing**:
- Docusaurus build validation (no build errors)
- Python syntax validation via CI (flake8, pylint)
- Code example execution tests (bash scripts in CI)
- Frontmatter YAML schema validation
- Link validation (check internal/external links)

**Target Platform**: Web (Docusaurus hosted on GitHub Pages), supporting browsers ES6+

**Project Type**: Web - static site generation (Docusaurus) + code examples repository

**Performance Goals**:
- Site build time < 2 minutes (Docusaurus build)
- Page load time < 3 seconds (90th percentile)
- Code example execution < 30 seconds (typical examples)
- Support offline documentation browsing (via HTML download)

**Constraints**:
- GitHub Pages free tier (storage limits ~1GB)
- Docusaurus versioning overhead (each version increases build size)
- ROS 2 examples require Linux environment (test in CI)
- Simulator installations must be documented; not bundled

**Scale/Scope**:
- 4 modules, ~15-20 chapters
- ~40-60 code examples (each 50-200 lines)
- ~60-100 exercises
- 4 capstone projects
- 3+ diagrams per chapter (~60 diagrams)
- Estimated 200-250 total Markdown files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principles Aligned**:
- ✅ **I. Education-First Design**: Plan emphasizes learner pathways, prerequisites, exercises, and capstone projects
- ✅ **II. Practical, Engineering-Focused**: Python 3.9+, ROS 2 Humble, simulators specified; no theoretical-only chapters
- ✅ **III. Content Accuracy & Safety**: Plan includes domain expert review gate (Phase 3), safety warning templates, and deprecation workflow
- ✅ **IV. Docusaurus Standards**: Markdown + YAML frontmatter, folder organization, sidebar auto-generation, asset management specified
- ✅ **V. Testable, Reproducible Examples**: Python linting, code example CI validation, requirements.txt per example, environment specs required
- ✅ **VI. Iterative Improvement**: CHANGELOG.md tracking, GitHub Issues for feedback, quarterly review cadence, versioning support

**Mandatory Sections Included**:
- ✅ Frontmatter YAML with metadata (title, description, sidebar_position, tags, module, prerequisites, estimated_time)
- ✅ Folder structure: `docs/[module-number]-[module-slug]/[chapter-slug]/`
- ✅ Code examples: extracted to `examples/[chapter-slug]/` with README
- ✅ Docusaurus versioning: semantic versioning (v1.0.0, v1.1.0) with deprecated chapter warnings
- ✅ Safety warnings: section template for hazardous operations
- ✅ Visuals: 2+ diagrams per chapter, stored in `docs/assets/`
- ✅ Exercises: 3-5 per chapter with acceptance criteria
- ✅ Capstone projects: per-module integrating project

**GATE RESULT**: ✅ PASS — All constitutional principles and mandatory sections addressed.

## Project Structure

### Documentation (this feature)

```text
specs/001-book-architecture/
├── spec.md                  # Feature specification (done)
├── plan.md                  # This file (/sp.plan output)
├── research.md              # Phase 0 output (in progress)
├── data-model.md            # Phase 1 output (in progress)
├── quickstart.md            # Phase 1 output (in progress)
├── contracts/               # Phase 1 output (in progress)
│   ├── chapter-schema.json  # Frontmatter YAML schema
│   ├── code-example.json    # Code example schema
│   └── docusaurus.json      # Docusaurus config schema
└── checklists/
    └── requirements.md      # Quality checklist (done)
```

### Source Code (repository root)

```text
docs/                                    # Content chapters
├── intro.md                             # Book introduction and learning path
├── 01-fundamentals/                     # Module 1: Concepts
│   ├── what-is-physical-ai.md
│   ├── embodied-intelligence.md
│   ├── basics-of-robotics.md
│   └── assets/                         # Module 1 diagrams/images
├── 02-humanoid-robotics/               # Module 2: ROS 2 - Robotic Nervous System
│   ├── ros2-architecture.md
│   ├── nodes-and-topics.md
│   ├── robot-control-basics.md
│   ├── kinematics-and-dynamics.md
│   ├── navigation-and-planning.md
│   └── assets/
├── 03-digital-twin/                    # Module 3: Digital Twin - Gazebo & Unity
│   ├── simulation-fundamentals.md
│   ├── gazebo-setup-tutorial.md
│   ├── unity-robotics-intro.md
│   ├── physics-simulation.md
│   └── assets/
├── 04-ai-brain/                        # Module 4: NVIDIA Isaac - AI Robot Brain
│   ├── nvidia-isaac-overview.md
│   ├── computer-vision-basics.md
│   ├── deep-learning-robotics.md
│   ├── reinforcement-learning.md
│   └── assets/
├── 05-vla/                             # Module 5: Vision-Language-Action (VLA)
│   ├── multimodal-learning.md
│   ├── language-grounding.md
│   ├── end-to-end-robotics.md
│   └── assets/
├── assets/                             # Shared diagrams, schematics
│   ├── diagrams/
│   ├── schematics/
│   └── photos/
└── _category_.json                     # Docusaurus category config

examples/                               # Code examples for each chapter
├── chapter-01-intro/
│   ├── README.md                       # Setup and run instructions
│   ├── requirements.txt
│   └── hello_robotics.py
├── chapter-02-ros2-basics/
│   ├── README.md
│   ├── requirements.txt
│   ├── ros2_node_example.py
│   └── custom_msg_setup.py
├── chapter-03-gazebo-simulation/
│   ├── README.md
│   ├── requirements.txt
│   ├── gazebo_sim.launch.py
│   └── sim_verify.py
├── chapter-04-kinematics/
│   ├── README.md
│   ├── requirements.txt
│   └── forward_kinematics.py
├── capstone-module-1/                  # Capstone project for Module 1
│   ├── README.md
│   ├── requirements.txt
│   └── integration_test.py
├── capstone-module-2/
│   ├── README.md
│   ├── requirements.txt
│   ├── launch/
│   └── src/
├── capstone-module-3/
│   └── ...
└── capstone-module-4/
    └── ...

.github/workflows/                      # CI/CD pipelines
├── validate-book.yml                   # Docusaurus build + linting
├── validate-examples.yml                # Python linting + syntax check
├── deploy-to-pages.yml                 # Deploy to GitHub Pages on main branch
└── check-links.yml                     # Link validation (optional)

docusaurus.config.js                    # Docusaurus main config
sidebars.js                             # Sidebar navigation (auto-generated via scripts)
package.json                            # Node.js dependencies
CHANGELOG.md                            # Version history and updates
CONTRIBUTING.md                         # Author guidelines and contribution process
README.md                               # Repository overview

.specify/templates/
├── chapter-template.md                 # Chapter authoring template (new)
├── code-example-template.py            # Python code example template (new)
├── exercise-template.md                # Exercise template (new)
└── capstone-template.md                # Capstone project template (new)
```

**Structure Decision**: Web application with Docusaurus static site + code examples repository. Docusaurus provides content management, versioning, and i18n. Code examples in `examples/` folder with CI validation. Configuration-driven structure (sidebars.js auto-generated from folder layout and frontmatter).

## Complexity Tracking

> No constitution violations. All requirements met with standard web project structure.

---

## Phase 0: Environment Setup & Research

**Objectives**:
- Verify development environment prerequisites
- Research and document best practices for Docusaurus configuration
- Identify dependency versions and compatibility
- Resolve any technical ambiguities

**Steps**:

1. **Environment Verification**:
   - Verify Node.js 18+ installed: `node --version`
   - Verify npm 8+ installed: `npm --version`
   - Verify Python 3.9+ installed: `python --version`
   - Verify git installed: `git --version`
   - Verify ROS 2 setup (optional, for testing examples): `ros2 --version`

2. **Dependency Research**:
   - Document Docusaurus v3.x latest LTS release version
   - List required npm packages: `docusaurus`, `docusaurus/core`, `docusaurus/preset-classic`, `docusaurus/plugin-content-docs`, `docusaurus/plugin-client-redirects`, `remark-*`, `rehype-*` plugins
   - List Python dev tools: `flake8`, `pylint`, `black`, `pytest`
   - List simulator dependencies: PyBullet, CoppeliaSim headless, Gazebo

3. **Docusaurus v3 Best Practices**:
   - Research auto-sidebar generation (docusaurus-auto-sidebar or manual config)
   - Research versioning workflow (versioned_docs folder structure)
   - Research i18n setup (Docusaurus i18n vs. external translation services)
   - Research MDX component setup (admonitions, code tabs, custom components)

4. **CI/CD Pipeline Research**:
   - GitHub Actions workflow for Docusaurus build validation
   - Python linting in CI (flake8, pylint configurations)
   - Code example execution testing (bash scripts to run .py files)
   - Link validation tools (e.g., `linkinator`, `htmlproofer`)

5. **Generate research.md**:
   - Document all decisions with rationale
   - List alternatives considered and rejected
   - Create dependency matrix (versions, compatibility)

**Dependencies**:
- None (initial setup phase)

**Expected Output**:
- `research.md` (2-3 pages): dependency versions, Docusaurus configuration approach, CI/CD strategy, MDX component plan
- Environment verification checklist (passed)
- Dependency matrix (Node.js, npm, Python, ROS 2, simulators, tools)

---

## Phase 1: Docusaurus Installation & Configuration

**Objectives**:
- Initialize Docusaurus v3 project
- Configure frontmatter YAML schema
- Setup sidebar navigation auto-generation
- Configure versioning and i18n
- Create MDX component setup
- Test build process

**Steps**:

1. **Initialize Docusaurus v3**:
   - Run `npx create-docusaurus@latest book-docs classic` (or integrate into existing repo)
   - Install additional plugins: `npm install @docusaurus/plugin-client-redirects docusaurus-auto-sidebar`
   - Remove unused default content; keep only `docs/`, `sidebars.js`, `docusaurus.config.js`

2. **Configure docusaurus.config.js**:
   - Set site metadata (title: "AI & Physical Robotics Book", tagline: "From Basics to Advanced")
   - Configure favicon and logo
   - Set GitHub repo link for Edit Page functionality
   - Enable versioning: `"lastVersion": "current"`, `"versions": {"current": {"label": "main (unstable)"}}`
   - Configure i18n locales: `locales: ["en"]`, `defaultLocale: "en"`, prepared for `"es"`, `"zh"`
   - Setup MDX plugins: `@docusaurus/remark-plugin-npm2yarn`, `@docusaurus/remark-plugin-codesandbox`, custom admonitions
   - Configure search (DocSearch or Algolia)

3. **Setup Sidebar Navigation**:
   - Option A (Manual): Create `sidebars.js` mapping folder structure to sidebar objects
   - Option B (Auto): Use `docusaurus-auto-sidebar` to auto-generate from folder structure
   - Add sidebar_position metadata to each chapter's frontmatter to order chapters
   - Test sidebar generation matches specification folder layout

4. **Configure Frontmatter YAML Schema**:
   - Create schema validation (JSON Schema) for chapter frontmatter
   - Mandatory fields: `title`, `description`, `sidebar_position`, `tags`, `module`, `estimated_time`
   - Optional fields: `prerequisites`, `authors`, `last_updated`, `difficulty_level`
   - Add remark plugin to validate frontmatter on build

5. **Setup Versioning Workflow**:
   - Create `versioned_docs/` folder structure for releases (e.g., `versioned_docs/version-1.0.0/`)
   - Create `versions.json` listing all versions: `["1.0.0", "0.9.0"]` (if applicable)
   - Setup deprecation banner for old versions (custom component)
   - Test version switching and URL patterns

6. **Configure MDX Components**:
   - Import `Admonition` components: `<Admonition type="note">`, `<Admonition type="warning">`, `<Admonition type="tip">`, `<Admonition type="danger">`
   - Setup code block tabs component (for multi-language examples)
   - Create custom button component for navigation (`<NextChapterButton/>`)
   - Create prerequisite callout component (`<PrerequisiteCard/>`)
   - Create learning objective component (`<LearningObjectives/>`)

7. **Setup i18n Infrastructure**:
   - Configure `docusaurus.config.js` for i18n structure
   - Create English translations in `i18n/en/` (sidebars, footer, header)
   - Prepare folder structure for Spanish (`i18n/es/`) and Chinese (`i18n/zh/`) (leave translations for later)
   - Document i18n workflow for translators

8. **Test Build & Deployment**:
   - Run `npm run build` locally; verify no errors
   - Run `npm run start` to preview site locally
   - Verify sidebar navigation works
   - Verify versioning dropdown (if applicable)
   - Verify i18n language selector

**Dependencies**:
- Phase 0: Environment Setup (Node.js 18+, npm 8+)
- research.md completed

**Expected Output**:
- Docusaurus v3 initialized and configured
- `docusaurus.config.js` with all settings (versioning, i18n, MDX plugins, search)
- `sidebars.js` with auto-generation setup
- Frontmatter YAML schema validation
- `i18n/en/docusaurus.json` created
- MDX custom components created
- Local build tested and verified
- `package.json` updated with dependencies
- Site preview working at `http://localhost:3000`

---

## Phase 2: Book Structure Creation

**Objectives**:
- Create folder structure for 4 modules
- Generate chapter stubs with metadata
- Create assets folder structure
- Create examples folder structure
- Create capstone project skeletons
- Test sidebar navigation with all chapters

**Steps**:

1. **Create Module Folders**:
   ```
   docs/
   ├── 01-fundamentals/
   ├── 02-humanoid-robotics/
   ├── 03-digital-twin/
   ├── 04-ai-brain/
   └── 05-vla/
   ```

2. **Create Chapter Stubs** (each module):
   - Module 1 (Fundamentals): 3-4 chapters
     - what-is-physical-ai.md
     - embodied-intelligence.md
     - basics-of-robotics.md
   - Module 2 (ROS 2): 4-5 chapters
     - ros2-architecture.md
     - nodes-and-topics.md
     - robot-control-basics.md
     - kinematics-and-dynamics.md
   - Module 3 (Digital Twin): 4 chapters
     - simulation-fundamentals.md
     - gazebo-setup-tutorial.md
     - unity-robotics-intro.md
     - physics-simulation.md
   - Module 4 (NVIDIA Isaac): 4 chapters
     - nvidia-isaac-overview.md
     - computer-vision-basics.md
     - deep-learning-robotics.md
     - reinforcement-learning.md
   - Module 5 (VLA): 3 chapters
     - multimodal-learning.md
     - language-grounding.md
     - end-to-end-robotics.md

3. **Populate Chapter Stubs with Frontmatter**:
   - Add YAML frontmatter to each chapter with: `title`, `description`, `sidebar_position`, `tags`, `module`, `estimated_time`, `prerequisites`, `difficulty_level`
   - Add chapter introduction section (placeholder text with learning objectives)
   - Add section headers (placeholder text for: Lesson Content, Code Examples, Exercises, Capstone Guidance)
   - Example:
     ```markdown
     ---
     title: "ROS 2 Architecture"
     description: "Understand ROS 2 structure, nodes, topics, and pub/sub communication"
     sidebar_position: 1
     tags: ["ROS 2", "robotics", "architecture"]
     module: "humanoid-robotics"
     estimated_time: "120 minutes"
     prerequisites: ["01-fundamentals/basics-of-robotics"]
     difficulty_level: "beginner"
     ---

     # ROS 2 Architecture

     ## Learning Objectives
     - Understand ROS 2 computation graph
     - Describe nodes, topics, services, and actions
     - Set up and run a basic ROS 2 example

     ## Lesson Content
     [To be filled]

     ## Code Examples
     [To be filled]

     ## Exercises
     [To be filled]

     ## Capstone Guidance
     [To be filled]
     ```

4. **Create Assets Folder Structure**:
   ```
   docs/assets/
   ├── 01-fundamentals/
   │   ├── what-is-physical-ai/
   │   ├── embodied-intelligence/
   │   └── basics-of-robotics/
   ├── 02-humanoid-robotics/
   │   ├── ros2-architecture/
   │   ├── nodes-and-topics/
   │   └── ...
   └── ...
   ```
   - Create placeholder `README.md` in each folder documenting image naming conventions and sizing

5. **Create Examples Folder Structure**:
   ```
   examples/
   ├── chapter-01-physical-ai/
   │   ├── README.md
   │   ├── requirements.txt
   │   └── example.py
   ├── chapter-02-ros2-basics/
   │   ├── README.md
   │   ├── requirements.txt
   │   └── example.py
   └── capstone-module-{1,2,3,4}/
       ├── README.md
       ├── requirements.txt
       └── [code files]
   ```

6. **Create Capstone Project Skeletons**:
   - `examples/capstone-module-1/`: Fundamentals integration project (title, description, required chapters, deliverables stub)
   - `examples/capstone-module-2/`: ROS 2 integration project (with launch files, nodes)
   - `examples/capstone-module-3/`: Digital Twin integration project (Gazebo + Unity setup)
   - `examples/capstone-module-4/`: AI + VLA integration project (vision + language + control)

7. **Test Sidebar Navigation**:
   - Run `npm run build`
   - Verify sidebar shows all 4 modules with chapter hierarchy
   - Click through chapters in sidebar; verify correct chapter loads
   - Check frontmatter validation passes

**Dependencies**:
- Phase 1: Docusaurus Installation & Configuration
- research.md completed

**Expected Output**:
- Complete folder structure for 4 modules with 15-20 chapter stubs
- Each chapter has YAML frontmatter with metadata
- Assets folder structure ready for diagrams
- Examples folder with code example stubs
- Capstone project skeletons created
- Sidebar navigation auto-generated and working
- Docusaurus build passes with no errors
- All chapters visible in sidebar navigation

---

## Phase 3: Content Writing & Development

**Objectives**:
- Author lesson content for each chapter
- Create 2+ code examples per chapter
- Author 3-5 exercises per chapter
- Create diagrams/visualizations (2+ per chapter)
- Write capstone project specifications
- Create CONTRIBUTING.md and authoring templates

**Steps**:

1. **Create Authoring Guidelines** (`.specify/templates/` + `CONTRIBUTING.md`):
   - Chapter template with sections (learning objectives, lesson, code examples, exercises, capstone guidance)
   - Code example template with setup instructions, dependencies, expected output
   - Exercise template with difficulty levels, acceptance criteria, estimated time
   - Capstone project template with required chapters, deliverables, grading rubric
   - Docusaurus best practices (link formatting, admonition usage, code block tags)

2. **Author Lesson Content** (16-20 chapters):
   - Write 2-3 page content per chapter (1500-3000 words)
   - Include diagrams/flowcharts at key points (embed in content)
   - Link to prerequisites using Docusaurus link syntax
   - Use admonitions for tips, warnings, key concepts
   - Cite sources (academic papers, hardware datasheets, ROS documentation)

3. **Create Code Examples**:
   - 2-3 working examples per chapter (40-50 examples total)
   - Each example in separate file under `examples/[chapter-slug]/`
   - Include setup instructions in README
   - List dependencies in requirements.txt
   - Specify Python version, tested OS, tested ROS 2 distribution
   - Add expected output / success criteria
   - Examples must run successfully when tested

4. **Author Exercises**:
   - 3-5 exercises per chapter (50-100 exercises total)
   - Include learning objective tied to chapter content
   - Provide difficulty level (beginner/intermediate/advanced)
   - Define acceptance criteria (what constitutes passing)
   - Estimate time to complete
   - Provide hint or starting code for complex exercises

5. **Create Diagrams & Visualizations**:
   - 2+ diagrams per chapter (40-60 diagrams total)
   - Types: architecture diagrams, flowcharts, system schematics, state machines
   - Store as PNG/SVG in `docs/assets/[module]/[chapter]/`
   - Add alt text to images (for accessibility)
   - Use consistent visual style (color scheme, fonts, arrow types)
   - Tools: draw.io, Graphviz, Inkscape, OmniGraffle, or Mermaid (if supported in Docusaurus)

6. **Write Capstone Projects** (1 per module):
   - Module 1 (Fundamentals): "Build a Basic Robot Simulator" (integrate concepts from 3 chapters)
   - Module 2 (ROS 2): "Create a Multi-Node Robotic System" (publisher/subscriber/service pattern)
   - Module 3 (Digital Twin): "Simulate a Humanoid in Gazebo & Unity" (physics, rendering, control)
   - Module 4 (NVIDIA Isaac + VLA): "Vision-Language-Action Robot Controller" (multimodal learning, control)
   - Each capstone: 300-500 word description, required chapters/tools, deliverables (code, report, demo video)

7. **Domain Expert Review Gate**:
   - Safety-critical chapters (control algorithms, mechanical/electrical hazards) reviewed by domain expert
   - Code examples tested in target environment (ROS 2 Humble, simulators)
   - Accuracy claims verified against datasheets/publications
   - Deprecation notices added for outdated frameworks

**Dependencies**:
- Phase 2: Book Structure Creation
- Authoring templates and guidelines prepared

**Expected Output**:
- Complete lesson content for all 16-20 chapters
- 40-50 working code examples with documentation
- 50-100 exercises with acceptance criteria
- 40-60 diagrams and visualizations
- 4 capstone project specifications
- CONTRIBUTING.md with authoring guidelines
- Templates: chapter, code example, exercise, capstone project
- Domain expert review completed for safety-critical content

---

## Phase 4: Testing & Quality Assurance

**Objectives**:
- Validate code examples (syntax, execution)
- Validate frontmatter YAML
- Test all internal/external links
- Verify accessibility (alt text, semantic HTML)
- Test versioning and deprecation workflow
- Verify i18n structure

**Steps**:

1. **Code Example Validation**:
   - Setup GitHub Actions workflow to lint all Python examples (flake8, pylint)
   - Run each example in CI environment; capture output
   - Compare actual output with expected output in README
   - Verify requirements.txt lists all dependencies
   - Verify Python version and environment specs match chapter documentation

2. **Frontmatter YAML Validation**:
   - Validate all chapter files have required YAML fields
   - Validate sidebar_position is unique per module
   - Validate prerequisites point to existing chapters
   - Check for typos in tags and module names

3. **Link Validation**:
   - Test all internal links (cross-chapter references) resolve correctly
   - Test all external links (documentation, papers, datasheets) return 200 status
   - Check links in code comments and README files
   - Generate link validation report with any broken links

4. **Accessibility Check**:
   - Verify all images have alt text
   - Verify semantic HTML structure (headings, lists)
   - Check color contrast ratios for diagrams
   - Test keyboard navigation in interactive components

5. **Build & Performance Testing**:
   - Docusaurus build time < 2 minutes
   - Site paginated correctly (100+ pages)
   - Search functionality works (DocSearch/Algolia)
   - Mobile responsiveness verified (mobile device or browser devtools)

6. **Versioning & Deprecation Workflow**:
   - Tag current version as v1.0.0 in git
   - Create v1.0.0 in Docusaurus versioning
   - Update a sample chapter and mark prior version as deprecated
   - Verify deprecation banner appears on v1.0.0 pages
   - Verify URL routing works for all versions

7. **i18n Structure Verification**:
   - Verify `i18n/en/` folder has all translation files
   - Verify `i18n/es/` and `i18n/zh/` folder structures created (empty, ready for translations)
   - Test language switcher in Docusaurus UI
   - Document i18n workflow for translators

**Dependencies**:
- Phase 3: Content Writing & Development
- GitHub Actions CI/CD configured

**Expected Output**:
- CI/CD GitHub Actions workflows created and passing:
  - `validate-book.yml` (Docusaurus build)
  - `validate-examples.yml` (Python linting + execution)
  - `check-links.yml` (link validation)
- Test results: 100% code examples passing, 100% links valid, all frontmatter valid
- Accessibility report: all images alt-text present, semantic HTML verified
- Build report: build time < 2 min, site size acceptable
- Versioning tested: v1.0.0 tags created, deprecation banners working
- i18n structure ready for translations

---

## Phase 5: Deployment & Documentation

**Objectives**:
- Setup GitHub Pages deployment
- Create deployment automation
- Generate final documentation (README, CONTRIBUTING.md, CHANGELOG.md)
- Setup feedback mechanisms (GitHub Issues, Discussions)
- Prepare for public launch

**Steps**:

1. **GitHub Pages Setup**:
   - Enable GitHub Pages in repository settings (deploy from `gh-pages` branch)
   - Configure custom domain (optional: `book.ai-robotics.org` or similar)
   - Setup HTTPS/SSL (auto-managed by GitHub Pages)

2. **Deployment Automation** (GitHub Actions):
   - Create `deploy-to-pages.yml` workflow:
     - Trigger on push to `main` branch
     - Run `npm run build` and `npm run deploy`
     - Push `build/` output to `gh-pages` branch
     - Publish to GitHub Pages
   - Test deployment pipeline: push to main → verify site updates within 2 minutes

3. **Repository Documentation**:
   - Create `README.md` (repository overview, how to use book, quick start, link to live site)
   - Create `CONTRIBUTING.md` (contributor guidelines, authoring templates, review process, code of conduct)
   - Create `CHANGELOG.md` (version history, deprecation notices, major updates)
   - Create `LICENSE.md` (specify open-source license: MIT, CC-BY-4.0, or other)

4. **Feedback Mechanisms**:
   - Enable GitHub Issues for bug reports, corrections, suggestions
   - Enable GitHub Discussions for general questions, community feedback
   - Create issue templates: `.github/ISSUE_TEMPLATE/bug_report.md`, `correction.md`, `feedback.md`
   - Document how to report safety concerns (security policy)

5. **Create Project Homepage**:
   - Write `docs/intro.md` with:
     - Welcome message and book overview
     - Learning path diagram (visual of 4 modules)
     - Prerequisites and assumed knowledge
     - How to use the book (sequential, module-by-module, or topic-by-topic)
     - Time estimates (estimated hours per module)
     - Link to live deployment
     - Call-to-action for feedback

6. **Setup Monitoring & Analytics** (optional):
   - Configure Google Analytics or Plausible Analytics (privacy-friendly) for usage insights
   - Monitor most-visited chapters, bounce rate, user flow
   - Track link clicks to external resources
   - Use analytics to inform quarterly review and updates

7. **Create Release Notes**:
   - Tag v1.0.0 on main branch with annotated message
   - Update `versions.json` in Docusaurus config (if versioning enabled)
   - Create GitHub Release with summary of all chapters and code examples
   - Prepare announcement (blog post, email, social media)

**Dependencies**:
- Phase 4: Testing & Quality Assurance (all tests passing)
- GitHub repository with main branch

**Expected Output**:
- GitHub Pages deployed and live at repository URL
- Deployment automation working (main → live within 2 min)
- Documentation complete: README, CONTRIBUTING, CHANGELOG, LICENSE
- Issue and discussion templates created
- GitHub Issues and Discussions enabled
- Book homepage (intro.md) created
- v1.0.0 released and tagged
- Analytics setup (optional, configured)

---

## Phase 6: Final Report & Handoff

**Objectives**:
- Document project completion
- Create project summary and metrics
- Prepare training materials for future maintainers
- Archive project artifacts
- Plan for ongoing maintenance

**Steps**:

1. **Project Completion Report**:
   - Document all deliverables (chapters, code examples, exercises, diagrams, capstones)
   - List all commits and file changes
   - Report metrics: total chapters (16-20), code examples (40-50), exercises (50-100), diagrams (40-60)
   - Summarize architecture decisions and rationale
   - Document any deviations from original specification

2. **Maintenance Playbook**:
   - How to update a chapter for a new library version
   - How to deprecate outdated content
   - How to add a new chapter following the architecture
   - How to release a new version (versioning workflow)
   - How to manage translations (i18n workflow)
   - Quarterly review checklist (check for library deprecations, update CHANGELOG)
   - Rollback procedure (if something breaks in deployment)

3. **Author & Contributor Guidelines**:
   - Complete `CONTRIBUTING.md` with step-by-step workflow (fork → branch → write → PR → review → merge)
   - Link to authoring templates and examples
   - Document review checklist (safety warnings, code examples tested, diagrams present, exercises defined)
   - Set expectations for response times (PR review within 7 days)

4. **Archive & Version Control**:
   - Tag v1.0.0 commit with complete metadata
   - Create GitHub Release with full project summary
   - Document all branches used (archive feature branches)
   - Confirm all work is committed and pushed to main

5. **Knowledge Transfer**:
   - Create video walkthrough of book structure (10-15 min)
   - Document decision log (why certain technologies chosen, alternatives rejected)
   - Create FAQ for common authoring questions
   - Schedule handoff meeting with project stakeholders

6. **Plan for Ongoing Improvement**:
   - Quarterly review schedule (Jan, Apr, Jul, Oct) to check for:
     - Library deprecations (ROS 2 releases, simulator updates)
     - High-traffic chapters (monitor analytics)
     - Community feedback (GitHub Issues)
     - Safety concerns or accuracy issues
   - Document issue backlog for next iteration
   - Plan next release (v1.1.0 with community contributions)

**Dependencies**:
- Phase 5: Deployment & Documentation (live and working)
- All testing passing

**Expected Output**:
- Project Completion Report (5-10 pages: summary, metrics, decisions, deliverables)
- Maintenance Playbook (3-5 pages: step-by-step procedures)
- Author & Contributor Guidelines (updated CONTRIBUTING.md)
- GitHub Release notes for v1.0.0
- Video walkthrough created and linked in README
- Decision log archived in `docs/architecture/` folder (optional)
- Quarterly review checklist created and scheduled
- Knowledge transfer meeting completed

---

## Timeline & Milestones

| Phase | Duration | Milestones |
|-------|----------|-----------|
| 0: Environment & Research | 3-5 days | `research.md` completed, dependencies documented |
| 1: Docusaurus Setup | 5-7 days | Docusaurus initialized, build working, sidebar auto-generation tested |
| 2: Structure Creation | 3-5 days | All chapter stubs created, frontmatter validated, examples folder ready |
| 3: Content Writing | 4-6 weeks | All chapters written, code examples working, exercises defined, diagrams created |
| 4: Testing & QA | 5-7 days | All tests passing, links validated, accessibility verified, versioning tested |
| 5: Deployment | 3-5 days | GitHub Pages live, deployment automation working, documentation complete |
| 6: Final Report | 3-5 days | Completion report, maintenance playbook, knowledge transfer |
| **TOTAL** | **~6-8 weeks** | **v1.0.0 released, live on GitHub Pages** |

---

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|-------------------|
| Content accuracy issues | Phase 3: Domain expert review gate for safety-critical chapters |
| Broken code examples | Phase 4: CI/CD linting + execution tests for all Python code |
| Navigation confusion | Phase 2: Test sidebar thoroughly; Phase 3: Add prerequisite callouts |
| Library deprecation | Phase 6: Quarterly review process to catch ROS 2, simulator updates |
| i18n scope creep | Phase 1: Structure i18n but defer translations to Phase 6+ |
| Deployment failures | Phase 5: Automated CI/CD with rollback (revert main branch) |
| Contributor friction | Phase 6: Clear CONTRIBUTING.md with templates and checklists |

---

## Success Criteria (from Specification)

✅ **SC-001**: Book architecture specification complete with all 4 modules, 3-5 chapters each, clear learning progression.

✅ **SC-002**: Docusaurus configuration supports architecture: sidebar auto-generates, YAML validates, site builds without errors.

✅ **SC-003**: Pilot chapter authored and published with lesson, 2+ code examples, 3+ exercises, capstone guidance.

✅ **SC-004**: 90% of learners identify correct starting chapter and understand prerequisites.

✅ **SC-005**: 100% of code examples pass linting and CI syntax checks.

✅ **SC-006**: Versioning workflow tested: update → archive as v1.0 → release as v2.0.

✅ **SC-007**: Capstone projects defined (200-500 word descriptions).

✅ **SC-008**: i18n folder structure and config support multiple languages.

✅ **SC-009**: Content author documentation created (chapter, code example, exercise, capstone templates).

---

## Next Steps (Post-Plan)

1. **Run `/sp.tasks`** to generate detailed task breakdown for Phase 0 & 1
2. **Start Phase 0**: Research and document dependencies
3. **Share plan** with project stakeholders for approval
4. **Schedule content authoring** timeline (Phase 3 is longest phase, ~4-6 weeks)
5. **Identify domain experts** for Phase 3 safety review
