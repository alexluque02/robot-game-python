from pocion import Pocion
from agua import Agua
from bomba import Bomba
from diamante import Diamond
from muro import Muro
from robot import Robot

import random

from suelo import Suelo
from trajeAgua import TrajeAgua


class Mapa:
    def __init__(self, ruta_archivo, tamano_celda, num_diamantes=12, num_trajes_agua=3, num_bombas=6, num_pociones=3):
        self.tamano_celda = tamano_celda
        self.num_diamantes = num_diamantes
        self.num_trajes_agua = num_trajes_agua
        self.num_bombas = num_bombas
        self.num_pociones = num_pociones
        self.diamantes = []
        self.robot = None
        self.muros = []
        self.aguas = []
        self.trajes_agua = []
        self.bombas = []
        self.pociones = []
        self.suelo = []
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
                    muro = Muro(fila, columna, self.tamano_celda)
                    self.muros.append(muro)
                elif caracter == 'R':
                    suelo = Suelo(fila, columna, self.tamano_celda)
                    self.suelo.append(suelo)
                    self.robot = Robot(fila, columna, self.tamano_celda)
                elif caracter == 'A':
                    agua = Agua(fila, columna, self.tamano_celda)
                    self.aguas.append(agua)
                elif caracter == ' ':
                    suelo = Suelo(fila, columna, self.tamano_celda)
                    self.suelo.append(suelo)

        for agua in self.aguas:
            print(agua.posicion)

        diamantes_agregados = 0
        while diamantes_agregados < self.num_diamantes:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if all(((fila, columna) != self.robot.posicion,
                    (fila, columna) not in (diamante.posicion for diamante in self.diamantes))):
                diamante = Diamond(fila, columna, self.tamano_celda)
                self.diamantes.append(diamante)
                diamantes_agregados += 1

        trajes_agua_agregados = 0
        while trajes_agua_agregados < self.num_trajes_agua:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if all(((fila, columna) not in (muro.posicion for muro in self.muros),
                    (fila, columna) != self.robot.posicion,
                    (fila, columna) not in (diamante.posicion for diamante in self.diamantes),
                    (fila, columna) not in (traje_agua.posicion for traje_agua in self.trajes_agua),
                    (fila, columna) not in (agua.posicion for agua in self.aguas))):
                traje_agua = TrajeAgua(fila, columna, self.tamano_celda)
                self.trajes_agua.append(traje_agua)
                trajes_agua_agregados += 1

        bombas_agregadas = 0
        while bombas_agregadas < self.num_bombas:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if all(((fila, columna) not in (muro.posicion for muro in self.muros),
                    (fila, columna) != self.robot.posicion,
                    (fila, columna) not in (diamante.posicion for diamante in self.diamantes),
                    (fila, columna) not in (traje_agua.posicion for traje_agua in self.trajes_agua),
                    (fila, columna) not in (bomba.posicion for bomba in self.bombas),
                    (fila, columna) not in (agua.posicion for agua in self.aguas))):
                bomba = Bomba(fila, columna, self.tamano_celda)
                self.bombas.append(bomba)
                bombas_agregadas += 1

        pociones_agregadas = 0
        while pociones_agregadas < self.num_pociones:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if all(((fila, columna) not in (muro.posicion for muro in self.muros),
                    (fila, columna) != self.robot.posicion,
                    (fila, columna) not in (diamante.posicion for diamante in self.diamantes),
                    (fila, columna) not in (traje_agua.posicion for traje_agua in self.trajes_agua),
                    (fila, columna) not in (bomba.posicion for bomba in self.bombas),
                    (fila, columna) not in (pocion.posicion for pocion in self.pociones),
                    (fila, columna) not in (agua.posicion for agua in self.aguas))):
                pocion = Pocion(fila, columna, self.tamano_celda)
                self.pociones.append(pocion)
                pociones_agregadas += 1

    def obtener_muro_en_posicion(self, fila, columna):
        for muro in self.muros:
            if muro.fila == fila and muro.columna == columna:
                return muro
        return None

    def obtener_traje_acuatico_en_posicion(self, fila, columna):
        for traje_agua in self.trajes_agua:
            if traje_agua.posicion == [fila, columna]:
                return traje_agua
        return None

    def obtener_bomba_en_posicion(self, fila, columna):
        for bomba in self.bombas:
            if bomba.posicion == [fila, columna]:
                return bomba
        return None

    def remover_muro(self, muro):
        self.muros.remove(muro)
        suelo = Suelo(muro.posicion[0], muro.posicion[1], self.tamano_celda)
        self.suelo.append(suelo)
        print(muro.posicion)

    def remover_traje_acuatico(self, traje_agua):
        self.trajes_agua.remove(traje_agua)

    def dibujar(self, screen):
        for muro in self.muros:
            muro.dibujar(screen)
        for suelo in self.suelo:
            suelo.dibujar(screen)
        for agua in self.aguas:
            agua.dibujar(screen)
        for diamante in self.diamantes:
            diamante.dibujar(screen)
        for traje_agua in self.trajes_agua:
            traje_agua.dibujar(screen)
        for bomba in self.bombas:
            bomba.dibujar(screen)
        for pocion in self.pociones:
            pocion.dibujar(screen)
