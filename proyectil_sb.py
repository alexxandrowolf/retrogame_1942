class ProyectilSb():
    def __init__(self, x: int, y: int, proyectilStats: list, dir_x : int, dir_y : int): #x, y serán la posicion desde donde tira el avion
        self.x = x
        self.y = y
        self.sprite = proyectilStats[0]
        self.speed = proyectilStats[1]
        self.alive = True
        self.dir_x = dir_x
        self.dir_y = dir_y
        

    def update(self):
        self.x += self.dir_x

        self.y += self.dir_y
        
    def draw(self):
        self.blt = (self.x, self.y, self.sprite[0],self.sprite[1], self.sprite[2], self.sprite[3], self.sprite[4])

        

