from agua import Agua
from diamante import Diamond
from muro import Muro
from robot import Robot

import random

from trajeAgua import TrajeAgua


class Mapa:
    def __init__(self, ruta_archivo, tamano_celda, num_diamantes=15,num_trajes_agua=2):
        self.tamano_celda = tamano_celda
        self.num_diamantes = num_diamantes
        self.num_trajes_agua = num_trajes_agua
        self.diamantes = []
        self.robot = None
        self.muros = []
        self.aguas = []
        self.trajes_agua = []
        self.cargar_mapa_desde_archivo(ruta_archivo)

    def cargar_mapa_desde_archivo(self, ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()

        self.filas = len(lineas)
        self.columnas = max(len(linea.strip()) for linea in lineas)

        for fila, linea in enumerate(lineas):
            for columna, caracter in enumerate(linea.strip()):
                caracter = lineas[fila][columna]
                if caracter == 'M':
                    # Crear un muro
                    muro = Muro(fila, columna, self.tamano_celda)
                    self.muros.append(muro)
                elif caracter == 'R':
                    # Crear la posición inicial del robot
                    self.robot = Robot(fila, columna, self.tamano_celda)
                elif caracter == 'A':
                    # Crear agua
                    agua = Agua(fila, columna, self.tamano_celda)
                    self.aguas.append(agua)

        # Colocar 15 diamantes aleatoriamente
        diamantes_agregados = 0
        while diamantes_agregados < self.num_diamantes:
            fila = random.randint(0, self.filas - 2)
            columna = random.randint(0, self.columnas - 1)
            if all(((fila, columna) not in #(muro.posicion for muro in self.muros),
                    (fila, columna) != self.robot.posicion,
                    (fila, columna) not in (diamante.posicion for diamante in self.diamantes))):
                diamante = Diamond(fila, columna, self.tamano_celda)
                self.diamantes.append(diamante)
                diamantes_agregados += 1

        trajes_agua_agregados = 0
        while trajes_agua_agregados < self.num_trajes_agua:
            fila = random.randint(0, self.filas - 2)  # Restamos 2 para excluir la última fila
            columna = random.randint(0, self.columnas - 1)
            if all(((fila, columna) not in (muro.posicion for muro in self.muros),
                    (fila, columna) != self.robot.posicion,
                    (fila, columna) not in (diamante.posicion for diamante in self.diamantes),
                    (fila, columna) not in (traje_agua.posicion for traje_agua in self.trajes_agua),
                    (fila, columna) not in (agua.posicion for agua in self.aguas))):
                traje_agua = TrajeAgua(fila, columna, self.tamano_celda)
                self.trajes_agua.append(traje_agua)
                trajes_agua_agregados += 1

    def dibujar(self, screen):
        for muro in self.muros:
            muro.dibujar(screen)
        for diamante in self.diamantes:
            diamante.dibujar(screen)
        for agua in self.aguas:
            agua.dibujar(screen)
        for traje_agua in self.trajes_agua:
            traje_agua.dibujar(screen)