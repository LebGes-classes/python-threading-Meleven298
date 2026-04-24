from DataParser import DateParser
from Aggregator import Aggregator
from Reporter import Reporter
from DataMerging import DataMerging
from PivotTable import PivotTable
from ReadingExcel import ReadingExcel
from WritingExcel import WritingExcel

import pandas as pd


class Manager:
    '''Класс менеджера.'''

    def __init__(self, filename):
        self.filename = filename

    def start_menu(self) -> None:
        '''Стартовое меню'''

        print('Здравствуйте.')
        print('Для просмотра таблицы  нажмите 1.')
        print('Для выхода из программы 0.')

    def work_menu(self) -> None:
        '''Рабочее меню.'''

        print('Что вы желаете увидеть?')
        print('1. Отчет по срокам калибровки оборудования.')
        print('2. Сводная таблица по проблемным оборудованиям(гарантия действительна).')
        print('3. Сводная таблица по непроблемным оборудованиям(гарантия действительна).')
        print('4. Сводная таблица по проблемным оборудованиям(гарантия недействительна).')
        print('5. Сводная таблица по непроблемным оборудованиям(гарантия недействительна).')
        print('6. Ничего не хочу.')
    
    def concrete_menu(self) -> None:
        '''Меню конкретики по девайсам.'''

        print('Хотите видеть конкретные девайсы у этих клиник?')
        print('1. Да.')
        print('0. Нет.')

    def option_manager(self, available_options: list[int]) -> int:
        '''Функция для слежки за корректным вводом.
        
        Args:
            available_options: список доступных вариантов ввода.

        Returns:
            option: Вариант ввода, выбранный пользователем и прошедший проверку.
        '''

        isWork = True
        option = None

        while isWork:
            try:
                option = int(input('Ваш выбор: '))

                if option not in available_options:
                    print(f"Ошибка: выберите число из {available_options}")
                else:
                    isWork = False

            except ValueError:
                print("Ошибка: введите корректное число")

        return option

    async def general_manager_a(self, option) -> None:
        '''Главная функция, вызывающая методы с разных классов в зависимости от ввода.'''

        isWork = True

        writer = WritingExcel(self.filename)

        df = await ReadingExcel().reading_excel_async(self.filename)

        sorted_dates = DateParser().sort_dates(df)
        calibri_problem, calibri_norm = Reporter().report(sorted_dates)
        clinics_by_issues = Aggregator().sort_by_groups(df)

        while isWork:
            if option == 1:
                concated_data = DataMerging().concat_data(calibri_problem, calibri_norm)

                writer.write_to_excel(concated_data.sort_values(by=['warranty_works_for', 'clinic_id', "device_id"], ascending=[False, True, False]))
            elif option == 2:
                merged_problem_data = pd.merge(left=calibri_problem, right=clinics_by_issues, how='left')

                pivot_table = PivotTable().make_pivot_table(merged_problem_data[merged_problem_data['warranty_works_for'] >= 0], 'days_until_calibration')

                pivot_table = pivot_table.sort_values(by='total_issues_12mo', ascending=False)

                writer.write_to_excel(pivot_table)
            elif option == 3:
                merged_norm_data = pd.merge(left=calibri_norm, right=clinics_by_issues, how='left')

                pivot_table = pivot_table = PivotTable().make_pivot_table(merged_norm_data[merged_norm_data['warranty_works_for'] >= 0], 'days_until_calibration')

                writer.write_to_excel(pivot_table)
            elif option == 4:
                merged_problem_data = pd.merge(left=calibri_problem, right=clinics_by_issues, how='left')

                pivot_table = PivotTable().make_pivot_table(merged_problem_data[merged_problem_data['warranty_works_for'] < 0], 'days_until_calibration')

                pivot_table.sort_values(by='total_issues_12mo', ascending=False)

                writer.write_to_excel(pivot_table)
            elif option == 5:
                merged_norm_data = pd.merge(left=calibri_norm, right=clinics_by_issues, how='left')

                pivot_table = PivotTable().make_pivot_table(merged_norm_data[merged_norm_data['warranty_works_for'] < 0], 'days_until_calibration')

                writer.write_to_excel(pivot_table)
            isWork = False

    def general_manager(self, option: int) -> None:
        '''Главная функция, вызывающая методы с разных классов в зависимости от ввода.

        Args:
            option: Выбор действия.
        '''

        isWork = True

        writer = WritingExcel(self.filename)

        df = ReadingExcel().reading_excel_sync(self.filename)

        sorted_dates = DateParser().sort_dates(df)
        calibri_problem, calibri_norm = Reporter().report(sorted_dates)
        clinics_by_issues = Aggregator().sort_by_groups(df)

        while isWork:
            if option == 1:
                concated_data = DataMerging().concat_data(calibri_problem, calibri_norm)

                writer.write_to_excel(concated_data.sort_values(by=['warranty_works_for', 'clinic_id', "device_id"], ascending=[False, True, False]))
            elif option == 2:
                merged_problem_data = pd.merge(left=calibri_problem, right=clinics_by_issues, how='left')

                pivot_table = PivotTable().make_pivot_table(merged_problem_data[merged_problem_data['warranty_works_for'] >= 0], 'days_until_calibration')

                pivot_table = pivot_table.sort_values(by='total_issues_12mo', ascending=False)

                writer.write_to_excel(pivot_table)
            elif option == 3:
                merged_norm_data = pd.merge(left=calibri_norm, right=clinics_by_issues, how='left')

                pivot_table = pivot_table = PivotTable().make_pivot_table(merged_norm_data[merged_norm_data['warranty_works_for'] >= 0], 'days_until_calibration')

                writer.write_to_excel(pivot_table)
            elif option == 4:
                merged_problem_data = pd.merge(left=calibri_problem, right=clinics_by_issues, how='left')

                pivot_table = PivotTable().make_pivot_table(merged_problem_data[merged_problem_data['warranty_works_for'] < 0], 'days_until_calibration')

                pivot_table.sort_values(by='total_issues_12mo', ascending=False)

                writer.write_to_excel(pivot_table)
            elif option == 5:
                merged_norm_data = pd.merge(left=calibri_norm, right=clinics_by_issues, how='left')

                pivot_table = PivotTable().make_pivot_table(merged_norm_data[merged_norm_data['warranty_works_for'] < 0], 'days_until_calibration')

                writer.write_to_excel(pivot_table)
            isWork = False
    