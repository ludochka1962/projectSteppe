#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Дополнительный модуль аналитики для фермерского планировщика
Содержит расширенные функции анализа и прогнозирования
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import math


class WeatherAnalyzer:
    """Анализатор погодных условий"""

    @staticmethod
    def calculate_frost_risk(month: int, climate_change: float,
                             frost_tolerance: float) -> Tuple[float, str]:
        """
        Расчёт риска заморозков

        Returns:
            (риск_в_процентах, описание)
        """
        # Базовая вероятность заморозков по месяцам
        frost_probability = {
            1: 0.95, 2: 0.90, 3: 0.60, 4: 0.30, 5: 0.05, 6: 0.01,
            7: 0.0, 8: 0.0, 9: 0.05, 10: 0.25, 11: 0.65, 12: 0.90
        }

        base_prob = frost_probability.get(month, 0.5)

        # Корректировка на изменение климата
        adjusted_prob = max(0, base_prob - (climate_change * 0.1))

        # Оценка ущерба с учётом морозостойкости
        if frost_tolerance >= -10:
            damage_factor = 0.5
        elif frost_tolerance >= -5:
            damage_factor = 0.7
        else:
            damage_factor = 0.9

        risk = adjusted_prob * damage_factor * 100

        if risk < 10:
            description = "Минимальный риск"
        elif risk < 30:
            description = "Низкий риск"
        elif risk < 60:
            description = "Умеренный риск"
        else:
            description = "Высокий риск"

        return risk, description

    @staticmethod
    def calculate_drought_risk(month: int, climate_change: float,
                               water_need: float) -> Tuple[float, str]:
        """
        Расчёт риска засухи

        Returns:
            (риск_в_процентах, описание)
        """
        # Базовый риск засухи по месяцам
        drought_risk = {
            1: 0.1, 2: 0.1, 3: 0.2, 4: 0.3, 5: 0.4, 6: 0.5,
            7: 0.6, 8: 0.5, 9: 0.3, 10: 0.2, 11: 0.1, 12: 0.1
        }

        base_risk = drought_risk.get(month, 0.3)

        # Изменение климата усиливает засухи
        adjusted_risk = min(1.0, base_risk + (climate_change * 0.08))

        # Учёт потребности в воде
        if water_need > 600:
            water_factor = 1.3
        elif water_need > 400:
            water_factor = 1.0
        else:
            water_factor = 0.7

        risk = adjusted_risk * water_factor * 100

        if risk < 20:
            description = "Минимальный риск засухи"
        elif risk < 40:
            description = "Умеренный риск засухи"
        elif risk < 70:
            description = "Высокий риск засухи - требуется орошение"
        else:
            description = "Критический риск засухи - орошение обязательно"

        return risk, description


class PestAnalyzer:
    """Анализатор рисков вредителей и болезней"""

    PESTS = {
        'Пшеница': ['Хлебная жужелица', 'Тля', 'Ржавчина'],
        'Кукуруза': ['Кукурузный мотылёк', 'Проволочник', 'Гниль початков'],
        'Картофель': ['Колорадский жук', 'Фитофтороз', 'Проволочник'],
        'Подсолнечник': ['Подсолнечниковая огнёвка', 'Заразиха', 'Белая гниль'],
        'Соя': ['Соевая тля', 'Паутинный клещ', 'Ржавчина'],
        'Томаты': ['Белокрылка', 'Фитофтороз', 'Вершинная гниль'],
        'Огурцы': ['Паутинный клещ', 'Мучнистая роса', 'Тля']
    }

    @staticmethod
    def get_pest_list(crop: str) -> List[str]:
        """Получить список основных вредителей для культуры"""
        return PestAnalyzer.PESTS.get(crop, ['Общие вредители'])

    @staticmethod
    def calculate_pest_damage(pest_vulnerability: float,
                              anthro_load: float,
                              protection_level: float) -> Dict[str, float]:
        """
        Расчёт потенциального ущерба от вредителей

        Returns:
            Словарь с прогнозом потерь урожая
        """
        # Базовый ущерб от вредителей
        base_damage = pest_vulnerability * 100

        # Антропогенная нагрузка увеличивает активность вредителей
        anthro_factor = 1 + (anthro_load / 200)
        adjusted_damage = base_damage * anthro_factor

        # Защита снижает ущерб
        protection_factor = (100 - protection_level) / 100
        final_damage = adjusted_damage * protection_factor

        return {
            'base_damage': base_damage,
            'with_anthro': adjusted_damage,
            'with_protection': final_damage,
            'prevented_damage': adjusted_damage - final_damage
        }


class AnimalDamageAnalyzer:
    """Анализатор ущерба от диких животных"""

    ANIMALS = {
        'низкий': ['Птицы', 'Мелкие грызуны'],
        'средний': ['Зайцы', 'Кроты', 'Скворцы (стаи)'],
        'высокий': ['Кабаны', 'Олени', 'Лоси']
    }

    @staticmethod
    def get_animal_threats(risk_level: float) -> List[str]:
        """Получить список потенциальных вредителей-животных"""
        if risk_level < 30:
            return AnimalDamageAnalyzer.ANIMALS['низкий']
        elif risk_level < 70:
            return AnimalDamageAnalyzer.ANIMALS['средний']
        else:
            return AnimalDamageAnalyzer.ANIMALS['высокий']

    @staticmethod
    def calculate_fence_requirements(risk_level: float,
                                     area: float) -> Dict[str, any]:
        """
        Расчёт требований к ограждению

        Returns:
            Словарь с рекомендациями по забору
        """
        # Расчёт периметра (приблизительно для квадратного участка)
        side_length = math.sqrt(area * 10000)  # га в м²
        perimeter = 4 * side_length

        if risk_level < 30:
            fence_type = "Простая сетка"
            height = 1.5
            cost_multiplier = 1.0
        elif risk_level < 70:
            fence_type = "Усиленная сетка с колючей проволокой"
            height = 2.0
            cost_multiplier = 1.5
        else:
            fence_type = "Прочное ограждение с заглублением"
            height = 2.5
            cost_multiplier = 2.0

        return {
            'fence_type': fence_type,
            'height': height,
            'perimeter': perimeter,
            'cost_multiplier': cost_multiplier,
            'animals': AnimalDamageAnalyzer.get_animal_threats(risk_level)
        }


class YieldPredictor:
    """Прогнозирование урожайности"""

    # Средняя урожайность в ц/га при идеальных условиях
    BASE_YIELDS = {
        'Пшеница': 40,
        'Кукуруза': 60,
        'Картофель': 250,
        'Подсолнечник': 25,
        'Соя': 22,
        'Озимая пшеница': 45,
        'Томаты': 500,
        'Огурцы': 400
    }

    @staticmethod
    def predict_yield(crop: str, area: float,
                      climate_impact: float,
                      pest_damage: float,
                      animal_damage: float,
                      irrigation: bool) -> Dict[str, float]:
        """
        Прогноз урожайности с учётом всех факторов

        Returns:
            Словарь с прогнозом урожая
        """
        base_yield = YieldPredictor.BASE_YIELDS.get(crop, 30)

        # Влияние климата
        if -1 <= climate_impact <= 2:
            climate_factor = 1.0 + (climate_impact * 0.05)  # небольшое потепление может быть полезно
        else:
            climate_factor = 1.0 - (abs(climate_impact - 1) * 0.1)

        # Влияние вредителей
        pest_factor = 1.0 - (pest_damage / 100)

        # Влияние животных
        animal_factor = 1.0 - (animal_damage / 100)

        # Орошение
        irrigation_factor = 1.2 if irrigation else 1.0

        # Итоговая урожайность
        final_yield = (base_yield * climate_factor * pest_factor *
                       animal_factor * irrigation_factor)

        total_production = final_yield * area

        return {
            'base_yield_per_ha': base_yield,
            'predicted_yield_per_ha': final_yield,
            'total_production': total_production,
            'climate_factor': climate_factor,
            'pest_factor': pest_factor,
            'animal_factor': animal_factor,
            'irrigation_factor': irrigation_factor,
            'production_loss_percent': ((base_yield - final_yield) / base_yield * 100)
        }


class ProfitCalculator:
    """Расчёт прибыльности"""

    # Средние рыночные цены (руб/ц)
    MARKET_PRICES = {
        'Пшеница': 1200,
        'Кукуруза': 1000,
        'Картофель': 800,
        'Подсолнечник': 3000,
        'Соя': 2500,
        'Озимая пшеница': 1300,
        'Томаты': 3500,
        'Огурцы': 4000
    }

    @staticmethod
    def calculate_profit(crop: str,
                         total_production: float,
                         total_costs: float,
                         price_fluctuation: float = 0) -> Dict[str, float]:
        """
        Расчёт прибыли

        Args:
            crop: название культуры
            total_production: общий урожай в центнерах
            total_costs: общие затраты
            price_fluctuation: колебание цены в процентах (-50 до +50)

        Returns:
            Словарь с финансовыми показателями
        """
        base_price = ProfitCalculator.MARKET_PRICES.get(crop, 1500)
        actual_price = base_price * (1 + price_fluctuation / 100)

        revenue = total_production * actual_price
        profit = revenue - total_costs
        roi = (profit / total_costs * 100) if total_costs > 0 else 0

        return {
            'base_price_per_unit': base_price,
            'actual_price_per_unit': actual_price,
            'total_revenue': revenue,
            'total_costs': total_costs,
            'net_profit': profit,
            'roi_percent': roi,
            'breakeven_production': total_costs / actual_price if actual_price > 0 else 0
        }


class SeasonalPlanner:
    """Планировщик сезонных работ"""

    @staticmethod
    def create_work_schedule(crop: str, planting_month: int,
                             growing_days: int) -> List[Dict]:
        """
        Создать график работ на сезон

        Returns:
            Список этапов работ с датами
        """
        schedule = []

        # Подготовка почвы (за 2 недели до посадки)
        prep_date = datetime(datetime.now().year, planting_month, 1) - timedelta(days=14)
        schedule.append({
            'stage': 'Подготовка почвы',
            'date': prep_date.strftime('%d.%m.%Y'),
            'tasks': ['Вспашка', 'Боронование', 'Внесение удобрений']
        })

        # Посадка
        plant_date = datetime(datetime.now().year, planting_month, 1)
        schedule.append({
            'stage': 'Посадка',
            'date': plant_date.strftime('%d.%m.%Y'),
            'tasks': ['Посев семян', 'Прикатывание', 'Первый полив']
        })

        # Уход (через 2 недели)
        care_date = plant_date + timedelta(days=14)
        schedule.append({
            'stage': 'Первый уход',
            'date': care_date.strftime('%d.%m.%Y'),
            'tasks': ['Прополка', 'Рыхление', 'Подкормка']
        })

        # Средний период (через месяц)
        mid_date = plant_date + timedelta(days=growing_days // 2)
        schedule.append({
            'stage': 'Средний период',
            'date': mid_date.strftime('%d.%m.%Y'),
            'tasks': ['Обработка от вредителей', 'Полив', 'Осмотр посевов']
        })

        # Уборка
        harvest_date = plant_date + timedelta(days=growing_days)
        schedule.append({
            'stage': 'Уборка урожая',
            'date': harvest_date.strftime('%d.%m.%Y'),
            'tasks': ['Скашивание/сбор', 'Транспортировка', 'Первичная обработка']
        })

        return schedule


# Функции для интеграции с основным приложением

def generate_extended_report(crop: str, area: float, climate_change: float,
                             anthro_load: float, animal_risk: float,
                             pest_vulnerability: float, protection_level: float,
                             irrigation: bool, planting_month: int,
                             growing_days: int, water_need: float,
                             frost_tolerance: float, total_costs: float) -> str:
    """
    Генерация расширенного отчёта с аналитикой
    """
    report = "\n" + "=" * 80 + "\n"
    report += "РАСШИРЕННАЯ АНАЛИТИКА\n"
    report += "=" * 80 + "\n\n"

    # Анализ погодных рисков
    frost_risk, frost_desc = WeatherAnalyzer.calculate_frost_risk(
        planting_month, climate_change, frost_tolerance
    )
    drought_risk, drought_desc = WeatherAnalyzer.calculate_drought_risk(
        planting_month, climate_change, water_need
    )

    report += "ПОГОДНЫЕ РИСКИ:\n"
    report += "-" * 80 + "\n"
    report += f"  Риск заморозков: {frost_risk:.1f}% - {frost_desc}\n"
    report += f"  Риск засухи: {drought_risk:.1f}% - {drought_desc}\n\n"

    # Анализ вредителей
    pest_damages = PestAnalyzer.calculate_pest_damage(
        pest_vulnerability, anthro_load, protection_level
    )
    pests = PestAnalyzer.get_pest_list(crop)

    report += "АНАЛИЗ ВРЕДИТЕЛЕЙ:\n"
    report += "-" * 80 + "\n"
    report += f"  Основные вредители: {', '.join(pests)}\n"
    report += f"  Базовый ущерб: {pest_damages['base_damage']:.1f}%\n"
    report += f"  С учётом антропогенной нагрузки: {pest_damages['with_anthro']:.1f}%\n"
    report += f"  После защитных мер: {pest_damages['with_protection']:.1f}%\n"
    report += f"  Предотвращённый ущерб: {pest_damages['prevented_damage']:.1f}%\n\n"

    # Анализ ущерба от животных
    fence_req = AnimalDamageAnalyzer.calculate_fence_requirements(animal_risk, area)

    report += "ЗАЩИТА ОТ ЖИВОТНЫХ:\n"
    report += "-" * 80 + "\n"
    report += f"  Потенциальные вредители: {', '.join(fence_req['animals'])}\n"
    report += f"  Рекомендуемый тип забора: {fence_req['fence_type']}\n"
    report += f"  Рекомендуемая высота: {fence_req['height']} м\n"
    report += f"  Требуемый периметр: {fence_req['perimeter']:.0f} м\n\n"

    # Прогноз урожайности
    yield_pred = YieldPredictor.predict_yield(
        crop, area, climate_change, pest_damages['with_protection'],
        animal_risk, irrigation
    )

    report += "ПРОГНОЗ УРОЖАЙНОСТИ:\n"
    report += "-" * 80 + "\n"
    report += f"  Базовая урожайность: {yield_pred['base_yield_per_ha']:.1f} ц/га\n"
    report += f"  Прогнозируемая урожайность: {yield_pred['predicted_yield_per_ha']:.1f} ц/га\n"
    report += f"  Общий урожай: {yield_pred['total_production']:.1f} ц\n"
    report += f"  Потери урожая: {yield_pred['production_loss_percent']:.1f}%\n\n"

    # Прогноз прибыли
    profit = ProfitCalculator.calculate_profit(
        crop, yield_pred['total_production'], total_costs
    )

    report += "ЭКОНОМИЧЕСКИЙ ПРОГНОЗ:\n"
    report += "-" * 80 + "\n"
    report += f"  Рыночная цена: {profit['base_price_per_unit']:.2f} руб/ц\n"
    report += f"  Выручка: {profit['total_revenue']:,.2f} руб\n"
    report += f"  Затраты: {profit['total_costs']:,.2f} руб\n"
    report += f"  Прибыль: {profit['net_profit']:,.2f} руб\n"
    report += f"  Рентабельность (ROI): {profit['roi_percent']:.1f}%\n"
    report += f"  Точка безубыточности: {profit['breakeven_production']:.1f} ц\n\n"

    # График работ
    schedule = SeasonalPlanner.create_work_schedule(crop, planting_month, growing_days)

    report += "ГРАФИК РАБОТ:\n"
    report += "-" * 80 + "\n"
    for stage in schedule:
        report += f"\n  {stage['stage']} ({stage['date']}):\n"
        for task in stage['tasks']:
            report += f"    • {task}\n"

    report += "\n" + "=" * 80 + "\n"

    return report


if __name__ == "__main__":
    # Пример использования аналитических функций
    print("Модуль аналитики загружен успешно")
    print("\nДоступные классы:")
    print("  - WeatherAnalyzer: анализ погодных условий")
    print("  - PestAnalyzer: анализ вредителей")
    print("  - AnimalDamageAnalyzer: анализ ущерба от животных")
    print("  - YieldPredictor: прогнозирование урожайности")
    print("  - ProfitCalculator: расчёт прибыльности")
    print("  - SeasonalPlanner: планирование работ")
