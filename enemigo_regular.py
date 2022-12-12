import config
from avionMadre import Avion
import random

class EnemigoRegular(Avion):
    def __init__(self, nave: list, stats = None):
        super().__init__(nave, stats)
        self.limite = random.randint(48, 188)
        self.girar = False
        self.contador_giro = 0
        self.direccionRandomX = random.randint(0,1)
        self.x_inicial = self.x


    def moverse(self):
        if self.x_inicial < 60:
            if not self.girar:
                self.x += 1
                self.y += 3
            else:
                if self.contador_giro < 30:
                    self.giro_derecha()
                else:
                    self.x += 1
                    self.y -= 3
                    self.sprite = config.ENEMIGO_REGULAR_DIMENSIONES_5
        else:
            if not self.girar:
                self.x -= 1
                self.y += 3
            else:
                if self.contador_giro < 30:
                    self.giro_izquierda()
                else:
                    self.x -= 1
                    self.y -= 3
                    self.sprite = config.ENEMIGO_REGULAR_DIMENSIONES_5                    

            
    def giro(self):
        self.girar = True
    
    def giro_derecha(self):
        if self.contador_giro < 10:
            self.contador_giro += 2
            self.x += 1
            self.y += 1
            self.sprite = config.ENEMIGO_REGULAR_DIMENSIONES_2
        elif self.contador_giro < 20:
            self.contador_giro += 2
            self.x += 1
            self.sprite = config.ENEMIGO_REGULAR_DIMENSIONES_3
        elif self.contador_giro < 30:
            self.contador_giro += 2
            self.x += 1
            self.y -= 1
            self.sprite = config.ENEMIGO_REGULAR_DIMENSIONES_4

    def giro_izquierda(self):
        if self.contador_giro < 10:
            self.contador_giro += 2
            self.x -= 1
            self.y += 1
            self.sprite = config.ENEMIGO_REGULAR_DIMENSIONES_2
        elif self.contador_giro < 20:
            self.contador_giro += 2
            self.x -= 1
            self.sprite = config.ENEMIGO_REGULAR_DIMENSIONES_3
        elif self.contador_giro < 30:
            self.contador_giro += 2
            self.x -= 1
            self.y -= 1
            self.sprite = config.ENEMIGO_REGULAR_DIMENSIONES_4        
            
            

             


    
