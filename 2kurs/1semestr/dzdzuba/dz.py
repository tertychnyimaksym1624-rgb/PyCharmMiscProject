import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

x = [4,7,6,8,5,4,5,8,7,6,9,4,3,8,6,5,5,8,10,5]
n = len(x)
x_sort = np.sort(x)
print(f"n = {n}")
print(f"Варіаційний ряд: {x_sort}")

# --- ЧАСТОТИ ---
freq = Counter(x_sort)
vals = sorted(freq.keys())
cnts = [freq[v] for v in vals]

print("\n--- Частоти ---")
print(f"{'xi':<5} | {'ni':<5}")
print("-" * 15)
for v, c in zip(vals, cnts):
    print(f"{v:<5} | {c:<5}")

#Обрахунок числових характеристик
x_mean = np.mean(x)
var_n = np.var(x, ddof=0)
var_n1 = np.var(x, ddof=1)
std_n = np.std(x, ddof=0)
std_n1 = np.std(x, ddof=1)
x_range = np.max(x) - np.min(x)
x_med = np.median(x)
x_mode = max(freq, key=freq.get)
Q = (x_sort[14] - x_sort[4]) / 2
V = (std_n1 / x_mean) * 100
A = np.mean(x - x_mean**3) / (std_n**3)
E = (np.mean(x - x_mean**4) / (std_n**4)) - 3


print("-"*50)
print("\n--- Числові характеристики ---")
print(f"\n1)Вибірркове середнє:  x̄ = {x_mean}")
print(f"2)Вибіркова дисперсія:  D = {var_n:.4f}")
print(f"3)Підправлена дисперсія:  s² = {var_n1:.4f}")
print(f"4)Вибіркове серднє квадратичне відхилення:  σ = {std_n:.4f}")
print(f"5)Підправлене середнє квадратичне відхилення:  s = {std_n1:.4f}")
print(f"6)Розмах вибірки:  R = {x_range}")
print(f"7)Медіана:  Me = {x_med}")
print(f"8)Мода:  Mo = {x_mode} ({freq[x_mode]} разів)")
print(f"9)Квадратильне відхилення:  Q = {Q}")
print(f"10)Коефіціієнт варіації: V = {V:.2f}%")
print(f"11)Коефіцієнт асиметрії: A = {A:.4f}")
print(f"12)Ексцес для вибірки: E = {E:.4f}")
print("-"*50)




#Побудова графіків
plt.figure(figsize=(16, 8))
# Гістограма
plt.subplot(1, 2, 1)
plt.hist(x, bins=int(((min(x)+max(x))/2)+1),color="green",
         edgecolor='black', align='left', rwidth=0.8)
plt.title('Статистичний розподіл вибірки')
plt.xlabel('Значення x')
plt.ylabel('Частота n')
plt.grid(axis='y', alpha=0.5)
plt.xticks(vals)
# Емпірична функція
plt.subplot(1, 2, 2)
x_cdf = np.sort(x)
y_cdf = np.arange(1, n+1) / n
plt.step(x_cdf, y_cdf,color="red", where='post')
plt.title('Емпірична функція розподілу')
plt.xlabel('Значення x')
plt.ylabel('Fn(x)')
plt.grid(True)
plt.yticks(np.arange(0, 1.1, 0.1))

plt.tight_layout()
plt.show()