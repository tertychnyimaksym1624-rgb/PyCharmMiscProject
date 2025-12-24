import numpy as np
import matplotlib.pyplot as plt

#Обрахунки
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris = np.genfromtxt(url, delimiter=',', dtype='object', encoding='utf-8')

spec = iris[:, 4].astype('str')
quan_charact = iris[:, :4].astype('float')
species_types = np.unique(spec)

# Дані для 3 та 4 графіків
vol = (np.pi * quan_charact[:, 2] * (quan_charact[:, 0]**2)) / 3
pl = quan_charact[:, 2]
p_cat = np.where(pl <= 3, "Валенькі", np.where(pl < 5, "Середні", "Великі"))
unique_cats, cat_counts = np.unique(p_cat, return_counts=True)

# Графіки
plt.figure(figsize=(14, 10))
# 1. Накладені гістограми розподілу
plt.subplot(2, 2, 1)
colors_map = {'Iris-setosa': 'red', 'Iris-versicolor': 'green', 'Iris-virginica': 'blue'}
for s in species_types:
    plt.hist(quan_charact[spec == s][:, 0], bins=10, alpha=0.5, label=s, color=colors_map[s])
plt.title("Розподіл Sepal Length за видами")
plt.xlabel("Довжина чашолистика (см)")
plt.ylabel("Частота (кількість)")
plt.legend()

# 2.Точкова діаграми з лініями кореляції
plt.subplot(2, 2, 2)
for s in species_types:
    mask = (spec == s)
    x, y = quan_charact[mask, 0], quan_charact[mask, 2]
    plt.scatter(x, y, label=s, alpha=0.5, c=colors_map[s])
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, c=colors_map[s], lw=2)
plt.title("Кореляція sl та pl за видами")
plt.xlabel("Довжина стебла")
plt.ylabel("Довжина пелюстки")
plt.legend()

# 3. Гістограма об'єму
plt.subplot(2, 2, 3)
plt.hist(vol, bins=15, color='teal', edgecolor='white', alpha=0.8)
plt.title("Гістограма об'єму чашолистика")
plt.xlabel("Об'єм ($см^3$)")
plt.ylabel("Кількість екземплярів")

# 4. Кругова діаграма
plt.subplot(2, 2, 4)
plt.pie(cat_counts, labels=unique_cats, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'], shadow=True)
plt.title("Категорії довжини пелюстки")

plt.tight_layout()
plt.show()