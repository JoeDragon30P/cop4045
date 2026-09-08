import math
import matplotlib.pyplot as plt

def plot_function(fun_str, domain, ns):
    xmin, xmax = domain
    step = (xmax - xmin) / (ns - 1)

    xs = [xmin + i * step for i in range(ns)]
    ys = []

    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    # Print formatted output table
    print(f"{'x':>10} {'y':>10}")
    for x_val, y_val in zip(xs, ys):
        print(f"{x_val:+10.4f} {y_val:+10.4f}")

    # plot function graph
    plt.figure()
    plt.plot(xs, ys, "b.-")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.grid(True)
    plt.show()

def main():
    fun_str = input("Enter function with variable x: ")
    ns = int(input("Enter number of samples: "))
    xmin = float(input("Enter xmin: "))
    xmax = float(input("Enter xmax: "))

    plot_function(fun_str, (xmin, xmax), ns)

if __name__ == "__main__":
    main()