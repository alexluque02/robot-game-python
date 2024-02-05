import pygame
import pygame.mixer
import sys

from mapa import Mapa

ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)


class Juego:
    def __init__(self, filas, columnas, tamano_celda, ruta_mapa):
        pygame.init()
        self.filas = filas
        self.columnas = columnas
        self.tamano_celda = tamano_celda
        self.screen = pygame.display.set_mode((columnas * tamano_celda, filas * tamano_celda + 30))
        pygame.display.set_caption("Juego del Robot")
        self.mapa = Mapa(ruta_mapa, tamano_celda)
        self.reloj = pygame.time.Clock()
        self.jugando = True
        self.reiniciar = False
        pygame.mixer.init()
        pygame.mixer.music.load("sound/melodia.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

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
        ganador = False

        while self.jugando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.salir_juego()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.mostrar_confirmacion_salida()

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

            if len(self.mapa.robot.diamantes) >= self.mapa.num_diamantes:
                ganador = True
                self.jugando = False

            if self.mapa.robot.vidas <= 0:
                print("¡Te quedaste sin vidas! Has perdido.")
                self.jugando = False

            self.screen.fill(BLANCO)
            self.mapa.dibujar(self.screen)
            self.screen.blit(self.mapa.robot.image,
                             (self.mapa.robot.posicion[1] * self.tamano_celda,
                              self.mapa.robot.posicion[0] * self.tamano_celda))

            self.dibujar_info()

            pygame.display.flip()

            self.reloj.tick(10)

        # Mostrar mensaje de ganar
        if ganador:
            self.mostrar_mensaje_ganador()
            self.mostrar_pantalla_reinicio()
        else:
            self.mostrar_game_over()
            self.mostrar_pantalla_reinicio()

    def mostrar_game_over(self):
        font = pygame.font.Font("fuente.ttf", 70)
        texto_game_over = font.render("Game Over", True, ROJO)

        fondo = pygame.Surface((self.columnas * self.tamano_celda, self.filas * self.tamano_celda))
        fondo.fill(NEGRO)

        x = (fondo.get_width() - texto_game_over.get_width()) // 2
        y = (fondo.get_height() - texto_game_over.get_height()) // 2

        fondo.blit(texto_game_over, (x, y))

        self.screen.blit(fondo, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)

    def mostrar_mensaje_ganador(self):
        font = pygame.font.Font("fuente.ttf", 70)
        texto_ganador = font.render("Felicidades, has ganado", True, ROJO)

        fondo = pygame.Surface((self.columnas * self.tamano_celda, self.filas * self.tamano_celda))
        fondo.fill(NEGRO)

        x = (fondo.get_width() - texto_ganador.get_width()) // 2
        y = (fondo.get_height() - texto_ganador.get_height()) // 2

        fondo.blit(texto_ganador, (x, y))

        self.screen.blit(fondo, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)

    def mostrar_pantalla_reinicio(self):
        button_width, button_height = 100, 50
        button_x = (self.screen.get_width() - 2 * button_width) // 2
        button_y = (self.screen.get_height() - button_height) // 2 + 70

        pygame.draw.rect(self.screen, BLANCO, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(self.screen, BLANCO, (button_x + button_width + 20, button_y, button_width, button_height))

        font_botones = pygame.font.Font(None, 24)
        text_reiniciar = font_botones.render("Reiniciar", True, ROJO)
        text_salir = font_botones.render("Salir", True, ROJO)

        self.screen.blit(text_reiniciar, (button_x + 15, button_y + 15))
        self.screen.blit(text_salir, (button_x + button_width + 50, button_y + 15))

        pygame.display.flip()

        esperando_click = True
        while esperando_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.salir_juego()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button_x < x < button_x + button_width and button_y < y < button_y + button_height:
                        self.reiniciar = True
                        esperando_click = False
                    elif button_x + button_width + 20 < x < button_x + 2 * button_width + 20 and button_y < y < button_y + button_height:
                        self.salir_juego()
                        esperando_click = False

    def salir_juego(self):
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

    def mostrar_confirmacion_salida(self):
        confirmacion = self.mostrar_botones_confirmacion("¿Estás seguro de que quieres salir?")
        if confirmacion == "Sí":
            self.salir_juego()

    def mostrar_botones_confirmacion(self, mensaje):
        fondo_ancho, fondo_alto = 500, 200
        fondo_x = (self.screen.get_width() - fondo_ancho) // 2
        fondo_y = (self.screen.get_height() - fondo_alto) // 2
        fondo = pygame.Surface((fondo_ancho, fondo_alto))
        fondo.fill(ROJO)
        self.screen.blit(fondo, (fondo_x, fondo_y))

        font_mensaje = pygame.font.Font(None, 36)
        text_mensaje = font_mensaje.render(mensaje, True, BLANCO)
        mensaje_x = (self.screen.get_width() - text_mensaje.get_width()) // 2
        mensaje_y = fondo_y + 50
        self.screen.blit(text_mensaje, (mensaje_x, mensaje_y))

        button_width, button_height = 100, 50
        button_x = (self.screen.get_width() - 2 * button_width) // 2
        button_y = fondo_y + 90

        pygame.draw.rect(self.screen, BLANCO, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(self.screen, BLANCO, (button_x + button_width + 20, button_y, button_width, button_height))

        font = pygame.font.Font(None, 24)
        text_si = font.render("Sí", True, ROJO)
        text_no = font.render("No", True, ROJO)

        self.screen.blit(text_si, (button_x + 40, button_y + 15))
        self.screen.blit(text_no, (button_x + button_width + 60, button_y + 15))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.salir_juego()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button_x < x < button_x + button_width and button_y < y < button_y + button_height:
                        return "Sí"
                    elif button_x + button_width + 20 < x < button_x + 2 * button_width + 20 and button_y < y < button_y + button_height:
                        return "No"
