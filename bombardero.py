import config
from avionMadre import Avion

'''La clase bombardero, que recibe herencia de la clase madre Avion'''
class Bombardero(Avion):
   def __init__(self, nave: list, stats: list = None):
        super().__init__(nave, stats)
        self.health = 5 #Establecemos la vida del bombardero
        
        self.puntuacion = 50 #La puntuación que el bombardero aporta al jugador al morir
        
        '''Contadores para el movimiento y la animación del avión'''
        self.contador = 0

   '''Establecemos el movimiento del bombardero, que al igual que el superbombardero va a ser fijo (nos habría gustado haber introducido algún patrón
   de movimiento más pero no hemos tenido tiempo). También se utilizan métodos de giro determinados, que siguen el mismo sistema que el superbomberdero'''
   def move(self):
      if self.contador < 140:
         self.y += 2
      
      elif self.contador < 185:
         self.giro_derecha_abajo(140)
      
      elif self.contador < 265:
         self.x += 2
         self.sprite = config.BOMBARDERO_DIMENSIONES_DERECHA

      elif self.contador < 310:
         self.giro_derecha_arriba(265)
      
      elif self.contador < 330:
         self.y -= 2
         self.sprite = config.BOMBARDERO_DIMENSIONES_ARRIBA
      
      elif self.contador < 375:
         self.giro_izquierda_arriba(330)

      elif self.contador < 455:
         self.x -= 2
         self.sprite = config.BOMBARDERO_DIMENSIONES_IZQUIERDA

      elif self.contador < 500:
         self.giro_izquierda_abajo(455)

      else: 
         self.y += 2
         self.sprite = config.BOMBARDERO_DIMENSIONES_ABAJO            

      self.contador += 2

      if self.y > 256:
         self.alive = False



   '''Los cuatro métodos siguientes se utilizan para que el bombardero haga los giros en el move. Se les introduce por parámetro el contador actual,
    para que se itere a partir de ese valor, y en cada intervalo los valores de x e y van variando, para así al final lograr el giro concreto que 
    queremos (igual que en el superbombardero)
   '''
   def giro_derecha_abajo(self, contador):
      if self.contador < contador + 15:
            self.y += 2
            self.x += 0.66
            self.sprite = config.BOMBARDERO_DERECHA_ABAJO_1 
      elif self.contador < contador + 30:
            self.y += 1.32
            self.x += 1.32
            self.sprite = config.BOMBARDERO_DERECHA_ABAJO_2 
      elif self.contador < contador + 45:
            self.y += 0.66
            self.x += 2
            self.sprite = config.BOMBARDERO_DERECHA_ABAJO_3 


   def giro_derecha_arriba(self, contador):
      if self.contador < contador + 15:
            self.y -= 0.66
            self.x += 2
            self.sprite = config.BOMBARDERO_DERECHA_ARRIBA_1
      elif self.contador < contador + 30:
            self.y -= 1.32
            self.x += 1.32
            self.sprite = config.BOMBARDERO_DERECHA_ARRIBA_2
      elif self.contador < contador + 45:
            self.y -= 2
            self.x += 0.66
            self.sprite = config.BOMBARDERO_DERECHA_ARRIBA_3

   def giro_izquierda_arriba(self, contador):
      if self.contador < contador + 15:
            self.y -= 2
            self.x -= 0.66
            self.sprite = config.BOMBARDERO_IZQUIERDA_ARRIBA_1
      elif self.contador < contador + 30:
            self.y -= 1.32
            self.x -= 1.32
            self.sprite = config.BOMBARDERO_IZQUIERDA_ARRIBA_2
      elif self.contador < contador + 45:
            self.y -= 0.66
            self.x -= 2
            self.sprite = config.BOMBARDERO_IZQUIERDA_ARRIBA_3

   def giro_izquierda_abajo(self, contador):
      if self.contador < contador + 15:
            self.y += 0.66
            self.x -= 2
            self.sprite = config.BOMBARDERO_IZQUIERDA_ABAJO_1
      elif self.contador < contador + 30:
            self.y += 1.32
            self.x -= 1.32
            self.sprite = config.BOMBARDERO_IZQUIERDA_ABAJO_2
      elif self.contador < contador + 45:
            self.y += 2
            self.x -= 0.66
            self.sprite = config.BOMBARDERO_IZQUIERDA_ABAJO_3      