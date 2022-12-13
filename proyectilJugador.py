'''Clase del proyectil que dispara el jugador. Se añaden por parámetro la posición del avión del jugador y los stats del avión (el sprite y la 
velocidad)'''
class Proyectil():
    def __init__(self, x: int, y: int, proyectilStats: list): #x, y serán la posicion desde donde tira el avion
        self.x = x
        self.y = y
        
        self.sprite = proyectilStats[0]
        self.speed = proyectilStats[1]
        
        self.alive = True
    
    '''En el update del proyectil la posición del eje y va disminuyendo (en función de la velocidad) hasta que sale de la pantalla, momento en que
    self.alive pasa a False y se elimina'''
    
    def update(self):
        if self.y > -10:
            self.y -= self.speed
        if self.y <= -10:
            self.alive = False    
        
    '''Método que establece el atributo blt para pintarse posteriormente en el método draw de board'''
    def draw(self):
        self.blt = (self.x, self.y, self.sprite[0],self.sprite[1], self.sprite[2], self.sprite[3], self.sprite[4])