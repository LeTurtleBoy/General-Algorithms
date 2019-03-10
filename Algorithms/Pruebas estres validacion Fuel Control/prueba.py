import requests
import time
from random import randrange
# r = requests.get('https://api.github.com/user', auth=('chris.mrn92@gmail.com', 'contraseña'))
import threading

def worker(cara):
    print("hilo ejecutado en la cara", cara)
    for i in range(4):
        time.sleep(randrange(20))
        print("Peticion isla", cara, "Iteración", i)
    return

threads = []
for i in range(1,16):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
    time.sleep(0.05)
    