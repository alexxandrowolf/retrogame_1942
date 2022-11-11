import pyxel

#Creamos el avión que va a controlar el jugador.
class AvionLocal():
    x: int
    y: int
    health: int
    damage: float
    
    def move(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            if self.x > 0:
                self.x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            if self.x < WIDTH:
                self.x += 1
        if pyxel.btn(pyxel.KEY_UP):
            if self.y > 0:
                self.y -= 1 
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.y < HEIGHT:
                self.y += 1

        return self.x, self.y
    
    def ataque():
        pass

WIDTH = 256
HEIGHT = 256