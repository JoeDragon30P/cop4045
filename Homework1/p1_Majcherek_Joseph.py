import math
import matplotlib.pyplot as plt

def main():
    while True:
        a_input = input("Enter a: ")
        # this would be when to type entering ctrl+Z/EOf stop the program
        if a_input == "" or a_input == "\x1a":
            break

        a = float(a_input)
        b = float(input("Enter b: "))
        c = float(input("Enter c: "))
 
        discriminant = b**2 - 4 * a * c
        
        # This calculate roots and set plot domain bounds
        if discriminant < 0:
            print("no real solutions")
            x_center = -b / (2 * a)
            x_min = x_center - 5.0
            x_max = x_center + 5.0
        elif discriminant == 0:
            x1 = -b / (2 * a)
            print(f"one solution: {x1:.5f}")
            x_min = x1 - 4.0
            x_max = x1 + 4.0
        else:
            x1 = (-b - math.sqrt(discriminant)) / (2 * a)
            x2 = (-b + math.sqrt(discriminant)) / (2 * a)
            print(f"two solutions: x1={x1:.5f} x2={x2:.5f}")
            lower_root = min(x1, x2)
            upper_root = max(x1, x2)
            padding = max(2.0, (upper_root - lower_root) * 0.5)
            x_min = lower_root - padding
            x_max = upper_root + padding
        
        # Plot curve using matplotlib.pyplot to build a list of 150 points ploting
        num_points = 150
        step = (x_max - x_min) / (num_points - 1)

        xs = []
        ys = []
        for i in range(num_points):
            x_val = x_min + i * step
            y_val = a * (x_val**2) + b * x_val + c
            xs.append(x_val)
            ys.append(y_val)

        # plot curve using matplotlib.pyplot
        plt.figure()
        plt.plot(xs, ys, "b.-")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(f"y = {a}x^2 + {b}x + {c}")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    main()