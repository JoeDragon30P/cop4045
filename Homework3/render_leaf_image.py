import math
import os
import matplotlib.pyplot as plt

def draw_leaf_branch(x: float, y: float, angle_deg: float, level: int, length: float, lines: list) -> None:
    """
    Recursively computes the line segments for draw_leaf_straight(6, 120).
    Follows the exact Turtle geometry:
      - forward(length)
      - left(45), recurse(level - 1, length * 0.5)
      - right(45), recurse(level - 1, length * 0.5)
      - backward(length)
    """
    if level <= 0 or length < 0.5:
         return

    # Calculate end point of current segment
    rad = math.radians(angle_deg)
    x_end = x + length * math.cos(rad)
    y_end = y + length * math.sin(rad)

    # Record segment for plotting
    lines.append(((x, x_end), (y, y_end)))

    # Left vein branch: left(45)
    draw_leaf_branch(x_end, y_end, angle_deg + 45.0, level - 1, length * 0.5, lines)

    # Right vein branch: right(45)
    draw_leaf_branch(x_end, y_end, angle_deg - 45.0, level - 1, length * 0.5, lines)


def main() -> None:
    segments = []
    # Start at (0, 0) facing vertically North (90 degrees), level=6, length=120
    draw_leaf_branch(0.0, 0.0, 90.0, 6, 120.0, segments)

    flg, ax = plt.subplots(figsize=(8, 10))

    for (xs, ys) in segments:
        ax.plot(xs, ys, color="black", linewidth=1.2)

    ax.set_aspect("equal")
    ax.axis("off")
    plt.title("draw_leaf_straight(6, 120) - Joseph Majcherek (Z23348563)", fontsize=11)

    # this save toward the Desktop directory
    desktop_dir = os.path.expanduser("~/Desktop")
    out_file = os.path.join(desktop_dir, "leaf_straight_6_120.png")

    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Successfully generated '{out_file}' without Tkinter!")

if __name__ == "__main__":
    main()