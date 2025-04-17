import mss
import time
import keyboard
import win32api, win32con
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
import cv2
import gymnasium as gym
#from paddleocr import PaddleOCR
import re
import os
import math
import random
from torch.utils.tensorboard import SummaryWriter
class minecraftenv(gym.Env):
    
    def __init__(self):
        #initializes all necessary variables, kinda like an object which is cool
        #self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        self.sct = mss.mss()
        #self.text_region = {"top": 450, "left": 1650, "width": 250, "height": 100,"monitor": self.sct.monitors[1]}
        self.screen_region = {"top": 296, "left": 716, "width": 488, "height": 488, "monitor" : self.sct.monitors[1]}
        self.action_space = gym.spaces.MultiDiscrete([20, 20])
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(224, 224, 3), dtype=np.uint8)
        self.current_step = 0
        self.max_step = 10
        #self.curmithril = 0
        #self.pastmithril = 0
        self.writer = SummaryWriter("./logs/run_7")
        self.vertical = 0
        keyboard.press('space')
        
    def _get_observation(self):
        #unsure if its needed to convert MSS's screen capture to RGB, looks good to me
        screenshot = np.array(self.sct.grab(self.screen_region))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)  # Convert from BGRA to BGR
        frame = cv2.resize(frame, (224, 224))  # Resize for simplicity
        
        return frame
    def reset(self, seed = None, options = None):
        """
        Reset the environment to the initial state.
        """
        self.current_step = 0  # Reset step counter
        observation = self._get_observation()
        info = {}  # Return an empty dictionary for additional metadata
        return observation, info
    def smooth_mouse_move(self,delta_x, delta_y, steps=40):
        prev_x, prev_y = 0, 0

        # Smooth S-curve easing for human-like speed change
        progress_values = [(1 - math.cos(i / (steps - 1) * math.pi)) / 2 for i in range(steps)]

        for i in range(steps):
            progress = progress_values[i]

            # Target coordinates based on progress
            target_x = round(progress * delta_x)
            target_y = round(progress * delta_y)

            # Add slight curve/wobble (simulating hand movement imprecision)
            wobble_x = random.uniform(-0.5, 0.5) * (1 - abs(0.5 - progress) * 2)  # Max in middle of path
            wobble_y = random.uniform(-0.5, 0.5) * (1 - abs(0.5 - progress) * 2)

            target_x += int(wobble_x)
            target_y += int(wobble_y)

            # Calculate delta from previous
            move_x = target_x - prev_x
            move_y = target_y - prev_y
            prev_x, prev_y = target_x, target_y

            # Actually move the mouse
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, move_x, move_y, 0, 0)

            # Randomized delay to mimic inconsistent hand speed
            time.sleep(random.uniform(0.005, 0.012))

        # Final correction step (in case rounding undershot)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, delta_x - prev_x, delta_y - prev_y, 0, 0)
    def get_pixel_color(self,x, y):
        
            # Capture the screen region
        screenshot = np.array(self.sct.grab(self.screen_region))

        # Get the pixel color at (x, y)
        color = screenshot[y, x, :3]  # Extract RGB values (ignore alpha channel)
        return color
    def step(self,action):
        reward = 0
        self.smooth_mouse_move(round(action[0])*10, round(action[1])*10, steps=30)
        # Clamp vertical tilt to [-50, 50]
        self.vertical += action[1]*10  # Adjust the tilt based on action
        if self.vertical > 50:
            self.vertical = 50
        elif self.vertical < -50:
            self.vertical = -50

        # Apply penalties for extreme tilt ranges
        if self.vertical > 30:
            reward -= 0.5
        elif self.vertical < -30:
            reward -= 0.5
        colr = self.get_pixel_color(244, 244)
        mithril = colr[0]
        titanium = colr[1]
        bedrock = colr[2]
        mith = False
        tita = False
        print("just moved")
        if mithril > 100 and titanium + bedrock == 0:
            print("looking at mithril")
            mith = True
            reward += 1
        elif titanium > 100 and mithril + bedrock == 0:
            tita = True
            print("looking at titanium")
            reward += 1
        else:
            print("looking at something else")
            reward -= 1
        print("waiting for break")
        time.sleep(0.5)
        if mithril > 100 and titanium + bedrock == 0:
            print("looking at mithril")
            reward -= 2.5
        elif titanium > 100 and mithril + bedrock == 0:
            print("looking at titanium")
            if mith == True:
                reward += 1.5
        elif bedrock > 100 and mithril + titanium == 0:
            if tita == True or tita == True:
                print("looking at bedrock")
                reward += 1.5
        else:
            print("looking at something else")
            reward -= 3
        colr = self.get_pixel_color(244, 244)
        if(titanium > 100 and mithril + bedrock == 0) or (bedrock > 100 and mithril + titanium == 0):
            print("looking at titanium or bedrock")
            reward += 0.5
        else:
            print("looking at mithril or something else")
            reward -= 1
        self.current_step += 1
        self.writer.add_scalar("reward/step", reward, self.current_step)
        info = {"reward": reward, "action_taken": action.tolist()  }
        obs = self._get_observation()
        return obs, reward, False, False, info
class StopTrainingCallback(BaseCallback):
    def __init__(self, verbose=1):
        super().__init__(verbose)
    def _on_step(self) -> bool:
        infos = self.locals["infos"]
        print(f"[Callback] Step call #{self.n_calls}")
        if keyboard.is_pressed('h'):
            print("Hotkey Cancelled")
            return False
        for info in infos:
            if "current_mithril" in info:
                self.logger.record("environment/current_mithril", info["current_mithril"])
            if "reward" in info:
                self.logger.record("environment/reward", info["reward"])
        return True

def main():
    
    env = DummyVecEnv([minecraftenv])  
    if os.path.exists("mithrilminingPPO.zip"):
        model = PPO.load("mithrilminingPPO.zip", env = env)

    else:
        model = PPO("CnnPolicy", env, verbose=2, ent_coef=0.1, n_steps=128, batch_size=16, learning_rate=0.0001, tensorboard_log="./logs/")
    callback = StopTrainingCallback()
    print("training started!")
    model.learn(total_timesteps= 2500, tb_log_name="run_17",callback=callback, log_interval=1) 
    print("Training finished. Saving the model...")
    model.save("mithrilminingPPO")
    print(f"Model saved")
main()