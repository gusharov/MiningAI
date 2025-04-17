import time
import random
import win32api
import win32con
import math

import time
import random
import win32api
import win32con
import math

def smooth_mouse_move(delta_x, delta_y, steps=40):
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


def main():
    print("Starting faster human-like mouse movement with abrupt stop simulation...")
    time.sleep(1)  # Wait 1 second before starting

    # Example: Move the mouse by 200 pixels right and 100 pixels down
    smooth_mouse_move(100, 100, steps=30)  # Reduced steps for faster movement
    time.sleep(2)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 100, 100, 0, 0)
    print("Mouse movement completed.")

if __name__ == "__main__":
    main()