'''Clase para el disparos de los enemigos que disparan aleatoriamente (enemigo regular y bombardero) se le introduce por parámetro la posición del
avión que dispara, la posición del avión al que dispara (el nuestro), y sus stats'''
class DisparoEnemigo:
    def __init__(self, posicionAvionEnemigo: list, posicionAvionJugador, stats: list):
        #Posición desde donde se va a lanzar
        self.x = posicionAvionEnemigo[0]
        self.y = posicionAvionEnemigo[1]

        #La posición del jugador será vital para que el enemigo sepa hacia que dirección disparar
        self.jugadorX = posicionAvionJugador[0]
        self.jugadorY = posicionAvionJugador[1]
        
        #Dirección
        self.direccionElegida = False
        self.dirX = 0
        self.dirY = 0 

        #Otros stats importantes
        self.sprite = stats[0]
        self.speed = stats[1]

        # self.estadoDisparo = False
        self.alive = True

    def update(self):
        '''La posición del jugador determina la DIRECCIÓN del disparo del enemigo'''
        
        if self.y > 256 or self.y < 0:
            self.alive = False
            
        if self.alive:
            if not self.direccionElegida:
                if self.x < 256 and self.jugadorX > self.x:
                    self.dirX = 1
                elif self.x > 0 and self.jugadorX < self.x:
                    self.dirX = 2
                elif self.x == self.jugadorX:
                    self.dirX = 3
                if self.y > self.jugadorY:
                    self.dirY = 1
                self.direccionElegida = True
            
            if self.dirX == 1: #1: Derecha 
                self.x += self.speed//2
            elif self.dirX == 2: #2: Izquierda 
                self.x -= self.speed//2
            elif self.dirX == 3: #3: Recto
                self.x += 0
            if self.dirY == 0: #Abajo
                self.y += self.speed*2
            else: #Arriba
                self.y -= self.speed*2

    def draw(self):
        self.blt = (self.x,  self.y, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], self.sprite[4])