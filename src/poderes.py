import pygame,sys
from pygame.locals import *
import numpy as np
import random 
import os
from .fondo_y_tiempo import *


#poderes

class Poderes:          #ATRIBUTOS DE LOS PODERES
    def __init__(self):
        self.tiempos_aparicion=25*FPS
        self.lista_poderes=[]
        self.tamaño_poderes=(64,64)
        self.chances_escudo=0.5
        self.duracion_escudo=5*FPS

class Poder:
    def __init__(self,posx,posy,tipo):
        global FPS
        ruta_vida_extra = os.path.join(SPRITES_DIR, "vida_extra.png")
        ruta_escudo = os.path.join(SPRITES_DIR, "pera_escudo.png")
        if tipo == 0:
            self.image = pygame.image.load(ruta_escudo).convert_alpha()
        if tipo == 1:
            self.image = pygame.image.load(ruta_vida_extra).convert_alpha()
        self.posx = posx
        self.posy = posy
        self.ancho = 64
        self.alto = 64
        self.tipo = tipo
        self.tiempo_restante = 10*FPS


poderes = Poderes()

#       ----------------        PODERES       -----------------

def aparecer_poder(poderes:Poderes):
    chan=random.random()
    if chan>poderes.chances_escudo: #0 = Escudo, 1 = Vida
        tipo=0
    else:
        tipo=1
    posicion=(random.randint(int(W/6),int(5*W/6)),random.randint(int(H/6),int(5*H/6)))
    poder = Poder(posicion[0],posicion[1],tipo)
    if len(poderes.lista_poderes)== 0: 
        poderes.lista_poderes.append(poder)

def tocar_poder(jugador,poderosa):
    poder=False
    centro_poder=((poderosa.posx+poderosa.ancho/2),poderosa.posy+poderosa.alto/2)
    if modulo((centro_poder[0])-(jugador.px+jugador.ancho/2))<((poderosa.ancho+jugador.ancho)/2) and modulo(centro_poder[1]-(jugador.py+jugador.ancho/2))<((poderosa.alto+jugador.ancho)/2):
        poder=True
        if poderosa.tipo==1:
            jugador.vidas+=1
        else:
            jugador.escudos+=1
    return poder

def actualizar_poderes(jugador,poderes:Poderes):
    lista_poderes_nueva=[]
    for elemento in poderes.lista_poderes:
        elemento.tiempo_restante-=1
        if elemento.tiempo_restante>0 and not (tocar_poder(jugador,elemento)):
            lista_poderes_nueva.append(elemento)
    poderes.lista_poderes = lista_poderes_nueva

def escudar(jugador,poderes:Poderes,definir_escudo):
    if jugador.escudos>0 and definir_escudo and jugador.escudo==0:
        jugador.escudos-=1
        jugador.t_invul=poderes.duracion_escudo
        jugador.escudo=jugador.t_invul
        jugador.invulnerable=True
    if jugador.escudo>0:
        jugador.escudo-=1
    elif  jugador.t_invul<=0:
        jugador.invulnerable=False

