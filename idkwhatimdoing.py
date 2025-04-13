import mss
import time
import keyboard
import win32api, win32con
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import DummyVecEnv
import cv2
import gymnasium as gym
from paddleocr import PaddleOCR
import re
    
class minecraftenv(gym.Env):
    def __init__(self):
        #initializes all necessary variables, kinda like an object which is cool
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        self.sct = mss.mss()
        self.text_region = {"top": 450, "left": 1700, "width": 200, "height": 100,"monitor": self.sct.monitors[1]}
        self.screen_region = {"top": 300, "left": 500, "width": 800, "height": 500, "monitor" : self.sct.monitors[1]}
        self.current = win32api.GetCursorPos()
        self.action_space = gym.spaces.Box(low=-10, high=10, shape=(2,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(224, 224, 3), dtype=np.uint8)
        self.curmithril = 0
        self.pastmithril = 0
    def _get_observation(self):
        screenshot = np.array(self.sct.grab(self.screen_region))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)  # Convert from BGRA to BGR
        frame = cv2.resize(frame, (224, 224))  # Resize for simplicity
        screenshot = np.array(self.sct.grab(self.text_region))
        # Capture the screen region
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)
        # Convert to rgb for OCR
        result = self.ocr(screenshot, cls=True)
        mithrilcheck = 0
        print(result)
        words = []
        for line in result:
            if line != None:
                for box in line:
                    if isinstance(box[1], tuple) and len(box[1]) == 2:
                        text, confidence = box[1]
                        words.append(text)
        for word in words:
            if "Mithril" in word:
                mithrilcheck = re.sub(r"\D", "", word)
                break
        if mithrilcheck == '':
            mithrilcheck = 0
        mithrilcheck = int(mithrilcheck)
        if mithrilcheck != 0:
            self.curmithril = mithrilcheck
            if self.pastmithril == 0:
                self.pastmithril = mithrilcheck
        return frame
    def reset(self, seed = None, options = None):
        """
        Reset the environment to the initial state.
        """
        super().reset(seed=seed)  # Call the parent class's reset method, if needed
        self.current_step = 0  # Reset step counter
        self.current_position = win32api.GetCursorPos()  # Reset mouse position
        observation = self._get_observation()
        info = {}  # Return an empty dictionary for additional metadata
        return observation, info
    
    def step(self,action):

        delta_x, delta_y = int(action[0]), int(action[1])
        keyboard.press('space')
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,delta_x,delta_y,0,0)
        obs = self._get_observation()
        reward = 0
        if self.curmithril > self.pastmithril:
            reward += 10
        #if delta_x + delta_y > 20:
        #   reward += 2
        self.current_step += 1
        
        return obs, reward, False, False, {}
def main():
    
    
    time.sleep(2)
    env = DummyVecEnv([minecraftenv])
    model = PPO("CnnPolicy", env, verbose=1)
    print("training started!")
    model.learn(1000) 
    print("Training finished. Saving the model...")
    model.save()
    print(f"Model saved")
main()