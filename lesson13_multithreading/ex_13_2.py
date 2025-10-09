from multiprocessing import Process

def print_numbers():
    for i in range(5):
        print(i)

processes = [Process(target=print_numbers) for _ in range(3)]

for p in processes:
    p.start()

for p in processes:
    p.join()
