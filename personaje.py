import pygame
import constantes as c

class Personaje():
    def __init__(self, x, y, animaciones, animacion_ataque,energia,animacion_dano=None):
        self.flip = False
        self.energia = energia
        self.animaciones = animaciones
        self.animacion_dano = animacion_dano if animacion_dano else animaciones
        self.animacion_ataque = animacion_ataque
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.shape = pygame.Rect(0, 0, c.ANCHO_PERSONAJE, c.ALTO_PERSONAJE)
        self.shape.center = (x, y)
        self.atacando = False
        self.recibiendo_golpe = False 
        self.moviendo = False  # Nueva variable para rastrear si el personaje se está moviendo

    def update(self):
        cooldown_animacion = 100

        # Si está recibiendo daño
        if self.recibiendo_golpe:
            self.image = self.animacion_dano[self.frame_index]
            if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animacion_dano):
                self.frame_index = 0
                self.recibiendo_golpe = False  # Volver al estado normal
                self.atacando = False  # Asegúrate de que no ataque si está siendo dañado

        
        # Si está atacando
        if self.atacando:
            self.image = self.animacion_ataque[self.frame_index]
            if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animacion_ataque):
                self.frame_index = 0
                self.atacando = False  # Termina el ataque
        else:
            # Actualiza la animación si el personaje se está moviendo
            if self.moviendo:
                self.image = self.animaciones[self.frame_index]
                if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()
                if self.frame_index >= len(self.animaciones):
                    self.frame_index = 0

    def dibujar(self, interfaz):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(image_flip, self.shape)

    def movimiento(self, delta_x, delta_y):
        
        if delta_x != 0 or delta_y != 0:
            self.moviendo = True  # Se está moviendo
        else:
            self.moviendo = False  # No se está moviendo

        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        
        self.shape.x += delta_x
        self.shape.y += delta_y
    
    def reducir_vida(self, cantidad):
        """Reduce la energía del personaje y activa la animación de daño"""
        self.energia -= cantidad
        if self.energia <= 0:
            self.energia = 0
            print("El personaje ha muerto")

        # Activar la animación de daño
        self.recibiendo_golpe = True
        self.frame_index = 0  # Reiniciar el índice de la animación de daño

    def atacar_enemigo(self, enemigo):
        rango_ataque = 50

        print("Atacando al enemigo")  # Debugging: Ver si se está llamando al método
        print(f"Posición del jugador: {self.shape.x}, {self.shape.y}")
        print(f"Posición del enemigo: {enemigo.shape.x}, {enemigo.shape.y}")
        if self.flip:  # Si el jugador está mirando a la izquierda
            if (self.shape.x - rango_ataque < enemigo.shape.x < self.shape.x and
                abs(self.shape.y - enemigo.shape.y) < rango_ataque):
                enemigo.reducir_vida(10)  # Causar daño al enemigo
                # ...
        else:  # Si el jugador está mirando a la derecha
            if (self.shape.x < enemigo.shape.x < self.shape.x + rango_ataque and
                abs(self.shape.y - enemigo.shape.y) < rango_ataque):
                enemigo.reducir_vida(10)  # Causar daño al enemigo
                # ...

                print("Ataque exitoso, energía del enemigo:", enemigo.energia)  # Mostrar energía
                enemigo.recibiendo_golpe = True  # Activar la animación de daño
                enemigo.frame_index = 0  # Reiniciar el índice de la animación de daño
            
