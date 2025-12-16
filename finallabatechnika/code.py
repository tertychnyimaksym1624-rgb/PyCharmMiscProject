import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, exp
from scipy import stats


# --- Декоратор для конвертації ---
def to_si_coulomb(func):
    def wrapper(self):
        val_esu_scaled = func(self)
        val_esu = val_esu_scaled * 1e-10
        conversion_factor = 3.33564e-10
        val_coulomb = val_esu * conversion_factor
        return val_coulomb

    return wrapper


# --- Базовий клас для статистики ---
class SingleSampleAnalysis:
    def __init__(self, data_array, alpha=0.99):
        self.data = np.array(data_array)
        self.n = len(self.data)
        self.alpha = alpha

        self.XSR = self.calc_mean()
        self.VBSRX = self.calc_variance()
        self.SX = self.calc_std_sample()
        self.SigmaX = self.calc_sigma_error()

        self.t_student = self.get_student_t(self.alpha)
        self.DeltaX = self.calc_absolute_error(self.t_student)

    def calc_mean(self):
        return np.mean(self.data)

    def calc_variance(self):
        return np.var(self.data, ddof=1)

    def calc_std_sample(self):
        return np.std(self.data, ddof=1)

    def calc_sigma_error(self):
        return self.SX / sqrt(self.n)

    def get_student_t(self, alpha):
        if self.n > 30:
            if alpha == 0.99: return 2.66
            if alpha == 0.95: return 2.00
        else:
            if self.n == 8:
                if alpha == 0.99: return 3.499
                if alpha == 0.95: return 2.365
        return 2.0

    def calc_absolute_error(self, t_val):
        return self.SigmaX * t_val


# --- Спеціалізований клас для Завдання 1.1 ---
class MillikanAnalysis(SingleSampleAnalysis):
    @to_si_coulomb
    def get_result_si(self):
        return self.XSR


# --- КЛАС ДЛЯ КОРЕЛЯЦІЙНОГО АНАЛІЗУ ---
class TwoSampleAnalysis:
    def __init__(self, sample_x: SingleSampleAnalysis, sample_y: SingleSampleAnalysis):
        if sample_x.n != sample_y.n:
            raise ValueError(f"Вибірки повинні бути однакової довжини: {sample_x.n} vs {sample_y.n}")

        self.sample_x = sample_x
        self.sample_y = sample_y
        self.n = sample_x.n

        # Параметри з об'єктів
        self.XSR = self.sample_x.XSR
        self.YSR = self.sample_y.XSR
        self.VBSRX = self.sample_x.VBSRX
        self.VBSRY = self.sample_y.VBSRX
        self.SX = self.sample_x.SX
        self.SY = self.sample_y.SX

        self.R = 0.0
        self.slope = 0.0
        self.intercept = 0.0

        self.df = self.n - 2
        self.t_obs = 0.0
        self.reliability = None

        self.calc_correlation_and_regression()
        self.check_significance()

    def calc_correlation_and_regression(self):
        numerator = np.sum((self.sample_x.data - self.XSR) * (self.sample_y.data - self.YSR))
        denominator = (self.n - 1) * self.SX * self.SY
        self.R = numerator / denominator

        self.slope = self.R * (self.SY / self.SX)
        self.intercept = self.YSR - (self.slope * self.XSR)

    def check_significance(self):
        r = self.R
        if abs(r) >= 1.0:
            self.t_obs = 0
            self.reliability = 1.0
            return

        self.t_obs = abs(r) * np.sqrt(self.df / (1 - r ** 2))
        thresholds = [0.999, 0.99, 0.95]
        self.reliability = None

        for alpha in thresholds:
            t_crit = stats.t.ppf((1 + alpha) / 2, self.df)
            if self.t_obs > t_crit:
                if self.reliability is None:
                    self.reliability = alpha


# --- КЛАС ДЛЯ ЗВІТІВ ---
class Report:
    @staticmethod
    def print_single_sample(experiment, precision=4):
        p = precision
        task_name = "Дослід Міллікена" if isinstance(experiment, MillikanAnalysis) else "Аналіз вибірки"
        print("-" * 50)
        print(f"ЗВІТ: {task_name} (n={experiment.n})")
        print("-" * 50)
        print(f"Середнє (XSR):             {experiment.XSR:.{p}f}")
        print(f"Дисперсія (VBSRX):         {experiment.VBSRX:.{p}f}")
        print(f"СКВ вибірки (SX):          {experiment.SX:.{p}f}")
        print(f"СК похибка (SigmaX):       {experiment.SigmaX:.{p}f}")
        if hasattr(experiment, 'get_result_si'):
            print(f"Значення в СІ:             {experiment.get_result_si():.4e} Кл")
        print(f"Довірчий інтервал (a={experiment.alpha}):")
        print(f"  {experiment.XSR:.{p}f} ± {experiment.DeltaX:.{p}f}")
        print("-" * 50 + "\n")

    @staticmethod
    def print_correlation(experiment: TwoSampleAnalysis, precision=4):
        p = precision
        print("-" * 60)
        print(f"ЗВІТ: Кореляційний аналіз (n={experiment.n})")
        print("-" * 60)

        print(f"{'Параметр':<15} | {'X (Темп.)':<18} | {'Y (Міцність)':<18}")
        print("-" * 60)
        print(f"{'Середнє':<15} | {experiment.XSR:<18.{p}f} | {experiment.YSR:<18.{p}f}")
        print(f"{'Дисперсія':<15} | {experiment.VBSRX:<18.{p}f} | {experiment.VBSRY:<18.{p}f}")
        print(f"{'СКВ (S)':<15} | {experiment.SX:<18.{p}f} | {experiment.SY:<18.{p}f}")
        print("-" * 60)

        r = experiment.R
        print(f"\nКоефіцієнт кореляції (r): {r:.4f}")

        if abs(r) > 0.9:
            print("Сила зв'язку: Дуже сильна.")
        elif abs(r) > 0.7:
            print("Сила зв'язку: Сильна.")
        elif abs(r) > 0.5:
            print("Сила зв'язку: Помірна.")
        else:
            print("Сила зв'язку: Слабка.")

        if r < 0: print("Напрямок: Зворотний (зі зростанням температури міцність падає).")

        print(f"Рівняння регресії: y = {experiment.slope:.{p}f}x + {experiment.intercept:.{p}f}")

        print(f"\n--- Перевірка значущості (t-критерій) ---")
        print(f"Ступені свободи (df = n-2): {experiment.df}")
        print(f"Розрахункове значення t-статистики: {experiment.t_obs:.4f}")

        print("\nВИСНОВОК ПРО ДОСТОВІРНІСТЬ:")
        if experiment.reliability:
            print(f"Зв'язок є статистично значущим з надійністю P > {experiment.reliability} (Поріг достовірності).")
        else:
            print("Зв'язок статистично незначущий (надійність P < 0.95).")
        print("-" * 60 + "\n")


# --- PLOTTER ---
class Plotter:
    @staticmethod
    def plot_histogram(data_input, bins=10, title="Гістограма", xlabel="Значення"):
        plt.figure(figsize=(8, 6))
        if hasattr(data_input, 'data'):
            data = data_input.data
            mean_val = data_input.XSR
        else:
            data = data_input
            mean_val = np.mean(data)
        plt.hist(data, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
        plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_val:.3f}')
        plt.title(title);
        plt.xlabel(xlabel);
        plt.legend();
        plt.grid(axis='y', alpha=0.5);
        plt.show()

    @staticmethod
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


# --- Main Execution ---
if __name__ == "__main__":
    # --- Завдання 1.1 ---
    data_millikan = np.array([
        4.781, 4.764, 4.777, 4.809, 4.761, 4.769, 4.772, 4.764,
        4.795, 4.776, 4.765, 4.790, 4.792, 4.806, 4.785, 4.788,
        4.769, 4.771, 4.785, 4.779, 4.758, 4.779, 4.799, 4.749,
        4.792, 4.789, 4.805, 4.788, 4.764, 4.785, 4.791, 4.774,
        4.779, 4.772, 4.768, 4.772, 4.810, 4.790, 4.783, 4.783,
        4.775, 4.789, 4.801, 4.791, 4.799, 4.777, 4.797, 4.781,
        4.782, 4.778, 4.808, 4.740, 4.790, 4.767, 4.791, 4.771,
        4.775, 4.747
    ])
    exp1 = MillikanAnalysis(data_millikan, alpha=0.99)
    Report.print_single_sample(exp1, precision=3)
    Plotter.plot_histogram(exp1, bins=8, title="Гістограма (Дослід Міллікена)", xlabel="Заряд")

    # --- Завдання 1.2 ---
    voltage_data = np.array([210, 205, 195, 200, 210, 220, 190, 210])
    exp2 = SingleSampleAnalysis(voltage_data, alpha=0.99)
    Report.print_single_sample(exp2, precision=2)

    # --- Завдання 1.3 ---
    temp_x = np.array([0, 50, 100, 150, 200, 300, 400, 500, 600, 700])
    strength_y = np.array([23.3, 21.0, 19.2, 16.4, 15.5, 13.3, 9.4, 5.9, 4.1, 1.9])

    sample_temp = SingleSampleAnalysis(temp_x)
    sample_strength = SingleSampleAnalysis(strength_y)

    exp3 = TwoSampleAnalysis(sample_temp, sample_strength)

    # Виводимо тільки текстовий звіт, графік прибрали
    Report.print_correlation(exp3, precision=3)

    # --- Завдання 2 ---
    Plotter.plot_gaussian_curves()
