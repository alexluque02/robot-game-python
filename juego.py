import pygame
import sys

from pygame.locals import KEYDOWN, K_t

import mapa
from mapa import Mapa

ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)


class Juego:
    def __init__(self, filas, columnas, tamano_celda, ruta_mapa, ruta_imagen_fondo):
        pygame.init()
        self.filas = filas
        self.columnas = columnas
        self.tamano_celda = tamano_celda
        self.screen = pygame.display.set_mode((columnas * tamano_celda, filas * tamano_celda + 30))
        pygame.display.set_caption("Juego del Robot")
        self.mapa = Mapa(ruta_mapa, tamano_celda)  # Crear instancia de Mapa
        self.imagen_fondo = pygame.image.load(ruta_imagen_fondo)  # Cargar la imagen de fondo
        self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (columnas * tamano_celda, filas * tamano_celda))
        self.reloj = pygame.time.Clock()

    def dibujar_info(self):
        font = pygame.font.Font(None, 24)
        imagen_diamante = pygame.image.load("images/diamond.png")
        imagen_diamante = pygame.transform.scale(imagen_diamante, (self.tamano_celda // 2, self.tamano_celda // 2))

        self.screen.blit(imagen_diamante, (10, self.filas * self.tamano_celda + 5))

        texto_diamantes = font.render(f" {len(self.mapa.robot.diamantes)}", True, NEGRO)
        self.screen.blit(texto_diamantes, (25, self.filas * self.tamano_celda + 5))

        imagen_corazon = pygame.image.load("images/corazon.png")
        imagen_corazon = pygame.transform.scale(imagen_corazon, (self.tamano_celda // 2, self.tamano_celda // 2))

        self.screen.blit(imagen_corazon, (55, self.filas * self.tamano_celda + 5))

        texto_vidas = font.render(f" {self.mapa.robot.vidas}", True, NEGRO)
        self.screen.blit(texto_vidas, (70, self.filas * self.tamano_celda + 5))

        imagen_traje = pygame.image.load("images/traje_agua.png")
        imagen_traje = pygame.transform.scale(imagen_traje, (self.tamano_celda // 2, self.tamano_celda // 2))

        self.screen.blit(imagen_traje, (110, self.filas * self.tamano_celda + 5))

        texto_trajes = font.render(f" {len(self.mapa.robot.trajes_agua)}", True, NEGRO)
        self.screen.blit(texto_trajes, (125, self.filas * self.tamano_celda + 5))

        imagen_bomba = pygame.image.load("images/bomba.png")
        imagen_bomba = pygame.transform.scale(imagen_bomba, (self.tamano_celda // 2, self.tamano_celda // 2))

        self.screen.blit(imagen_bomba, (160, self.filas * self.tamano_celda + 5))

        texto_bombas = font.render(f" {len(self.mapa.robot.bombas)}", True, NEGRO)
        self.screen.blit(texto_bombas, (175, self.filas * self.tamano_celda + 5))

        imagen_pocion = pygame.image.load("images/pocion.png")
        imagen_pocion = pygame.transform.scale(imagen_pocion, (self.tamano_celda // 2, self.tamano_celda // 2))

        self.screen.blit(imagen_pocion, (210, self.filas * self.tamano_celda + 5))

        texto_pocion = font.render(f" {len(self.mapa.robot.pociones)}", True, NEGRO)
        self.screen.blit(texto_pocion, (225, self.filas * self.tamano_celda + 5))

    def run(self, tamano_celda):
        jugando = True
        #ganador = False

        while jugando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.mapa.robot.mover("arriba", self.mapa, tamano_celda)
            elif keys[pygame.K_DOWN]:
                self.mapa.robot.mover("abajo", self.mapa, tamano_celda)
            elif keys[pygame.K_LEFT]:
                self.mapa.robot.mover("izquierda", self.mapa, tamano_celda)
            elif keys[pygame.K_RIGHT]:
                self.mapa.robot.mover("derecha", self.mapa, tamano_celda)

            if keys[pygame.K_t]:
                self.mapa.robot.usar_traje_agua()

            if keys[pygame.K_b]:
                self.mapa.robot.detonar_bomba(self.mapa)

            if keys[pygame.K_p]:
                self.mapa.robot.tomar_pocion()

            self.mapa.robot.recoger_diamantes(self.mapa)
            self.mapa.robot.recoger_trajes_agua(self.mapa)
            self.mapa.robot.recoger_bombas(self.mapa)
            self.mapa.robot.recoger_pociones(self.mapa)

            if self.mapa.robot.vidas <= 0:
                print("¡Te quedaste sin vidas! Has perdido.")
                jugando = False

            #if self.mapa.robot.check_win(self.mapa) and not ganador:
            #    ganador = True

            self.screen.fill(BLANCO)
            self.screen.blit(self.imagen_fondo, (0, 0))
            self.mapa.dibujar(self.screen)
            self.screen.blit(self.mapa.robot.image,
                             (self.mapa.robot.posicion[1] * self.tamano_celda,
                              self.mapa.robot.posicion[0] * self.tamano_celda))

            # Dibujar información
            self.dibujar_info()

            pygame.display.flip()

            self.reloj.tick(10)

        pygame.quit()
        sys.exit()
