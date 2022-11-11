#En este fichero vamos a crear todas las clases que usaremos en nuestro juego.

#Clase del avión que controla el jugador
class AvionLocal:
    #Atributos
    x: int
    y: int
    health: int
    daño: int #Podrá variar en función de los bonuses de los enemigos rojos
    #sprite

    def move(self):
        pass

    def ataque(self):
        pass

#Clases de los aviones enemigos
class EnemigoRegular:
    #Atributos
    x: int
    y: int
    health: int
    daño: int
    # Consultar cómo se determina el sprite como atributo
    # sprite: str

    #Métodos
    def move(self):
        pass

    def ataque(self):
        pass

class EnemigoRojo:
    #Atributos
    x: int
    y: int
    health: int
    bonus: int #¿Creamos una lista con diferentes bonus aleatorios?
    # sprite: str

    #Métodos
    def move(self):
        pass

class Bombardero:
    #Atributos
    x: int
    y: int
    health: int
    daño: int
    # sprite: str

    #Métodos
    def move(self):
        pass

    def ataque(self):
        pass

class SuperBombardero:
    #Atributos
    x: int
    y: int
    health: int
    daño: int
    # sprite: str

    #Métodos
    def move(self):
        pass

    def ataque(self):
        pass