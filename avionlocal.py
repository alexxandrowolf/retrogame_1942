import config
from proyectil import Proyectil
from avionMadre import Avion
#Creamos el avión que va a controlar el jugador.
class AvionJugador(Avion):
    def __init__(self, nave: list, stats = None):
        super().__init__(nave, stats)
        self.disparos = []
        self.contador_right = 0
        self.contador_left = 0
        self.contador_retorno = 0
        self.contador_voltereta = 0
        self.voltereta = False

        self.highScore = 0
        self.puntuacionFinal = 0

        self.respawn = 3
        self.rojo = 0
        self.regular = 0
        self.bombardero = 0
        self.superbombardero = 0
        

    def move(self, direction = "none"):
        if direction == "left":
            self.contador_retorno = 0
            self.contador_right = 0
            if self.x > 0:
                self.x -= self.speed
            if self.contador_left < 15:
                self.sprite = config.AVION_JUGADOR_SPRITE_LEFT_1
                self.contador_left += 2
            elif self.contador_left < 30:
                self.sprite = config.AVION_JUGADOR_SPRITE_LEFT_2 
                self.contador_left += 2  
            else:
                self.sprite = config.AVION_JUGADOR_SPRITE_LEFT_3
                self.contador_left += 2  
               
        if direction == "right":
            self.contador_retorno = 0
            self.contador_left = 0
            if self.x < self.SCREEN_WIDTH - self.sprite[3]:
                self.x += self.speed
            if self.contador_right < 15:
                self.sprite = config.AVION_JUGADOR_SPRITE_RIGHT_1
                self.contador_right += 2
            elif self.contador_right < 30:
                self.sprite = config.AVION_JUGADOR_SPRITE_RIGHT_2 
                self.contador_right += 2  
            else:
                self.sprite = config.AVION_JUGADOR_SPRITE_RIGHT_3
                self.contador_right += 2     
        if direction == "up":
            if self.y > 60:
                self.y -= self.speed
        if direction == "down":
            if self.y < self.SCREEN_HEIGHT- self.sprite[4]:
                self.y += self.speed
        if direction == "none":
            if self.contador_left >= 30:
                if self.contador_retorno < 20:
                    self.sprite = config.AVION_JUGADOR_SPRITE_LEFT_2
                    self.contador_retorno += 2
                elif self.contador_retorno < 40:
                    self.sprite = config.AVION_JUGADOR_SPRITE_LEFT_1 
                    self.contador_retorno += 2  
                else:
                    self.sprite = config.AVION_JUGADOR_SPRITE
                    self.contador_retorno += 2
                    self.contador_left = 0

            elif self.contador_left < 30 and self.contador_left >= 15:
                if self.contador_retorno < 20:
                    self.sprite = config.AVION_JUGADOR_SPRITE_LEFT_1 
                    self.contador_retorno += 2  
                else:
                    self.sprite = config.AVION_JUGADOR_SPRITE
                    self.contador_retorno += 2
                    self.contador_left = 0

            elif self.contador_left < 15 and self.contador_left != 0:
                self.sprite = config.AVION_JUGADOR_SPRITE
                self.contador_left = 0
        
            elif self.contador_right >= 30:
                if self.contador_retorno < 20:
                    self.sprite = config.AVION_JUGADOR_SPRITE_RIGHT_2
                    self.contador_retorno += 2
                elif self.contador_retorno < 40:
                    self.sprite = config.AVION_JUGADOR_SPRITE_RIGHT_1
                    self.contador_retorno += 2  
                else:
                    self.sprite = config.AVION_JUGADOR_SPRITE
                    self.contador_retorno += 2
                    self.contador_right = 0

            elif self.contador_right < 30 and self.contador_right >= 15:
                if self.contador_retorno < 20:
                    self.sprite = config.AVION_JUGADOR_SPRITE_RIGHT_1
                    self.contador_retorno += 2  
                else:
                    self.sprite = config.AVION_JUGADOR_SPRITE
                    self.contador_retorno += 2
                    self.contador_right = 0

            elif self.contador_right < 15 and self.contador_right != 0:
                self.sprite = config.AVION_JUGADOR_SPRITE
                self.contador_right = 0
        
        
        
        return self.x, self.y

    
    def disparar(self, disparoChetado):
        if not disparoChetado:
            self.disparos.append(Proyectil(self.x + 7, self.y - 2, config.PROYECTIL_JUGADOR)) #Encapsulación
        else:
            self.disparos.append(Proyectil(self.x + 7, self.y - 2, [config.PROYECTIL_CHETADO, 5]))
   
    def hacer_voltereta(self): 
        if self.contador_voltereta < 10:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_1
            self.contador_voltereta += 2
        elif self.contador_voltereta < 20:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_2
            self.contador_voltereta += 2       
        elif self.contador_voltereta < 30:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_3
            self.contador_voltereta += 2
        elif self.contador_voltereta < 40:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_4
            self.contador_voltereta += 2
        elif self.contador_voltereta < 50:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_5
            self.contador_voltereta += 2
        elif self.contador_voltereta < 60:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_6
            self.contador_voltereta += 2
        elif self.contador_voltereta < 70:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_7
            self.contador_voltereta += 2
        elif self.contador_voltereta < 80:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_8
            self.contador_voltereta += 2
        elif self.contador_voltereta < 90:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_9
            self.contador_voltereta += 2
        elif self.contador_voltereta < 100:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_10
            self.contador_voltereta += 2
        elif self.contador_voltereta < 110:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_11
            self.contador_voltereta += 2
        elif self.contador_voltereta < 120:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_12
            self.contador_voltereta += 2
        elif self.contador_voltereta < 130:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_13
            self.contador_voltereta += 2
        elif self.contador_voltereta < 140:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_14
            self.contador_voltereta += 2
        elif self.contador_voltereta < 150:
            self.sprite = config.AVION_JUGADOR_SPRITE_VOLTERETA_15
            self.contador_voltereta += 2
        else:
            self.sprite = config.AVION_JUGADOR_SPRITE
            self.voltereta = False 

    def reset(self):
        if self.puntuacion > self.highScore:
            self.highScore = self.puntuacion
        self.puntuacionFinal += self.puntuacion
        self.puntuacion = 0
        self.alive = True
        self.sprite = config.AVION_JUGADOR_SPRITE
        self.respawn -= 1
        self.health = 1
        self.x, self.y = config.POSICION[0], config.POSICION[1]
    
    def gameover(self):
        self.respawn = 3                                                                  
        

