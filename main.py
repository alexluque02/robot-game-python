from juego import Juego


# Configuración del juego
filas = 30
columnas = 50
tamano_celda = 30
ruta_mapa = 'mapa.txt'
ruta_imagen_fondo = 'images/fondo.jpg'

# Iniciar el juego
juego = Juego(filas, columnas, tamano_celda, ruta_mapa, ruta_imagen_fondo)
juego.run()

