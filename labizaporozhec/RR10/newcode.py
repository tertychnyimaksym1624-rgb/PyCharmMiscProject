from vpython import *
import numpy as np



# --- 1. Константи та параметри [cite: 19, 23-31] ---
kB = 1.38e-23
n = 50  # Кількість частинок (збільшено для наочності)
T = 100  # Температура
m = 6.65e-26  # Маса аргону
r0 = 3.4e-10  # Параметр r0
sigma = r0 / (2 ** (1 / 6))  # Sigma з r0 (класичний зв'язок для L-J потенціалу)
# У завданні sigma = 119*kB (це epsilon в Кельвінах, помилка в умові, але виправимо на epsilon)
epsilon = 119 * kB

R = r0 / 2
L = 8e-9  # Розмір ящика (Lx, Ly, Lz)
t_global = 1e-9
dt = 2e-14  # Крок часу

# Коефіцієнт для масштабування візуалізації
scale = 1.5 / L

# --- 2. Візуалізація (Сцена та Графіки) [cite: 35-43] ---
scene = canvas(width=800, height=600, background=vector(0.1, 0.1, 0.1), align='left')
scene.title = "3D Модель Реального Газу (Аргон)"

# Малювання 3D коробки (границі)
box_lines = curve(pos=[vector(0, 0, 0), vector(L, 0, 0), vector(L, L, 0), vector(0, L, 0), vector(0, 0, 0),
                       vector(0, 0, L), vector(L, 0, L), vector(L, L, L), vector(0, L, L), vector(0, 0, L),
                       vector(L, 0, L), vector(L, 0, 0), vector(L, L, 0), vector(L, L, L), vector(0, L, L),
                       vector(0, L, 0)],
                  color=color.yellow, radius=0.005 * L)
box_lines.scale = scale  # Застосовуємо масштаб до коробки (але vpython краще масштабує позиції)
# Примітка: для простоти множимо координати атомів на scale при візуалізації.

# Графіки енергії
egraph = graph(title="Енергія системи", xtitle="Час (кроки)", ytitle="Енергія (Дж)", width=500, height=300,
               align='right')
g_ek = gcurve(color=color.red, label="Кінетична")
g_ep = gcurve(color=color.green, label="Потенціальна")
g_et = gcurve(color=color.yellow, label="Повна")


# --- 3. Ініціалізація змінних (Numpy Arrays)  ---
# Координати (x, y, z), Швидкості (vx, vy, vz), Сили (fx, fy, fz)
pos = np.zeros((n, 3))
v = np.zeros((n, 3))
f = np.zeros((n, 3))
atoms_visual = []  # Список об'єктів vpython


# --- 4. Функції ---

# Розподіл Максвелла через бібліотечні функції
def maxwell_velocities(n, T, m):
    sigma_v = np.sqrt(kB * T / m)
    return np.random.normal(0, sigma_v, (n, 3))


# Перевірка на накладання при ініціалізації [cite: 11]
def init_atoms_safe():
    count = 0
    while count < n:
        # Генеруємо випадкову позицію
        candidate = np.random.uniform(R, L - R, 3)

        valid = True
        # Перевіряємо відстань до вже створених частинок
        for i in range(count):
            dist = np.linalg.norm(candidate - pos[i])
            if dist < 1.1 * r0:  # 1.1 r0 - запас, щоб не було шалених сил відштовхування
                valid = False
                break

        if valid:
            pos[count] = candidate
            count += 1

    # Задаємо швидкості
    global v
    v = maxwell_velocities(n, T, m)

    # Створюємо графічні об'єкти
    for i in range(n):
        atoms_visual.append(sphere(pos=vector(*pos[i]) * scale, radius=R * scale, color=color.cyan))


# Функція сил (оптимізована, без exp/log) [cite: 7, 17]
def compute_forces_and_potential():
    global f
    f.fill(0.0)  # Очистити сили
    Ep_total = 0.0

    # Подвійний цикл (можна векторизувати, але цикл зрозуміліший для лаби)
    for i in range(n):
        for j in range(i + 1, n):
            d_vec = pos[i] - pos[j]
            r2 = np.sum(d_vec ** 2)  # r^2
            r = np.sqrt(r2)

            if r < R: r = R  # Захист від ділення на нуль

            # Оптимізація формули Леннарда-Джонса:
            # V(r) = 4*eps * ((s/r)^12 - (s/r)^6)
            # F(r) = 24*eps/r * (2*(s/r)^12 - (s/r)^6)

            sr2 = (sigma ** 2) / r2  # (sigma/r)^2
            sr6 = sr2 ** 3  # (sigma/r)^6
            sr12 = sr6 ** 2  # (sigma/r)^12

            # Потенціальна енергія пари
            Ep_pair = 4 * epsilon * (sr12 - sr6)
            Ep_total += Ep_pair

            # Сила (скалярна величина F/r)
            F_mag = (24 * epsilon / r2) * (2 * sr12 - sr6)

            # Проекції сил
            f_vec = F_mag * d_vec

            f[i] += f_vec
            f[j] -= f_vec  # Третій закон Ньютона

    return Ep_total


# Відбивання від стінок (GB_wall)
def apply_boundary_conditions():
    global pos, v
    # Для кожної вісі (0=x, 1=y, 2=z)
    for i in range(3):
        # Якщо менше 0
        mask_min = pos[:, i] < R
        pos[mask_min, i] = R  # Повертаємо на межу
        v[mask_min, i] *= -1  # Інвертуємо швидкість

        # Якщо більше L
        mask_max = pos[:, i] > (L - R)
        pos[mask_max, i] = L - R
        v[mask_max, i] *= -1


#Розфарбовування за швидкістю
def update_colors():
    speeds = np.linalg.norm(v, axis=1)
    max_speed = np.max(speeds) if np.max(speeds) > 0 else 1.0
    for i in range(n):
        intensity = speeds[i] / max_speed
        # Від синього (повільний) до червоного (швидкий)
        atoms_visual[i].color = vector(intensity, 0, 1 - intensity)
        atoms_visual[i].pos = vector(*pos[i]) * scale


# --- 5. Головний цикл ---
init_atoms_safe()
t = 0
step = 0
output_file = open("txtfile", "w")
output_file.write("Time\tEk\tEp\tE_total\n")
while True:
    rate(100)  # Обмеження FPS

    # 1. Обчислення сил та енергії
    Ep = compute_forces_and_potential()

    # 2. Інтегрування руху (метод Ейлера для простоти, можна змінити на Velocity Verlet)
    # v = v + (F/m)*dt
    v += (f / m) * dt
    # r = r + v*dt
    pos += v * dt

    # 3. Граничні умови (Стінки)
    apply_boundary_conditions()

    # 4. Обчислення кінетичної енергії
    # Ek = sum(m * v^2 / 2)
    v2 = np.sum(v ** 2, axis=1)
    Ek = 0.5 * m * np.sum(v2)

    # 5. Термостат (утримуємо температуру, щоб система не розігрівалась похибками) [cite: 114-118]
    # T_curr = 2*Ek / (3*n*kB) (для 3D газу ступенів свободи 3n)
    # scale_factor = sqrt(T_req / T_curr)
    if Ek > 0:
        scale_v = np.sqrt(((3 * n * kB * T) / 2) / Ek)
        v *= scale_v  # Масштабуємо швидкості
        Ek = (3 * n * kB * T) / 2  # Оновлюємо Ek після масштабування для графіка

    # 6. Оновлення графіки та графіків
    if step % 5 == 0:  # Оновлюємо не кожен крок для швидкодії
        update_colors()
        g_ek.plot(t, Ek)
        g_ep.plot(t, Ep)
        g_et.plot(t, Ek + Ep)
    #запис даних в файл
  #   try:
  #       with open(output_file, 'w', encoding='utf-8') as f:  # Відкриваємо файл для запису
  #           # .write("x\ty\n")  # Записуємо заголовок
  # # Обчислюємо та записуємо точки

    output_file.write(f"{t:.4e}\t{Ek:.4e}\t{Ep:.4e}\t{Ek+Ep:.4e}\n")  # Записуємо рядок
    output_file.flush()
    #     print("Файл", output_file, "успішно створено.")
    # except Exception as e:
    #     print("Сталася помилка при записі файлу:", e)
    t += dt
    step += 1