class Proyectil():
    def __init__(self, x: int, y: int, proyectilStats: list): #x, y serán la posicion desde donde tira el avion
        self.x = x
        self.y = y
        self.sprite = proyectilStats[0]
        self.speed = proyectilStats[1]
        self.alive = True
    
    def update(self):
        if self.y > -10:
            self.y -= self.speed
        if self.y <= -10:
            self.alive = False    
        
    def draw(self):
        self.blt = (self.x, self.y, self.sprite[0],self.sprite[1], self.sprite[2], self.sprite[3], self.sprite[4])