import numpy as np


def analytical_function(x):
    return 0.5 * x * np.sin(3 * x)



start_x = -10.0
end_x = 10.0
step = 0.1
output_file = 'coordinates_growing_wave.txt'
x_values = np.arange(start_x, end_x + step, step)#Генеруємо діапазон значень x


try:
    with open(output_file, 'w', encoding='utf-8') as f:#Відкриваємо файл для запису
        f.write("x\ty\n")# Записуємо заголовок
        for x in x_values:#Обчислюємо та записуємо точки
            if x == 0.0:# Запобігання помилки з -0.0, яка буває при форматуванні
                x = 0.0
            y = analytical_function(x)
            f.write(f"{x:.2f}\t{y:.6f}\n")#Записуємо рядок

    print("Файл", output_file, "успішно створено.")
except Exception as e:
    print("Сталася помилка при записі файлу:",e)