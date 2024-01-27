import pygame

class Robot(pygame.sprite.Sprite):
    def __init__(self, fila, columna, tamano_celda):
        super().__init__()
        self.image = pygame.image.load("images/robot.png")
        self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
        self.rect = self.image.get_rect()
        self.posicion = [fila, columna]
        self.vidas = 10
        self.parpadear = False
        self.tiempo_parpadeo = 0
        self.trajes_agua=[]
        self.diamantes=[]

    def mover(self, direccion, mapa):
        nueva_posicion = self.posicion.copy()

        if direccion == "arriba" and nueva_posicion[0] > 0:
            nueva_posicion[0] -= 1
        elif direccion == "abajo" and nueva_posicion[0] < mapa.filas - 1:
            nueva_posicion[0] += 1
        elif direccion == "izquierda" and nueva_posicion[1] > 0:
            nueva_posicion[1] -= 1
        elif direccion == "derecha" and nueva_posicion[1] < mapa.columnas - 1:
            nueva_posicion[1] += 1

        for agua in mapa.aguas:
            if nueva_posicion == [agua.fila, agua.columna]:
                self.vidas -= 3  # Restar 3 puntos de vida por cada celda de agua
                print("Te sumergiste en el agua. Vidas restantes:", self.vidas)
                break

        if nueva_posicion not in [(diamante.posicion[0], diamante.posicion[1]) for diamante in mapa.diamantes]:
            for muro in mapa.muros:
                if nueva_posicion == [muro.fila, muro.columna]:
                    self.vidas -= 1  # Restar vida si choca con un muro
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
                self.trajes_agua.append(traje_agua)  # Agregar el traje de agua recogido a la lista
                print("Traje de agua recogido!")
                print(len(self.trajes_agua))
                # Puedes agregar aquí la lógica para aplicar el efecto del traje de agua si es necesario
                break

    def check_win(self, mapa):
        return len(mapa.diamantes) == 0