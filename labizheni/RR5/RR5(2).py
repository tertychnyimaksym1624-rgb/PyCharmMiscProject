import numpy as np

# Підготовка: Завантаження даних
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris = np.genfromtxt(url, delimiter=',', dtype='object', encoding='utf-8')

# 1. Стовпець species у 1D-масив spec
spec = iris[:, 4].astype('str')

# 2. Кількісні характеристики у 2D-масив quan_charact
quan_charact = iris[:, :4].astype('float')

# 3. Середнє, медіана, СВ для стовпця sepallength
sl = quan_charact[:, 0]
print("Пункт 3 (Середнє, Медіана, СВ):", np.mean(sl), np.median(sl), np.std(sl))

# 4. Нормалізація sepallength (0-1)
sl_norm = (sl - sl.min()) / (sl.max() - sl.min())
print("Пункт 4 (Перші 5 значень нормалізації):", sl_norm[:5])

# 5. Унікальні значення та кількість по species
species_types, counts = np.unique(spec, return_counts=True)
print("Пункт 5 (Види та їх кількість):", species_types, counts)

# 6-8. Пошук та вивід рядків з NaN
has_nan = np.isnan(quan_charact).any()
rows_with_nan = iris[np.isnan(quan_charact).any(axis=1)]
print("Пункт 7-8 (Чи є NaN, Рядки з NaN):", has_nan, rows_with_nan)

# 9. Заміна NaN (заповнення середнім значенням)
col_means = np.nanmean(quan_charact, axis=0)
inds = np.where(np.isnan(quan_charact))
quan_charact[inds] = np.take(col_means, inds[1])
print("Пункт 9 (Заміна NaN завершена)")

# 10. Фільтрація: petallength > 1.5 та sepallength < 5.0
mask = (quan_charact[:, 2] > 1.5) & (quan_charact[:, 0] < 5.0)
filtered = iris[mask]
print("Пункт 10 (Відфільтровані дані):", filtered)

# 11. Кореляція (1-й та 3-й стовпці)
corr = np.corrcoef(quan_charact[:, 0], quan_charact[:, 2])[0, 1]
print("Пункт 11 (Кореляція):", corr)

# 12. Сортування за sepallength
iris_sorted = iris[quan_charact[:, 0].argsort()]
print("Пункт 12 (Перші 3 рядки після сортування):", iris_sorted[:3])

# 13. Статистика для кожного сорту
print("Пункт 13 (Середнє для кожного сорту):")
for s in species_types:
    subset = quan_charact[spec == s]
    print(s, ":", np.mean(subset, axis=0))

# 14. Категоризація за petallength
pl = quan_charact[:, 2]
p_cat = np.where(pl <= 3, "маленький", np.where(pl < 5, "середній", "великий"))
print("Пункт 14 (Категорії для перших 5):", p_cat[:5])

# 15. Новий стовпець "Об'єм"
vol = (np.pi * quan_charact[:, 2] * (quan_charact[:, 0]**2)) / 3
iris_res = np.column_stack((iris, vol))
print("Пункт 15 (Дані з об'ємом, перший рядок):", iris_res[0])

# 16. Найчастіше значення petallength
u, c = np.unique(pl, return_counts=True)
most_freq = u[c.argmax()]
print("Пункт 16 (Мода petallength):", most_freq)

# 17-18. Аналіз сорту setosa
setosa_pl = quan_charact[spec == 'Iris-setosa'][:, 2]
print("Пункт 17 (Min, Max Setosa):", setosa_pl.min(), setosa_pl.max())
print("Пункт 18 (2-й за довжиною Setosa):", np.unique(setosa_pl)[-2])