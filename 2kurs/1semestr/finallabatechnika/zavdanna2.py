import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi

def plot_gaussian_curves():
    print("\n--- Розрахунок площ під кривими Гауса ---")
    mu_array = [10]
    sigma_array = [1, 3, 6]
    x = np.linspace(-10, 30, 1000)

    plt.figure(figsize=(10, 6))
    for mu in mu_array:
        for sigma in sigma_array:
            # Розрахунок Y
            y = (1 / (sigma * sqrt(2 * pi))) * np.exp(- ((x - mu) ** 2) / (2 * sigma ** 2))

            # Розрахунок площі
            area = np.trapezoid(y, x)
            print(f"Параметри (mu={mu}, sigma={sigma}) -> Площа: {area:.5f}")

            plt.plot(x, y, linewidth=2, label=f'$\mu={mu}, \sigma={sigma}$')
    print("Висновок: Зі збільшенням параметру сігма графік стає ширшим і нижчим, але площа завжди дорівнює ~1.")
    print("-" * 40)
    plt.title('Gaussian Curves');
    plt.legend();
    plt.grid(True, alpha=0.3);
    plt.show()

plot_gaussian_curves()