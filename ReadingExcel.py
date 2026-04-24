import pandas as pd
import aiofiles
import io


class ReadingExcel:
    '''Класс чтения.'''

    def reading_excel_sync(self, data: str) -> pd.DataFrame:
        '''Функция чтения иксель файлов.

        Args:
            data: Файл, который нужно прочитать.

        Returns:
            df: pandas.DatFrame'''

        df = pd.read_excel(data, engine='openpyxl')

        return df

    async def reading_excel_async(self, data: str) -> pd.DataFrame:
        '''Функция асинхронного чтения иксель файлов.

        Args:
            data: Файл, который нужно прочитать.
            
        Returns:
            df: pandas.DatFrame.
        '''
         
        async with aiofiles.open(data, 'rb') as f:
            async_data = await f.read()

        df = pd.read_excel(io.BytesIO(async_data), engine='openpyxl')

        return df
    