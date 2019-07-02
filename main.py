import threading
import random
import time
'''
5 filósofos e 5 garfos; é necessário 3 garfos para comer;
Deadlock é evitado para nunca esperar um garfo com outro garfo na mão;
"Procedure" é bloquear ao esperar o primeiro garfo e desbloquear ao pegar o segundo garfo.
Se falhar ao pegar o segundo garfo, o primeiro garfo é largado e os garfos são trocados.
'''


class Filosofo(threading.Thread):
    running = True

    def __init__(self, nome, garfo_esquerda, garfo_direita):
        threading.Thread.__init__(self)
        self.nome = nome
        self.garfo_esquerda = garfo_esquerda
        self.garfa_direita = garfo_direita
        self.comeu = False

    def run(self):
        while self.running:
            # Filósofo está pensando (dormindo).
            # time.sleep(5)
            time.sleep(random.uniform(5, 15))
            print(F"{self.nome} está pensando!")
            self.comer()

    def comer(self):
        garfo1, garfo2 = self.garfo_esquerda, self.garfa_direita

        while self.running:
            garfo1.acquire(True)
            locked = garfo2.acquire(False)
            if locked:
                break
            garfo1.release()

            # print(F"{self.nome} parou de comer")
            # garfo1, garfo2 = garfo2, garfo1
        else:
            return

        self.jantando()
        garfo2.release()
        garfo1.release()

    def jantando(self):
        print(F"{self.nome} começou a comer")
        # time.sleep(random.uniform(1, 10))
        time.sleep(5)
        print(F"{self.nome} parou de comer")  # ao terminar de comer


if __name__ == '__main__':
    # número base para gerar valores aleatórios
    random.seed(507129)
    # nome dos filósofos
    nomes = ("Arthur", "Jesus", "VitorV", "Dijkstra", "Neymar")
    # garfos com lock para impedir que dois acessem o mesmo garfo
    garfos = [threading.Lock() for _ in range(5)]
    # mesa com
    mesa = [Filosofo(nomes[i], garfos[i % 5], garfos[(i + 1) % 5]) for i in range(5)]

    for _ in range(2):
        print("start")
        Filosofo.running = True

        for filosofo in mesa:
            filosofo.start()

        time.sleep(100)
        Filosofo.running = False
        print("end")
