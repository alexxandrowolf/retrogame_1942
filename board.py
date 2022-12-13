import pyxel
import random 
import config
from avionLocal import AvionJugador
from enemigoRegular import EnemigoRegular
from superBombardero import SuperBombardero
from enemigoRojo import EnemigoRojo
from explosion import Explosion
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

        self.avion = AvionJugador(config.NAVE_JUGADOR, config.STATS_NAVE_JUGADOR)

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
                    #Resetear el número de enemigos derrotados
                    self.avion.rojo = 0
                    self.avion.regular = 0
                    self.avion.bombardero = 0
                    self.avion.superbombardero = 0
                    self.resetearPuntuacion = False
        
        '''Si el atributo respawn del avión se hace 0 (es decir, las vidas que tiene el jugador), self.gameover pasa a True, y el juego entra en la
        pantalla de GameOver, en la que te pone las estadísticas de tu partida y en la que si pulsas la tecla x, vuelves a la pantalla inicial'''
        
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
            
            if pyxel.btn(pyxel.KEY_LEFT):
                self.avion.move("left")
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.avion.move("right")
            if pyxel.btn(pyxel.KEY_UP):
                self.avion.move("up")
            if pyxel.btn(pyxel.KEY_DOWN):
                self.avion.move("down")
            pyxel.btn(pyxel.KEY_LEFT)
            if not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_DOWN) and not pyxel.btn(pyxel.KEY_UP):
                self.avion.move()
            if pyxel.btnp(pyxel.KEY_SPACE) and not self.avion.voltereta and self.avion.alive:
                self.avion.disparar(self.disparoChetado)
            if pyxel.btnp(pyxel.KEY_Z) and not self.avion.voltereta and self.avion.numeroVolteretas > 0:
                self.avion.numeroVolteretas -= 1
                self.avion.contador_voltereta = 0
                self.avion.voltereta = True
            if self.avion.voltereta:
                self.avion.hacer_voltereta()

            #Duración de los textos que se muestran en el interludio
            if pyxel.frame_count % 125 == 0:
                self.interludio = False

            #Controlamos si matan a nuestro avión, así como sus disparos
            if not self.avion.alive and self.animacionAcabadaAuxiliar:
                self.animacionAcabadaAuxiliar = False
                self.avion.reset()
                if self.avion.respawn == 0:
                    self.avion.gameover()
                    self.gameover = True
                else:
                    self.interludio = True

            '''Cuando se ejecuta el metodo del avion perderVida y se hace 0, animacionMuerte pasa a ser True y activa esta condición. Lo que hace es 
            insertar un objeto de la clase Explosion a la lista self.explosiones de board, justo en la posición en la que ha muerto el jugador. Este 
            objeto lo único que hace es una animación de explosión, antes de desaparecer. Además, establece el alive del avión a False'''

            if self.avion.animacionMuerte:
                self.avion.animacionMuerte = False
                self.explosiones.append(Explosion(self.avion.x + self.avion.sprite[3]//2, self.avion.y + self.avion.sprite[4]//2, config.SPRITES_EXPLOSION_POR_COLISION, config.CARACTERISTICAS_EXPLOSION_JUGADOR))
                self.avion.alive = False

            '''Cuando pulsamos la tecla espacio y se ejecuta el método disparar del avión, en la lista disparos (atributo del avión), se inserta
            un objeto proyectil. Este bucle for se recorre constantemente esta lista, haciendo posible que los misiles del avion se muevan e interactúen
            correctamente con el resto de enemigos. Cuando disparo.alive se hace False (ya sea por que sale de la pantalla o por que colisiona con
            algún enemigo), simplemente se borra ese proyectil de la lista'''
            
            for disparo in self.avion.disparos:
                disparo.update()
                if not disparo.alive:
                    self.avion.disparos.pop(self.avion.disparos.index(disparo))

            '''En este apartado simplemente establecemos cada cuántos frames va a aparecer cada enemigo, utilizando el pyxel.frame_count e insertando 
            el número deseado de enemigos en su lista correspondiente. Los enemigos regulares aparecen cada 200 frames, los enemigos rojos cada 600,
            los bombarderos medianos cada 700, y los superbombarderos cada 1250.'''
            #Enemigos Regulares
            if pyxel.frame_count % 100 == 0:
                for i in range(random.randint(2, 5)):
                    lado = random.randint(0,1)
                    if lado == 0:
                        self.enemigosRegulares.append(EnemigoRegular([config.ENEMIGO_REGULAR_DIMENSIONES_1, [random.randint(-30,20), random.randint(-300,-10)]]))
                    else:
                        self.enemigosRegulares.append(EnemigoRegular([config.ENEMIGO_REGULAR_DIMENSIONES_1, [random.randint(230,280), random.randint(-300,-10)]]))
           
            '''Los enemigos rojos aparecen de cinco en cinco. Aprovechamos el bucle for para hacer que cada uno aparezca más a la izquierda que el
            anterior, con la idea de que no aparezcan los cinco en la misma posición'''
            
            #Enemigos Rojos
            if pyxel.frame_count % 600 == 0:
                self.enemigosRojosDerrotados = 0 
                for i in range(0, 5):
                    self.enemigosRojos.append(EnemigoRojo([config.ROJO_DCHA_LOOP, [-30 - (i * 40), 40]]))

            #Bombardero
            if pyxel.frame_count % 400 == 0:
                self.bombarderos.append(Bombardero([config.BOMBARDERO_DIMENSIONES_ABAJO, [60, -50]]))

            #Superbombardero
            if pyxel.frame_count % 1000 == 0:
                self.super_bombarderos.append(SuperBombardero([config.SUPER_BOMBARDERO_DIMENSIONES ,config.POSICION_SB], [20,-1,-1,True, 100]))

            '''En el sigguiente bucle for establecemos la lógica del superbombardero. si su atributo alive es True, se ejecutan los métodos move
            y disparar, y si es False se ejecuta el método morir. Si su atributo contador_muerte es igual a 2, significa que el avión ha sido eliminado
            por el jugador, por lo que se le suma a las estadísticas del jugador. Otra implementación es que cuando el enemigo elimina al superbombardero,
            no se elimina inmediatamente, si no que espera a que se ejecute la animación de muerte, y a que los disparos hayan salido de la pantalla, ya 
            que si no se eliminarían también los disparos, pues estos pertenecen al objeto (por supuesto mientras ocurre la animación no existen colisiones
            con el jugador). También se elimina si posicion_muerte es True, que significa que el supercombardero ha salido de la pantalla. Por último se 
            establecen las colisiones entre las balas del bombardero y el jugador, entre el propio bombardero y el jugador, y entre las balas del jugador y
            el bombardero, con sus respectivas pérdidas de salud y desapariciones de los disparos (para las colisiones utilizamos un método general que se 
            explica más abajo)'''

            #Super bombardero
            for sb in self.super_bombarderos:
                if sb.alive:
                    sb.move()
                    sb.disparar()
                
                if not sb.alive:
                    sb.morir()

                if sb.contador_muerte == 2:
                    self.avion.superbombardero += 1
                    self.avion.puntuacion += sb.puntuacion

                if (not sb.alive and len(sb.disparos) == 0 and sb.contador_muerte >= 209) or sb.posicion_muerte:
                    self.super_bombarderos.pop(self.super_bombarderos.index(sb))

                for disparo in self.avion.disparos:
                    if self.colisiones(disparo, sb) and sb.alive:
                        disparo.alive = False
                        sb.perderVida2()
                            
                    
                if self.colisiones(self.avion, sb) and sb.alive and not self.avion.voltereta and self.avion.alive:
                    sb.disparos.clear()
                    sb.perderVida2()
                    self.avion.perderVida()
                        
                
                for disparo in sb.disparos:
                    if disparo.x > 260 or disparo.x < -8 or disparo.y > 260:
                        sb.disparos.pop(sb.disparos.index(disparo))
                    
                    disparo.update()
                    
                    if self.colisiones(self.avion, disparo) and not self.avion.voltereta:
                        disparo.alive = False
                        self.avion.perderVida()
            
            '''En el caso del bombardero mediano, el disparo es diferente, ya que no son disparos prefijados como en el superbombardero. Se realizan de manera
            aleatoria, con una posibilidad de 1 entre 100 (que por cada frame no es tan poco como parece). Para disparar, en la lista disparos (atributo 
            de board), se inserta un objeto DisparoEnemigo, en el que se introduce por parámetro por un lado la posición del bombardero, y por otro lado
            la posición del avión del jugador, para que el disparo vaya en una dirección que tenga sentido y no vaya en sentidos extraños. Cuando la 
            vida del bombardero se reduce a 0, animacionMuerte pasa a True y además de eliminarse el objeto, ocurre la animación de la explosión como
            ya se ha explicado'''
            
            #Bombardero
            for bombardero in self.bombarderos:
                if bombardero.alive:
                    bombardero.move()
                
                disparoRandom = random.randint(1,100)    
                if disparoRandom == 1:
                    self.disparos.append(DisparoEnemigo([bombardero.x + bombardero.sprite[3]//3, bombardero.y + bombardero.sprite[4]//2], [self.avion.x, self.avion.y], config.PROYECTIL_SB))
            
                if bombardero.animacionMuerte:
                    self.explosiones.append(Explosion(bombardero.x + bombardero.sprite[3]//2, bombardero.y + bombardero.sprite[4]//2, config.SPRITES_EXPLOSION_BOMBARDERO, config.CARACTERISTICAS_EXPLOSION_BOMBARDERO))
                    bombardero.alive = False 

                if self.colisiones(bombardero, self.avion) and not self.avion.voltereta and self.avion.alive:
                    self.avion.perderVida()
                    bombardero.perderVida()

                if not bombardero.alive:
                    if bombardero.health == 0:
                        self.avion.bombardero += 1
                        self.avion.puntuacion += bombardero.puntuacion
                    self.bombarderos.pop(self.bombarderos.index(bombardero))

            '''En los enemigos regulares, su movimiento predeterminado es en diagonal hacia abajo, y según si ha aparecido por la izquierda o por la 
            derecha irá en un sentido o en otro. Sin embargo, cuando se acerca demasiado al avión del jugador, cambia su driección y vuelve hacia arriba,
            con su animación correspondiente. Se estableven las colisiones y el disparo, que será el mismo que el del bombardero. La muerte también seguirá
            el mismo método que el bombardero.
            '''
            
            #Enemigo Regular
            for enemigo in self.enemigosRegulares:
                if enemigo.y + 45 >= self.avion.y: 
                    enemigo.giro()
                
                if self.colisiones(enemigo, self.avion) and not self.avion.voltereta and self.avion.alive:
                    self.avion.perderVida()
                    enemigo.perderVida()
                
                if enemigo.y <= -20 and enemigo.contador_giro != 0:
                    enemigo.alive = False
                
                disparoRandom = random.randint(1,100)    
                if disparoRandom == 1:
                    self.disparos.append(DisparoEnemigo([enemigo.x + enemigo.sprite[3]//2, enemigo.y + enemigo.sprite[4]//2], [self.avion.x, self.avion.y], config.PROYECTIL_SB))
            
                enemigo.moverse()        

                if enemigo.animacionMuerte:
                    self.explosiones.append(Explosion(enemigo.x + enemigo.sprite[3]//2, enemigo.y + enemigo.sprite[4]//2, config.SPRITES_EXPLOSION_POR_DISPARO))
                    enemigo.alive = False  
                
                if not enemigo.alive:
                    if enemigo.health <= 0:
                        self.avion.puntuacion += enemigo.puntuacion
                        self.avion.regular += 1
                    self.enemigosRegulares.pop(self.enemigosRegulares.index(enemigo))
                
            '''Los enemigos rojos no disparan, simplemente se mueven en círculos y sueltan un bonus cuando son eliminados todos ellos (la lógica de los 
            bonus se explica más adelante). Las colisiones y su animación de muerte se realiza de la misma forma que en los dos casos anterores'''
            
            #Enemigo Rojo
            for enemigo in self.enemigosRojos:

                enemigo.moverse()

                if self.colisiones(enemigo, self.avion) and not self.avion.voltereta and self.avion.alive:
                        self.avion.perderVida()
                        enemigo.perderVida()

                if enemigo.animacionMuerte:
                    self.explosiones.append(Explosion(enemigo.x + enemigo.sprite[3]//2, enemigo.y + enemigo.sprite[4]//2, config.SPRITES_EXPLOSION_POR_DISPARO))
                    enemigo.alive = False 
                
                if not enemigo.alive:
                    if enemigo.health <= 0:
                        self.avion.puntuacion += enemigo.puntuacion
                        self.avion.rojo += 1
                    self.enemigosRojos.pop(self.enemigosRojos.index(enemigo))
                        
            '''Aquí viene determinada la lógica de la explosión. Cuando matas a un enemigo e introduces el objeto Explosion en la lista, este for se la
            recorre y la ejecuta. Si explosion.alive es True, simplemente se ejecuta la animacion. Cuando se acaba pasa a False, y en el caso de que esa
            explosion sea la del jugador, esAnimacionMuerteJugador sería True, y daría paso al interludio o a la pantalla de gameover en caso de tener 0
            vidas. En caso de ser la explosion de un avion cualquiera, simplemente la explosion se elimina de la lista al acabar la animación'''
            for explosion in self.explosiones:
                if explosion.alive:
                    explosion.update()
                else:
                    if explosion.esAnimacionMuerteJugador:
                        self.animacionAcabadaAuxiliar = True
                    self.explosiones.pop(self.explosiones.index(explosion))

            '''Lógica de los disparos enemigos, se mueven hasta que chocan con el avión del jugador o hasta que salen de la pantalla, momento en el que
            son eliminados de la lista'''
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

            #Entre balas del jugador y enemigosRegulares
            for enemigo in self.enemigosRegulares:
                for disparo in self.avion.disparos:
                    if self.colisiones(disparo, enemigo):
                        disparo.alive = False
                        enemigo.perderVida()

            #Entre balas del jugador y enemigos rojos
            for enemigo in self.enemigosRojos:
                for disparo in self.avion.disparos:
                    if self.colisiones(disparo, enemigo):
                        self.enemigosRojosDerrotados += 1
                        disparo.alive = False
                        enemigo.perderVida()

            #Entre balas del jugador y bombarderos medianos
            for enemigo in self.bombarderos:
                for disparo in self.avion.disparos:
                    if self.colisiones(disparo, enemigo):
                        disparo.alive = False
                        enemigo.perderVida()

            #Entre balas enemigas y nuestro avion
            for disparo in self.disparos:
                if self.colisiones(disparo, self.avion) and not self.avion.voltereta:
                    disparo.alive = False
                    self.avion.perderVida()

            #Entre el avión del jugador y el bonus
            for bonus in self.bonusJugador:
                if self.colisiones(self.avion, bonus):
                    bonus.activado = True


            '''En este apartado se ejevuta la lógica de los bonus. Primero tenemos la aparición del bonus, que se realiza cuando el jugador mata a 
            los cinco aviones rojo de una misma oleada. Cuando esto ocurre, se inserta un objeto BonusEnemigoRojo en una posición aleatoria de la 
            pantalla que puede ser de tres tipos. Uno es muy parecido a la estrella del Mario Bros, te hace inmune a los enemigos y hace que si te 
            chocas con ellos los elimines al instante. Otro te da un proyectil más ancho, que es útil para fallar menos balas. Y el último es una 
            bomba nuclear que elimina a todos los enemigos que haya en pantalla instantáneamente.'''
            
            if self.enemigosRojosDerrotados == 5: 
                self.enemigosRojosDerrotados = 0
                self.bonusEnemigoRojo = True
                self.bonusJugador.append(BonusEnemigoRojo(random.randint(25, 225), random.randint(85, 225), random.randint(0,2)))

            for bonus in self.bonusJugador:
                if bonus.activado:
                    if bonus.devolverTipoBonus() == "estrella":
                        self.avion.health = 1000000 # Tu vida se hace infinita y la vida del resto pasa a ser 1, para que cuando colisiones con ellos se eliminen
                        for sb in self.super_bombarderos:
                            sb.health = 1
                        for bombardero in self.bombarderos:
                            bombardero.health = 1
                    elif bonus.devolverTipoBonus() == "proyectilChetado":
                        self.disparoChetado = True # disparoChetado True activa el disparo más ancho
                    else:
                        for enemigo in self.enemigosRegulares: # Elimina a todo tipo de enemigos que haya en pantalla
                            enemigo.health = 0
                            enemigo.animacionMuerte = True
                            
                        for enemigo in self.enemigosRojos:
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
                    bonus.duracionDisplayBonusEnPantalla() #Cuando todavía no se ha recogiso el bonus también tiene una duración en pantalla determinada

                if not bonus.alive: #Cuando se acaba el bonus, todos los stats vuelven a sus valores estándar y el bonus se elimina de la lista
                    self.avion.health = 1
                    self.disparoChetado = False
                    for sb in self.super_bombarderos:
                        sb.health = 20
                    for bombardero in self.bombarderos:
                        bombardero.health = 5
                    self.bonusJugador.pop(self.bonusJugador.index(bonus))

    def draw(self):
        '''En el draw, lo primero que se pinta es la pantalla inicial. En ella, el fondo es el mismo que en el juego, un azul marino que simula el
        océano, y también se pueden ver las islas, que van apareciendo de forma periódica a medida que pasa el tiempo. Además, aparece el título del
        juego, y si pulsas la tecla S el juego se inicia'''
        
        if not self.gameover:
            #CAPA **0**
            pyxel.load("assets/fondo.pyxres") #Cargamos el archivo pyxres que contiene los sprites de las islas que aparecen de fondo
            pyxel.cls(5)
            
            isla1_x = -500 + (pyxel.frame_count % (pyxel.height + 1300))
            isla2_x = -1200 + (pyxel.frame_count % (pyxel.height + 1300)) #Definimos cuándo van a aparecer las islas y con qué frecuencia
            
            pyxel.blt(0, isla1_x, 0, 0, 0, 101, 151, colkey=0)
            pyxel.blt(pyxel.width - 131, isla2_x, 0, 124, 0, 131, 126, colkey=0) 
            
            if not self.start and not self.gameover:
                self.pantallaInicio()    
            
            if self.start:
                pyxel.text(5, 5,"HIGH SCORE:", col=7)
                pyxel.text(5, 15, "SCORE:", col=7)
                pyxel.text(200, 5,"VOLTERETAS:", col=7)
                pyxel.text(220, 15,"VIDAS:", col=7)

                pyxel.text(60, 5, str(self.avion.highScore), col=7)
                pyxel.text(40, 15, str(self.avion.puntuacion), col=7)
                pyxel.text(245, 5, str(self.avion.numeroVolteretas), col=7)
                pyxel.text(245, 15, str(self.avion.respawn), col=7)
        
        if self.gameover: #Si el avión pierde todas sus vidas se ejecuta este método
            self.pantallaGameover()

        '''Una vez que se inicia el juego, se pinta lo que es la partida. Se pinta el avión del jugador, con sus respectivas animaciones de giro.
        Se pintan los enemigos, siempre recorriendo bucles for, y pintando el sprite correspondiente a la animación que el objeto esté realizando.
        También se pintan todos los disparos, tanto de los enemigos como los nuestros, y las explosiones. Para pintar todos los objetos simplemente 
        hacemos pyxel.blt al atributo blt de cada objeto, en el que se encuentran todos los parámetros para que el sprite se pinte correctamente 
        (importante añadir el asterisco antes de cada blt, para que se introduzca cada valor de la lista por separado; y el colkey, para eliminar el
        fondo indeseado de los sprites'''
        
        #CAPA **1**
        if self.start and not self.gameover:
            # pyxel.pal()
            pyxel.load("assets/avionPlayersyOtros.pyxres") #Cargamos el archivo pyxres en el que están los sprites de los aviones las explosiones

            if self.avion.alive:
                self.avion.drawAvion()
                pyxel.blt(*self.avion.blt, colkey = 8)

            
            for sb in self.super_bombarderos:
                if sb.alive or sb.contador_muerte < 630: #El contador_muerte lo utilizamos para que el superbombardero se pinte hasta que su animación de muerte haya acabado
                    sb.drawAvion()
                    pyxel.blt(*sb.blt, colkey = 7)
                for disparo in sb.disparos: 
                    disparo.draw()
                    pyxel.blt(*disparo.blt, colkey=7)
            
            for disparo in self.avion.disparos:
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


            '''En este apartado se pintan las hélices de los aviones, tanto las del jugador como de los enemigos. El sistema es simple, donde se encuentran
            las hélices de los sprites, se dibujan de manera intermitente cuatro rayas, que al aparecer y desaparecer tan rápido, dan la sensación de que
            son dos hélices girando. Ha quedado bastante largo y repetitivo, pero no hemos encontrado forma de simplificarlo ya que para cada sprite de cada 
            animación de cada avión hay que pintar las hélices en posiciones diferentes y de longitudes diferentes'''
            
            #Para el avión del jugador
            if self.avion.alive: 
                if pyxel.frame_count % 2 == 0 and (self.avion.sprite == config.AVION_JUGADOR_SPRITE or self.avion.sprite == config.AVION_JUGADOR_SPRITE_LEFT_1 or self.avion.sprite == config.AVION_JUGADOR_SPRITE_RIGHT_1):
                    pyxel.rect(self.avion.x+5, self.avion.y+2, 3, 1, col=4)
                    pyxel.rect(self.avion.x+9, self.avion.y+2, 3, 1, col=10)
                    pyxel.rect(self.avion.x+15, self.avion.y+2, 3, 1, col=10)
                    pyxel.rect(self.avion.x+19, self.avion.y+2, 3, 1, col=4)
                if pyxel.frame_count % 2 == 0 and self.avion.sprite == config.AVION_JUGADOR_SPRITE_LEFT_2:
                    pyxel.rect(self.avion.x+4, self.avion.y+2, 3, 1, col=4)
                    pyxel.rect(self.avion.x+8, self.avion.y+2, 2, 1, col=10)
                    pyxel.rect(self.avion.x+13, self.avion.y+2, 3, 1, col=10)
                    pyxel.rect(self.avion.x+17, self.avion.y+2, 3, 1, col=4)
                if pyxel.frame_count % 2 == 0 and self.avion.sprite == config.AVION_JUGADOR_SPRITE_LEFT_3:
                    pyxel.rect(self.avion.x+3, self.avion.y+2, 3, 1, col=4)
                    pyxel.rect(self.avion.x+8, self.avion.y+2, 1, 1, col=10)
                    pyxel.rect(self.avion.x+10, self.avion.y+2, 3, 1, col=10)
                    pyxel.rect(self.avion.x+14, self.avion.y+2, 3, 1, col=4)    
                if pyxel.frame_count % 2 == 0 and self.avion.sprite == config.AVION_JUGADOR_SPRITE_RIGHT_2:
                    pyxel.rect(self.avion.x+5, self.avion.y+2, 3, 1, col=4)
                    pyxel.rect(self.avion.x+9, self.avion.y+2, 3, 1, col=10)
                    pyxel.rect(self.avion.x+15, self.avion.y+2, 2, 1, col=10)
                    pyxel.rect(self.avion.x+18, self.avion.y+2, 3, 1, col=4)    
                if pyxel.frame_count % 2 == 0 and self.avion.sprite == config.AVION_JUGADOR_SPRITE_RIGHT_3:
                    pyxel.rect(self.avion.x+4, self.avion.y+2, 3, 1, col=4)
                    pyxel.rect(self.avion.x+8, self.avion.y+2, 3, 1, col=10)
                    pyxel.rect(self.avion.x+13, self.avion.y+2, 1, 1, col=10)
                    pyxel.rect(self.avion.x+15, self.avion.y+2, 3, 1, col=4) 

            
            #Para el enemigo regular
            for enemigo in self.enemigosRegulares:
                if pyxel.frame_count % 2 == 0 and enemigo.sprite == config.ENEMIGO_REGULAR_DIMENSIONES_1:
                    pyxel.rect(enemigo.x+5, enemigo.y+14, 3, 1, col=10)
                    pyxel.rect(enemigo.x+9, enemigo.y+14, 3, 1, col=12)
                if pyxel.frame_count % 2 == 0 and enemigo.sprite == config.ENEMIGO_REGULAR_DIMENSIONES_5:
                    pyxel.rect(enemigo.x+5, enemigo.y+1, 3, 1, col=10)
                    pyxel.rect(enemigo.x+9, enemigo.y+1, 3, 1, col=13)    
                    
            #Para el bombardero
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

            #Para el superbombardero
            for sb in self.super_bombarderos:
                if pyxel.frame_count % 2 == 0 and sb.alive:
                    pyxel.rect(sb.x + 17, sb.y + 9, 4, 1, col=4)
                    pyxel.rect(sb.x+ 22, sb.y + 9, 4, 1, col=10)
                    pyxel.rect(sb.x+ 39, sb.y + 9, 4, 1, col=10)
                    pyxel.rect(sb.x+ 44, sb.y + 9, 4, 1, col=4)

            #Aquí se dibujan las explosiones de la lista explosiones que hemos mencionado anteriormente
            for explosion in self.explosiones:
                explosion.draw()
                pyxel.blt(*explosion.blt, colkey=7)
            
            '''Aquí se dibujan los bonus en pantalla, además de que si se activa el bonus estrella, se cambian los colores del avión con los del arcoíris
            con la función pyxel.pal
            '''
            for bonus in self.bonusJugador:
                if self.bonusEnemigoRojo and not bonus.activado:
                    pyxel.blt(bonus.x, bonus.y, *bonus.sprite, colkey=8)
                if bonus.activado and bonus.devolverTipoBonus() == "estrella":
                    pyxel.pal(13, pyxel.frame_count % 16)
                else:
                    pyxel.pal()

            if self.interludio:
                self.pantallaEntreMuertes()         
    
    
    '''Esta es la función general para las colisiones, en la que introduces por parámetro los objetos entre los que quieres establecer la colisión.
    En la función, se toma el ancho y el largo de los sprites de ambos objetos, y se comprueba las interseccion tanto en el eje y como en el eje x de 
    los dos objetos. Si se cumple la colisión, el método devuelve True, y se producirá la pérdida de vida o la eliminación del objeto correspondiente'''
    
    def colisiones(self, objeto1, objeto2):
        
        if (objeto1.x + objeto1.sprite[3] - 1  > objeto2.x 
            and objeto2.x + objeto2.sprite[3] - 1  > objeto1.x # Comprobamos intersección en el eje [x]
            and objeto1.y + objeto1.sprite[4] - 1 > objeto2.y #Comprobamos intersección en el eje [y]
            and objeto2.y + objeto2.sprite[4] - 1 > objeto1.y):
            return True

    '''Este es el método en el que se pinta la pantalla del principio. En ella se dibuja el título, con efecto 3D y con el cambio de colores realizado
    con el pyxel.pal.'''
    
    def pantallaInicio(self):
        pyxel.load("assets/titulo.pyxres") #Se carga el archivo pyxres en el que están los sprites del título
        pyxel.pal()
        pyxel.pal(15, pyxel.frame_count % 16)

        pyxel.blt(16, 64, *config.UNO, colkey=7)
        pyxel.blt(60, 64, *config.NUEVE, colkey=7)
        pyxel.blt(118, 64, *config.CUATRO, colkey=7)
        pyxel.blt(182, 64, *config.DOS, colkey=7)

        pyxel.text(108, 180, "PRESIONA S", col=15)

        pyxel.load("assets/avionPlayersyOtros.pyxres")
        pyxel.blt(96, 220, 1,4,37,64,15)

    '''La pantalla del interludio, en la que básicamente ya aparece nuestro avión y te pone la frase de la Batalla de Midway'''
    def pantallaEntreMuertes(self):
        pyxel.text(95, 40,"BATALLA DE MIDWAY", col=7)
        pyxel.text(73, 50, "¡DESTRUYE A TODOS PARA GANAR!", col=7)

    '''La pantalla de Gameover, en la que aparecen tus estadísticas: tu puntuación récord, los enemigos abatidos de cada tipo...'''
    def pantallaGameover(self):
        pyxel.cls(12)
        pyxel.pal(15, pyxel.frame_count%16)
        pyxel.text(100, 50, "G A M E  O V E R", col=8)
        pyxel.text(75, 80, "TOTAL SCORE:", col=7)
        pyxel.text(180, 80, str(self.avion.puntuacionFinal), col=7)

        pyxel.text(75, 90,"HIGHEST SCORE:", col=7)
        pyxel.text(180, 90, str(self.avion.highScore), col=7)

        pyxel.text(75, 100, "ENEMIGOS ABATIDOS:", col=7)
        
        pyxel.text(75, 110, "ENEMIGOS REGULARES",col=7)
        pyxel.text(180, 110, str(self.avion.regular), col=7)

        pyxel.text(75, 120, "ENEMIGOS ROJOS",col=7)
        pyxel.text(180, 120, str(self.avion.rojo), col=7)

        pyxel.text(75, 130, "ENEMIGOS BOMBARDERO",col=7)
        pyxel.text(180, 130, str(self.avion.bombardero), col=7)

        pyxel.text(75, 140, "ENEMIGOS SUPERBOMBARDERO",col=7)
        pyxel.text(180, 140, str(self.avion.superbombardero), col=7)
        
        pyxel.text(80, 240, "PRESIONA X PARA CONTINUAR", col=15)                
App()