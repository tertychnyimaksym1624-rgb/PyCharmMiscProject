def validate_water_physics(func):
    def wrapper(self, target_temp, *args, **kwargs):
        if target_temp < 0:
            raise ValueError(f"Помилка: Вода замерзне при {target_temp}°C! Чайник не розрахований на лід.")
        if target_temp > 100:
            raise ValueError(f"Помилка: Вода википить при {target_temp}°C! Максимум 100°C.")
        if target_temp <= self.current_temp:
            raise ValueError(f"Помилка: Цільова температура ({target_temp}°C) нижча або рівна поточній.")
        return func(self, target_temp, *args, **kwargs)

    return wrapper


class ElectricKettle:
    SPECIFIC_HEAT_WATER = 4200
    LATENT_HEAT_VAPORIZATION = 2_260_000
    def __init__(self, volume_liters: float, power_watts: float, current_temp: float = 20):
        self.mass = volume_liters
        self.power = power_watts
        self.current_temp = current_temp

    @validate_water_physics
    def heat_water(self, target_temp: float):
        delta_t = target_temp - self.current_temp
        energy_needed = self.SPECIFIC_HEAT_WATER * self.mass * delta_t
        time_seconds = energy_needed / self.power

        print(f"--- Запуск чайника ---")
        print(f"Об'єм: {self.mass} л, Потужність: {self.power} Вт")
        print(f"Нагрів: {self.current_temp}°C -> {target_temp}°C")
        print(f"Енергія: {energy_needed / 1000:.1f} кДж")
        print(f"Час: {time_seconds:.1f} сек ({time_seconds / 60:.2f} хв)")

        self.current_temp = target_temp
        print("Готово! Вода нагріта.\n")

    def evaporate_water(self):
        if self.mass <= 0:
            print("Помилка: Чайник порожній, нічого випаровувати.")
            return

        if self.current_temp < 100:
            print(f"Увага: Вода має {self.current_temp}°C. Спочатку доведіть до кипіння.")
            return

        energy_needed = self.mass * self.LATENT_HEAT_VAPORIZATION
        time_seconds = energy_needed / self.power

        print(f"--- Випаровування (Phase Change) ---")
        print(f"Перетворення {self.mass} л окропу в пару.")
        print(f"Необхідна енергія: {energy_needed / 1000:.1f} кДж")
        print(f"Час до повного википання: {time_seconds:.1f} сек ({time_seconds / 60:.2f} хв)")

        self.mass = 0
        print("Вода повністю википіла.\n")

if __name__ == "__main__":
    kettle = ElectricKettle(volume_liters=1.5, power_watts=2000, current_temp=20)

    try:
        kettle.heat_water(90)
        kettle.heat_water(150)


    except ValueError as e:
        print(e)

    try:
        kettle.heat_water(-5)
    except ValueError as e:
        print(e)

    try:
        kettle.evaporate_water()
    except ValueError as e:
        print(e)

    try:
        kettle.heat_water(100)
        kettle.evaporate_water()
    except ValueError as e:
        print(e)