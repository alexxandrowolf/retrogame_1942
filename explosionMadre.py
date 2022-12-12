class Explosion:
    def __init__(self, x, y, longitudEntreFrames: int, transparencia: bool, esAnimacionMuerteJugador:bool, sprites: list):
        
        #Posición
        self.x = x
        self.y = y

        self.alive = True

        #Variables auxiliares para la animación
        self.indiceSprite = 0 #Determina la posición del sprite de la lista
        self.frames = 0 #Frames que han pasado
        self.spritesExplosion = sprites
        self.longitudEntreFrames = longitudEntreFrames #Intervalo entre sprites
        self.transparencia = transparencia #Si la transparencia es True genera un efecto intermitente
        self.esAnimacionMuerteJugador = esAnimacionMuerteJugador #Nos permite discriminar en el board si la animación es por la muerte del jugador o no

    def update(self):
        
        if self.frames == 0:
            self.indiceSprite = 0
        elif self.frames == self.longitudEntreFrames:
            self.indiceSprite = 1
        elif self.frames == self.longitudEntreFrames*2:
            self.indiceSprite = 2
        elif self.frames == self.longitudEntreFrames*3:
            self.indiceSprite = 3
        elif self.frames == self.longitudEntreFrames*4:
            self.indiceSprite = 4
        elif self.frames == self.longitudEntreFrames*5:
            self.indiceSprite = 5
        elif self.frames == self.longitudEntreFrames*6:
            self.alive = False
        elif self.transparencia:
            self.indiceSprite = 6
        self.frames += 1

    def draw(self):
        self.blt = (self.x, self.y, *self.spritesExplosion[self.indiceSprite])