import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime, timedelta
import math

CROPS = {
    'Пшеница': {'temp': (15, 25), 'frost': -5, 'days': 90, 'water': 450, 'pest': 0.6},
    'Кукуруза': {'temp': (20, 30), 'frost': 0, 'days': 120, 'water': 500, 'pest': 0.7},
    'Картофель': {'temp': (15, 22), 'frost': -2, 'days': 100, 'water': 400, 'pest': 0.8},
    'Подсолнечник': {'temp': (20, 27), 'frost': -3, 'days': 110, 'water': 550, 'pest': 0.5},
    'Томаты': {'temp': (18, 26), 'frost': 0, 'days': 85, 'water': 600, 'pest': 0.7},
}

TEMPS = {1: -10, 2: -8, 3: -2, 4: 8, 5: 15, 6: 20, 7: 22, 8: 20, 9: 14, 10: 7, 11: 0, 12: -6}


COSTS = {
    'забор': 500, 'орошение': 150000, 'семена': {'Пшеница': 8000, 'Кукуруза': 12000,
                                                 'Картофель': 35000, 'Подсолнечник': 15000, 'Томаты': 50000},
    'удобрения': 15000, 'пестициды': 10000, 'топливо': 5000, 'труд': 20000, 'аренда': 25000
}


PRICES = {'Пшеница': 1200, 'Кукуруза': 1000, 'Картофель': 800, 'Подсолнечник': 3000, 'Томаты': 3500}


YIELDS = {'Пшеница': 40, 'Кукуруза': 60, 'Картофель': 250, 'Подсолнечник': 25, 'Томаты': 500}


class FarmApp:
    def __init__(self, root):
        self.root = root
        root.title("Сельхоз планировщик")
        root.geometry("900x700")


        input_frame = ttk.LabelFrame(root, text="Параметры", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)


        ttk.Label(input_frame, text="Культура:").grid(row=0, column=0, sticky='w', pady=3)
        self.crop = tk.StringVar(value='Пшеница')
        ttk.Combobox(input_frame, textvariable=self.crop, values=list(CROPS.keys()), width=20).grid(row=0, column=1,
                                                                                                    pady=3)


        ttk.Label(input_frame, text="Площадь (га):").grid(row=1, column=0, sticky='w', pady=3)
        self.area = tk.StringVar(value="10")
        ttk.Entry(input_frame, textvariable=self.area, width=22).grid(row=1, column=1, pady=3)


        ttk.Label(input_frame, text="Длина забора (м):").grid(row=2, column=0, sticky='w', pady=3)
        self.fence = tk.StringVar(value="400")
        ttk.Entry(input_frame, textvariable=self.fence, width=22).grid(row=2, column=1, pady=3)


        ttk.Label(input_frame, text="Изменение климата (°C):").grid(row=0, column=2, sticky='w', pady=3, padx=(20, 0))
        self.climate = tk.DoubleVar(value=0)
        ttk.Scale(input_frame, from_=-2, to=5, variable=self.climate, orient='horizontal', length=150).grid(row=0,
                                                                                                            column=3,
                                                                                                            pady=3)
        self.climate_lbl = ttk.Label(input_frame, text="0.0°C")
        self.climate_lbl.grid(row=0, column=4, pady=3)
        self.climate.trace('w', lambda *_: self.climate_lbl.config(text=f"{self.climate.get():.1f}°C"))


        ttk.Label(input_frame, text="Антропогенная нагрузка (%):").grid(row=1, column=2, sticky='w', pady=3,
                                                                        padx=(20, 0))
        self.anthro = tk.DoubleVar(value=50)
        ttk.Scale(input_frame, from_=0, to=100, variable=self.anthro, orient='horizontal', length=150).grid(row=1,
                                                                                                            column=3,
                                                                                                            pady=3)
        self.anthro_lbl = ttk.Label(input_frame, text="50%")
        self.anthro_lbl.grid(row=1, column=4, pady=3)
        self.anthro.trace('w', lambda *_: self.anthro_lbl.config(text=f"{self.anthro.get():.0f}%"))


        ttk.Label(input_frame, text="Риск от животных (%):").grid(row=2, column=2, sticky='w', pady=3, padx=(20, 0))
        self.animal = tk.DoubleVar(value=30)
        ttk.Scale(input_frame, from_=0, to=100, variable=self.animal, orient='horizontal', length=150).grid(row=2,
                                                                                                            column=3,
                                                                                                            pady=3)
        self.animal_lbl = ttk.Label(input_frame, text="30%")
        self.animal_lbl.grid(row=2, column=4, pady=3)
        self.animal.trace('w', lambda *_: self.animal_lbl.config(text=f"{self.animal.get():.0f}%"))


        self.irrigation = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Орошение", variable=self.irrigation).grid(row=3, column=0, columnspan=2,
                                                                                     sticky='w', pady=3)
        self.rental = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Аренда техники", variable=self.rental).grid(row=3, column=2, columnspan=2,
                                                                                       sticky='w', pady=3, padx=(20, 0))


        ttk.Label(input_frame, text="Защита от вредителей (%):").grid(row=4, column=0, sticky='w', pady=3)
        self.protection = tk.DoubleVar(value=70)
        ttk.Scale(input_frame, from_=0, to=100, variable=self.protection, orient='horizontal', length=150).grid(row=4,
                                                                                                                column=1,
                                                                                                                pady=3)
        self.prot_lbl = ttk.Label(input_frame, text="70%")
        self.prot_lbl.grid(row=4, column=2, pady=3, sticky='w', padx=(20, 0))
        self.protection.trace('w', lambda *_: self.prot_lbl.config(text=f"{self.protection.get():.0f}%"))


        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Рассчитать время посадки", command=self.calc_planting).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Рассчитать затраты", command=self.calc_costs).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Полный анализ", command=self.full_analysis).pack(side='left', padx=5)


        ttk.Label(root, text="Результаты:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10)
        self.results = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, font=('Courier', 9))
        self.results.pack(fill='both', expand=True, padx=10, pady=5)

    def calc_planting(self):
        try:
            crop = self.crop.get()
            info = CROPS[crop]
            climate = self.climate.get()
            risk = (info['pest'] * 100 * 0.4 + self.anthro.get() * 0.3 + self.animal.get() * 0.3)


            months = []
            for m in range(3, 7):
                temp = TEMPS[m] + climate
                if info['temp'][0] <= temp <= info['temp'][1]:
                    months.append(m)

            month_names = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                           'Октябрь', 'Ноябрь', 'Декабрь']

            report = "=" * 70 + "\nРАСЧЁТ ВРЕМЕНИ ПОСАДКИ\n" + "=" * 70 + "\n\n"
            report += f"Культура: {crop}\n"
            report += f"Оптимальная температура: {info['temp'][0]}°C - {info['temp'][1]}°C\n"
            report += f"Период вегетации: {info['days']} дней\n\n"

            if months:
                report += "Рекомендуемые месяцы посадки:\n"
                for m in months:
                    report += f"  • {month_names[m]}: {TEMPS[m] + climate:.1f}°C\n"
                report += f"\nЛУЧШИЙ МЕСЯЦ: {month_names[months[len(months) // 2]]}\n\n"
            else:
                report += "⚠ Подходящих месяцев не найдено!\n\n"

            report += f"Общий уровень риска: {risk:.1f}% "
            report += f"({'НИЗКИЙ' if risk < 30 else 'СРЕДНИЙ' if risk < 60 else 'ВЫСОКИЙ'})\n"

            if risk > 50:
                report += "\n⚠ РЕКОМЕНДАЦИИ:\n  • Установка защитного ограждения\n  • Усиленная обработка пестицидами\n"

            self.results.delete(1.0, tk.END)
            self.results.insert(tk.END, report)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def calc_costs(self):
        try:
            crop = self.crop.get()
            area = float(self.area.get())
            fence = float(self.fence.get())

            costs = {}
            costs['Забор'] = fence * COSTS['забор']
            costs['Орошение'] = area * COSTS['орошение'] if self.irrigation.get() else 0
            costs['Техника'] = area * COSTS['аренда'] if self.rental.get() else 350000
            costs['Семена'] = area * COSTS['семена'].get(crop, 10000)
            costs['Удобрения'] = area * COSTS['удобрения']
            costs['Пестициды'] = area * COSTS['пестициды'] * (self.protection.get() / 100)
            costs['Топливо'] = area * COSTS['топливо']
            costs['Труд'] = area * COSTS['труд']

            total = sum(costs.values())

            report = "=" * 70 + "\nРАСЧЁТ ЗАТРАТ\n" + "=" * 70 + "\n\n"
            report += f"Культура: {crop}\nПлощадь: {area} га\n\n"
            report += "Детализация затрат:\n" + "-" * 70 + "\n"

            for cat, cost in costs.items():
                report += f"{cat:.<40} {cost:>15,.2f} руб.\n"

            report += "-" * 70 + f"\nИТОГО: {total:>15,.2f} руб.\n"
            report += f"На 1 га: {total / area:,.2f} руб.\n\n"

            if costs['Орошение'] > 0:
                report += "💡 Рекомендация: Капельное орошение экономит до 30% воды\n"

            self.results.delete(1.0, tk.END)
            self.results.insert(tk.END, report)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def full_analysis(self):
        try:
            crop = self.crop.get()
            area = float(self.area.get())
            info = CROPS[crop]

            # Затраты
            fence = float(self.fence.get())
            total_costs = (
                    fence * COSTS['забор'] +
                    (area * COSTS['орошение'] if self.irrigation.get() else 0) +
                    (area * COSTS['аренда'] if self.rental.get() else 350000) +
                    area * (COSTS['семена'].get(crop, 10000) + COSTS['удобрения'] +
                            COSTS['пестициды'] * self.protection.get() / 100 + COSTS['топливо'] + COSTS['труд'])
            )


            base_yield = YIELDS.get(crop, 30)
            climate_f = 1.0 + (self.climate.get() * 0.05) if -1 <= self.climate.get() <= 2 else 1.0 - abs(
                self.climate.get() - 1) * 0.1
            pest_damage = info['pest'] * 100 * (1 + self.anthro.get() / 200) * (100 - self.protection.get()) / 100
            pest_f = 1.0 - (pest_damage / 100)
            animal_f = 1.0 - (self.animal.get() / 100)
            irrig_f = 1.2 if self.irrigation.get() else 1.0

            final_yield = base_yield * climate_f * pest_f * animal_f * irrig_f
            total_prod = final_yield * area


            price = PRICES.get(crop, 1500)
            revenue = total_prod * price
            profit = revenue - total_costs
            roi = (profit / total_costs * 100) if total_costs > 0 else 0

            report = "=" * 70 + "\nПОЛНЫЙ АНАЛИЗ\n" + "=" * 70 + "\n\n"
            report += f"Культура: {crop} | Площадь: {area} га\n\n"

            report += "ПРОГНОЗ УРОЖАЯ:\n" + "-" * 70 + "\n"
            report += f"Базовая урожайность: {base_yield:.1f} ц/га\n"
            report += f"Прогноз с учётом факторов: {final_yield:.1f} ц/га\n"
            report += f"Общий урожай: {total_prod:.1f} ц\n"
            report += f"Потери: {((base_yield - final_yield) / base_yield * 100):.1f}%\n\n"

            report += "ЭКОНОМИКА:\n" + "-" * 70 + "\n"
            report += f"Затраты: {total_costs:,.2f} руб.\n"
            report += f"Выручка: {revenue:,.2f} руб. (по {price} руб/ц)\n"
            report += f"Прибыль: {profit:,.2f} руб.\n"
            report += f"Рентабельность: {roi:.1f}%\n\n"

            report += "ФАКТОРЫ ВЛИЯНИЯ:\n" + "-" * 70 + "\n"
            report += f"Климат: {climate_f:.2f} | Вредители: {pest_f:.2f} | "
            report += f"Животные: {animal_f:.2f} | Орошение: {irrig_f:.2f}\n\n"

            if profit > 0:
                report += f"✓ Проект РЕНТАБЕЛЕН (ROI: {roi:.1f}%)\n"
            else:
                report += "⚠ Проект УБЫТОЧЕН - пересмотрите параметры\n"

            self.results.delete(1.0, tk.END)
            self.results.insert(tk.END, report)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FarmApp(root)
    root.mainloop()
