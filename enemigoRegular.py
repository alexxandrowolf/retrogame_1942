import config
from avionMadre import Avion
import random
'''La clas del enemigo regular, que recibe herencia de la clase madre Avion'''
class EnemigoRegular(Avion):
    def __init__(self, nave: list, stats = None):
        super().__init__(nave, stats)
        
        self.girar = False #Booleano que sirve para decirle al objeto si tiene que girar o no
        self.contador_giro = 0 #Contador para establecer la animación de giro
        
        self.x_inicial = self.x #La posición inicial del avión al crearse en el eje x


    '''La función moverse va a realizar un movimiento u otro dependiendo de la posición inicial en la que el objeto sea generado. Si es generado a la 
    izquierda, el objeto empezará moviéndose hacia abajo y a la derecha, y si es generado a la derecha irá hacia abajo y a la izquierda. En el momento
    en el que el enemigo se acerca mucho a la posición del avión jugador en el eje x, self.girar pasa a True, y el avión pasa de ir hacia abajo a ir
    hacia arriba con una pequeña animación, que dependerá de si gira hacia la izquierda o hacia la derecha'''
    
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
    
    '''Las funciones de giro, que son iguales que las de los bombarderos y superbombarderos, a través de un contador se va variando la velocidad del 
    avión en el eje x y la del eje y, logrando el giro deseado'''
    
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