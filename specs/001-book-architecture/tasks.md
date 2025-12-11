# Tasks: Book Architecture & Content Structure

**Input**: Design documents from `/specs/001-book-architecture/`
**Status**: Ready for Phase 0 & Phase 1 implementation
**Total Tasks**: 95 tasks across 6 phases + Polish

**Organization**: Tasks are grouped by user story and phase to enable independent implementation and testing.

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files/folders, no dependencies)
- **[Story]**: Which user story this belongs to (US1, US2, US3, US4)
- File paths are absolute and specific

---

## Phase 1: Setup & Environment (Days 1-5)

**Purpose**: Project initialization, environment verification, and foundational configuration

### Environment & Dependency Verification

- [ ] T001 Verify Node.js 18+ installation: `node --version`
- [ ] T002 Verify npm 8+ installation: `npm --version`
- [ ] T003 Verify Python 3.9+ installation: `python --version`
- [ ] T004 Verify git installation: `git --version`
- [ ] T005 [P] Document all required npm dependencies in `package.json`
- [ ] T006 [P] Document all required Python dev tools (flake8, pylint, black, pytest)
- [ ] T007 [P] Document all simulator dependencies (PyBullet 3.2+, Gazebo Harmonic, CoppeliaSim 4.7+)
- [ ] T008 Create `docs/ENVIRONMENT.md` with complete setup instructions

### Research & Decision Documentation

- [ ] T009 Research Docusaurus v3.x latest LTS release version
- [ ] T010 Research auto-sidebar generation options (docusaurus-auto-sidebar plugin vs manual sidebars.js)
- [ ] T011 Research MDX component best practices and available plugins
- [ ] T012 Research GitHub Actions workflows for Docusaurus CI/CD
- [ ] T013 [P] Research Python linting tools (flake8 vs pylint vs black)
- [ ] T014 [P] Research link validation tools (linkinator, htmlproofer, etc.)
- [ ] T015 Create `specs/001-book-architecture/research.md` documenting all findings, decisions, and rationale

---

## Phase 2: Docusaurus Installation & Configuration (Days 6-12)

**Purpose**: Initialize Docusaurus v3, configure core settings, and setup infrastructure

### Docusaurus Project Initialization

- [ ] T016 Initialize Docusaurus v3 project: `npx create-docusaurus@latest book-docs classic`
- [ ] T017 Remove unused default content and keep only `docs/`, `sidebars.js`, `docusaurus.config.js`
- [ ] T018 [P] Install additional npm packages: `@docusaurus/plugin-client-redirects`, `docusaurus-auto-sidebar`
- [ ] T019 [P] Install markdown processing packages: `remark-gfm`, `rehype-raw`
- [ ] T020 Update `package.json` with all required scripts (build, start, deploy)

### Docusaurus Configuration

- [ ] T021 Configure site metadata in `docusaurus.config.js`:
  - Title: "AI & Physical Robotics Book"
  - Tagline: "From Basics to Advanced"
  - Favicon and logo paths
  - GitHub repo link for "Edit this page" functionality

- [ ] T022 [P] Configure versioning in `docusaurus.config.js`:
  - Set `lastVersion: "current"`
  - Configure `versions: {current: {label: "main (unstable)"}}`
  - Create `versions.json` for version tracking

- [ ] T023 [P] Configure i18n in `docusaurus.config.js`:
  - Set locales: `["en"]`
  - Set defaultLocale: `"en"`
  - Prepare structure for future locales (es, zh)

- [ ] T024 [P] Configure MDX plugins in `docusaurus.config.js`:
  - Setup admonition components (note, warning, tip, danger)
  - Setup code block tabs for multi-language examples
  - Setup custom markdown syntax plugins

- [ ] T025 [P] Configure search in `docusaurus.config.js`:
  - Setup DocSearch or Algolia integration
  - Configure search options

### Sidebar & Navigation Setup

- [ ] T026 Create `sidebars.js` template with auto-generation setup
- [ ] T027 [P] Configure sidebar_position auto-ordering for chapters
- [ ] T028 [P] Create sidebar documentation in `docs/SIDEBAR.md` explaining structure

### Frontmatter Schema Configuration

- [ ] T029 Create `specs/001-book-architecture/contracts/chapter-schema.json` with JSON Schema for chapter frontmatter:
  - Mandatory fields: title, description, sidebar_position, tags, module, estimated_time
  - Optional fields: prerequisites, authors, last_updated, difficulty_level

- [ ] T030 [P] Create frontmatter validation script in `.specify/scripts/validate-frontmatter.sh`
- [ ] T031 [P] Add frontmatter validation to build pipeline (remark plugin or pre-build script)

### MDX Components Setup

- [ ] T032 Create custom MDX component for learning objectives in `src/components/LearningObjectives.jsx`
- [ ] T033 [P] Create custom MDX component for prerequisite cards in `src/components/PrerequisiteCard.jsx`
- [ ] T034 [P] Create custom MDX component for next chapter navigation in `src/components/NextChapterButton.jsx`
- [ ] T035 [P] Create custom MDX component for code block tabs in `src/components/CodeTabs.jsx`
- [ ] T036 [P] Create admonition component wrapper in `src/components/Admonition.jsx` (note, warning, tip, danger)

### i18n Infrastructure Setup

- [ ] T037 Create `i18n/en/docusaurus.json` with English translations for sidebar, footer, navbar
- [ ] T038 Create folder structure for Spanish translations: `i18n/es/docusaurus.json` (placeholder)
- [ ] T039 Create folder structure for Chinese translations: `i18n/zh/docusaurus.json` (placeholder)
- [ ] T040 Create `docs/i18n-WORKFLOW.md` documenting translation process for future translators

### Build & Test Verification

- [ ] T041 Run `npm run build` locally; verify no build errors
- [ ] T042 Run `npm run start` locally; verify site preview at `http://localhost:3000`
- [ ] T043 [P] Verify sidebar navigation renders correctly
- [ ] T044 [P] Verify frontmatter YAML validation passes
- [ ] T045 [P] Verify MDX components render without errors
- [ ] T046 Create `docs/BUILD.md` documenting build process and troubleshooting

**Checkpoint**: Docusaurus configured, local build working, ready for book structure creation

---

## Phase 3: User Story 1 - Book Author Creates Structured Content (Priority: P1) 🎯

**Goal**: Enable book authors to create structured chapters following a consistent template with lessons, code examples, exercises, and capstone guidance, with chapters automatically integrating into Docusaurus sidebar navigation.

**Independent Test**: An author can create a single chapter (e.g., "ROS 2 Architecture") with lesson content, 2+ code examples (with README and requirements.txt), 3+ exercises with acceptance criteria, and have it automatically appear in the sidebar with correct metadata and linking.

### Phase 3A: Templates & Guidelines Creation

- [ ] T047 Create chapter authoring template in `.specify/templates/chapter-template.md` with sections:
  - Frontmatter YAML (title, description, sidebar_position, tags, module, estimated_time, prerequisites, difficulty_level)
  - Learning Objectives section
  - Lesson Content section (with guidance on clarity, prerequisites, real examples before theory)
  - Code Examples section (with links to external examples)
  - Exercises section (with difficulty levels)
  - Capstone Guidance section
  - Safety Warnings section (if applicable)
  - References & Attribution section

- [ ] T048 [P] Create code example template in `.specify/templates/code-example-template.py` with:
  - File header with title, description, environment specs
  - Setup instructions comment block
  - Example code with inline comments
  - Expected output documentation
  - links to parent chapter

- [ ] T049 [P] Create exercise template in `.specify/templates/exercise-template.md` with:
  - Exercise title and difficulty level
  - Learning objective reference
  - Description of task
  - Acceptance criteria (what constitutes passing)
  - Time estimate
  - Optional: hints or starting code

- [ ] T050 [P] Create capstone project template in `.specify/templates/capstone-template.md` with:
  - Project title and module reference
  - Required chapters list
  - Project description (300-500 words)
  - Required tools and environment specs
  - Deliverables checklist
  - Grading rubric (if for coursework)

- [ ] T051 [P] Create `CONTRIBUTING.md` with:
  - Contributor code of conduct
  - Step-by-step workflow (fork → branch → write → commit → PR → review → merge)
  - Link to all authoring templates
  - Review checklist (safety warnings, code examples tested, diagrams present, exercises defined)
  - Expected response times (PR review within 7 days)
  - Docusaurus best practices (link formatting, admonition usage, code block tagging)

- [ ] T052 [P] Create `.specify/AUTHORING_GUIDE.md` comprehensive guide with:
  - Chapter structure overview
  - Folder organization rules
  - Frontmatter field definitions
  - Code example guidelines (Python version, dependencies, environment specs, expected output)
  - Exercise best practices (learning objectives, difficulty levels, acceptance criteria)
  - Diagram guidelines (tools, naming, sizing, accessibility)
  - Safety warning templates
  - Citation and attribution requirements

### Phase 3B: Folder Structure Creation

- [ ] T053 Create module folder structure in `docs/`:
  - `docs/01-fundamentals/`
  - `docs/02-humanoid-robotics/`
  - `docs/03-digital-twin/`
  - `docs/04-ai-brain/`
  - `docs/05-vla/`

- [ ] T054 [P] Create placeholder `_category_.json` in each module folder for Docusaurus category configuration
- [ ] T055 [P] Create assets folder structure in `docs/assets/`:
  - `docs/assets/01-fundamentals/`
  - `docs/assets/02-humanoid-robotics/`
  - `docs/assets/03-digital-twin/`
  - `docs/assets/04-ai-brain/`
  - `docs/assets/05-vla/`
- [ ] T056 [P] Create `docs/assets/README.md` documenting image naming conventions and sizing guidelines

### Phase 3C: Chapter Stubs Creation

- [ ] T057 Create chapter stubs for Module 1 (01-fundamentals) in `docs/01-fundamentals/`:
  - `what-is-physical-ai.md` with YAML frontmatter and section placeholders
  - `embodied-intelligence.md` with YAML frontmatter and section placeholders
  - `basics-of-robotics.md` with YAML frontmatter and section placeholders

- [ ] T058 [P] Create chapter stubs for Module 2 (02-humanoid-robotics) in `docs/02-humanoid-robotics/`:
  - `ros2-architecture.md`
  - `nodes-and-topics.md`
  - `robot-control-basics.md`
  - `kinematics-and-dynamics.md`
  - `navigation-and-planning.md`

- [ ] T059 [P] Create chapter stubs for Module 3 (03-digital-twin) in `docs/03-digital-twin/`:
  - `simulation-fundamentals.md`
  - `gazebo-setup-tutorial.md`
  - `unity-robotics-intro.md`
  - `physics-simulation.md`

- [ ] T060 [P] Create chapter stubs for Module 4 (04-ai-brain) in `docs/04-ai-brain/`:
  - `nvidia-isaac-overview.md`
  - `computer-vision-basics.md`
  - `deep-learning-robotics.md`
  - `reinforcement-learning.md`

- [ ] T061 [P] Create chapter stubs for Module 5 (05-vla) in `docs/05-vla/`:
  - `multimodal-learning.md`
  - `language-grounding.md`
  - `end-to-end-robotics.md`

- [ ] T062 Each chapter stub includes proper frontmatter YAML template with all required fields

### Phase 3D: Code Examples Folder Structure

- [ ] T063 Create `examples/` folder structure for code examples:
  - `examples/chapter-01-physical-ai/` with README.md, requirements.txt, example.py placeholder
  - `examples/chapter-02-ros2-basics/` with same structure
  - (Create additional folders for each chapter as needed)

- [ ] T064 [P] Create `examples/README.md` documenting:
  - Code example organization
  - Naming conventions
  - How to run examples
  - Environment setup instructions
  - Testing procedures

- [ ] T065 [P] Create `examples/TEMPLATE/` with template files:
  - `examples/TEMPLATE/README.md` (template for code example README)
  - `examples/TEMPLATE/requirements.txt` (template for dependencies)
  - `examples/TEMPLATE/example.py` (template for code example with comments)

### Phase 3E: Sidebar Navigation Testing

- [ ] T066 Run `npm run build` to auto-generate sidebar from folder structure
- [ ] T067 Verify sidebar renders all 5 modules with correct chapter hierarchy
- [ ] T068 Verify sidebar_position ordering is correct within each module
- [ ] T069 Click through sidebar to verify each chapter stub loads correctly
- [ ] T070 [P] Verify frontmatter YAML validation passes for all stubs

**Checkpoint**: Chapter templates created, folder structure in place, authors can begin writing content

---

## Phase 4: User Story 2 - Learners Navigate & Progress Through Book (Priority: P1)

**Goal**: Provide learners with a clear learning path, prerequisites documentation, progress tracking, and next-chapter guidance so they can progress from fundamentals through advanced topics coherently.

**Independent Test**: A new learner can view the book introduction, see a learning path diagram showing 4 modules with prerequisites, identify which chapter to start with, view prerequisites on each chapter, and navigate sequentially through the book.

### Phase 4A: Introduction & Learning Path

- [ ] T071 [US2] Create `docs/intro.md` with:
  - Welcome message and book overview
  - Learning path diagram (visual of 4 modules, prerequisites, estimated hours)
  - Prerequisite knowledge assumptions
  - How to use the book (sequential, module-by-module, or topic-by-topic options)
  - Time estimates per module
  - Call-to-action for feedback

- [ ] T072 [P] [US2] Create prerequisites matrix in `docs/PREREQUISITES.md` showing:
  - Chapter dependency graph
  - Prerequisites for each chapter (which chapters must be completed first)
  - Estimated completion time per chapter and per module
  - Learning path suggestions (sequential, parallel options)

### Phase 4B: Prerequisite Callouts & Navigation

- [ ] T073 [US2] Update chapter template to include prerequisite section:
  - "Prerequisites" heading with list of required prior knowledge
  - Links to prerequisite chapters using Docusaurus link syntax
  - Warning admonition if prerequisites not met

- [ ] T074 [P] [US2] Update chapter template to include "Next Chapter" section:
  - "What's Next?" heading with link to recommended next chapter
  - Optional: "Alternative Paths" showing other chapters at same level

- [ ] T075 [P] [US2] Create progress tracker component in `src/components/ProgressIndicator.jsx` that shows:
  - Current chapter/module
  - Progress bar showing percentage of book completed
  - Total chapters and current position

### Phase 4C: Learning Objectives & Clarity

- [ ] T076 [US2] Ensure each chapter stub includes clear Learning Objectives:
  - 3-5 measurable learning objectives
  - Phrased as "Learners will be able to..."
  - Verifiable outcomes

- [ ] T077 [P] [US2] Create learning objective validation checklist in `.specify/QUALITY_CHECKLIST.md`:
  - Each chapter has learning objectives
  - Learning objectives are measurable
  - Chapter content addresses all learning objectives
  - Exercises test each learning objective

### Phase 4D: Docusaurus Navigation Features

- [ ] T078 [US2] Configure Docusaurus navbar in `docusaurus.config.js`:
  - Book title and logo
  - Module links (if desired)
  - Link to GitHub repository
  - Link to Discussions for questions
  - Language selector (if i18n enabled)

- [ ] T079 [P] [US2] Configure sidebar in `sidebars.js` to include:
  - Module categories with collapsible sections
  - Chapter links with accurate sidebar_position
  - Grouped by module for clear visual hierarchy

- [ ] T080 [P] [US2] Configure search in Docusaurus:
  - Enable DocSearch or Algolia for chapter/concept search
  - Test search with common robotics terms (ROS 2, kinematics, simulation, etc.)

### Phase 4E: Testing Learner Journey

- [ ] T081 [US2] Test learner journey: New user opens book
  - Can identify correct starting chapter
  - Understands prerequisites before progressing
  - Can navigate sequentially or jump to modules
  - Sees next-chapter suggestions

- [ ] T082 [P] [US2] Verify all internal links work (chapter-to-chapter references)
- [ ] T083 [P] [US2] Verify all prerequisite links are correct

**Checkpoint**: Learning path clear, navigation intuitive, learners can progress independently

---

## Phase 5: User Story 3 - Instructors Deliver Customized Learning Paths (Priority: P2)

**Goal**: Enable instructors to customize content by selecting modules, reordering chapters, and generating customized learning paths for their curricula.

**Independent Test**: An instructor can configure a custom learning path (e.g., only Digital Twin + NVIDIA Isaac modules), the system generates a valid learning path with prerequisites resolved, and can export as PDF or interactive HTML.

### Phase 5A: Custom Path Configuration

- [ ] T084 [US3] Create instructor configuration format in `docs/INSTRUCTOR_GUIDE.md`:
  - How to select modules for a custom path
  - How to reorder chapters
  - How to add supplementary materials
  - Example configurations (all 4 modules, just AI modules, etc.)

- [ ] T085 [P] [US3] Create module selection script in `.specify/scripts/generate-custom-path.sh`:
  - Takes module list as input (e.g., `01-fundamentals 04-ai-brain`)
  - Generates filtered sidebar and chapter list
  - Validates dependencies are satisfied

### Phase 5B: Dependency Resolution

- [ ] T086 [US3] Create dependency resolver in `.specify/scripts/resolve-dependencies.py`:
  - Reads chapter prerequisites from frontmatter
  - Validates selected chapters have all prerequisites
  - Suggests additional chapters if dependencies missing
  - Outputs resolved chapter list in correct order

- [ ] T087 [P] [US3] Create prerequisite validation in `.specify/scripts/validate-custom-path.sh`:
  - Checks that all prerequisites are included in custom path
  - Warns if prerequisites missing
  - Suggests minimal additional chapters needed

### Phase 5C: Export Functionality

- [ ] T088 [US3] Research PDF export tools for Docusaurus (e.g., Docusaurus to PDF plugin)
- [ ] T089 [P] [US3] Implement PDF export script in `.specify/scripts/export-to-pdf.sh`:
  - Takes custom path as input
  - Generates PDF with selected chapters
  - Includes table of contents
  - Preserves formatting and code examples

- [ ] T090 [P] [US3] Implement HTML export script in `.specify/scripts/export-to-html.sh`:
  - Takes custom path as input
  - Generates standalone HTML version
  - Includes offline-compatible styling
  - Preserves sidebar navigation

**Checkpoint**: Instructors can create custom learning paths matching their curricula

---

## Phase 6: User Story 4 - Content Versioning & Maintenance (Priority: P2)

**Goal**: Enable maintainers to track content updates, deprecate outdated guidance, and provide learners access to both current and archived versions.

**Independent Test**: A chapter can be updated, prior version archived as v1.0, current version marked v2.0, and both versions accessible with deprecation banners on old versions.

### Phase 6A: Versioning Setup

- [ ] T091 [US4] Configure Docusaurus versioning in `docusaurus.config.js`:
  - Enable versioned_docs folder
  - Setup versions.json for version tracking
  - Configure version dropdown in navbar

- [ ] T092 [P] [US4] Create versioning workflow in `docs/VERSIONING.md`:
  - How to create a new version (e.g., v1.0.0)
  - How to mark content as deprecated
  - How to archive old versions
  - Semantic versioning rules (MAJOR.MINOR.PATCH)

### Phase 6B: Deprecation Warnings

- [ ] T093 [US4] Create deprecation banner component in `src/components/DeprecationBanner.jsx`:
  - Shows on old versions (e.g., v1.0.0)
  - Message: "This version is deprecated. See [current version link]"
  - Styling to make prominent but not intrusive

- [ ] T094 [P] [US4] Create deprecation notice template in `.specify/templates/deprecation-notice.md`:
  - What changed in current version
  - Migration guide from old version
  - Link to current version
  - Estimated upgrade effort

### Phase 6C: Versioning & Deprecation Testing

- [ ] T095 [US4] Test versioning workflow:
  - Tag v1.0.0 in git
  - Create v1.0.0 in Docusaurus (versioned_docs/version-1.0.0/)
  - Update a chapter in main
  - Verify deprecation banner appears on v1.0.0 pages
  - Verify URL routing works for all versions (current /docs/chapter vs /docs/1.0.0/chapter)

**Checkpoint**: Versioning infrastructure in place, maintenance workflow established

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, and quality assurance across all user stories

- [ ] T096 [P] Create comprehensive `README.md` at repository root:
  - Repository overview
  - Quick start (how to view book locally)
  - How to contribute (link to CONTRIBUTING.md)
  - Link to live deployment
  - How to report issues

- [ ] T097 [P] Create `CHANGELOG.md`:
  - Version history (v1.0.0, v0.9.0, etc.)
  - What changed in each version
  - Deprecation notices
  - Breaking changes

- [ ] T098 [P] Create `LICENSE.md` (choose MIT, CC-BY-4.0, or other)

- [ ] T099 [P] Create GitHub issue templates in `.github/ISSUE_TEMPLATE/`:
  - `bug_report.md`: Report errors or broken examples
  - `correction.md`: Report inaccuracies or outdated content
  - `feedback.md`: General feedback and suggestions
  - `feature_request.md`: Suggest new chapters or content

- [ ] T100 Final build and validation:
  - Run `npm run build`; verify no errors
  - Run `npm run start`; verify site preview works
  - Test all internal links
  - Verify all chapters render with correct metadata

**Checkpoint**: Book structure complete and ready for content authoring phase

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Docusaurus Config)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phases 3-6 (User Stories)**: All depend on Phase 2 completion
  - Can proceed sequentially (P1 → P2 → P3) or in parallel (if staffed)
  - Each user story is independently testable
- **Phase 7 (Polish)**: Depends on Phase 2 completion; final tasks after user stories

### Within Each Phase

- All Setup tasks (Phase 1): Generally parallelizable
- All Docusaurus tasks (Phase 2): Mostly sequential (need config before MDX components)
- All User Story tasks: Can be worked independently once Phases 1-2 complete

### Task Dependencies

- T001-T008 (environment verification) should complete before T009-T015 (research)
- T016-T020 (Docusaurus init) should complete before T021-T040 (configuration)
- T016-T040 (Docusaurus setup) BLOCKS T047-T082 (user story work)
- T047-T070 (templates and stubs for US1) enables author work
- T071-T083 (US2 navigation) depends on T047-T070 (chapter stubs)
- T084-T090 (US3 custom paths) depends on T047-T070 (chapter prerequisites)
- T091-T095 (US4 versioning) depends on T047-T070 (chapter structure)

### Parallel Opportunities

**Phase 1**: All verification tasks marked [P] can run in parallel
**Phase 2**: Can parallelize:
- T005-T007 (dependency docs)
- T013-T014 (tool research)
- T018-T019 (npm packages)
- T022-T025 (Docusaurus config)
- T032-T036 (MDX components)

**Phase 3**: Can parallelize:
- T048-T050 (templates for code/exercises/capstones)
- T053-T061 (folder structure creation across modules)

**After Phase 2**: User Stories 1-4 can be worked in parallel if team capacity allows

---

## Parallel Example: Phase 3 (Template & Folder Creation)

```
# These can run in parallel:
T048: Create code example template
T049: Create exercise template
T050: Create capstone template

T053: Create Module 1 folders
T054: Create Module 2 folders (after T053, different folder)
T055: Create Module 3 folders (after T054, different folder)

# Then combine results:
T057-T061: Create chapter stubs (depends on folders ready)
```

---

## Implementation Strategy

### MVP First (Just User Story 1)

1. Complete Phase 1: Environment Setup (Days 1-5)
2. Complete Phase 2: Docusaurus Config (Days 6-12)
3. Complete Phase 3: Create US1 templates and stubs (Days 13-17)
4. **STOP and VALIDATE**: Authors can create chapters independently
5. Demonstrate: A sample chapter authored and published

### Incremental Delivery with User Stories

1. Phase 1 + Phase 2 → Foundation ready
2. Phase 3 (US1) → Authors can create structured content
3. Phase 4 (US2) → Learners can navigate and progress
4. Phase 5 (US3) → Instructors can customize paths
5. Phase 6 (US4) → Maintainers can version and deprecate
6. Phase 7 → Polish and finalize

### Team Strategy (Multiple Contributors)

With 3 developers:
1. Days 1-5: Team completes Phase 1 together
2. Days 6-12: Team completes Phase 2 together
3. Days 13+:
   - Developer A: Phase 3 (author templates & stubs)
   - Developer B: Phase 4 (learner navigation)
   - Developer C: Phase 5-6 (customization & versioning)
4. Days 17-20: Team completes Phase 7 (polish)

---

## Quality Checkpoints

✅ **After Phase 2**: Docusaurus builds without errors, local preview works
✅ **After Phase 3**: Authors can create chapters using templates; chapters appear in sidebar
✅ **After Phase 4**: Learners can identify starting chapter and navigate sequentially
✅ **After Phase 5**: Custom learning paths can be generated with dependency resolution
✅ **After Phase 6**: Versions can be created and deprecated correctly
✅ **After Phase 7**: All documentation complete, book ready for content authoring

---

## Notes

- [P] marked tasks = different files/folders, no dependencies with other tasks in same phase
- Each user story independently completable and testable
- Commit after each logical group (1-3 tasks) for good history
- Stop at any checkpoint to validate story independently
- Next phase: Content authoring (Phase 3 of plan.md) - authors use templates from Phase 3 to write chapters
