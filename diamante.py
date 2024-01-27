import pygame


class Diamond(pygame.sprite.Sprite):
    def __init__(self, fila, columna, tamano_celda):
        super().__init__()
        self.image = pygame.image.load("images/diamond.png")
        self.image = pygame.transform.scale(self.image, (tamano_celda // 2, tamano_celda // 2))
        self.rect = self.image.get_rect()
        self.posicion = [fila, columna]
        self.rect.topleft = (columna * tamano_celda + tamano_celda // 4, fila * tamano_celda + tamano_celda // 4)

    def dibujar(self, screen):
        screen.blit(self.image, self.rect)