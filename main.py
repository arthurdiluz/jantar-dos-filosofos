from threading import Thread, Lock
from random import seed, uniform
from time import sleep
'''
5 filósofos e 5 garfos; é necessário 2 garfos para comer
Deadlock é evitado para nunca esperar um garfo com outro garfo na mão
Se falhar ao pegar o segundo garfo, o primeiro garfo é largado e os garfos são trocados
'''


class Filosofo(Thread):
    executando = True  # começa executando para

    def __init__(self, nome, garfo_esquerda, garfo_direita):
        Thread.__init__(self)
        self.nome = nome
        self.garfo_esquerda = garfo_esquerda
        self.garfa_direita = garfo_direita

    # Sobrescrita de Thread.
    def run(self):
        while self.executando:
            print(F"> {self.nome} está pensando")
            sleep(uniform(5, 15))
            self.comer()

    def comer(self):
        '''
        Pega o garfo 1 e tenta pegar o garfo 2. Se o garfo 2 estiver livre,
        o ele janta e solta os dois garfos em seguida, caso contrário,
        ele desiste de comer e continua pensando.
        '''

        garfo1, garfo2 = self.garfo_esquerda, self.garfa_direita
        while self.executando:
            garfo1.acquire(True)  # tenta pegar o primeiro garfo
            locked = garfo2.acquire(False)  # verifica se o segundo garfo está disponível
            if locked:
                break
            garfo1.release()
        else:
            return  # se nao for possível comer

        print(F" >{self.nome} começou a comer")
        sleep(uniform(5, 10))
        print(F"> {self.nome} parou de comer")
        garfo1.release()
        garfo2.release()


if __name__ == '__main__':
    seed(507129)
    nomes = ("Arthur", "Jesus", "VitorV", "Dijkstra", "Neymar")
    garfos = [Lock() for _ in range(5)]
    mesa = [Filosofo(nomes[i], garfos[i % 5], garfos[(i + 1) % 5]) for i in range(5)]

    for _ in range(50):
        Filosofo.executando = True
        for filosofo in mesa:
            try:
                filosofo.start()
                sleep(2)
            except RuntimeError:  # caso a thread já tenha sido iniciada
                pass
        sleep(uniform(5, 15))
        Filosofo.executando = False
