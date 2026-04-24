from Proccessor import run_threaded
from Manager import Manager

import time


if __name__ == '__main__':
    Manager('').work_menu()

    option = Manager('').option_manager([1,2,3,4,5])

    files = ["medical_diagnostic_devices_1.xlsx", "medical_diagnostic_devices_2.xlsx",
              "medical_diagnostic_devices_3.xlsx", "medical_diagnostic_devices_4.xlsx",
                "medical_diagnostic_devices_5.xlsx", "medical_diagnostic_devices_6.xlsx",
                "medical_diagnostic_devices_7.xlsx", "medical_diagnostic_devices_8.xlsx",
                "medical_diagnostic_devices_9.xlsx", "medical_diagnostic_devices_10.xlsx"
                ]
    
    start_thread = time.time()
    thread_times = run_threaded(files, option)
    total_thread = time.time() - start_thread

    print(f"\nThreading общее время: {total_thread:.1f} сек\n")
    