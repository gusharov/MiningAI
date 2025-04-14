import time
import random
import win32api
import win32con
import math

def smooth_mouse_move(delta_x, delta_y, steps=30):
    """
    Moves the mouse smoothly like a human by starting slow, peaking at the middle,
    and stopping more abruptly at the end.

    :param delta_x: Total x-axis movement (in pixels).
    :param delta_y: Total y-axis movement (in pixels).
    :param steps: Number of steps to break the movement into (fewer steps = faster movement).
    """
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

def main():
    print("Starting faster human-like mouse movement with abrupt stop simulation...")
    time.sleep(1)  # Wait 1 second before starting

    # Example: Move the mouse by 200 pixels right and 100 pixels down
    smooth_mouse_move(100, 100, steps=30)  # Reduced steps for faster movement

    print("Mouse movement completed.")

if __name__ == "__main__":
    main()