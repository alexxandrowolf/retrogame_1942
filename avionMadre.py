class Avion():

    '''Esta clase va a ser nuestra clase madre para todos los aviones, enemigos incluidos. En el init vemos que se introducen por parametro una lista
    denominada nave, en cuya primera posición está el sprite del avión (que en el draw de board será introducido en el pyxel.blt para pintar el avión),
    y en la segunda posición se introducirá la posición que va a tener el avión en el momento de su creación. Acto seguido se introduce por parámetro
    otra lista, llamada stats, en la que están propiedades importantes de cada avión como son su vida, su velocidad, si está vivo o no, y la 
    puntuación que otorga al morir  
    '''
    
    def __init__(self, nave: list, stats = None):
        #Tamaño de nuestra pantalla
        self.SCREEN_WIDTH = 256
        self.SCREEN_HEIGHT = 256

        #Posición
        self.x = nave[1][0]
        self.y = nave[1][1]

        #Sprite de nuestro avión (contiene banco de imagén, posición y dimensión)
        self.sprite = nave[0]

        #Otros atributos básicos
        self.stats = stats
        self.health = self.stats[0]
        self.speed = self.stats[1]
        self.alive = self.stats[2]
        self.puntuacion = self.stats[3]
        self.animacionMuerte = False

    '''Esta property la utilizamos para darle valores seguros a todos los stats en caso de no introducir nada por parámetro
    '''
    @property
    def stats(self):
        return self.__stats
    @stats.setter
    def stats(self, stats):
        if stats == None:
            self.__stats = [1, 2, True, 10]
        else:
            self.__stats = stats    

    '''El método drawAvion es importante ya que al atributo blt (que luego será introducido en el pyxel.blt de board), se va actualizando con las
    diferentes posiciones que va tomando el avion, y con los diferentes sprites en caso de que se esté llevando a cabo una animación
    '''

    def drawAvion(self):
        self.blt = (self.x, self.y, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], self.sprite[4])

    '''El método perderVida es bastante útil ya que realiza dos acciones. Le resta 1 a la vida del avión, y luego comprueba si es a 0 no. En caso de
    que así sea, estabelece como True a self.animacionMuerte, lo que hace que en el board se introduzca en una lista los sprites de explosión del 
    avión en cuestión, además de poner self.alive a False 
    '''
    
    def perderVida(self):
        self.health -= 1
        if self.health == 0:
            self.animacionMuerte = True

    '''El método perderVida2 se utiliza con aquellos aviones que tienen una animación de muerte propia y no utilizan la clase Explosión (que en nuestro
    caso es sólo el super0bombardero). Hace lo mismo que el método anterior, pero si detecta que self.health es igual a 0, directamente pone como
    False a self.alive
    '''
    
    def perderVida2(self):
        self.health -= 1
        if self.health == 0:
            self.alive = False        