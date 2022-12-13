import config
from proyectilJugador import Proyectil
from avionMadre import Avion
'''Creamos el avión que va a controlar el jugador, que recibe herencia de la clase madre Avion.'''
class AvionJugador(Avion):
    def __init__(self, nave: list, stats = None):
        super().__init__(nave, stats)
        self.disparos = [] #La lista en la que se van a insertar los disparos del avión
        
        '''Los contadores que vamos a utilizar para iterar las animaciones del movimiento, uno para la animación hacia la izquierda, otro para la
        derecha, y otro para la animación de retorno, es decir, si el avión está inclinado hacia un lado, la animación para devolverlo a la posición
        original'''
        self.contador_right = 0
        self.contador_left = 0
        self.contador_retorno = 0
        
        '''Aquí establecemos los atributos para la voltereta: un contador para la animación; el número de volteretas, que disminuye según se usan;
        y el booleano que indica si se está realizando la voletereta (muy útil para las colisiones)'''
        self.contador_voltereta = 0
        self.numeroVolteretas = 3
        self.voltereta = False

        '''Los contadores de los puntos, tanto el HighScore como el actual'''
        self.highScore = 0
        self.puntuacionFinal = 0

        '''Las vidas que tiene el jugador antes de pasar a la pantalla Gameover'''
        self.respawn = 3
        
        '''Un contador para cada tipo de enemigo que se actualiza cuando los vamos eliminando'''
        self.rojo = 0
        self.regular = 0
        self.bombardero = 0
        self.superbombardero = 0
        

    '''La función move, que ejecuta el movimiento en función de la tecla que estemos pulsando. El valor que se introduce por parámetro viene definido
    por la tecla que estés pulsando. Si direccion es "left", el avión se mueve hacia la izquierda y reliza una animación de giro gracias al contador_left,
    que se reinicia cuando dejas de pulsar la tecla. Lo mismo pasa con la dirección right pero hacia la derecha. Hacia arriba y hacia abajo es más simple
    ya que no tiene animación. Tiene como valor por defecto "none", que se ejecuta siempre que no estemos pulsando ninguna tecla de movimiento. Este valor
    hace que si el avión ha dejado de ir hacia la izquierda o la derecha y tiene un sprite inclinado, vuelva a su sprite original. Para ello 
    determina si el contador izquierda o derecha es mayor que 0, y si es así dependiendo de su valor, va a realizar una animación de vuelta más larga
    o menos.'''
    
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
            '''Dependiendo del valor de contador_left o contador_right, realiza una animación con más sprites o menos'''
            
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

    
    '''La función disparar, que determina si el avión posee el bonus del disparo chetado o no, y en consecuencia inserta en la lista self.disparos
    un proyctil u otro'''
    
    def disparar(self, disparoChetado):
        if not disparoChetado:
            self.disparos.append(Proyectil(self.x + 7, self.y - 2, config.PROYECTIL_JUGADOR)) 
        else:
            self.disparos.append(Proyectil(self.x + 7, self.y - 2, [config.PROYECTIL_CHETADO, 5]))
   
    '''La función de hacer la voltereta, que como en el resto de animaciones, utiliza un contador para iterar cada sprite de la animación'''
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

    
    '''La función que resetea los stats del avión por cada vida que pierde'''
    def reset(self):
        if self.puntuacion > self.highScore:
            self.highScore = self.puntuacion
        self.puntuacionFinal += self.puntuacion
        self.puntuacion = 0
        self.sprite = config.AVION_JUGADOR_SPRITE
        self.numeroVolteretas = 3
        self.respawn -= 1
        self.health = 1
        self.alive = True
        self.x, self.y = config.POSICION[0], config.POSICION[1]
    
    '''La función que resetea las vidas del avión en caso de que las pierda todas y se inicie una nueva partida'''
    def gameover(self):
        self.respawn = 3                                                                  