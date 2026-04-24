from Manager import Manager

import asyncio
import threading
import time


async def process_file_async(filename: str, option: int) -> float:
    '''Время асинхронного выполнения по каждому.
    
    Args:
        filename: Название файла.
        option: Выбор действия.

    Returns:
        elapsed: Ушедшее на файл время.
    '''

    start = time.time()
    manager = Manager(filename)

    await manager.general_manager_a(option)
    elapsed = time.time() - start

    print(f"[Async] {filename} завершён за {elapsed:.1f} сек")

    return elapsed

async def run_async(files: list, option: int) -> list:
    '''Собираем время асинхронного выполнения.

    Args:
        files: Список файлов.
        option: Выбор действия.

    Returns:
        Список времен.
    '''

    tasks = [process_file_async(f, option) for f in files]

    return await asyncio.gather(*tasks)

def process_file_sync(filename: str, option: int) -> float:
   '''Время синхронного выполнения по каждому.
    
    Args:
        filename: Название файла.
        option: Выбор действия.

    Returns:
        elapsed: Ушедшее на файл время.
    '''

   start = time.time()
   manager = Manager(filename)

   manager.general_manager(option)

   elapsed = time.time() - start

   print(f"[Thread] {filename} завершён за {elapsed:.1f} сек")

   return elapsed

def run_sync(files: list, option: int) -> list:
    '''Собираем время асинхронного выполнения.

    Args:
        files: Список файлов.
        option: Выбор действия.

    Returns:
        Список времен.
    '''

    return [process_file_sync(f, option) for f in files]

def process_file_threaded(filename: str, option: int) -> float:
    '''Время многопоточного выполнения по каждому.
    
    Args:
        filename: Название файла.
        option: Выбор действия.

    Returns:
        Ушедшее на файл время.
    '''

    return process_file_sync(filename, option)

def thread_worker(filename: str, option: int, results: list, lock: threading.Lock):
    '''Функция, выполняемая в отдельном потоке. Вызывает 
    обработку и сохраняет результат в общий список.

    Args:
        filename: Название файла.
        option: Выбор действия.
        results: список кортежей состоящих из названия файла и потраченного времени.
        lock: блокировщик Thread.
    '''

    try:
        elapsed = process_file_threaded(filename, option)

        with lock:
            results.append((elapsed, filename))
    except Exception as e:
        print(f"[Thread] Ошибка в файле {filename}: {e}")

def run_threaded(files: list, option: int) -> list:
    '''Запуск нескольких файлов в потоках.
    Результаты собираются в обычный список с блокировкой.

    Args:
        filename: Название файла.
        option: Выбор действия.

    Returns:
        times: список времен.
    '''

    results = []
    lock = threading.Lock()
    threads = []

    for f in files:
        t = threading.Thread(target=thread_worker, args=(f, option, results, lock))
        threads.append(t)

        t.start()

    for t in threads:
        t.join()

    times = []

    for elapsed, fname in results:
        print(f"[Thread] {fname} завершён за {elapsed:.1f} сек")

        times.append(elapsed)

    return times


if __name__ == "__main__":
    manager = Manager('')

    manager.work_menu()
    option = manager.option_manager([1, 2, 3, 4, 5])

    files = [
        "medical_diagnostic_devices_1.xlsx",
        "medical_diagnostic_devices_2.xlsx",
        "medical_diagnostic_devices_3.xlsx",
        "medical_diagnostic_devices_4.xlsx",
        "medical_diagnostic_devices_5.xlsx",
        "medical_diagnostic_devices_6.xlsx",
        "medical_diagnostic_devices_7.xlsx",
        "medical_diagnostic_devices_8.xlsx",
        "medical_diagnostic_devices_9.xlsx",
        "medical_diagnostic_devices_10.xlsx"
    ]

    start_thread = time.time()
    thread_times = run_threaded(files, option)
    total_thread = time.time() - start_thread

    print(f"\nThreading общее время: {total_thread:.1f} сек\n")

    start_async = time.time()
    async_times = asyncio.run(run_async(files, option))
    total_async = time.time() - start_async

    print(f"\nAsync общее время: {total_async:.1f} сек\n")

    print("=" * 40)
    print(f"Async total     : {total_async:.2f} сек")
    print(f"Threading total : {total_thread:.2f} сек")
    