from random import seed, uniform
from time import sleep
from threading import Thread, Lock


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
