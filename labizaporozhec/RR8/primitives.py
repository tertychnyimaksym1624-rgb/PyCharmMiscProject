from vpython import *


scene = canvas(width=800, height=600, title='VPython Primitives & Widgets')
scene.background = color.gray(0.1) # Темний фон, щоб краще бачити кольори

# Функція-заглушка для віджетів (щоб код не ламався)
def widget_event(evt):
    print(f"Віджет спрацював! Значення: {evt.value if hasattr(evt, 'value') else 'клік'}")


# 1. BOX (Куб)
# box(pos=vector(0, 0, 0), length=3, height=3, width=3, color=color.red)



# 2. SPHERE (Сфера)
# sphere(pos=vector(0, 0, 0), radius=2, color=color.green)



# 3. CYLINDER (Циліндр)
# cylinder(pos=vector(0, 0, 0), axis=vector(5, 0, 0), radius=1, color=color.blue)



# 4. CONE (Конус)
# cone(pos=vector(0, 0, 0), axis=vector(0, 4, 0), radius=2, color=color.yellow)



# 5. PYRAMID (Піраміда - прямокутна основа)
# pyramid(pos=vector(0, 0, 0), size=vector(4, 3, 2), color=color.orange)



# 6. RING (Кільце / "Бублик")
# ring(pos=vector(0, 0, 0), axis=vector(0, 0, 1), radius=2, thickness=0.2, color=color.cyan)



# 7. HELIX (Спіраль / Пружина)
# helix(pos=vector(0, 0, 0), axis=vector(5, 0, 0), radius=2, coils=5, thickness=0.2, color=color.magenta)



# 8. ARROW (Стрілка - вектор)
# arrow(pos=vector(0, 0, 0), axis=vector(3, 3, 0), shaftwidth=0.5, color=color.white)



# 9. ELLIPSOID (Еліпсоїд - сплюснута сфера)
# ellipsoid(pos=vector(0, 0, 0), length=4, height=2, width=1, color=color.purple)



# 10. CURVE (Лінія / Траєкторія через точки)
# c = curve(color=color.yellow, radius=0.1)
# c.append(vector(-2, -2, 0))
# c.append(vector(0, 2, 0))
# c.append(vector(2, -2, 0))



# 11. LABEL (Текстова мітка над об'єктом - 2D текст у 3D просторі)
# label(pos=vector(0, 1, 0), text='Hello VPython', xoffset=20, yoffset=50, height=16, border=4, font='sans')



# 12.TEXT (Об'ємний текст - це повноцінний 3D об'єкт)
text(text='3D', pos=vector(-2, 0, 0), depth=0.5, color=color.green, height=2)




# Для віджетів важливо: вони з'являються під сценою (у `caption`).
# Я додав scene.append_to_caption, щоб вони не злипалися.

# 1. BUTTON (Кнопка)
# scene.append_to_caption('\nButton: ')
# button(text='Натисни мене', bind=widget_event)



# 2. SLIDER (Повзунок)
# scene.append_to_caption('\n\nSlider: ')
# slider(min=0, max=100, value=50, length=200, bind=widget_event)



# 3. RADIO BUTTON (Перемикач - вибір одного з варіантів)
# scene.append_to_caption('\n\nRadio: ')
# radio(bind=widget_event, text='Option A ', checked=True)
# radio(bind=widget_event, text='Option B ')



# 4. CHECKBOX (Галочка - вкл/викл)
# scene.append_to_caption('\n\nCheckbox: ')
# checkbox(bind=widget_event, text='Show Trail', checked=False)



# 5. MENU (Випадаючий список)
# scene.append_to_caption('\n\nMenu: ')
# menu(choices=['Red', 'Green', 'Blue'], bind=widget_event)



# 6. WINPUT (Поле введення тексту)
# scene.append_to_caption('\n\nInput: ')
# winput(bind=widget_event, text='Type here...')



# 7. WTEXT (Динамічний текст у інтерфейсі - не на сцені, а поряд з віджетами)
scene.append_to_caption('\n\nInfo: ')
wtext(text='Це просто текст для відображення даних')

while True:
    rate(30)