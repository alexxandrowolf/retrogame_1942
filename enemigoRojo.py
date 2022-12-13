import config
import pyxel
from avionMadre import Avion
'''La clase de los enemigos rojos, que recibe herencia de la clase madre Avion'''
class EnemigoRojo(Avion):
    def __init__(self, nave: list, stats = None):
        super().__init__(nave, stats)
        self.looping = False
                
        self.contadorAngulos = 0
        
        self.X_looping = 0
        self.Y_looping = 0
        
        self.primerLoopingCompletado = False

    '''
    Los enemigos Rojos trazan su trayectoria a partir de funciones trigonométricas:
    A través de self.X_Looping y self.y_Looping determinamos que alrededor de un punto (x, y) a través
    de un contador que representa ángulos, se le pone como parámetro a la función coseno (abcisa) y
    la función seno (ordenada) de modo, estos atributos van cambiando realizando una circunferencia.

    Luego simplemente indicamos al avión que se aproxime a esas coordenadas y dependiendo del ángulo
    en el que se encuentre se le asigna un sprite u otro. En la práctica no realiza una circunferencia
    como tal sino un cuadrado, esto se debe a que como pyxel no reconoce valores reales, nuestro aviones
    lograban realizar una circunferencia perfecta pero generaban un efecto visual feo.
    '''
    def moverse(self):
        if not self.looping:
            self.x += self.speed
            if self.x > 256:
                self.alive = False
            if self.x == 60 or self.x == 180:
                self.looping = True
        else:
            if self.contadorAngulos == 360:
                self.looping = False
                self.primerLoopingCompletado = True
                self.contadorAngulos = 0
                self.sprite = config.ROJO_DCHA_LOOP
            else:
                if not self.primerLoopingCompletado:
                    self.X_looping = int(round(60 + pyxel.cos(self.contadorAngulos)*50))
                else:
                    self.X_looping = int(round(180 + pyxel.cos(self.contadorAngulos)*50))

                self.Y_looping = int(round(50 + pyxel.sin(self.contadorAngulos)*50))

                if self.contadorAngulos < 60:  
                    self.sprite = config.ROJO_360_GRADOS
                elif self.contadorAngulos < 85:
                    self.sprite = config.ROJO_ENTRANDO
                elif self.contadorAngulos < 110:
                    self.sprite = config.ROJO_90_GRADOS
                elif self.contadorAngulos < 135:
                    self.sprite = config.ROJO_SALIENDO
                elif self.contadorAngulos < 200:
                    self.sprite = config.ROJO_180_GRADOS
                elif self.contadorAngulos < 225:
                    self.sprite = config.ROJO_SALIENDO
                elif self.contadorAngulos < 290:
                    self.sprite = config.ROJO_270_GRADOS
                elif self.contadorAngulos < 325:
                    self.sprite = config.ROJO_ENTRANDO
                elif self.contadorAngulos < 360:
                    self.sprite = config.ROJO_360_GRADOS
            
                if self.x < self.X_looping: 
                    self.direccionX = 1 
                elif self.x > self.X_looping:
                    self.direccionX = 2
                if self.y < self.Y_looping:
                    self.direccionY = 3
                elif self.y > self.Y_looping:
                    self.direccionY = 4

                if self.direccionX == 1: #Derecha
                    self.x += self.speed//2
                if self.direccionX == 2: #Izquierda
                    self.x -= self.speed//2
                if self.direccionY == 3: #Abajo
                    self.y += self.speed//2
                if self.direccionY == 4: #Arriba
                    self.y -= self.speed//2

                self.contadorAngulos += 2