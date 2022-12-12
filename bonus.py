import config
class BonusEnemigoRojo:
    def __init__(self, x, y, indiceBonus: int):
        self.x = x
        self.y = y
        self.alive = True
        self.activado = False
        self.contador = 0
        self.contador_2 = 0
        self.posiblesBonus = [config.ESTRELLA, config.PROYECTIL_CHETADO, config.FAT_MAN]
        self.sprite = self.posiblesBonus[indiceBonus]
        self.bonus = ""

        if indiceBonus == 0:
            self.bonus = "estrella"
        elif indiceBonus == 1:
            self.bonus = "proyectilChetado"
        else: 
            self.bonus = "fatMan"
    
    def devolverTipoBonus(self):
        return self.bonus

    def duracionBonus(self):
        if self.contador == 200: #El bonus activado tiene una duración de 200 frames
            self.alive = False
        self.contador += 1
    
    def duracionDisplayBonusEnPantalla(self):
        if not self.activado:
            if self.contador_2 == 150: #Si el bonus no se activa desaparece a los 150 frames
                self.alive = False
            self.contador_2 += 1
    