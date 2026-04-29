import pygame,sys
from pygame.locals import *
import numpy as np
import random 
import os
from .fondo_y_tiempo import *
from .poderes import escudar,poderes


#variables del jugador

class Jugador:
    def __init__(self):
        global const_tiempo
        ruta_image = os.path.join(SPRITES_DIR, "pera0-c.png")
        self.image=pygame.image.load(ruta_image).convert_alpha()
        ruta_vida_extra = os.path.join(SPRITES_DIR, "pera_vida_extra_transparente.png")
        ruta_escudo = os.path.join(SPRITES_DIR, "pera_escudo_transparente.png")
        self.imagen_vida_extra = pygame.image.load(ruta_vida_extra).convert_alpha()
        self.imagen_escudo = pygame.image.load(ruta_escudo).convert_alpha()
        ruta_esc1 = os.path.join(SPRITES_DIR, "pera_escudo1.png")
        ruta_esc2 = os.path.join(SPRITES_DIR, "pera_escudo2.png")
        ruta_esc3 = os.path.join(SPRITES_DIR, "pera_escudo3.png")
        ruta_esc0 = os.path.join(SPRITES_DIR, "pera_escudo0.png")
        self.escudo_im=[pygame.image.load(ruta_esc1).convert_alpha(),pygame.image.load(ruta_esc2).convert_alpha(),pygame.image.load(ruta_esc3).convert_alpha(),pygame.image.load(ruta_esc0).convert_alpha()]
        self.px = W//2
        self.py = H//2
        self.ancho = 64
        self.alto = 64
        
        #movimiento
        self.vel = 10*const_tiempo
        self.velocidad=self.vel
        self.cte_dash=4
        self.cldn_dash=1
        self.arriba=False
        self.abajo=False
        self.izquierda=False
        self.derecha=False
        self.cuentaPasos=0
        #poderes
        self.invulnerable = False
        self.escudos = 1
        self.escudo = 0
        self.vidas = 3
        self.t_invul = 2*FPS
        self.tiempo_dash = 0


#     -------------- MOVIMIENTO JUGADOR  ---------------------



def movimiento(jugador:Jugador,partida:Partida):
    keys=pygame.key.get_pressed()
    jugador.t_invul-=1
    if jugador.t_invul>0:
        jugador.invulnerable=True
    elif jugador.t_invul<=0:
        jugador.invulnerable=False
    escudar(jugador,poderes,keys[pygame.K_e])
    dash=keys[pygame.K_SPACE]
    kl=keys[pygame.K_LEFT]  or keys[pygame.K_a]
    kr=keys[pygame.K_RIGHT]  or keys[pygame.K_d]
    kd=keys[pygame.K_DOWN]  or keys[pygame.K_s]
    ku=keys[pygame.K_UP]  or keys[pygame.K_w]
    if jugador.px>W-jugador.ancho/2: jugador.px=-jugador.ancho/2
    if jugador.px<-jugador.ancho/2: jugador.px=W-jugador.ancho/2
    if jugador.py<-jugador.ancho/2: jugador.py=H-jugador.ancho/2
    if jugador.py>H-jugador.ancho/2: jugador.py=-jugador.ancho/2
    if dash and (partida.tiempo-jugador.tiempo_dash)>jugador.cldn_dash:
        if jugador.velocidad==jugador.vel:
            jugador.velocidad*=jugador.cte_dash
            jugador.tiempo_dash=partida.tiempo
    if jugador.velocidad>jugador.vel:
        jugador.velocidad-=jugador.vel*jugador.cte_dash/(0.2*FPS)
    if jugador.velocidad<jugador.vel:
        jugador.velocidad = jugador.vel
    
    if kl and ku:
        jugador.px-=(jugador.velocidad*raiz)
        jugador.py-=(jugador.velocidad*raiz)
        jugador.arriba=True
        jugador.abajo=False
        jugador.izquierda=True
        jugador.derecha=False
    elif kr and ku:
        jugador.px+=(jugador.velocidad*raiz)
        jugador.py-=(jugador.velocidad*raiz)
        jugador.arriba=True
        jugador.abajo=False
        jugador.izquierda=False
        jugador.derecha=True
    elif kl and kd:
        jugador.px-=(jugador.velocidad*raiz)
        jugador.py+=(jugador.velocidad*raiz)
        jugador.arriba=False
        jugador.abajo=True
        jugador.izquierda=True
        jugador.derecha=False
    elif kr and kd:
        jugador.px+=(jugador.velocidad*raiz)
        jugador.py+=(jugador.velocidad*raiz)
        jugador.arriba=False
        jugador.abajo=True
        jugador.izquierda=False
        jugador.derecha=True
    elif kl:
        jugador.px-=jugador.velocidad
        jugador.izquierda=True
        jugador.derecha=False
    elif kr:
        jugador.px+=jugador.velocidad
        jugador.derecha=True
        jugador.izquierda=False
    elif kd:
        jugador.py+=jugador.velocidad
        jugador.abajo=True
        jugador.arriba=False
    elif ku:
        jugador.py-=jugador.velocidad
        jugador.arriba=True
        jugador.abajo=False
    else:
        jugador.arriba=False
        jugador.abajo=False
        jugador.izquierda=False
        jugador.derecha=False
    if keys[pygame.K_v]:
        partida.vol-=0.02
    if keys[pygame.K_b]:
        partida.vol+=0.02
    if keys[pygame.K_ESCAPE]:
            if partida.juego:
                partida.menu_pausa = True
                partida.manejar_musica(3)
            if partida.menu_controles:
                partida.menu_controles=False
                partida.menu_principal=True

