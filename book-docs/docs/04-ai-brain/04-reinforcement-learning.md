---
title: "Reinforcement Learning for Robotics"
description: "Teaching robots to learn through interaction using reinforcement learning algorithms"
sidebar_position: 4
tags: ["reinforcement-learning", "q-learning", "policy-gradient", "robot-learning"]
module: "ai-brain"
estimated_time: "120 minutes"
prerequisites: ["./03-deep-learning-robotics"]
difficulty_level: "advanced"
authors: ["AI & Robotics Team"]
last_updated: "2025-12-12"
---

# Reinforcement Learning for Robotics

## Learning Objectives

After completing this chapter, learners will be able to:
- Understand reinforcement learning concepts and theory
- Apply classic RL algorithms (Q-learning, DQN) to robot tasks
- Implement policy gradient methods for continuous control
- Use simulation for safe RL training
- Deploy RL policies on real robots
- Understand sim-to-real transfer challenges and solutions

:::info Prerequisites
Before starting this chapter, ensure you have completed:
- [Deep Learning for Robotics](./03-deep-learning-robotics.md)
:::

## Lesson Content

### Section 1: Reinforcement Learning Fundamentals

RL enables robots to learn optimal behaviors through trial and error:

**Key Components:**
- **Agent:** The robot learning a task
- **Environment:** Physical or simulated world
- **State:** Current situation (sensor readings)
- **Action:** What the robot can do (motor commands)
- **Reward:** Feedback for good/bad behavior

**Learning Loop:**

```
┌─────────────────────────────────────────────┐
│ 1. Observe State (s_t)                      │
│ 2. Select Action (a_t) using Policy         │
│ 3. Receive Reward (r_t) + Next State (s_{t+1}) │
│ 4. Update Policy based on Reward            │
│ 5. Repeat                                   │
└─────────────────────────────────────────────┘
```

**Exploration vs. Exploitation:**
- **Exploration:** Try new actions to discover good behaviors
- **Exploitation:** Use known good actions for immediate reward
- **Balance:** Essential for effective learning

### Section 2: Classic RL Algorithms

**Q-Learning:**
Learns value of state-action pairs through temporal difference:

```python
Q(s,a) ← Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
```

- **Advantages:** Model-free, convergence guarantees
- **Disadvantages:** Discrete actions, poor scalability
- **Use Case:** Grid navigation, discrete control tasks

**Deep Q-Networks (DQN):**
Combines Q-learning with deep neural networks:

```python
import torch
import torch.nn as nn

class DQNAgent:
    def __init__(self, state_dim, action_dim):
        self.q_network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def select_action(self, state):
        q_values = self.q_network(state)
        return q_values.argmax()
```

- **Advantages:** Works with continuous state spaces
- **Disadvantages:** Discrete actions, off-policy, unstable
- **Use Case:** Complex perception tasks (camera-based control)

### Section 3: Policy Gradient Methods

Learn policy directly without value functions:

**REINFORCE Algorithm:**
```
∇J(θ) = E[∇log π_θ(a|s) * Q(s,a)]
```

- Directly optimize policy
- Works for continuous and discrete actions
- High variance, slow learning

**Actor-Critic Methods:**
Combine policy gradient (actor) with value function (critic):

```python
class ActorCritic:
    def __init__(self, state_dim, action_dim):
        self.actor = nn.Sequential(...)   # Policy
        self.critic = nn.Sequential(...)  # Value function

    def train_step(self, state, action, reward, next_state):
        # Critic learns to estimate value
        value_loss = compute_value_loss(...)

        # Actor improves policy using advantage
        advantage = reward - self.critic(state)
        policy_loss = -log_prob * advantage

        return value_loss + policy_loss
```

- **Advantages:** Lower variance, faster convergence
- **Use Case:** Continuous control (manipulation, locomotion)

**Proximal Policy Optimization (PPO):**
- Stable policy gradient with clipped objective
- Popular in robotics research
- Handles high-dimensional continuous control

### Section 4: Simulation for RL Training

Training in simulation enables safe, fast learning:

**Advantages:**
- Safety: No hardware damage from exploration
- Speed: Thousands of simulated trials per hour
- Reproducibility: Exact same conditions
- Parallelization: Train multiple agents simultaneously

**Challenges:**
- Sim-to-Real Gap: Simulation != reality
- Computational Cost: Training takes hours/days
- Tuning: Hyperparameters critical for success

### Section 5: Sim-to-Real Transfer

Deploying policies trained in simulation to real robots:

**Domain Randomization:**
- Vary simulation parameters (friction, mass, colors)
- Policy learns to be robust to variations
- Improves transfer to real world

**Real-World Fine-Tuning:**
- Train in simulation with randomization
- Deploy to real robot
- Fine-tune with real data (samples from real world)
- Reduces real-world training time

**Physics Accuracy:**
- More accurate simulation → better transfer
- Trade-off between accuracy and training speed

## Code Examples

This chapter includes reinforcement learning examples:

1. **Q-Learning Agent** - `chapter-04-rl/q_learning_robot.py`
   - Simple tabular Q-learning
   - Grid-based environment

2. **Policy Gradient** - `chapter-04-rl/policy_gradient.py`
   - REINFORCE algorithm
   - Continuous control task

3. **Sim-to-Real** - `chapter-04-rl/sim_to_real_transfer.py`
   - Domain randomization
   - Transfer learning pipeline

See the examples folder for complete code and setup instructions.

## Exercises

### Exercise 1: Implement Q-Learning Agent
**Difficulty:** Intermediate | **Time:** 60 minutes

Create Q-learning agent for navigation task:
- Define state/action spaces
- Implement Q-learning update rule
- Train on grid-world environment
- Plot learning curves (reward vs. episode)

**Acceptance Criteria:**
- Agent learns to reach goal efficiently
- Reward increases over training
- Final policy achieves high success rate (>90%)

---

### Exercise 2: Train Policy with Actor-Critic
**Difficulty:** Advanced | **Time:** 90 minutes

Implement actor-critic for continuous control:
- Define continuous action space
- Implement actor (policy) and critic (value)
- Train on control task in simulation
- Evaluate final policy performance

**Acceptance Criteria:**
- Policy learns smooth, effective control
- Critic loss decreases during training
- Task completion rate >80%

---

### Exercise 3: Sim-to-Real Transfer Project
**Difficulty:** Advanced | **Time:** 120 minutes

Complete sim-to-real pipeline:
- Train with domain randomization in simulation
- Evaluate on varied simulations
- Deploy to real robot (or detailed simulator)
- Measure transfer success rate
- Document performance gaps

**Acceptance Criteria:**
- Policy successfully transfers to reality
- Real-world performance >70% of simulation
- Identified causes of sim-to-real gap

## Capstone Guidance

Reinforcement Learning is essential for the **Module 4 Capstone: "AI-Powered Robot Brain"**

**How This Chapter Helps:**
- Skill 1: Design and implement RL algorithms for robot learning
- Skill 2: Use simulation to accelerate training safely
- Skill 3: Transfer policies from simulation to real robots

## Summary

In this chapter, we covered:
- **RL Fundamentals:** Agent, environment, reward, learning loop
- **Algorithms:** Q-learning, DQN, policy gradients, actor-critic
- **Simulation:** Safe training environment for robots
- **Sim-to-Real:** Domain randomization and transfer learning
- **Applications:** Navigation, manipulation, locomotion

## What's Next?

You've completed the AI Brain module! Now explore Vision-Language-Action for multimodal robot intelligence.

[Continue to VLA Module →](../05-vla/)

**Module Capstone:**
- [AI-Powered Robot Brain](../04-ai-brain/capstone.md)

**Alternative Paths:**
- [Review Deep Learning](./03-deep-learning-robotics.md)
- [Review Computer Vision](./02-computer-vision-basics.md)

## References & Attribution

- Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction. MIT Press.
- Silver, D., et al. (2016). Mastering the game of Go with deep neural networks and tree search.
- Levine, S., et al. (2016). End-to-End Training of Deep Visuomotor Policies.
- OpenAI Spinning Up: https://spinningup.openai.com/

---

**Last Updated:** 2025-12-12 | **Module:** AI Brain
