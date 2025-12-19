from vpython import *
import math

# 1. Налаштування сцени
scene = canvas(width=800, height=600)
ground = box(pos=vector(0, -1, 0), size=vector(50, 1, 10), color=color.green)

# 2. Створення примітивів
# Гармата (основа + дуло)
base = sphere(pos=vector(-20, 0, 0), radius=1.5, color=color.gray(0.5))
barrel = cylinder(pos=vector(-20, 0, 0), axis=vector(5, 2, 0), radius=0.8, color=color.blue)

# Снаряд
bullet = sphere(pos=vector(-20, 0, 0), radius=0.5, color=color.red, make_trail=False)

# Мішень
target = cylinder(pos=vector(15, 0, 0), axis=vector(0, 0.4, 0), radius=2, color=color.orange)

# 3. Змінні стану
v0 = 15  # Початкова швидкість
theta = 30  # Кут в градусах
g = 9.8  # Гравітація
firing = False  # Чи летить куля зараз
t = 0  # Час польоту


# 4. Функції для віджетів
def set_angle(s):
    global theta
    theta = s.value
    # Перерахунок вектора дула (математика для візуалізації)
    rad = math.radians(theta)
    barrel.axis = vector(5 * math.cos(rad), 5 * math.sin(rad), 0)
    wt.text = f'{theta:.1f} deg'


def set_speed(s):
    global v0
    v0 = s.value
    ws.text = f'{v0:.1f} m/s'


def shoot(b):
    global firing, t
    if not firing:
        firing = True
        t = 0
        bullet.pos = barrel.pos + barrel.axis  # Старт з кінця дула
        bullet.clear_trail()  # Очистити старий слід


def toggle_trail(c):
    bullet.make_trail = c.checked


# 5. Створення віджетів
scene.append_to_caption('\nКут нахилу: ')
sl_angle = slider(min=0, max=90, value=30, length=220, bind=set_angle)
wt = wtext(text='30.0 deg')

scene.append_to_caption('\n\nСила пострілу: ')
sl_speed = slider(min=5, max=30, value=15, length=220, bind=set_speed)
ws = wtext(text='15.0 m/s')

scene.append_to_caption('\n\n')
btn_fire = button(text='ВОГОНЬ!', bind=shoot)
scene.append_to_caption('   ')
chk_trail = checkbox(text='Малювати траєкторію', bind=toggle_trail, checked=False)

# 6. Головний цикл (Анімація)
while True:
    rate(60)  # 60 кадрів на секунду

    if firing:
        t += 0.05
        rad = math.radians(theta)

        # Фізика польоту (x = x0 + vx*t, y = y0 + vy*t - 0.5*g*t^2)
        # Початок польоту зміщено до кінця дула
        start_pos = base.pos + barrel.axis

        x = start_pos.x + v0 * math.cos(rad) * t
        y = start_pos.y + v0 * math.sin(rad) * t - 0.5 * g * t ** 2

        bullet.pos = vector(x, y, 0)

        # Перевірка на зіткнення з землею
        if y < 0:
            firing = False
            bullet.pos.y = 0

            # Перевірка влучання (проста перевірка відстані)
            if mag(bullet.pos - target.pos) < (target.radius + bullet.radius):
                target.color = color.red  # Ефект влучання
            else:
                target.color = color.orange  # Скидання кольору