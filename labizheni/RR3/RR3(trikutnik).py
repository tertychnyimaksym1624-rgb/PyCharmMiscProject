import matplotlib.pyplot as plt


def draw_sierpinski(x1, y1, x2, y2, x3, y3, level):
    if level == 0:
        plt.fill([x1, x2, x3], [y1, y2, y3], 'blue')
        return
    x12 = (x1 + x2) / 2
    y12 = (y1 + y2) / 2
    x23 = (x2 + x3) / 2
    y23 = (y2 + y3) / 2
    x31 = (x3 + x1) / 2
    y31 = (y3 + y1) / 2
    draw_sierpinski(x1, y1, x12, y12, x31, y31, level - 1)
    draw_sierpinski(x12, y12, x2, y2, x23, y23, level - 1)
    draw_sierpinski(x31, y31, x23, y23, x3, y3, level - 1)
plt.figure(figsize=(8, 8))
plt.axis('equal')
plt.axis('off')
n = int(input("depth? "))

draw_sierpinski(0, 1, -1, -0.5, 1, -0.5, n)
plt.show()
