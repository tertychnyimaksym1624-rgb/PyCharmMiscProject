import numpy as np

# 1. Створити одновимірний масив чисел від 0 до 9
arr = np.arange(10)

# 2. Створити масив розміром 3*3 зі значеннями True
arr_bool = np.full((3, 3), True, dtype=bool)

# 3. Залишити в масиві лише непарні числа
arr_odd = arr[arr % 2 == 1]

# 4. Замінити в масиві усі непарні числа на -1 (зміна оригіналу)
arr[arr % 2 == 1] = -1

# 5. Утворити новий масив із заданого, замінивши непарні числа на -1
arr_original = np.arange(10)
new_arr = np.where(arr_original % 2 == 1, -1, arr_original)

# 6. Перетворити 1D-масив на 2D-масив із 2 рядками
arr_2d = np.arange(10).reshape(2, -1)

# 7. Скласти масиви a і b вертикально
a = np.arange(10).reshape(2,5)
b = np.repeat(1, 10).reshape(2,5)
v_stack = np.vstack([a, b])

# 8. Скласти масиви a і b горизонтально
h_stack = np.hstack([a, b])

a = np.array([1, 2, 3, 2, 3, 4, 3, 4, 5, 6])
b = np.array([7, 2, 10, 2, 7, 4, 9, 4, 9, 8])

# 9. Отримати спільні елементи масивів a і b
common = np.intersect1d(a, b)

# 10. З масиву a видалити всі елементи, присутні в масиві b
diff = np.setdiff1d(a, b)

# 11. Визначити позиції, на яких елементи a і b співпадають
matches = np.where(a == b)

# 12. Новий масив: лише елементи від 5 до 10
arr_range = a[(a >= 5) & (a <= 10)]

# 13. Перетворити функцію maxx на роботу з масивами
def maxx(x, y):
    return x if x >= y else y
pair_max = np.vectorize(maxx, otypes=[float])

# 14. Поміняти в масиві місцями стовпці 1 і 2
arr_3x3 = np.arange(9).reshape(3,3)
arr_swapped_cols = arr_3x3[:, [1, 0, 2]]

# 15. Поміняти в масиві місцями рядки 2 і 3
arr_swapped_rows = arr_3x3[[0, 2, 1], :]

# 16. Поміняти порядок рядків на зворотний
rev_rows = arr_3x3[::-1, :]

# 17. Поміняти порядок стовпців на зворотний
rev_cols = arr_3x3[:, ::-1]

# 18. 2D-масив 5x3 з випадковими числами від 5 до 10
rand_arr = np.random.uniform(5, 10, size=(5, 3))

# 19. Вивести елементи, округлені до третього знаку
np.set_printoptions(precision=3)

# 20. Вивести масив у звичайному (неекспоненційному) форматі
np.set_printoptions(suppress=True)

# 21. Обмежити кількість елементів при виведенні (max 6)
np.set_printoptions(threshold=6)

# 22. Вивести всі елементи (якщо встановлено скорочений формат)
import sys
np.set_printoptions(threshold=sys.maxsize)

# 23. Вставити np.nan у 5 випадкових позицій масиву 3x3
arr_nan = np.random.random((3, 3))
indices = np.random.choice(arr_nan.size, 5, replace=False)
arr_nan.ravel()[indices] = np.nan

# 24. Замінити усі nan на 0
arr_nan[np.isnan(arr_nan)] = 0

# 25. Замінити значення > 30 на 30, а < 10 на 10
arr_target = np.random.randint(0, 50, 20)
clipped_arr = np.clip(arr_target, 10, 30)