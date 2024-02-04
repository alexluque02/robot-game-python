import pygame


class Suelo(pygame.sprite.Sprite):
    def __init__(self, fila, columna, tamano_celda):
        super().__init__()
        self.image = pygame.image.load("images/campo.jpg")
        self.image = pygame.transform.scale(self.image, (tamano_celda, tamano_celda))
        self.rect = self.image.get_rect()
        self.posicion = [fila, columna]
        self.tamano_celda = tamano_celda

    def dibujar(self, screen):
        screen.blit(self.image, (self.posicion[1] * self.rect.width, self.posicion[0] * self.rect.height))
