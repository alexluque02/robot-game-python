import pygame


class Agua(pygame.sprite.Sprite):
    def __init__(self, fila, columna, tamano_celda):
        super().__init__()
        self.image = pygame.image.load("images/agua.jpeg").convert()
        self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
        self.rect = self.image.get_rect()
        self.rect.x = columna * tamano_celda
        self.rect.y = fila * tamano_celda
        self.fila = fila
        self.columna = columna
        self.posicion = (fila, columna)

    def dibujar(self, screen):
        screen.blit(self.image, self.rect)
