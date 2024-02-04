import pygame


class Bomba(pygame.sprite.Sprite):
    def __init__(self, fila, columna, tamano_celda):
        super().__init__()
        self.image = pygame.image.load("images/bomba.png")
        self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
        self.rect = self.image.get_rect()
        self.posicion = [fila, columna]
        self.tamano_celda = tamano_celda

    def explotar(self, mapa, posicion):
        adyacentes = [
            (posicion[0] - 1, posicion[1]),  # Arriba
            (posicion[0] + 1, posicion[1]),  # Abajo
            (posicion[0], posicion[1] - 1),  # Izquierda
            (posicion[0], posicion[1] + 1)  # Derecha
        ]

        for fila, columna in adyacentes:
            # Verificar si la posición es válida en el mapa
            if 0 <= fila < mapa.filas and 0 <= columna < mapa.columnas:
                muro = mapa.obtener_muro_en_posicion(fila, columna)
                if muro:
                    mapa.remover_muro(muro)
                traje_acuatico = mapa.obtener_traje_acuatico_en_posicion(fila, columna)
                if traje_acuatico:
                    mapa.remover_traje_acuatico(traje_acuatico)

                bomba = mapa.obtener_bomba_en_posicion(fila, columna)
                if bomba:
                    bomba.explotar(mapa, posicion)

    def dibujar(self, screen):
        screen.blit(self.image, (self.posicion[1] * self.rect.width, self.posicion[0] * self.rect.height))

