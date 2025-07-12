# PyTorch-Based Game Automation

**Duration:** Sept. 2023 – Jan. 2024  
**Tech Stack:** PyTorch, Stable-Baselines3, TensorFlow, Win32 API, MSS

## Project Summary

This project focuses on training a reinforcement learning agent to interact with a game using screen captures and simulated mouse inputs. It combines a custom environment with visual input processing and progressive training phases to teach increasingly complex tasks.

## What I Built

- **Custom RL Environment**  
  I created a custom environment using `Stable-Baselines3`. The agent interacts with the game via the Win32 API for mouse inputs (action space) and uses `mss` to capture specific regions of the screen (observation space).

- **Model Selection & Training**  
  I tested different convolutional architectures and hyperparameters. PPO (Proximal Policy Optimization) with low entropy and a small learning rate gave the best results for this type of visual task.

- **Real-Time Logging**  
  Added TensorFlow-based logging to track average reward, episode performance, and other key metrics during training.

- **Progressive Task Learning**  
  Training was done in stages:
  1. Mouse movement and clicking
  2. Depth-based decision-making
  3. Visual recognition of in-game objects  
  This helped the agent learn in a more stable and interpretable way.

## Results

- The agent became increasingly accurate with fine motor tasks and visual recognition.
- PPO outperformed other models in terms of stability and convergence.
- Logging made it easy to track issues and measure performance during longer runs.

## Tools & Dependencies

- Python 3.8+
- PyTorch
- Stable-Baselines3
- TensorFlow
- `mss` (for screen capture)
- `pywin32` (for Windows API)

## Next Steps

- Use frame stacking or optical flow to give the agent better temporal awareness.
- Speed up training with parallel environments.
- Test on other games or interfaces with similar control schemes.

---

This was a fun way to explore reinforcement learning in a more practical and visual setting. It also gave me deeper insight into reward shaping, policy tuning, and debugging real-world agents.
