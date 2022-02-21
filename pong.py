from turtle import right
import pygame as pg

pg.init() # Inicializa PyGame

# Define las dimensiones de la ventana en donde correrá el juego
ANCHO, ALTO = 700, 500 
VENTANA = pg.display.set_mode((ANCHO, ALTO)) 

# Le pone titulo a la ventana
pg.display.set_caption('Juego Pong')

# Definir variables
FPS = 60
AZUL = (100, 149, 237)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (237, 189, 100)
FUENTE_PUNTUACION = pg.font.SysFont('verdana', 30, bold=True)

ANCHO_BARRITA, ALTO_BARRITA = 20, 100
RADIO_BOLITA = 7
PUNTUACION_GANADORA = 5

class Barrita:
    COLOR = BLANCO
    VELOCIDAD = 4
    
    def __init__(self, x, y, ancho, alto):
        self.x = self.x_original = x
        self.y = self.y_original = y
        self.ancho = ancho
        self.alto = alto
        
    def mostrar(self, ventana):
        pg.draw.rect(
            ventana, self.COLOR, (self.x, self.y, self.ancho, self.alto))
    
    def mover(self, arriba=True):
        if arriba:
            self.y -= self.VELOCIDAD
        else:
            self.y += self.VELOCIDAD
    
    def reset(self):
        self.x = self.x_original
        self.y = self.y_original

class Bolita:
    VEL_MAX = 5
    COLOR = BLANCO
    
    def __init__(self, x, y, radio):
        self.x = self.x_original = x
        self.y = self.y_original = y
        self.radio = radio
        self.vel_x = self.VEL_MAX
        self.vel_y = 0
    
    def mostrar(self, ventana):
        pg.draw.circle(ventana, self.COLOR, (self.x, self.y), self.radio)
    
    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y
    
    def reset(self):
        self.x = self.x_original
        self.y = self.y_original
        self.vel_y = 0
        self.vel_x *= -1
                
def mostrar(ventana, barritas, bolita, puntuacion_izquierda, puntuacion_derecha):
    ventana.fill(AZUL)
    
    texto_puntuacion_izquierda = FUENTE_PUNTUACION.render(f'{puntuacion_izquierda}', 1, BLANCO) 
    texto_puntuacion_derecha = FUENTE_PUNTUACION.render(f'{puntuacion_derecha}', 1, BLANCO) 
    ventana.blit(texto_puntuacion_izquierda, (ANCHO // 4 - texto_puntuacion_izquierda.get_width() // 2, 20))
    ventana.blit(texto_puntuacion_derecha, (ANCHO * (3/4) - texto_puntuacion_derecha.get_width() // 2, 20))

    for barrita in barritas:
        barrita.mostrar(ventana)
    
    for i in range(10, ALTO, ALTO // 20):
        if i % 2 == 1:
            continue
        
        pg.draw.rect(
            ventana, BLANCO, (ANCHO // 2 - 5, i, 10, ALTO // 20))
    
    bolita.mostrar(ventana)
    
    pg.display.update()

def control_colision(bolita, barrita_izquierda, barrita_derecha):
    if bolita.y + bolita.radio >= ALTO:
        bolita.vel_y *= -1
    elif bolita.y - bolita.radio <= 0:
        bolita.vel_y *= -1 
    
    if bolita.vel_x < 0:
        if bolita.y >= barrita_izquierda.y and bolita.y <= barrita_izquierda.y + barrita_izquierda.alto:
            if bolita.x - bolita.radio <= barrita_izquierda.x + barrita_izquierda.ancho:
                bolita.vel_x *= -1
                
                medio_y = barrita_izquierda.y + barrita_izquierda.alto / 2
                diferencia_en_y = medio_y - bolita.y
                factor_reduccion = (barrita_izquierda.alto / 2) / bolita.VEL_MAX
                vel_y = diferencia_en_y / factor_reduccion
                bolita.vel_y = -1 * vel_y        
    else:
        if bolita.y >= barrita_derecha.y and bolita.y <= barrita_derecha.y + barrita_derecha.alto:
            if bolita.x + bolita.radio >= barrita_derecha.x:
                bolita.vel_x *= -1
                
                medio_y = barrita_derecha.y + barrita_derecha.alto / 2
                diferencia_en_y = medio_y - bolita.y
                factor_reduccion = (barrita_derecha.alto / 2) / bolita.VEL_MAX
                vel_y = diferencia_en_y / factor_reduccion
                bolita.vel_y = -1 * vel_y                   
                
def control_movimiento_barrita(teclas, barrita_izquierda, barrita_derecha):
    if teclas[pg.K_w] and barrita_izquierda.y - barrita_izquierda.VELOCIDAD >= 0:
        barrita_izquierda.mover(arriba=True)
    if teclas[pg.K_s] and barrita_izquierda.y + barrita_izquierda.VELOCIDAD + barrita_izquierda.alto <= ALTO:
        barrita_izquierda.mover(arriba=False)

    if teclas[pg.K_UP] and barrita_derecha.y - barrita_derecha.VELOCIDAD >= 0:
        barrita_derecha.mover(arriba=True)
    if teclas[pg.K_DOWN] and barrita_derecha.y + barrita_derecha.VELOCIDAD + barrita_derecha.alto <= ALTO:
        barrita_derecha.mover(arriba=False)
        
def main():
    encendido = True
    clock = pg.time.Clock()
    
    barrita_izquierda = Barrita(
                        10, ALTO // 2 - ALTO_BARRITA // 2, ANCHO_BARRITA, ALTO_BARRITA)
    barrita_derecha = Barrita(
                        ANCHO - 10 - ANCHO_BARRITA, ALTO // 2 - ALTO_BARRITA // 2, ANCHO_BARRITA, ALTO_BARRITA)
    bolita = Bolita(ANCHO // 2, ALTO // 2, RADIO_BOLITA)
    
    puntuacion_derecha = 0
    puntuacion_izquierda = 0
    
    while encendido: # Mientras el juego este encendido, checa los eventos que hay y si uno es QUIT (salir),
        clock.tick(FPS) 
        mostrar(VENTANA, [barrita_izquierda, barrita_derecha], bolita, puntuacion_izquierda, puntuacion_derecha)
        
        for evento in pg.event.get(): # quita el juego y cierra la ventana finalizando el programa
            if evento.type == pg.QUIT:
                encendido = False
                break
        
        teclas = pg.key.get_pressed()
        control_movimiento_barrita(teclas, barrita_izquierda, barrita_derecha)
        bolita.mover()
        control_colision(bolita, barrita_izquierda, barrita_derecha)
        
        if bolita.x < 0:
            puntuacion_derecha += 1
            bolita.reset()
        elif bolita.x > ANCHO:
            puntuacion_izquierda += 1
            bolita.reset()
        
        ganador = False
        
        if puntuacion_izquierda >= PUNTUACION_GANADORA:
            ganador = True
            texto_ganador = 'El jugador 1 ha ganado'
        elif puntuacion_derecha >= PUNTUACION_GANADORA:
            ganador = True
            texto_ganador = 'El jugador 2 ha ganado'
    
        if ganador:
            texto = FUENTE_PUNTUACION.render(texto_ganador, 1, BLANCO)
            VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
            pg.display.update()
            pg.time.delay(5000)
            bolita.reset()   
            barrita_izquierda.reset()
            barrita_derecha.reset()  
                     
            puntuacion_izquierda = 0
            puntuacion_derecha = 0
            
    pg.quit()

if __name__ == '__main__':
    main()