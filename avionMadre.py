class Avion():
    def __init__(self, nave: list, stats = None):
        #Tamaño de nuestra pantalla
        self.SCREEN_WIDTH = 256
        self.SCREEN_HEIGHT = 256

        #Posición
        self.x = nave[1][0]
        self.y = nave[1][1]

        #Sprite de nuestro avión (contiene banco de imagén, posición y dimensión)
        self.sprite = nave[0]

        #Otros atributos básicos
        self.stats = stats
        self.health = self.stats[0]
        self.damage = self.stats[1]
        self.speed = self.stats[2]
        self.alive = self.stats[3]
        self.puntuacion = self.stats[4]
        self.animacionMuerte = False

    @property
    def stats(self):
        return self.__stats
    @stats.setter
    def stats(self, stats):
        if stats == None:
            self.__stats = [1, 1, 2, True, 10]
        else:
            self.__stats = stats    


    def __str__(self) -> str:
        stats = f'''
        Health: {self.health}
        Damage: {self.damage}
        Speed: {self.speed}
        Alive: {self.alive}
        '''
        return stats

    def drawAvion(self):
        self.blt = (self.x, self.y, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], self.sprite[4])

    def perderVida(self):
        self.health -= 1
        if self.health <= 0:
            self.animacionMuerte = True

    def perderVida2(self):
        self.health -= 1
        if self.health == 0:
            self.alive = False        


