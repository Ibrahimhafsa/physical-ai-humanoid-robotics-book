---
title: "Gazebo Setup and Configuration"
description: "Installing and configuring Gazebo for robot simulation with ROS 2"
sidebar_position: 2
tags: ["gazebo", "simulation", "ros2", "setup"]
module: "digital-twin"
estimated_time: "90 minutes"
prerequisites: ["./01-simulation-fundamentals"]
difficulty_level: "intermediate"
authors: ["AI & Robotics Team"]
last_updated: "2025-12-12"
---

# Gazebo Setup and Configuration

## Learning Objectives

After completing this chapter, learners will be able to:
- Install and configure Gazebo for ROS 2
- Create and load robot URDF models
- Configure world files for simulation environments
- Run and control simulated robots
- Troubleshoot common Gazebo issues

:::info Prerequisites
Before starting this chapter, ensure you have completed:
- [Simulation Fundamentals](./01-simulation-fundamentals.md)
:::

## Lesson Content

### Section 1: Gazebo Installation

Gazebo Harmonic (latest stable release) works with ROS 2 Humble:

**Installation Steps:**
1. Add Gazebo repository
2. Install Gazebo binaries and ROS 2 integration packages
3. Verify installation with sample world
4. Configure environment variables

**System Requirements:**
- Ubuntu 22.04 LTS (recommended)
- 4GB RAM minimum (8GB recommended)
- 2GB disk space for models and dependencies

### Section 2: URDF Robot Modeling

URDF (Unified Robot Description Format) defines robot structure:

```xml
<robot name="simple_robot">
  <link name="base_link">
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.5 0.5 0.3"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.3"/>
      </geometry>
    </collision>
  </link>

  <joint name="wheel_joint" type="revolute">
    <parent link="base_link"/>
    <child link="wheel"/>
    <limit lower="-3.14" upper="3.14" effort="10" velocity="1"/>
  </joint>
</robot>
```

**Key Components:**
- **Links:** Rigid bodies (collision geometry, visual appearance, inertia)
- **Joints:** Connections between links (revolute, prismatic, fixed)
- **Inertia:** Mass distribution properties
- **Geometry:** Visual and collision shapes

### Section 3: World Files and Environments

World files (.world or .sdf) define the simulation environment:

**Contents:**
- Physics engine configuration
- Ground plane and static objects
- Lighting and visual settings
- Robot spawn positions
- Plugin configurations

### Section 4: Running Gazebo with ROS 2

Integration between Gazebo and ROS 2 enables robot control:

**Workflow:**
1. Define robot in URDF
2. Create world file with robot spawn
3. Launch Gazebo with ROS 2 launch file
4. Publish commands to ROS 2 topics
5. Subscribe to sensor data from simulation

## Code Examples

This chapter includes Gazebo setup examples:

1. **Simple URDF Model** - `chapter-02-gazebo/simple_robot.urdf`
   - Basic robot structure
   - Mass and geometry definition

2. **World File** - `chapter-02-gazebo/simple_world.world`
   - Ground plane, objects
   - Robot spawn configuration

3. **Launch File** - `chapter-02-gazebo/launch_gazebo.py`
   - ROS 2 launch configuration
   - Gazebo integration

See the examples folder for complete code and setup instructions.

## Exercises

### Exercise 1: Load a Pre-built Model
**Difficulty:** Beginner | **Time:** 20 minutes

Load a robot model from Gazebo model database:
- Launch Gazebo
- Insert model (e.g., TurtleBot3)
- Verify model loads correctly
- Document model properties

**Acceptance Criteria:**
- Model appears in Gazebo window
- No loading errors
- Model properties documented

---

### Exercise 2: Create a Custom Robot URDF
**Difficulty:** Intermediate | **Time:** 60 minutes

Design and create a simple robot URDF:
- Define base link with mass and geometry
- Add wheels/actuators
- Add sensors (camera, lidar)
- Load in Gazebo and verify

**Acceptance Criteria:**
- URDF loads without errors
- Robot appears correct in Gazebo
- All links and joints functional

---

### Exercise 3: Control Simulated Robot
**Difficulty:** Intermediate | **Time:** 45 minutes

Control a Gazebo robot via ROS 2 topics:
- Launch Gazebo with robot
- Create simple controller node
- Send movement commands
- Verify robot responds

**Acceptance Criteria:**
- Robot moves in response to commands
- Sensor data published correctly
- Movement matches command intent

## Capstone Guidance

Gazebo Configuration is essential for the **Module 3 Capstone: "Complete Digital Twin Simulation"**

**How This Chapter Helps:**
- Skill 1: Set up Gazebo environment for robot simulation
- Skill 2: Create custom robot URDF models
- Skill 3: Integrate ROS 2 control with Gazebo

## Summary

In this chapter, we covered:
- **Gazebo Installation:** Setting up ROS 2 and Gazebo integration
- **URDF Modeling:** Defining robot structure with links and joints
- **World Configuration:** Environments and simulation setup
- **ROS 2 Integration:** Publishing commands and subscribing to data

## What's Next?

Learn about Unity Robotics for high-quality visualization and alternative simulation.

[Continue to Next Chapter →](./03-unity-robotics-intro.md)

**Alternative Paths:**
- [Jump to Physics Simulation](./04-physics-simulation.md)
- [Return to Simulation Fundamentals](./01-simulation-fundamentals.md)

## References & Attribution

- Gazebo Official Documentation: https://gazebosim.org/
- ROS 2 Gazebo Integration: https://github.com/gazebosim/ros_gz

---

**Last Updated:** 2025-12-12 | **Module:** Digital Twin
