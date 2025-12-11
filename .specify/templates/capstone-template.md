# Capstone Project: PROJECT_TITLE_HERE

**Module:** [Module Name] | **Difficulty:** Advanced | **Estimated Time:** 40-60 hours

## Project Overview

### Learning Objective
After completing this capstone project, you will be able to:
- Integrate concepts from [list chapters] into a cohesive solution
- Apply [major concept 1] and [major concept 2] together
- Demonstrate proficiency in [technical skill 1] and [technical skill 2]

### Real-World Context
Explain why this project matters and how it relates to industry/research applications.

> This capstone recreates the experience of [realistic scenario], which is encountered in [professional setting].

## Required Knowledge

Before starting this capstone, you must have completed:
- [ ] [Chapter 1 Name](../chapter-1) - Foundational concept A
- [ ] [Chapter 2 Name](../chapter-2) - Foundational concept B
- [ ] [Chapter 3 Name](../chapter-3) - Advanced topic
- [ ] [Chapter 4 Name](../chapter-4) - Integration technique

**Time to review:** 2-3 hours if rusty on any topic

## Project Setup

### Environment Requirements
- **Language:** Python 3.9+
- **OS:** Ubuntu 22.04 / Windows / macOS
- **ROS 2:** Humble (if applicable)
- **Simulator:** Gazebo Harmonic (if applicable)
- **Memory:** 4GB minimum, 8GB recommended
- **Disk Space:** 2GB for dependencies

### Installation Instructions

1. **Clone the starter code:**
   ```bash
   git clone https://github.com/ai-physical-robotics/capstone-[project-name].git
   cd capstone-[project-name]
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify setup:**
   ```bash
   python verify_setup.py
   ```

### Project Structure
```
capstone-[project-name]/
├── README.md                 # Setup instructions
├── requirements.txt          # Python dependencies
├── src/
│   ├── main.py              # Entry point
│   ├── module_1.py          # Component 1
│   └── module_2.py          # Component 2
├── tests/
│   ├── test_module_1.py
│   └── test_module_2.py
├── examples/
│   └── example_usage.py
├── data/
│   └── sample_data.json
└── docs/
    └── architecture.md
```

## Project Requirements

### Phase 1: Design (5-10 hours)

#### Design Document
Create a design document describing:
- **System Architecture:** How components interact
- **Data Flow:** How information moves through the system
- **Algorithm Design:** Key algorithms or approaches
- **Technology Choices:** Why you chose specific libraries/tools

**Deliverable:** `docs/design.md` (500-1000 words)

```markdown
# Design Document

## 1. System Architecture
[Diagram or description of system]

## 2. Data Flow
[How data moves through the system]

## 3. Key Algorithms
[Describe main algorithms/approaches]

## 4. Technology Stack
- Component A: [Technology] because [reason]
- Component B: [Technology] because [reason]
```

### Phase 2: Implementation (20-30 hours)

#### Core Features
Implement the following features:

- **Feature 1:** [Description]
  - Acceptance Criteria:
    - [ ] Function works correctly
    - [ ] Handles edge cases
    - [ ] Code is documented

- **Feature 2:** [Description]
  - Acceptance Criteria:
    - [ ] Function works correctly
    - [ ] Integrates with Feature 1
    - [ ] Performance acceptable

- **Feature 3:** [Description]
  - Acceptance Criteria:
    - [ ] Function works correctly
    - [ ] Follows design specification
    - [ ] Code tested

#### Code Quality Standards
- **Style:** Follow PEP 8 guidelines
- **Documentation:** Docstrings for all functions
- **Testing:** Unit tests for critical functions
- **Comments:** Explain complex logic
- **Error Handling:** Graceful failures with informative messages

### Phase 3: Testing (5-10 hours)

#### Unit Tests
Create tests for each component:
```python
def test_function_basic():
    """Test basic functionality."""
    result = function(input)
    assert result == expected_output

def test_function_edge_case():
    """Test edge cases."""
    result = function(edge_input)
    assert result is not None
```

#### Integration Tests
Test how components work together:
```bash
python -m pytest tests/
python tests/integration_test.py
```

#### System Test
Test the complete system:
```bash
python src/main.py
# Verify output is correct
```

**Test Report:** Document test results in `tests/TEST_REPORT.md`

### Phase 4: Documentation & Delivery (5-10 hours)

#### README with Setup Instructions
```markdown
# [Project Name]

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Run the project: `python src/main.py`
3. View results in output.txt

## Features
- Feature 1: [description]
- Feature 2: [description]
- Feature 3: [description]
```

#### Technical Documentation
- **API Documentation:** Describe functions and classes
- **Architecture Diagram:** System design visualization
- **Algorithm Documentation:** Explain complex algorithms

#### Reflection Paper (1-2 pages)
- What was the most challenging part?
- What would you do differently next time?
- How did you approach problem-solving?
- What did you learn?

## Deliverables Checklist

### Code Deliverables
- [ ] **Source Code:** Well-organized, documented, tested
  - Directory: `src/`
  - All functions have docstrings
  - No dead code or debug statements

- [ ] **Unit Tests:** >80% code coverage
  - Directory: `tests/`
  - Tests pass: `pytest tests/`

- [ ] **Examples:** Working examples demonstrating usage
  - Directory: `examples/`
  - README with instructions
  - Example runs without errors

### Documentation Deliverables
- [ ] **README.md:** Setup and usage instructions
- [ ] **Design Document:** `docs/design.md`
- [ ] **API Documentation:** `docs/api.md`
- [ ] **Test Report:** `tests/TEST_REPORT.md`
- [ ] **Reflection:** `docs/REFLECTION.md`

### Presentation Deliverables (if applicable)
- [ ] **Demo:** Functional system demonstration (10-15 min)
- [ ] **Slides:** Architecture and results (10-15 slides)
- [ ] **Video:** Screen recording of working system (optional)

## Grading Rubric

| Category | Excellent (5) | Good (4) | Satisfactory (3) | Needs Work (2) | Poor (1) |
|----------|---------------|---------|-----------------|----------------|----------|
| **Functionality** | All features work perfectly | Minor bugs | Most features work | Several bugs | Doesn't work |
| **Code Quality** | Clean, well-organized | Generally good | Readable | Messy | Unreadable |
| **Documentation** | Complete and clear | Mostly complete | Adequate | Incomplete | Missing |
| **Testing** | Comprehensive tests | Good coverage | Basic tests | Minimal testing | No tests |
| **Design** | Excellent architecture | Good design | Adequate design | Poor design | No design |
| **Integration** | Seamless integration | Works well together | Components work | Some issues | Doesn't integrate |
| **Presentation** | Professional, clear | Well-prepared | Adequate | Unprepared | Poor |

**Total: 35 points (5 points per category)**

## Success Criteria

Your capstone is successful when:

✓ **Functionality**
- All required features implemented and working
- Code runs without errors
- Output is correct and complete

✓ **Quality**
- Code is clean, readable, and well-documented
- Tests pass with >80% coverage
- No memory leaks or performance issues

✓ **Integration**
- Components work together seamlessly
- Design is followed consistently
- Architecture is sound

✓ **Documentation**
- Setup instructions are clear and accurate
- API is fully documented
- Design decisions explained

## Submission Instructions

### Step 1: Final Testing
```bash
cd capstone-[project-name]
pytest tests/
python src/main.py
```

### Step 2: Package Your Work
```bash
# Create project archive
zip -r capstone-[project-name].zip . -x ".git/*" "*.pyc" "__pycache__/*"

# Verify contents
unzip -l capstone-[project-name].zip | head -20
```

### Step 3: Submit
- [ ] Code pushed to GitHub repository
- [ ] All tests passing
- [ ] Documentation complete
- [ ] README has setup instructions
- [ ] Reflection paper included

**Submission Deadline:** [Date and Time]

## Troubleshooting Guide

### Setup Issues
**Problem:** ImportError for missing module
**Solution:** Run `pip install -r requirements.txt` again

**Problem:** Gazebo won't launch
**Solution:** [Check ROS 2 setup](https://docs.ros.org)

### Runtime Issues
**Problem:** Program crashes with AttributeError
**Solution:** Check data format matches expectations

**Problem:** Performance is too slow
**Solution:** Review algorithm complexity, consider optimization

## Resources

### Documentation
- [Chapter 1 Review](../chapter-1) - Refresh foundational concepts
- [Code Examples](../examples) - Reference implementations
- [Official Documentation](https://example.com) - API reference

### Similar Projects
- [Example Project 1](https://github.com/example)
- [Example Project 2](https://github.com/example)

### Community
- [GitHub Issues](https://github.com/ai-physical-robotics/ai-physical-robotics-book/issues)
- [Discussions](https://github.com/ai-physical-robotics/ai-physical-robotics-book/discussions)

## Next Steps

After completing this capstone:
1. Share your work with the community
2. Review others' solutions
3. Explore extensions and advanced topics
4. Consider contributing improvements

---

**Estimated Effort:** 40-60 hours
**Difficulty:** Advanced
**Prerequisites:** [List chapter links]
**Recommended Start Date:** [Date]
**Suggested Completion Date:** [Date + 3-4 weeks]
