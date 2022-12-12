class Explosion:
    def __init__(self, x, y, sprites: list, caracteristicasAnimacion = None):
        
        #Posición
        self.x = x
        self.y = y

        self.alive = True

        #Variables auxiliares para la animación
        self.indiceSprite = 0 #Determina la posición del sprite de la lista
        self.frames = 0 #Frames que han pasado
        self.spritesExplosion = sprites
        self.caracteristicasAnimacion = caracteristicasAnimacion
        self.longitudEntreFrames = self.caracteristicasAnimacion[0] #Intervalo entre sprites
        self.transparencia = self.caracteristicasAnimacion[1] #Si la transparencia es True genera un efecto intermitente
        self.esAnimacionMuerteJugador = self.caracteristicasAnimacion[2] #Nos permite discriminar en el board si la animación es por la muerte del jugador o no
    
    @property
    def caracteristicasAnimacion(self):
        return self.__caracteristicasAnimacion

    @caracteristicasAnimacion.setter
    def caracteristicasAnimacion(self, caracteristicasAnimacion):
        if caracteristicasAnimacion == None:
            self.__caracteristicasAnimacion = [2, True, False]
        else:
            self.__caracteristicasAnimacion = caracteristicasAnimacion
            
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
    
