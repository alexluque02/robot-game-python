from juego import Juego

filas = 30
columnas = 50
tamano_celda = 30
ruta_mapa = 'mapa.txt'

juego = Juego(filas, columnas, tamano_celda, ruta_mapa)
juego.run(tamano_celda)

while True:

    if juego.reiniciar:
        juego.reiniciar = False
        juego = Juego(filas, columnas, tamano_celda, ruta_mapa)
        juego.run(tamano_celda)
    else:
        break
