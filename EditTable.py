import pandas as pd


class EditTable:
    '''Класс правки таблицы.'''

    def empty_to_unknown(self, df: pd.DataFrame) -> pd.DataFrame:
        '''Преобразуем пустые значения в строках.
        
        Args:
            df: Датафрейм для преобразований.

        Returns:
            Преобразованный датафрейм.
        '''

        return df.fillna('unknown').replace('', 'unknown')

    def normalize_status(self, df: pd.DataFrame) -> pd.DataFrame:
        '''Нормализуем статусы оборудований.

        Args:
            df: Датафрейм для нормализации.

        Returns:
            df: Датафрейм с нормализованными статусами.
        '''

        df = self.empty_to_unknown(df)
        
        planned_keywords = [
            'planned', 'plan', 'scheduled_install', 'to_install', 
            'pending', 'waiting', 'scheduled install', 'install scheduled',
            'planned_installation', 'planned installation', 'to install',
            'scheduled install'
        ]

        faulty_keywords = [
            'fault', 'faulty', 'broken', 'repair', 'error', 
            'needs_repair', 'needs repair', 'failed', 'failure',
            'not working', 'down', 'out of order', 'malfunction'
        ]

        maintenance_keywords = [
            'maintenance', 'maint', 'schedule', 'scheduled', 
            'maint_sched', 'service_scheduled', 'service scheduled',
            'due', 'maintenance_scheduled', 'maintenance scheduled',
            'service due', 'maintenance due'
        ]

        operational_values = [
            'operational', 'ok', 'working', 'op', 
            'operational1', 'operational2', 'operational3', 'operational4',
            'active', 'online', 'good', 'normal', 'functioning'
        ]

        df['status'] = df['status'].replace(planned_keywords, 'planned_installation')
        df['status'] = df['status'].replace(faulty_keywords, 'faulty')
        df['status'] = df['status'].replace(maintenance_keywords, 'maintenance_scheduled')
        df['status'] = df['status'].replace(operational_values, 'operational')

        return df
    