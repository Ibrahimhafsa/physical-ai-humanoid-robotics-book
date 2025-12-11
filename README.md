# AI & Physical Robotics Book

A comprehensive, open-source educational resource for learning AI and robotics from fundamentals to advanced topics. Built with Docusaurus for easy reading, contribution, and community collaboration.

## 🚀 Quick Start

### View the Book Online
The book is published at: [https://ai-physical-robotics-book.github.io](https://ai-physical-robotics-book.github.io)

### Run Locally

#### Prerequisites
- Node.js 18+ and npm 8+
- Python 3.9+ (for code examples)
- Git

#### Installation

```bash
# Clone the repository
git clone https://github.com/ai-physical-robotics/ai-physical-robotics-book.git
cd ai-physical-robotics-book

# Install JavaScript dependencies
cd book-docs
npm install

# Start the development server
npm start
```

The site will be available at `http://localhost:3000`

## 📚 Book Structure

The book is organized into 5 modules with 15-20 chapters:

### Module 1: Fundamentals (3 chapters)
- What is Physical AI?
- Embodied Intelligence
- Basics of Robotics

### Module 2: Humanoid Robotics (5 chapters)
- ROS 2 Architecture
- Nodes and Topics
- Robot Control Basics
- Kinematics and Dynamics
- Navigation and Planning

### Module 3: Digital Twin (4 chapters)
- Simulation Fundamentals
- Gazebo Setup Tutorial
- Unity Robotics Introduction
- Physics Simulation

### Module 4: AI Brain (4 chapters)
- NVIDIA Isaac Overview
- Computer Vision Basics
- Deep Learning for Robotics
- Reinforcement Learning

### Module 5: Vision-Language-Action (VLA) (3 chapters)
- Multimodal Learning
- Language Grounding
- End-to-End Robotics

## 🔧 Development

### Build the Site
```bash
cd book-docs
npm run build
```

### Serve Built Site Locally
```bash
cd book-docs
npm run serve
```

### Deploy to GitHub Pages
```bash
cd book-docs
npm run deploy
```

## ✏️ Contributing

We welcome contributions! Here's how to get involved:

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/ai-physical-robotics-book.git
cd ai-physical-robotics-book
git checkout -b feature/my-contribution
```

### 2. Write Content
Use the templates provided in `.specify/templates/`:
- `chapter-template.md` - Write a new chapter
- `code-example-template.py` - Add a code example
- `exercise-template.md` - Create an exercise
- `capstone-template.md` - Design a capstone project

### 3. Follow Guidelines
See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Code style standards
- Documentation requirements
- Review process
- Expected response times

### 4. Submit a Pull Request
- Ensure all tests pass: `npm run build`
- Add a clear description of your changes
- Reference any related issues

## 📖 Using the Book

### For Learners
- **Start with Module 1** if you're new to robotics
- **Check prerequisites** before each chapter
- **Do the exercises** to reinforce learning
- **Try the capstone projects** for practical integration

### For Instructors
- **Customize learning paths** using our module selection tools
- **Export for your classroom** (PDF or HTML)
- **Add your own exercises** and assignments
- See [INSTRUCTOR_GUIDE.md](./docs/INSTRUCTOR_GUIDE.md) for details

### For Contributors
- **Review templates** in `.specify/templates/`
- **Follow the authoring guide** in `.specify/AUTHORING_GUIDE.md`
- **Test code examples** before submitting
- **Use the checklist** in CONTRIBUTING.md for reviews

## 📦 Code Examples

All code examples are in the `examples/` directory, organized by chapter:

```
examples/
├── chapter-01-physical-ai/
│   ├── README.md              # Setup instructions
│   ├── requirements.txt       # Dependencies
│   └── example.py             # Example code
├── chapter-02-embodied-intelligence/
│   └── ...
└── capstone-module-1/         # Capstone projects
```

### Running Examples

```bash
cd examples/chapter-01-physical-ai
pip install -r requirements.txt
python example.py
```

Each example includes:
- Clear documentation
- Setup instructions
- Expected output
- Troubleshooting guide

## 🧪 Testing

### Validate Build
```bash
cd book-docs
npm run build
```

### Lint Code Examples
```bash
cd examples
flake8 .                    # PEP 8 style checking
pylint *.py                 # Code analysis
black .                     # Code formatting
pytest                      # Run unit tests
```

## 🐛 Reporting Issues

Found a bug or have a suggestion? Please:

1. **Check existing issues** at [GitHub Issues](https://github.com/ai-physical-robotics/ai-physical-robotics-book/issues)
2. **Create a new issue** if yours doesn't exist
3. **Include:**
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Node.js version, etc.)

## 💬 Community Discussion

Have questions or want to discuss ideas?

- [GitHub Discussions](https://github.com/ai-physical-robotics/ai-physical-robotics-book/discussions)
- Start a discussion for:
  - Questions about chapters
  - Alternative solutions
  - Book improvement suggestions
  - General robotics/AI topics

## 📄 Documentation

- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines and workflow
- **[.specify/AUTHORING_GUIDE.md](./.specify/AUTHORING_GUIDE.md)** - Detailed authoring instructions
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history and updates
- **[LICENSE.md](./LICENSE.md)** - License information (MIT)

## 📊 Project Status

**Current Phase:** Phase 3 - Chapter Templates & Module Structure Complete

**Completion:**
- ✅ Phase 1: Environment Setup (100%)
- ✅ Phase 2: Docusaurus Configuration (100%)
- ✅ Phase 3: Templates & Module Structure (100%)
- 🔄 Phase 4: Navigation Features (In Progress)
- ⏳ Phase 5: Content Writing & Development (Planned)
- ⏳ Phase 6: Testing & Quality Assurance (Planned)
- ⏳ Phase 7: Deployment (Planned)

**Latest Release:** v0.1.0-alpha (Initial Structure)

## 🔗 Resources

- [ROS 2 Documentation](https://docs.ros.org/)
- [Docusaurus Documentation](https://docusaurus.io/)
- [Python Best Practices](https://pep8.org/)
- [Robotics Community](https://www.robotics.org/)

## 📞 Support

### Getting Help
1. Check the [FAQ](./docs/FAQ.md)
2. Search [existing issues](https://github.com/ai-physical-robotics/ai-physical-robotics-book/issues)
3. Ask in [Discussions](https://github.com/ai-physical-robotics/ai-physical-robotics-book/discussions)
4. Open a [new issue](https://github.com/ai-physical-robotics/ai-physical-robotics-book/issues/new)

### For Instructors
- Check [INSTRUCTOR_GUIDE.md](./docs/INSTRUCTOR_GUIDE.md)
- Browse [export tools](./tools/)
- Contact maintainers for curriculum customization

## 📈 Roadmap

**Next Steps (Q1 2025):**
- Complete Module 1 content authoring
- Create 15+ code examples
- Add 30+ exercises
- Set up CI/CD pipelines

**Future (Q2-Q3 2025):**
- Complete all module content
- Implement versioning system
- Add internationalization (Spanish, Chinese)
- Launch community contribution program

## 🤝 Acknowledgments

This project builds on the work of educators, roboticists, and open-source contributors in the AI and robotics communities.

**Special thanks to:**
- ROS 2 maintainers and community
- Docusaurus team for excellent documentation tooling
- Early contributors and reviewers

## 📜 License

This project is licensed under the MIT License - see [LICENSE.md](./LICENSE.md) for details.

**Content:** All chapter content and examples are provided as educational material.
**Code:** All code examples are open source and available for educational and research use.

## 🌟 Star & Follow

If you find this project useful, please:
- ⭐ Star this repository
- 🔔 Follow for updates
- 📢 Share with others learning robotics and AI

---

**Last Updated:** 2025-12-12
**Version:** 0.1.0-alpha
**Maintainers:** [AI & Physical Robotics Team](https://github.com/ai-physical-robotics)

For the latest updates, visit [our GitHub repository](https://github.com/ai-physical-robotics/ai-physical-robotics-book)
