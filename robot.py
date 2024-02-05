import pygame
import pygame.mixer


class Robot(pygame.sprite.Sprite):
    def __init__(self, fila, columna, tamano_celda):
        super().__init__()
        self.image = pygame.image.load("images/spriteabajo.png")
        self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
        self.rect = self.image.get_rect()
        self.posicion = [fila, columna]
        self.vidas = 10
        self.parpadear = False
        self.tiempo_parpadeo = 0
        self.trajes_agua = []
        self.diamantes = []
        self.bombas = []
        self.pociones = []
        self.usando_traje_agua = False
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def mover(self, direccion, mapa, tamano_celda):
        nueva_posicion = self.posicion.copy()

        if direccion == "arriba" and nueva_posicion[0] > 0:
            nueva_posicion[0] -= 1
            if self.usando_traje_agua:
                self.image = pygame.image.load("images/spritearribawater.png")
                self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
            else:
                self.image = pygame.image.load("images/spritearriba.png")
                self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
        elif direccion == "abajo" and nueva_posicion[0] < mapa.filas - 1:
            nueva_posicion[0] += 1
            if self.usando_traje_agua:
                self.image = pygame.image.load("images/spriteabajowater.png")
                self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
            else:
                self.image = pygame.image.load("images/spriteabajo.png")
                self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
        elif direccion == "izquierda" and nueva_posicion[1] > 0:
            nueva_posicion[1] -= 1
            if self.usando_traje_agua:
                self.image = pygame.image.load("images/spriteizqwater.png")
                self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
            else:
                self.image = pygame.image.load("images/spriteizq.png")
                self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
        elif direccion == "derecha" and nueva_posicion[1] < mapa.columnas - 1:
            nueva_posicion[1] += 1
            if self.usando_traje_agua:
                self.image = pygame.image.load("images/spritederwater.png")
                self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
            else:
                self.image = pygame.image.load("images/spriteder.png")
                self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))

        for agua in mapa.aguas:
            if nueva_posicion == [agua.posicion[0], agua.posicion[1]]:
                if self.usando_traje_agua:
                    print("Estás usando el traje de agua")
                else:
                    self.vidas -= 3  # Restar 3 puntos de vida por cada celda de agua
                    print("Te sumergiste en el agua. Vidas restantes:", self.vidas)
                break
            if self.posicion == [agua.posicion[0], agua.posicion[1]] and all(nueva_posicion != [a.posicion[0],
                                                                                                a.posicion[1]] for a in
                                                                             mapa.aguas):
                if self.usando_traje_agua:
                    self.quitar_traje_agua()
                    self.usando_traje_agua = False
                    print("Has salido del agua. El traje de agua se ha quitado.")
                break

        if nueva_posicion not in [(diamante.posicion[0], diamante.posicion[1]) for diamante in mapa.diamantes]:
            for muro in mapa.muros:
                if nueva_posicion == [muro.fila, muro.columna]:
                    sonido_wrong = pygame.mixer.Sound("sound/wrong.mp3")
                    sonido_wrong.set_volume(1)
                    sonido_wrong.play()
                    self.vidas -= 1
                    return
            self.posicion = nueva_posicion

    def recoger_diamantes(self, mapa):
        for diamante in mapa.diamantes:
            if self.posicion == diamante.posicion:
                sonido_diamante = pygame.mixer.Sound("sound/diamante.mp3")
                sonido_diamante.set_volume(0.5)
                sonido_diamante.play()
                mapa.diamantes.remove(diamante)
                self.diamantes.append(diamante)
                break

    def recoger_trajes_agua(self, mapa):
        for traje_agua in mapa.trajes_agua:
            if self.posicion == traje_agua.posicion:
                sonido_traje = pygame.mixer.Sound("sound/collect.mp3")
                sonido_traje.set_volume(0.5)
                sonido_traje.play()
                mapa.trajes_agua.remove(traje_agua)
                self.trajes_agua.append(traje_agua)
                break

    def recoger_bombas(self, mapa):
        for bomba in mapa.bombas:
            if self.posicion == bomba.posicion:
                sonido_bomba = pygame.mixer.Sound("sound/collect.mp3")
                sonido_bomba.set_volume(0.5)
                sonido_bomba.play()
                mapa.bombas.remove(bomba)
                self.bombas.append(bomba)
                break

    def recoger_pociones(self, mapa):
        for pocion in mapa.pociones:
            if self.posicion == pocion.posicion:
                sonido_pocion = pygame.mixer.Sound("sound/collect.mp3")
                sonido_pocion.set_volume(0.5)
                sonido_pocion.play()
                mapa.pociones.remove(pocion)
                self.pociones.append(pocion)
                break

    def usar_traje_agua(self):
        if self.trajes_agua:
            traje_actual = self.trajes_agua.pop(0)
            if not traje_actual.usado:
                sonido_traje = pygame.mixer.Sound("sound/traje.mp3")
                sonido_traje.set_volume(0.5)
                sonido_traje.play()
                self.usando_traje_agua = True
            else:
                sonido_wrong = pygame.mixer.Sound("sound/wrong.mp3")
                sonido_wrong.set_volume(1)
                sonido_wrong.play()
        else:
            sonido_wrong = pygame.mixer.Sound("sound/wrong.mp3")
            sonido_wrong.set_volume(1)
            sonido_wrong.play()

    def quitar_traje_agua(self):
        trajes_no_usados = [traje for traje in self.trajes_agua if not traje.usado]
        if trajes_no_usados:
            sonido_quitar = pygame.mixer.Sound("sound/quitar_traje.mp3")
            sonido_quitar.set_volume(0.5)
            sonido_quitar.play()
            traje = trajes_no_usados.pop(0)
            traje.usado = True
            print("Se ha quitado un traje de agua.")

    def detonar_bomba(self, mapa):
        if self.bombas:
            sonido_bomba = pygame.mixer.Sound("sound/bomba.mp3")
            sonido_bomba.set_volume(0.5)
            sonido_bomba.play()
            bomba = self.bombas.pop(0)
            bomba.explotar(mapa, self.posicion)
        else:
            sonido_wrong = pygame.mixer.Sound("sound/wrong.mp3")
            sonido_wrong.set_volume(1)
            sonido_wrong.play()

    def tomar_pocion(self):
        if self.pociones:
            if self.vidas >= 10:
                sonido_wrong = pygame.mixer.Sound("sound/wrong.mp3")
                sonido_wrong.set_volume(1)
                sonido_wrong.play()
            else:
                sonido_pocion = pygame.mixer.Sound("sound/drink.mp3")
                sonido_pocion.set_volume(0.5)
                sonido_pocion.play()
                self.vidas = min(10, self.vidas + 5)  # Aumentar las vidas, asegurándose de no superar el máximo (10)
                self.pociones.remove(self.pociones[0])
        else:
            sonido_wrong = pygame.mixer.Sound("sound/wrong.mp3")
            sonido_wrong.set_volume(1)
            sonido_wrong.play()


