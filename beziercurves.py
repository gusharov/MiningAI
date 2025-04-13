import numpy as np
import math
import time

def bezier_curve(p0, p1, p2, t):
    """Generate a point on a quadratic Bézier curve."""
    return (1-t)**2 * p0 + 2 * (1-t) * t * p1 + t**2 * p2

def move_mouse_smoothly(start, end, duration=0.5, output_deltas=False):
    """
    Move the mouse smoothly using Bézier curves and optionally output raw deltas.

    Args:
        start (tuple): Starting position (x, y).
        end (tuple): Target position (x, y).
        duration (float): Total duration of the movement in seconds.
        output_deltas (bool): Whether to output raw mouse deltas.

    Returns:
        list: List of raw mouse deltas (deltaX, deltaY) if output_deltas is True.
    """
    # Define control point for Bézier curve (adding a vertical offset to simulate arc motion)
    p0 = np.array(start)
    p1 = np.array([(start[0] + end[0]) // 2, start[1] - 100])  # Control point
    p2 = np.array(end)

    steps = int(duration * 100)  # Number of steps
    deltas = []  # To store raw mouse deltas if needed

    for t in np.linspace(0, 1, steps):
        point = bezier_curve(p0, p1, p2, t)
        #pyautogui.moveTo(point[0], point[1])
        
        if output_deltas:
            if t > 0:  # Skip the first point since there is no previous position
                delta_x = point[0] - prev_point[0]
                delta_y = point[1] - prev_point[1]
                deltas.append((delta_x, delta_y))
        
        prev_point = point
        time.sleep(duration / steps)

    if output_deltas:
        return deltas

def calculate_mouse_deltas(current_pos, target_pos, step_size=5):
    """
    Calculate raw mouse deltas to move towards a target position.

    Args:
        current_pos (tuple): Current mouse position (x1, y1).
        target_pos (tuple): Target mouse position (x2, y2).
        step_size (float): The step size for movement.

    Returns:
        tuple: (deltaX, deltaY) for raw mouse movement.
    """
    x1, y1 = current_pos
    x2, y2 = target_pos
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    if distance == 0:
        return (0, 0)  # Target reached

    delta_x = step_size * (x2 - x1) / distance
    delta_y = step_size * (y2 - y1) / distance

    return (delta_x, delta_y)

# Example usage of Bézier curve-based movement with raw delta output
start_pos = (100, 100)
end_pos = (400, 300)
deltas = move_mouse_smoothly(start_pos, end_pos, duration=1.0, output_deltas=True)
print(f"Raw mouse deltas (using Bézier curve): {deltas}")

# Example usage of standalone raw delta calculation
current_pos = (100, 100)
target_pos = (400, 300)
delta_x, delta_y = calculate_mouse_deltas(current_pos, target_pos, step_size=10)
print(f"Raw mouse delta (direct calculation): ({delta_x}, {delta_y})")