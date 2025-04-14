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
from paddleocr import PaddleOCR
import re
import os
import math
import random
class minecraftenv(gym.Env):
    def __init__(self):
        #initializes all necessary variables, kinda like an object which is cool
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        self.sct = mss.mss()
        self.text_region = {"top": 450, "left": 1650, "width": 250, "height": 100,"monitor": self.sct.monitors[1]}
        self.screen_region = {"top": 174, "left": 594, "width": 732, "height": 732, "monitor" : self.sct.monitors[1]}
        self.action_space = gym.spaces.Box(low=-100, high=100, shape=(2,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(224, 224, 3), dtype=np.uint8)
        self.current_step = 0
        self.max_step = 5
        self.curmithril = 0
        self.pastmithril = 0
        keyboard.press('space')
    def _get_observation(self):
        #unsure if its needed to convert MSS's screen capture to RGB, looks good to me
        screenshot = np.array(self.sct.grab(self.screen_region))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)  # Convert from BGRA to BGR
        frame = cv2.resize(frame, (224, 224))  # Resize for simplicity
        screenshot = np.array(self.sct.grab(self.text_region))
        # Capture the screen region
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)
        # Convert to rgb for OCR
        result = self.ocr(screenshot, cls=True)
        #print(result)                 
        mithrilcheck = ""
        if result[0] == None:

            print("It is none :(")
        else:
            for i in range(len(result[1])):
                if "Mithril" in result[1][i][0]:
                    mithrilcheck = re.sub(r"\D", "", result[1][i][0])
                    break
        if mithrilcheck != "":
            self.curmithril = int(mithrilcheck)
        if self.pastmithril == 0:
            self.pastmithril = self.curmithril
        print("current mithril powder:", self.curmithril)

        
        return frame
    def reset(self, seed = None, options = None):
        """
        Reset the environment to the initial state.
        """
        self.current_step = 0  # Reset step counter
        observation = self._get_observation()
        info = {}  # Return an empty dictionary for additional metadata
        return observation, info
    def smooth_mouse_move(self,delta_x, delta_y, steps=30):
        
        # Pre-compute the easing progress for each step (using the sinusoidal easing function)
        progress_values = [(1 - math.cos(i / steps * math.pi)) ** 2 for i in range(steps)]

        # Initialize previous positions
        prev_x, prev_y = 0, 0

        # Pre-compute random delays for efficiency
        delays = [random.uniform(0.005, 0.01) for _ in range(steps)]

        # Perform the mouse movement
        for step in range(steps):
            # Get the current progress
            progress = progress_values[step]

            # Calculate the current target position based on progress
            current_x = round(progress * delta_x)
            current_y = round(progress * delta_y)

            # Calculate the incremental movement for this step
            move_x = current_x - prev_x
            move_y = current_y - prev_y
            prev_x, prev_y = current_x, current_y

            # Move the mouse by the calculated delta
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, move_x, move_y, 0, 0)

            # Add a short delay between steps
            time.sleep(delays[step])
    def step(self,action):
        print("action", action)
        self.smooth_mouse_move(int(action[0]), int(action[1]), steps=30)
        obs = self._get_observation()
        reward = 0
        movement_magnitude = abs(action[0]) + abs(action[1])
        reward += 0.1 * movement_magnitude  # Scale this factor as needed
        if self.curmithril > self.pastmithril:
            self.pastmithril = self.curmithril
            reward += 1

        self.current_step += 1
        print("current step" , self.current_step)
        
        done = self.current_step >= self.max_step
            
        return obs, reward, done, False, {}
class StopTrainingCallback(BaseCallback):
    def __init__(self, max_calls=5, verbose=1):
        super().__init__(verbose)
        self.max_calls = max_calls
        self.n_calls = 0

    def _on_step(self) -> bool:
        self.n_calls += 1
        print(f"[Callback] Step call #{self.n_calls/2}")
        if keyboard.is_pressed('h'):
            print("Hotkey Cancelled")
            return False
        if self.n_calls >= self.max_calls:
            print("[Callback] Reached max_calls, stopping training early.")
            return False  # Returning False stops training
        return True

def main():
    
    env = DummyVecEnv([minecraftenv])  
    if os.path.exists("mithrilminingPPO.zip"):
        model = PPO.load("mithrilminingPPO.zip")
        model.set_env(env)
    else:
        model = PPO("CnnPolicy", env, verbose=1, ent_coef=0.2,)
    callback = StopTrainingCallback(max_calls=200)
    print("training started!")
    model.learn(10, callback=callback) 
    print("Training finished. Saving the model...")
    model.save("mithrilminingPPO")
    print(f"Model saved")
main()