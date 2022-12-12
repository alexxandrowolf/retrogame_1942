import pyxel
import random 
import config
from avionlocal import AvionJugador
from enemigo_regular import EnemigoRegular
from super_bombardero import SuperBombardero
from enemigoRojo import EnemigoRojo
from explosionMadre import Explosion
from proyectilEnemigo import DisparoEnemigo
from bonus import BonusEnemigoRojo
from bombardero import Bombardero

class App:
    def __init__(self):

        self.PANTALLA = config.PANTALLA

        '''
        Estas variables nos permiten gestionar los 3 "menús" que existen en el juego.
        Mientras que self.start es "False" se muestra por pantalla el menú de inicio. Al pulsar "s"
        se inicia la partida (el display de los menús es controlado con estos booleanos).
        Cada vez que el jugador muere mostramos un interludio básico que consiste en dos textos.
        Y finalmente, cundo self.gameover es "True" se activa la pantalla de muerte en el que se muestran
        todas las estadísticas de la partida. Al pulsar "x" vuelves al menú principal.
        '''

        self.start = False
        self.interludio = True
        self.gameover = False
        
        '''
        PuntuaciónAuxiliar nos va a ayudar a gestionar la puntuación. En nuestro videojuego cada vez
        que matas a un enemigo te suma en un contador interno del jugador el número de enemigos a los que has derrotado
        
        Cada enemigo tiene asociada una puntuación de modo, que cuando existe una colisión entre el disparo
        del jugador y el enemigo este suma al jugador su puntuación. Sin embargo, existen dos enemigos especiales:
        el bombardero y el superbombardero que requieren de variables auxiliares para ir sumando fracciones de
        puntuación cada vez que reciben disparos. Cuando estos enemigos pierden toda la vida, entonces
        si esta variable auxiliar y la puntuación asociada al bombardero son iguales le suma la puntuación
        al jugador.

        Por último, el High Score se establece como si buscáramos un máximo.
        '''

        '''
        AnimaciónAcabadaAuxiliar nos permite comprobar cuando la animación de explosión del jugador
        ha acabado para así poder ejecutar su "reset" (explicado más adelante) 
        '''

        # self.puntuacionAuxiliar = 0 #Variable auxiliar para contabilizar la puntuacion del superbombardero
        # self.puntuacionAuxiliar2 = 0  #Variable auxiliar para contabilizar la puntuación del bombardero
        self.resetearPuntuacion = True
        self.animacionAcabadaAuxiliar = False

        '''
        Las variables que se encuentran a continuación permiten controlar el bonus que recibe el jugador
        al matar una oleada de enemigos rojos. Si enemigosRojosDerrotado es igual al número de enemigos
        rojos por oleada (5) se activa el bonusEnemigoRojo y se crea un objeto Bonus.

        El objeto bonus es posicionado y elegido aleatoriamente. Existen tres tipos de bonus:
        --> "Estrella": da inmunidad al jugador
        --> "FatMan": elimina a todos los enemigos de la pantalla
        --> "ProyectilChetado": cambia el proyectil del jugador por uno con mayor superficie
        '''
        self.enemigosRojosDerrotados = 0
        self.bonusEnemigoRojo = False
        self.bonusJugador = []
        self.disparoChetado = False

        self.avion = []
        self.avion.append(AvionJugador(config.NAVE_JUGADOR, config.STATS_NAVE_JUGADOR))

        '''
        Creamos las listas en las que vamos a almacenar: enemigos, explosiones, disparos.
        La idea es tener dos listas en "paralelo". Por un lado, el "update" va recorriendo las listas
        todo el tiempo, de modo que si encuentra un objeto en ella va a ejecutar su lógica.
        Por otro lado, las listas en el "draw" funcionan igual que en el update pero lo que ejecuta es el "display" en la pantalla.
        '''

        self.enemigosRegulares = []
        
        self.enemigosRojos = []

        self.bombarderos = []
 
        self.super_bombarderos = []

        self.explosiones = []

        self.disparos = []
 
        
        pyxel.init(self.PANTALLA[0],self.PANTALLA[1]) #Definimos el alto y el ancho de nuestra pantalla
        pyxel.run(self.update,self.draw)
        

    def update(self):
        if pyxel.btn(pyxel.KEY_Q): #Establecemos que al pulsar la tecla Q se salga del juego
            pyxel.quit()
        
        if not self.start:
            self.explosiones.clear()
            if pyxel.btn(pyxel.KEY_S):
                self.start = True
                if self.resetearPuntuacion:
                    for avion in self.avion: #Resetear el número de enemigos derrotados
                        avion.rojo = 0
                        avion.regular = 0
                        avion.bombardero = 0
                        avion.superbombardero = 0
                    self.resetearPuntuacion = False
        if self.gameover:
            if pyxel.btn(pyxel.KEY_X):
                self.gameover = False
                self.start = False
                self.resetearPuntuacion = True
        
        if self.interludio or self.gameover:
            #Eliminamos a todos los enemigos para que cuando reaparezca el jugador no haya ninguno
            self.enemigosRegulares.clear()
            self.enemigosRojos.clear()
            self.bombarderos.clear()
            self.super_bombarderos.clear()
            self.explosiones.clear()
            self.bonusJugador.clear()
            self.disparos.clear()

        if self.start and not self.gameover:
            '''En esta parte del código escribimos lo que se va a ejecutar durante la partida. Las teclas de movimiento, que llaman
            al método move del avión principal, (también establecemos que si no se pulsa ninguna tecla, ejecute move sin ningún parámetro,
            lo cual es útil para las animaciones de movimiento, como veremos en el propio método). Por otro lado tenemos que al pulsar la
            tecla espacio ejecute el método disparar del avión, y que al pulsar la tecla z ejecute el método hacer_voltereta del avión.
            '''            
            for avion in self.avion:
                if pyxel.btn(pyxel.KEY_LEFT):
                    avion.move("left")
                if pyxel.btn(pyxel.KEY_RIGHT):
                    avion.move("right")
                if pyxel.btn(pyxel.KEY_UP):
                    avion.move("up")
                if pyxel.btn(pyxel.KEY_DOWN):
                    avion.move("down")
                pyxel.btn(pyxel.KEY_LEFT)
                if not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_DOWN) and not pyxel.btn(pyxel.KEY_UP):
                    avion.move()
                if pyxel.btnp(pyxel.KEY_SPACE) and not avion.voltereta and avion.alive:
                    avion.disparar(self.disparoChetado)
                if pyxel.btnp(pyxel.KEY_Z) and not avion.voltereta and avion.numeroVolteretas > 0:
                    avion.numeroVolteretas -= 1
                    avion.contador_voltereta = 0
                    avion.voltereta = True
                if avion.voltereta:
                    avion.hacer_voltereta()

            #Duración de los textos que se muestran en el interludio
            if pyxel.frame_count % 125 == 0:
                self.interludio = False
            
            #Controlamos que cada vez que aparezcan los enemigos rojos su contador para el bonus se restablezca
            if pyxel.frame_count % 300 == 0:
                self.enemigosRojosDerrotados = 0

            #Controlamos si matan a nuestro avión, así como sus disparos
            for avion in self.avion:
                if not avion.alive and self.animacionAcabadaAuxiliar:
                    self.animacionAcabadaAuxiliar = False
                    avion.reset()
                    if avion.respawn == 0:
                        avion.gameover()
                        self.gameover = True
                    else:
                        self.interludio = True
                    

                if avion.animacionMuerte:
                    avion.animacionMuerte = False
                    self.explosiones.append(Explosion(avion.x + avion.sprite[3]//2, avion.y + avion.sprite[4]//2, config.SPRITES_EXPLOSION_POR_COLISION, config.CARACTERISTICAS_EXPLOSION_JUGADOR))
                    avion.alive = False
            
            for avion in self.avion:
                for disparo in avion.disparos:
                    disparo.update()
                    if not disparo.alive:
                        avion.disparos.pop(avion.disparos.index(disparo))

            #Establecemos la periodicidad con la que los enemigos van a aparecer
            if pyxel.frame_count % 200000 == 0:
                for i in range(random.randint(2, 5)):
                    lado = random.randint(0,1)
                    if lado == 0:
                        self.enemigosRegulares.append(EnemigoRegular([config.ENEMIGO_REGULAR_DIMENSIONES_1, [random.randint(-30,20), random.randint(-300,-10)]]))
                    else:
                        self.enemigosRegulares.append(EnemigoRegular([config.ENEMIGO_REGULAR_DIMENSIONES_1, [random.randint(230,280), random.randint(-300,-10)]]))
           
            if pyxel.frame_count % 300 == 0:
                for i in range(0, 5):
                    self.enemigosRojos.append(EnemigoRojo([config.ROJO_DCHA_LOOP, [-30 - (i * 40), 40]]))

            if pyxel.frame_count % 200 == 0:
                self.bombarderos.append(Bombardero([config.BOMBARDERO_DIMENSIONES_ABAJO, [60, -50]]))

            if pyxel.frame_count % 500000 == 0:
                self.super_bombarderos.append(SuperBombardero([config.SUPER_BOMBARDERO_DIMENSIONES ,config.POSICION_SB], [20,-1,-1,True, 100]))

            #Super bombardero
            for sb in self.super_bombarderos:
                if sb.alive:
                    sb.move()
                    sb.disparar()
                
                if not sb.alive:
                    sb.morir()

                if sb.contador_muerte == 2:
                    for avion in self.avion:
                        avion.superbombardero += 1
                        avion.puntuacion += sb.puntuacion

                if not sb.alive and len(sb.disparos) == 0 and sb.contador_muerte >= 209:
                    self.super_bombarderos.pop(self.super_bombarderos.index(sb))

                for avion in self.avion:
                    for disparo in avion.disparos:
                        if self.colisiones(disparo, sb) and sb.alive:
                            disparo.alive = False
                            sb.perderVida2()
                            
                    
                for avion in self.avion:
                    if self.colisiones(avion, sb) and sb.alive and not avion.voltereta and avion.alive:
                        sb.disparos.clear()
                        sb.perderVida2()
                        avion.perderVida()
                        
                
                for disparo in sb.disparos:
                    if disparo.x > 260 or disparo.x < -8 or disparo.y > 260:
                        sb.disparos.pop(sb.disparos.index(disparo))
                    
                    disparo.update()
                    
                    for avion in self.avion:
                        if self.colisiones(avion, disparo) and not avion.voltereta:
                            disparo.alive = False
                            avion.perderVida()
            #Bombardero
            for bombardero in self.bombarderos:
                if bombardero.alive:
                    bombardero.move()
                
                for avion in self.avion:
                    disparoRandom = random.randint(1,100)    
                    if disparoRandom == 1:
                        self.disparos.append(DisparoEnemigo([bombardero.x + bombardero.sprite[3]//3, bombardero.y + bombardero.sprite[4]//2], [avion.x, avion.y], config.PROYECTIL_SB))
                
                if bombardero.animacionMuerte:
                    self.explosiones.append(Explosion(bombardero.x + bombardero.sprite[3]//2, bombardero.y + bombardero.sprite[4]//2, config.SPRITES_EXPLOSION_BOMBARDERO, config.CARACTERISTICAS_EXPLOSION_BOMBARDERO))
                    bombardero.alive = False 

                for avion in self.avion:
                    if self.colisiones(bombardero, avion) and not avion.voltereta and avion.alive:
                        avion.perderVida()
                        bombardero.perderVida()

                if not bombardero.alive:
                    if bombardero.health == 0:
                        for avion in self.avion:
                            avion.bombardero += 1
                            avion.puntuacion += bombardero.puntuacion
                    self.bombarderos.pop(self.bombarderos.index(bombardero))

            #Enemigo Regular
            for enemigo in self.enemigosRegulares:
                for avion in self.avion:    
                    if enemigo.y + 45 >= avion.y: 
                        enemigo.giro()
                    if self.colisiones(enemigo, avion) and not avion.voltereta and avion.alive:
                        avion.perderVida()
                        enemigo.perderVida()
                if enemigo.y <= -20 and enemigo.contador_giro != 0:
                    enemigo.alive = False
                
                for avion in self.avion:
                    disparoRandom = random.randint(1,100)    
                    if disparoRandom == 1:
                        self.disparos.append(DisparoEnemigo([enemigo.x + enemigo.sprite[3]//2, enemigo.y + enemigo.sprite[4]//2], [avion.x, avion.y], config.PROYECTIL_SB))
               
                enemigo.moverse()        

                if enemigo.animacionMuerte:
                    self.explosiones.append(Explosion(enemigo.x + enemigo.sprite[3]//2, enemigo.y + enemigo.sprite[4]//2, config.SPRITES_EXPLOSION_POR_DISPARO))
                    enemigo.alive = False  
                
                if not enemigo.alive:
                    if enemigo.health <= 0:
                        for avion in self.avion:
                            avion.puntuacion += enemigo.puntuacion
                            avion.regular += 1
                    self.enemigosRegulares.pop(self.enemigosRegulares.index(enemigo))
                
            #Enemigo Rojo
            for enemigo in self.enemigosRojos:

                enemigo.moverse()

                for avion in self.avion:
                    if self.colisiones(enemigo, avion) and not avion.voltereta and avion.alive:
                            avion.perderVida()
                            enemigo.perderVida()

                if enemigo.animacionMuerte:
                    self.explosiones.append(Explosion(enemigo.x + enemigo.sprite[3]//2, enemigo.y + enemigo.sprite[4]//2, config.SPRITES_EXPLOSION_POR_DISPARO))
                    enemigo.alive = False 
                
                if not enemigo.alive:
                    if enemigo.health <= 0:
                        for avion in self.avion:
                            avion.puntuacion += enemigo.puntuacion
                            avion.rojo += 1
                    self.enemigosRojos.pop(self.enemigosRojos.index(enemigo))
                        
            #Lógica de la explosión
            for explosion in self.explosiones:
                if explosion.alive:
                    explosion.update()
                else:
                    if explosion.esAnimacionMuerteJugador:
                        self.animacionAcabadaAuxiliar = True
                    self.explosiones.pop(self.explosiones.index(explosion))

            #Lógica de las Disparos de los enemigos
            for disparo in self.disparos:
                if disparo.alive:
                    disparo.update()
                else:
                    self.disparos.pop(self.disparos.index(disparo))

            '''
            Nuestro sistema de colisiones (la lógica de colisión está contenida en el método colisiones)
            está basado en el sistema de dos dimensiones AABB comprueba si existe una intersección entre
            dos objetos a partir de comparar sus [x] e [y] máximas y mínimas.
            '''

            #A) Entre balas y enemigosRegulares
            for enemigo in self.enemigosRegulares:
                for avion in self.avion:
                    for disparo in avion.disparos:
                        if self.colisiones(disparo, enemigo):
                            disparo.alive = False
                            enemigo.perderVida()

            for enemigo in self.enemigosRojos:
                for avion in self.avion:
                    for disparo in avion.disparos:
                        if self.colisiones(disparo, enemigo):
                            self.enemigosRojosDerrotados += 1
                            disparo.alive = False
                            enemigo.perderVida()

            for enemigo in self.bombarderos:
                for avion in self.avion:
                    for disparo in avion.disparos:
                        if self.colisiones(disparo, enemigo):
                            disparo.alive = False
                            enemigo.perderVida()

            #B) Entre balas enemigas y nuestro avion
            for disparo in self.disparos:
                for avion in self.avion:
                    if self.colisiones(disparo, avion) and not avion.voltereta:
                        disparo.alive = False
                        avion.perderVida()

            #C) Entre el avión del jugador y el bonus
            for avion in self.avion:
                for bonus in self.bonusJugador:
                    if self.colisiones(avion, bonus):
                        bonus.activado = True


            #Construimos la lógica de los bonus
            if self.enemigosRojosDerrotados == 5: 
                self.enemigosRojosDerrotados = 0
                self.bonusEnemigoRojo = True
                self.bonusJugador.append(BonusEnemigoRojo(random.randint(25, 225), random.randint(85, 225), random.randint(0,2)))

            for bonus in self.bonusJugador:
                if bonus.activado:
                    if bonus.devolverTipoBonus() == "estrella":
                        for avion in self.avion:
                            avion.health = 1000000
                            for sb in self.super_bombarderos:
                                sb.health = 1
                            for bombardero in self.bombarderos:
                                bombardero.health = 1
                    elif bonus.devolverTipoBonus() == "proyectilChetado":
                        self.disparoChetado = True
                    else:
                        for avion in self.avion:
                            for enemigo in self.enemigosRegulares:
                                # avion.regular += 1
                                # avion.puntuacion += enemigo.puntuacion
                                enemigo.health = 0
                                enemigo.animacionMuerte = True
                                
                            for enemigo in self.enemigosRojos:
                                # avion.rojo += 1
                                # avion.puntuacion += enemigo.puntuacion
                                enemigo.health = 0
                                enemigo.animacionMuerte = True
                            
                            for bombardero in self.bombarderos:
                                bombardero.health = 0
                                bombardero.animacionMuerte = True
                                
                            for sb in self.super_bombarderos:
                                sb.health = 0
                                sb.alive = False
                                                        
                    bonus.duracionBonus() #Cuando el bonus está activado tiene una duración determinada
                else:
                    bonus.duracionDisplayBonusEnPantalla()

                if not bonus.alive:
                    for avion in self.avion:
                        avion.health = 1
                    self.disparoChetado = False
                    for sb in self.super_bombarderos:
                        sb.health = 20
                    for bombardero in self.bombarderos:
                        bombardero.health = 5
                    self.bonusJugador.pop(self.bonusJugador.index(bonus))

    def draw(self):
        if not self.gameover:
            #CAPA **0**
            pyxel.load("assets/fondo.pyxres")
            pyxel.cls(12)
            
            isla1_x = -500 + (pyxel.frame_count % (pyxel.height + 1300))
            isla2_x = -1200 + (pyxel.frame_count % (pyxel.height + 1300)) #Definimos cuándo van a aparecer las islas y con qué frecuencia
            
            pyxel.blt(0, isla1_x, 0, 0, 0, 101, 151, colkey=0)
            pyxel.blt(pyxel.width - 131, isla2_x, 0, 124, 0, 131, 126, colkey=0) 
            
            pyxel.text(5, 5,"HIGH SCORE:", col=7)
            pyxel.text(5, 15, "SCORE:", col=7)
            pyxel.text(200, 5,"VOLTERETAS:", col=7)
            pyxel.text(220, 15,"VIDAS:", col=7)

            for avion in self.avion:
                pyxel.text(60, 5, str(avion.highScore), col=7)
                pyxel.text(40, 15, str(avion.puntuacion), col=7)
                pyxel.text(245, 5, str(avion.numeroVolteretas), col=7)
                pyxel.text(245, 15, str(avion.respawn), col=7)

        if not self.start and not self.gameover:
            self.pantallaInicio()
        
        if self.gameover:
            self.pantallaGameover()

        #CAPA **1**
        if self.start and not self.gameover:
            # pyxel.pal()
            pyxel.load("assets/avionPlayersyOtros.pyxres")

            for avion in self.avion:
                if avion.alive:
                    avion.drawAvion()
                    pyxel.blt(*avion.blt, colkey = 8)

            
            for sb in self.super_bombarderos:
                if sb.alive or sb.contador_muerte < 630: 
                    sb.drawAvion()
                    pyxel.blt(*sb.blt, colkey = 7)
                for disparo in sb.disparos: 
                    disparo.draw()
                    pyxel.blt(*disparo.blt, colkey=7)
            
            
            for avion in self.avion:
                for disparo in avion.disparos:
                    disparo.draw()
                    pyxel.blt(*disparo.blt, colkey=8)

            for bombardero in self.bombarderos:
                if bombardero.alive:
                    bombardero.drawAvion()
                    pyxel.blt(*bombardero.blt, colkey=7)        
            
            for enemigo in self.enemigosRegulares:
                enemigo.drawAvion()
                pyxel.blt(*enemigo.blt, colkey = 8)


            for enemigo in self.enemigosRojos:
                enemigo.drawAvion()
                pyxel.blt(*enemigo.blt, colkey = 7)
        
            
            for disparo in self.disparos:
                disparo.draw()
                pyxel.blt(*disparo.blt, colkey=7)


            #Aquí se pintan las hélices
            for avion in self.avion:
                if avion.alive:
                    if pyxel.frame_count % 2 == 0 and (avion.sprite == config.AVION_JUGADOR_SPRITE or avion.sprite == config.AVION_JUGADOR_SPRITE_LEFT_1 or avion.sprite == config.AVION_JUGADOR_SPRITE_RIGHT_1):
                        pyxel.rect(avion.x+5, avion.y+2, 3, 1, col=4)
                        pyxel.rect(avion.x+9, avion.y+2, 3, 1, col=10)
                        pyxel.rect(avion.x+15, avion.y+2, 3, 1, col=10)
                        pyxel.rect(avion.x+19, avion.y+2, 3, 1, col=4)
                    if pyxel.frame_count % 2 == 0 and avion.sprite == config.AVION_JUGADOR_SPRITE_LEFT_2:
                        pyxel.rect(avion.x+4, avion.y+2, 3, 1, col=4)
                        pyxel.rect(avion.x+8, avion.y+2, 2, 1, col=10)
                        pyxel.rect(avion.x+13, avion.y+2, 3, 1, col=10)
                        pyxel.rect(avion.x+17, avion.y+2, 3, 1, col=4)
                    if pyxel.frame_count % 2 == 0 and avion.sprite == config.AVION_JUGADOR_SPRITE_LEFT_3:
                        pyxel.rect(avion.x+3, avion.y+2, 3, 1, col=4)
                        pyxel.rect(avion.x+8, avion.y+2, 1, 1, col=10)
                        pyxel.rect(avion.x+10, avion.y+2, 3, 1, col=10)
                        pyxel.rect(avion.x+14, avion.y+2, 3, 1, col=4)    
                    if pyxel.frame_count % 2 == 0 and avion.sprite == config.AVION_JUGADOR_SPRITE_RIGHT_2:
                        pyxel.rect(avion.x+5, avion.y+2, 3, 1, col=4)
                        pyxel.rect(avion.x+9, avion.y+2, 3, 1, col=10)
                        pyxel.rect(avion.x+15, avion.y+2, 2, 1, col=10)
                        pyxel.rect(avion.x+18, avion.y+2, 3, 1, col=4)    
                    if pyxel.frame_count % 2 == 0 and avion.sprite == config.AVION_JUGADOR_SPRITE_RIGHT_3:
                        pyxel.rect(avion.x+4, avion.y+2, 3, 1, col=4)
                        pyxel.rect(avion.x+8, avion.y+2, 3, 1, col=10)
                        pyxel.rect(avion.x+13, avion.y+2, 1, 1, col=10)
                        pyxel.rect(avion.x+15, avion.y+2, 3, 1, col=4) 

            for enemigo in self.enemigosRegulares:
                if pyxel.frame_count % 2 == 0 and enemigo.sprite == config.ENEMIGO_REGULAR_DIMENSIONES_1:
                    pyxel.rect(enemigo.x+5, enemigo.y+14, 3, 1, col=10)
                    pyxel.rect(enemigo.x+9, enemigo.y+14, 3, 1, col=12)
                if pyxel.frame_count % 2 == 0 and enemigo.sprite == config.ENEMIGO_REGULAR_DIMENSIONES_5:
                    pyxel.rect(enemigo.x+5, enemigo.y+1, 3, 1, col=10)
                    pyxel.rect(enemigo.x+9, enemigo.y+1, 3, 1, col=13)    
                    
            for bombardero in self.bombarderos:
                if pyxel.frame_count % 2 == 0 and bombardero.sprite == config.BOMBARDERO_DIMENSIONES_ABAJO:
                    pyxel.rect(bombardero.x + 8, bombardero.y + 20, 3, 1, col=4)
                    pyxel.rect(bombardero.x+ 12, bombardero.y + 20, 3, 1, col=10)
                    pyxel.rect(bombardero.x+ 18, bombardero.y + 20, 3, 1, col=10)
                    pyxel.rect(bombardero.x+ 22, bombardero.y + 20, 3, 1, col=4)

                if pyxel.frame_count % 2 == 0 and bombardero.sprite == config.BOMBARDERO_DIMENSIONES_DERECHA:
                    pyxel.rect(bombardero.x + 21, bombardero.y + 7, 2, 1, col=4)
                    pyxel.rect(bombardero.x+ 21, bombardero.y + 10, 2, 1, col=10)
                    pyxel.rect(bombardero.x+ 21, bombardero.y + 17, 2, 1, col=10)
                    pyxel.rect(bombardero.x+ 21, bombardero.y + 20, 2, 1, col=4)

            for sb in self.super_bombarderos:
                if pyxel.frame_count % 2 == 0 and sb.alive:
                    pyxel.rect(sb.x + 17, sb.y + 9, 4, 1, col=4)
                    pyxel.rect(sb.x+ 22, sb.y + 9, 4, 1, col=10)
                    pyxel.rect(sb.x+ 39, sb.y + 9, 4, 1, col=10)
                    pyxel.rect(sb.x+ 44, sb.y + 9, 4, 1, col=4)

            #Dibujamos las explosiones
            for explosion in self.explosiones:
                explosion.draw()
                pyxel.blt(*explosion.blt, colkey=7)
            
            #Dibujamos los bonuses
            for bonus in self.bonusJugador:
                if self.bonusEnemigoRojo and not bonus.activado:
                    pyxel.blt(bonus.x, bonus.y, *bonus.sprite, colkey=8)
                if bonus.activado and bonus.devolverTipoBonus() == "estrella":
                    pyxel.pal(13, pyxel.frame_count % 16)
                else:
                    pyxel.pal()

            if self.interludio:
                self.pantallaEntreMuertes()         
    
    
    def colisiones(self, objeto1, objeto2):
        
        if (objeto1.x + objeto1.sprite[3] - 1  > objeto2.x 
            and objeto2.x + objeto2.sprite[3] - 1  > objeto1.x # Comprobamos intersección en el eje [x]
            and objeto1.y + objeto1.sprite[4] - 1 > objeto2.y #Comprobamos intersección en el eje [y]
            and objeto2.y + objeto2.sprite[4] - 1 > objeto1.y):
            return True

    def pantallaInicio(self):
        pyxel.load("assets/titulo.pyxres")
        pyxel.pal()
        pyxel.pal(15, pyxel.frame_count % 16)

        pyxel.blt(16, 64, *config.UNO, colkey=7)
        pyxel.blt(60, 64, *config.NUEVE, colkey=7)
        pyxel.blt(118, 64, *config.CUATRO, colkey=7)
        pyxel.blt(182, 64, *config.DOS, colkey=7)

        pyxel.text(108, 180, "PRESIONA S", col=15)

        pyxel.load("assets/avionPlayersyOtros.pyxres")
        pyxel.blt(96, 220, 1,4,37,64,15)

    def pantallaEntreMuertes(self):
        pyxel.text(95, 40,"BATALLA DE MIDWAY", col=7)
        pyxel.text(73, 50, "¡DESTRUYE A TODOS PARA GANAR!", col=7)

    def pantallaGameover(self):
        pyxel.cls(12)
        pyxel.pal(15, pyxel.frame_count%16)
        pyxel.text(100, 50, "G A M E  O V E R", col=8)
        pyxel.text(75, 80, "TOTAL SCORE:", col=7)
        pyxel.text(180, 80, str(self.avion[0].puntuacionFinal), col=7)

        pyxel.text(75, 90,"HIGHEST SCORE:", col=7)
        pyxel.text(180, 90, str(self.avion[0].highScore), col=7)

        pyxel.text(75, 100, "ENEMIGOS ABATIDOS:", col=7)
        
        pyxel.text(75, 110, "ENEMIGOS REGULARES",col=7)
        pyxel.text(180, 110, str(self.avion[0].regular), col=7)

        pyxel.text(75, 120, "ENEMIGOS ROJOS",col=7)
        pyxel.text(180, 120, str(self.avion[0].rojo), col=7)

        pyxel.text(75, 130, "ENEMIGOS BOMBARDERO",col=7)
        pyxel.text(180, 130, str(self.avion[0].bombardero), col=7)

        pyxel.text(75, 140, "ENEMIGOS SUPERBOMBARDERO",col=7)
        pyxel.text(180, 140, str(self.avion[0].superbombardero), col=7)
        
        pyxel.text(80, 240, "PRESIONA X PARA CONTINUAR", col=15)                
App()