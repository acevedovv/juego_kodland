import pygame
import constantes as c
from personaje import Personaje
import os


#funciones
def escalar_img(image,scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image,(w*scale,h*scale))
    return nueva_imagen

def mostrar_game_over_y_menu(ventana):
    font = pygame.font.Font(None, 74)
    texto_game_over = font.render("Game Over", True, (255, 0, 0))
    texto_menu = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    ventana.fill((0, 0, 0))
    ventana.blit(texto_game_over, (c.ANCHO_VENTANA // 2 - texto_game_over.get_width() // 2, c.ALTO_VENTANA // 2 - texto_game_over.get_height() // 2 - 50))
    ventana.blit(texto_menu, (c.ANCHO_VENTANA // 2 - texto_menu.get_width() // 2, c.ALTO_VENTANA // 2 + 50))
    pygame.display.update()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    return "reiniciar"
                if event.key == pygame.K_q:  # Salir
                    pygame.quit()
                    exit()
            

animaciones = []
animaciones_enemigos = []
animaciones_princesa = []

pygame.init()
pygame.mixer.init()

ventana = pygame.display.set_mode((c.ANCHO_VENTANA,c.ALTO_VENTANA))
pygame.display.set_caption("Kodland game")

pygame.mixer.music.load("sounds/musiquita.mp3")  # musica
pygame.mixer.music.play(-1)

pygame.font.init()
fuente_game_over = pygame.font.SysFont('Arial', 64)  # Fuente y tamaño del texto


fondo = pygame.image.load("assets/images/background/fondo.webp")
fondo = pygame.transform.scale(fondo, (c.ANCHO_VENTANA, c.ALTO_VENTANA))



#animaciones del personaje principal
for i in range(6):
    img = pygame.image.load(f"assets/images/characters/player/sprite_{i}.png")
    img = escalar_img(img,c.SCALA_PERSONAJE)
    animaciones.append(img)

#animaciones del enemigo
animaciones_ataque = [escalar_img(pygame.image.load(f"assets/images/characters/ataques/attack_{i}.png"), c.SCALA_PERSONAJE) for i in range(5)]

for i in range(8):
    img = pygame.image.load(f"assets/images/characters/enemies/Bringer-of-Death_Walk_{i}.png")
    img = escalar_img(img,c.SCALA_PERSONAJE)
    animaciones_enemigos.append(img)

animaciones_ataque_enemigos = [escalar_img(pygame.image.load(f"assets/images/characters/ataques_enemigos/Bringer-of-Death_Attack_{i}.png"), c.SCALA_PERSONAJE) for i in range(10)]
animaciones_enemigo_atacado = [escalar_img(pygame.image.load(f"assets/images/characters/enemigo_atacado/Bringer-of-Death_Hurt_{i}.png"), c.SCALA_PERSONAJE) for i in range(3)]
#animaciones de la princesa

img = pygame.image.load(f"assets\images\characters\princess\hurt_princess_1.png")
img = escalar_img(img,c.SCALA_PRINCESA)
animaciones_princesa.append(img)
animaciones_princesa_atacada = [escalar_img(pygame.image.load(f"assets\images\characters\princess\hurt_princess_{i}.png"), c.SCALA_PRINCESA) for i in range(4)]



# Inicializar el jugador con la nueva animación de ataque
jugador = Personaje(150, 200, animaciones, animaciones_ataque,100)
enemigo = Personaje(330,255,animaciones_enemigos, animaciones_ataque_enemigos,300)
enemigo.animacion_dano = animaciones_enemigo_atacado
princesa = Personaje(330,255,animaciones_princesa,animaciones_princesa_atacada,100)
princesa.animacion_dano = animaciones_princesa_atacada


mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

x_objetivo = 240
y_objetivo = 160

reloj = pygame.time.Clock()

run = True

while run:

    reloj.tick(c.FPS)

    

    ventana.blit(fondo, (0, 0))

    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = c.VELOCIDAD_PERSONAJE

    if mover_izquierda == True:
        delta_x = -c.VELOCIDAD_PERSONAJE

    if mover_arriba == True:
        delta_y = -c.VELOCIDAD_PERSONAJE

    if mover_abajo == True:
        delta_y = c.VELOCIDAD_PERSONAJE

    
    jugador.movimiento(delta_x,delta_y) #Este codigo me permite mover el personaje
    

    # Dentro del ciclo principal, en la lógica de movimiento del enemigo

    if not enemigo.atacando:
        delta_x = 0
        delta_y = 0

        if abs(enemigo.shape.x - x_objetivo) > 5:
            if enemigo.shape.x < x_objetivo:
                delta_x = c.VELOCIDAD_PERSONAJE
            elif enemigo.shape.x > x_objetivo:
                delta_x = -c.VELOCIDAD_PERSONAJE

        if abs(enemigo.shape.y - y_objetivo) > 5:
            if enemigo.shape.y < y_objetivo:
                delta_y = c.VELOCIDAD_PERSONAJE
            elif enemigo.shape.y > y_objetivo:
                delta_y = -c.VELOCIDAD_PERSONAJE

        # Mueve al enemigo y actualiza la variable de movimiento
        enemigo.movimiento(delta_x, delta_y)

        # Si no se está moviendo, la animación se detiene
        if delta_x == 0 and delta_y == 0:
            enemigo.moviendo = False
        else:
            enemigo.moviendo = True

        # Verificar si el enemigo ha llegado al objetivo
        if abs(enemigo.shape.x - x_objetivo) <= 5 and abs(enemigo.shape.y - y_objetivo) <= 5:
            enemigo.atacando = True
            enemigo.frame_index = 0
            princesa.reducir_vida(10)
            print(f"vida princesa:{princesa.energia}")
            
            if princesa.energia <= 0:


                resultado = mostrar_game_over_y_menu(ventana)
                if resultado == "reiniciar":
                    # Reiniciar el estado del juego
                    jugador.energia = 100
                    enemigo.energia = 300
                    princesa.energia = 100
                    jugador.shape.topleft = (330, 255)
                    enemigo.shape.topleft = (330, 255)
                    jugador.frame_index = 0
                    enemigo.frame_index = 0
                    continue  # Reinicia el bucle principal
                elif resultado == "salir":
                    run = False
                    continue  # Salir del bucle principal

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


    jugador.update()
    enemigo.update()
    princesa.update()

    jugador.dibujar(ventana)
    enemigo.dibujar(ventana)
    princesa.dibujar(ventana)

    for event in pygame.event.get(): #este evento lo que hace es verificar si se presiono x o altf4 para cerrar la ventana
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN: # este evento lo que hace es verificar si se presiono una tecla
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True
            if event.key == pygame.K_SPACE:  # Tecla para atacar (puedes cambiarla)
                jugador.atacando = True  # Activar el estado de ataque
                jugador.frame_index = 0 
                jugador.atacar_enemigo(enemigo)
                print("Energía del enemigo después del ataque:", enemigo.energia)  # Debe mostrar la energía actualizada
                
        
        if event.type == pygame.KEYUP:  # Para manejar la liberación de teclas
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

            
        

    pygame.display.update() #hace que cualquier cambio que suceda en la interfaz se muestre en la pantalla

pygame.quit()