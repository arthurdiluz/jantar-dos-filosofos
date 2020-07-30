from filosofo import *

'''
5 filósofos e 5 garfos; é necessário 2 garfos para comer
Deadlock é evitado para nunca esperar um garfo com outro garfo na mão
Se falhar ao pegar o segundo garfo, o primeiro garfo é largado e os garfos são trocados
'''

if __name__ == '__main__':
    seed(507129)
    nomes = ("Arthur", "Gabriel", "Vitor", "Neymar", "Dijkstra")
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
