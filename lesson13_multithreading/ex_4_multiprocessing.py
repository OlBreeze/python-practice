from multiprocessing import Process

def print_numbers():
    for i in range(5):
        print(i)

process = Process(target=print_numbers)
process.start()
process.join()


# Используется модуль multiprocessing, который создаёт отдельный процесс (в отличие от потоков).
#
# Функция print_numbers() будет выполняться в отдельном процессе.
#
# process.start() запускает новый процесс.
#
# process.join() ожидает завершения процесса, прежде чем программа продолжит выполнение.
