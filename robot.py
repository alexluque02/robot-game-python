import pygame


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
                    self.vidas -= 1
                    print("¡Chocaste con un obstáculo! Vidas restantes:", self.vidas)
                    return
            self.posicion = nueva_posicion

    def recoger_diamantes(self, mapa):
        for diamante in mapa.diamantes:
            if self.posicion == diamante.posicion:
                mapa.diamantes.remove(diamante)
                self.diamantes.append(diamante)
                print("Diamante recogido!")
                print(len(mapa.diamantes))
                break

    def recoger_trajes_agua(self, mapa):
        for traje_agua in mapa.trajes_agua:
            if self.posicion == traje_agua.posicion:
                mapa.trajes_agua.remove(traje_agua)
                self.trajes_agua.append(traje_agua)
                print("Traje de agua recogido!")
                print(len(self.trajes_agua))
                break

    def recoger_bombas(self, mapa):
        for bomba in mapa.bombas:
            if self.posicion == bomba.posicion:
                mapa.bombas.remove(bomba)
                self.bombas.append(bomba)
                print("Bomba recogida!")
                print(len(self.bombas))
                break

    def recoger_pociones(self, mapa):
        for pocion in mapa.pociones:
            if self.posicion == pocion.posicion:
                mapa.pociones.remove(pocion)
                self.pociones.append(pocion)
                print("Poción recogida!")
                print(len(self.pociones))
                break

    def usar_traje_agua(self):
        if self.trajes_agua:
            traje_actual = self.trajes_agua.pop(0)
            if not traje_actual.usado:
                self.usando_traje_agua = True
                print("Estás usando un traje de agua")
            else:
                print("Este traje de agua ya ha sido usado.")
        else:
            print("No tienes trajes de agua disponibles.")

    def quitar_traje_agua(self):
        trajes_no_usados = [traje for traje in self.trajes_agua if not traje.usado]
        if trajes_no_usados:
            traje = trajes_no_usados.pop(0)
            traje.usado = True
            print("Se ha quitado un traje de agua.")

    def detonar_bomba(self, mapa):
        if self.bombas:
            bomba = self.bombas.pop(0)
            bomba.explotar(mapa, self.posicion)

    def tomar_pocion(self):
        if self.pociones:
            if self.vidas >= 10:
                print("Ya tienes la vida al máximo")
            else:
                self.vidas = min(10, self.vidas + 5)  # Aumentar las vidas, asegurándose de no superar el máximo (10)
                self.pociones.remove(self.pociones[0])
                print("Tomaste una poción. Vidas restantes:", self.vidas)
        else:
            print("No tienes pociones disponibles.")

    def check_win(self, mapa):
        return len(mapa.diamantes) == 0


