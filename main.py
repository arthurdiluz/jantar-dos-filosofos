from threading import Thread, Lock
from random import seed, uniform
from time import sleep
'''
5 filósofos e 5 garfos; é necessário 3 garfos para comer;
Deadlock é evitado para nunca esperar um garfo com outro garfo na mão;
"Procedure" é bloquear ao esperar o primeiro garfo e desbloquear ao pegar o segundo garfo.
Se falhar ao pegar o segundo garfo, o primeiro garfo é largado e os garfos são trocados.
'''


class Filosofo(Thread):
    executando = True  # Thread começa executando

    # Construtor da classe Filosofo
    def __init__(self, nome, garfo_esquerda, garfo_direita):
        Thread.__init__(self)  # Herança dos atributos da classe Thread
        self.nome = nome
        self.garfo_esquerda = garfo_esquerda
        self.garfa_direita = garfo_direita

    # Sobrescrita do método "run" da classe "Thread".
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
            garfo1.acquire(True)
            locked = garfo2.acquire(False)
            if locked:
                break
            garfo1.release()
        else:
            return

        print(F" >{self.nome} começou a comer")
        sleep(uniform(5, 10))
        print(F"> {self.nome} parou de comer")
        garfo1.release()
        garfo2.release()


if __name__ == '__main__':
    # número base para gerar valores aleatórios
    seed(507129)
    # nome dos filósofos
    nomes = ("Arthur", "Jesus", "VitorV", "Dijkstra", "Neymar")
    # garfos com lock para impedir que dois acessem o mesmo garfo
    garfos = [Lock() for _ in range(5)]
    # mesa com 5 filósofos e 1 garfo para cada
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
