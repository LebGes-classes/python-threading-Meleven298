import pandas as pd


class Reporter:
    '''Класс репортера.'''

    def report(self, df: pd.DataFrame) ->  pd.DataFrame:
        '''Функция для отдачи отчета.

        Args:
            df_to_report: Данные для отчета.

        Returns:
            problem_calibration_data: Отчет по пробленым оборудованиям
            norm_calibration_data: Отчет по нормальным оборудованиям
        '''

        today = pd.Timestamp.now().normalize()

        df['have_problem'] = df['issues_reported_12mo'].apply(lambda x: 'yes' if x > 0 else 'no')

        mask = df['last_calibration_date'] >= df['install_date']
        calibration_data = df.loc[mask, ['device_id', 'clinic_id', 'have_problem',
                                         'install_date', 'warranty_until', 'last_calibration_date',
                                         'issues_reported_12mo']].copy()
        
        calibration_data['days_until_calibration'] = (calibration_data['last_calibration_date'] - today).dt.days
        calibration_data['warranty_works_for'] = (calibration_data['warranty_until'] - today).dt.days

        calibration_data = calibration_data[['device_id', 'clinic_id', 'have_problem',
                                             'days_until_calibration', 'warranty_works_for',
                                             'issues_reported_12mo']]
        
        problem = calibration_data[calibration_data['have_problem'] == 'yes']
        norm = calibration_data[calibration_data['have_problem'] == 'no']

        return problem, norm
    