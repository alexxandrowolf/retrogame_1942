import config
'''Clase de los bonus que sueltan los enemigos rojos al morir'''
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
    
    '''
    Esta función se utiliza en board para comprobar que tipo de bonus se ha escogido
    '''

    def devolverTipoBonus(self):
        return self.bonus

    '''
    Esta función determina cuanto tiempo permanece activo el bonus tras que el jugador lo coja.
    También tiene especificado que en el caso de la bomba solo dure un frame para que solo tenga
    efecto en ese momento.
    '''

    def duracionBonus(self):        
        if self.devolverTipoBonus() == "fatMan" and self.contador == 1:
            self.contador = 200
        if self.contador == 200: #El bonus activado tiene una duración de 200 frames
            self.alive = False
        self.contador += 1
    
    '''
    Por último, esta función determina el tiempo que va a estar en bonus en la pantalla, si pasa
    ese tiempo y el jugador no colisiona con el bonus este desaparecerá.
    '''

    def duracionDisplayBonusEnPantalla(self):
        if not self.activado:
            if self.contador_2 == 150: #Si el bonus no se activa desaparece a los 150 frames
                self.alive = False
            self.contador_2 += 1