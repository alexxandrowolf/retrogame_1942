import config
from avionMadre import Avion
from proyectil_sb import ProyectilSb

class SuperBombardero(Avion):
    '''Realizamos herencia para que el superbombardero reciba los mismos métodos de la clase Avion, al igual que los atributos del init tal como
    nave, stats...
    '''
    
    def __init__(self, nave: list, stats: list = None):

        super().__init__(nave, stats)
        self.health = 20
        self.puntuacion = 100
        self.disparos = []
        self.contador = 0
        self.contador_muerte = 0
        

    def move(self):
        if self.y <= -100:  #Establecemos que si el superbombardero sale del mapa su self.alive pase a False
            self.alive = False

        #A partir de aquí, utilizamos contadores que se actualizan cada frame para hacer el movimiento

        if self.contador < 290:
            self.y -= 2
        
        elif self.contador < 380:
            self.x -= 2
        
        elif self.contador < 470: 
            self.giro_izquierda_abajo(380)
        
        elif self.contador < 560:
            self.giro_derecha_abajo(470)     
        
        elif self.contador < 600:
            self.x += 1
        
        elif self.contador < 690:
            self.giro_derecha_arriba(600)
            
        elif self.contador < 730:
            self.x += 1
        
        elif self.contador < 820:
            self.giro_derecha_abajo(730)
        
        elif self.contador < 910:
            self.giro_derecha_arriba(820)    

        elif self.contador < 1000:
            self.giro_izquierda_arriba(910)

        else:
            self.y -= 1

        self.contador += 2

    '''Los cuatro métodos siguientes se utilizan para que el bombardero haga los giros en el move. Se les introduce por parámetro el contador actual,
    para que se itere a partir de ese valor, y en cada intervalo los valores de x e y van variando, para así al final lograr el giro concreto que 
    queremos
    '''
    
    def giro_izquierda_abajo(self, contador):
        if self.contador < contador + 15:
            self.y += 0.16
            self.x -= 1    
        elif self.contador < contador + 30:
            self.y += 0.32
            self.x -= 0.84    
        elif self.contador < contador + 45:
            self.y += 0.48
            self.x -= 0.68    
        elif self.contador < contador + 60:
            self.y += 0.64
            self.x -= 0.52    
        elif self.contador < contador + 75:
            self.y += 0.80
            self.x -= 0.36    
        elif self.contador < contador + 90:
            self.y += 1
            self.x -= 0.20    
    def giro_derecha_abajo(self, contador):
        if self.contador < contador + 15:
            self.y += 1
            self.x += 0.16
        elif self.contador < contador + 30:
            self.y += 0.84
            self.x += 0.32
        elif self.contador < contador + 45:
            self.y += 0.68
            self.x += 0.48
        elif self.contador < contador + 60:
            self.y += 0.52
            self.x += 0.64
        elif self.contador < contador + 75:
            self.y += 0.36
            self.x += 0.80
        elif self.contador < contador + 90:
            self.y += 0.20
            self.x += 1
    
    def giro_derecha_arriba(self,contador):
        if self.contador < contador + 15:
            self.y -= 0.16
            self.x += 1
        elif self.contador < contador + 30:
            self.y -= 0.32
            self.x += 0.84
        elif self.contador < contador + 45:
            self.y -= 0.48
            self.x += 0.68
        elif self.contador < contador + 60:
            self.y -= 0.64
            self.x += 0.52
        elif self.contador < contador + 75:
            self.y -= 0.80
            self.x += 0.36
        elif self.contador < contador + 90:
            self.y -= 1
            self.x += 0.16
    def giro_izquierda_arriba(self, contador):
        if self.contador < contador + 15:
            self.y -= 1
            self.x -= 0.16
        elif self.contador < contador + 30:
            self.y -= 0.84
            self.x -= 0.32
        elif self.contador < contador + 45:
            self.y -= 0.68
            self.x -= 0.48
        elif self.contador < contador + 60:
            self.y -= 0.52
            self.x -= 0.64
        elif self.contador < contador + 75:
            self.y -= 0.36
            self.x -= 0.80
        elif self.contador < contador + 90:
            self.y -= 0.20
            self.x -= 1

    
    def disparar(self):
        #Primera ráfaga
        if self.contador == 312:
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 1, 3))
        elif self.contador == 316:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 0, 3))
        elif self.contador == 320:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, -1, 3))
        
        #Segunda ráfaga
        elif self.contador == 470:
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 1, 3))
        elif self.contador == 474:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 2, 3))
        elif self.contador == 478:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 3, 3))
               
        
        #Tercera ráfaga
        elif self.contador == 600:
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 1, 3))
        elif self.contador == 604:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 0, 3))
        elif self.contador == 608:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, -1, 3))
        
        #Cuarta ráfaga
        elif self.contador == 730:
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 1, 3))
        elif self.contador == 734:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, 0, 3))
        elif self.contador == 738:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, -1, 3)) 

        #Quinta ráfaga
        elif self.contador == 910:
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, -1, 3))
        elif self.contador == 914:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, -2, 3))
        elif self.contador == 918:    
            self.disparos.append(ProyectilSb(self.x + 30, self.y + 30, config.PROYECTIL_SB, -3, 3))

    def morir(self):
        if self.contador_muerte < 10:
            self.sprite = config.SB_MUERTE_1 
        elif self.contador_muerte < 20:
            self.sprite = config.SB_MUERTE_2_5 
        elif self.contador_muerte < 30:
            self.sprite = config.SB_MUERTE_3_6 
        elif self.contador_muerte < 40:
            self.sprite = config.SB_MUERTE_4_7 
        elif self.contador_muerte < 50:
            self.sprite = config.SB_MUERTE_2_5 
        elif self.contador_muerte < 60:
            self.sprite = config.SB_MUERTE_3_6 
        elif self.contador_muerte < 70:
            self.sprite = config.SB_MUERTE_4_7 
        elif self.contador_muerte < 80:
            self.sprite = config.SB_MUERTE_8 
        elif self.contador_muerte < 90:
            self.sprite = config.SB_MUERTE_9 
        elif self.contador_muerte < 100:
            self.sprite = config.SB_MUERTE_10 
        elif self.contador_muerte < 110:
            self.sprite = config.SB_MUERTE_11 
        elif self.contador_muerte < 120:
            self.sprite = config.SB_MUERTE_12 
        elif self.contador_muerte < 130:
            self.sprite = config.SB_MUERTE_13 
        elif self.contador_muerte < 140:
            self.sprite = config.SB_MUERTE_14 
        elif self.contador_muerte < 150:
            self.sprite = config.BOMBARDERO_EXPLOSION_VI 
        elif self.contador_muerte < 160:
            self.sprite = config.BOMBARDERO_EXPLOSION_I
        elif self.contador_muerte < 170:
            self.sprite = config.BOMBARDERO_EXPLOSION_VI
        elif self.contador_muerte < 180:
            self.sprite = config.BOMBARDERO_EXPLOSION_I
        elif self.contador_muerte < 190:
            self.sprite = config.BOMBARDERO_EXPLOSION_II
        elif self.contador_muerte < 200:
            self.sprite = config.BOMBARDERO_EXPLOSION_III
        elif self.contador_muerte < 210:
            self.sprite = config.BOMBARDERO_EXPLOSION_IV
        self.contador_muerte += 2