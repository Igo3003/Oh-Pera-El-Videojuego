import pygame,sys
from pygame.locals import *
import numpy as np
import random 
import os
from .logros import *


#                   -----   ENEMIGOS    ------

class Dificultad():
    def __init__(self,Llamas,Angel,Notas,Fuego):
        self.v_spawnLL=int(Llamas/const_tiempo) #a menor v, más rápido
        self.v_spawnAN=int(Angel/const_tiempo)
        self.notas_creadas=Notas
        self.v_spawnFU=int(Fuego/const_tiempo)

class Enemigos(Dificultad):
    def __init__(self,Llamas,Angel,Notas,Fuego):
        super().__init__(Llamas,Angel,Notas,Fuego)
        self.lista_enemigos_siguen_pj = []
        self.lista_enemigos_normal = []
        self.lista_fonditos = [[Fondito(0,0),Fondito(0,3),Fondito(1,2),Fondito(1,5),Fondito(2,0),Fondito(2,3),Fondito(3,2),Fondito(3,5),Fondito(4,0),Fondito(4,3),Fondito(5,2),Fondito(5,5)], 
                            [Fondito(0,1),Fondito(0,4),Fondito(1,0),Fondito(1,3),Fondito(2,1),Fondito(2,4),Fondito(3,0),Fondito(3,3),Fondito(4,1),Fondito(4,4),Fondito(5,0),Fondito(5,3)], 
                            [Fondito(0,2),Fondito(0,5),Fondito(1,1),Fondito(1,4),Fondito(2,2),Fondito(2,5),Fondito(3,1),Fondito(3,4),Fondito(4,2),Fondito(4,5),Fondito(5,1),Fondito(5,4)]]
        self.lista_fondos = [Fondo(0,0),Fondo(0,1),Fondo(1,0),Fondo(1,1)]
        self.Vladimir = False
        self.generador_enemigos = 0   #contador que cuando llega al v_spawn del momento genera dicho enemigo
        
        self.chances_llama = 0.15 #chances de que aparezca una llama sobre 1
        self.tiempo_animacion_notas=int(240*FPS/140)
    
    def copiar_a_otro(self,otro):
        self.v_spawnLL = otro.v_spawnLL
        self.v_spawnAN = otro.v_spawnAN
        self.notas_creadas = otro.notas_creadas
        self.v_spawnFU = otro.v_spawnFU

class Llama():
    def __init__(self,posx):
        global const_tiempo
        self.ruta_img = os.path.join(SPRITES_DIR, "llama.png")
        self.image = pygame.image.load(self.ruta_img).convert_alpha()
        self.vy = 3*const_tiempo
        self.vx = 1*const_tiempo
        self.ancho = 48
        self.alto = 48
        self.posx = posx
        self.posy = -self.alto
        self.direccion = 0


class Llamas():
    def __init__(self,posx):
        global const_tiempo
        self.ruta_img = os.path.join(SPRITES_DIR, "llamas.png")
        self.image = pygame.image.load(self.ruta_img).convert_alpha()
        self.vy = 3*const_tiempo
        self.vx = 1*const_tiempo
        self.ancho = 48
        self.alto = 48
        self.posx = posx
        self.posy = -self.alto
        self.direccion = 0


class Aro():
    def __init__(self,posx,posy,direccion):
        global const_tiempo
        self.ruta_img = os.path.join(SPRITES_DIR, "angel_aro.png")
        self.image = pygame.image.load(self.ruta_img).convert_alpha()
        self.vy = 2*const_tiempo
        self.vx = 2*const_tiempo
        self.ancho = 64
        self.alto = 64
        self.posx = posx
        self.posy = posy
        self.direccion = direccion #0 es vertical, 1 es horizontal


class Vladimir():
    def __init__(self):
        global const_tiempo,W,H
        self.ruta_img = os.path.join(SPRITES_DIR, "Vladimir.jpeg")
        self.image = pygame.image.load(self.ruta_img).convert()
        self.vy = 0*const_tiempo
        self.vx = 0*const_tiempo
        self.ancho = 143
        self.alto = 180
        self.posx = (W-self.ancho)//2
        self.posy = (H-self.alto)//2


class Fondito():
    def __init__(self,fila,columna): # fila y columna contando desde 0 a 5
        global W,H
        self.ancho = W//6
        self.alto = H//6
        self.posx = self.ancho*columna
        self.posy = self.alto*fila 

class Fondo():
    def __init__(self,fila,columna): # fila y columna contando desde 0 a 1
        global W,H
        self.ancho = W//2
        self.alto = H//2
        self.posx = self.ancho*columna
        self.posy = self.alto*fila 



class Bajo():
    def __init__(self):
        global const_tiempo,W,H
        self.ruta_img = os.path.join(SPRITES_DIR, "bajo_ladimir.png")
        self.image = pygame.image.load(self.ruta_img).convert_alpha()
        self.vy = 0*const_tiempo
        self.vx = 0*const_tiempo
        self.ancho = 160
        self.alto = 64
        self.posx = 0.45*W
        self.posy = 0.55*H

class Nota():
    def __init__(self,vx,vy):
        global const_tiempo,W,H
        self.ruta_img = os.path.join(SPRITES_DIR, "nota_enemiga.png")
        self.image = pygame.image.load(self.ruta_img).convert_alpha()
        self.vel = 6*const_tiempo
        self.vy = vx*self.vel
        self.vx = vy*self.vel
        self.ancho = 48
        self.alto = 48
        self.posx = (W-self.ancho)//2
        self.posy = (H-self.alto)//2

class Fuego_angel():
    def __init__(self,posx,posy,direccion):
        global const_tiempo
        self.ruta_img = os.path.join(SPRITES_DIR, "fuego_angel.png")
        self.image = pygame.image.load(self.ruta_img).convert_alpha()
        self.vy = 3.5*const_tiempo
        self.vx = 3.5*const_tiempo
        self.ancho = 48
        self.alto = 48
        self.posx = posx
        self.posy = posy
        self.direccion = direccion #0 es vertical, 1 es horizontal



#                               ----------      COLISIONES      ---------------


def chequear_enemigo(jugador,enemigo:Llama,logros = logros):
    devolver=False
    centrox=jugador.px+jugador.ancho/2
    centroy=jugador.py+jugador.alto/2
    enem_cx=enemigo.posx+enemigo.ancho/2
    enem_cy=enemigo.posy+enemigo.alto/2
    dist_x=modulo(centrox-enem_cx) < (jugador.ancho/2+enemigo.ancho/2)
    if dist_x:
        dist_y=modulo(centroy-enem_cy) < (jugador.alto/2+enemigo.alto/2)
        if dist_y:
            if hasattr(enemigo,"ruta_img"):
                if enemigo.ruta_img == os.path.join(SPRITES_DIR, "llama.png") and not jugador.invulnerable:
                    logros.llamas+=1
                if not jugador.invulnerable and enemigo.ruta_img ==os.path.join(SPRITES_DIR, "Vladimir.jpeg"):
                    logros.huevo = True
            devolver=True
    return devolver

def chequear_colision(jugador,enemigos:Enemigos):
    perdio=False
    if not jugador.invulnerable:
        i=0
        while i<len(enemigos.lista_enemigos_normal) and not perdio:
            perdio=chequear_enemigo(jugador,enemigos.lista_enemigos_normal[i])
            i+=1
        i = 0
        while i<len(enemigos.lista_enemigos_siguen_pj) and not perdio:
            perdio=chequear_enemigo(jugador,enemigos.lista_enemigos_siguen_pj[i])
            i+=1
    return perdio


def colision_fondo_final(jugador,casilla_fondo): #Para el final
    perdio = False
    if not jugador.invulnerable:
        perdio = chequear_enemigo(jugador,casilla_fondo)
    return perdio

def fondo_enemigo(jugador,enemigos:Enemigos,momento):#Recibe la lista de fonditos del momento
    perdio=False
    i=0
    while i<12 and not perdio:
        perdio=chequear_enemigo(jugador,enemigos.lista_fonditos[momento][i])
        i+=1
    
    return perdio

#                               ----------      CREAR ENEMIGOS      ---------------
#         ETAPA 1
def crear_llama(enemigos: Enemigos):
    if enemigos.generador_enemigos%enemigos.v_spawnLL==0:
        x=random.randrange(W)
        if random.random()<enemigos.chances_llama:
            enemigo = Llama(x)
        else:
            enemigo = Llamas(x)
        
        enemigos.lista_enemigos_siguen_pj.append(enemigo)


#     ETAPA 2
def crear_angel(enemigos:Enemigos):
    if enemigos.generador_enemigos%enemigos.v_spawnAN==0:
        select=random.random()
        if select>0.75:
            x=random.randrange(W)
            enemigo = Aro(x,0,0)
        elif select>0.5:
            y=random.randrange(H)
            enemigo = Aro(0,y,1)
        elif select>0.25:
            x=random.randrange(W)
            enemigo = Aro(x,H,0)
            enemigo.vy*=-1
        else:
            y=random.randrange(H)
            enemigo = Aro(W,H,1)
            enemigo.vx *=-1
        
        enemigos.lista_enemigos_siguen_pj.append(enemigo)






def crear_vladimir(enemigos:Enemigos):
    vladimir = Vladimir()
    enemigos.Vladimir = True
    enemigos.lista_enemigos_normal.append(vladimir)



def crear_nota(partida:Partida, enemigos:Enemigos, etapas:Etapas,cantidad =1):
    reloj_inicio_notas=etapas.inicio_etapa_3
    if partida.reloj>=reloj_inicio_notas:
        verificar=int((partida.reloj-reloj_inicio_notas)%(enemigos.tiempo_animacion_notas))
        if verificar==0 or verificar==int((3/8)*enemigos.tiempo_animacion_notas) or verificar==int((6/8)*enemigos.tiempo_animacion_notas):
            for i in range(int(enemigos.notas_creadas*cantidad)):
                lis=[1,-1]
                vx=random.random()*lis[random.randint(0,1)]
                vy=np.sqrt(1-(vx)**2)*lis[random.randint(0,1)]
                enemigo = Nota(vx,vy)
                enemigos.lista_enemigos_normal.append(enemigo)



#etapa 4
def crear_fuego(enemigos:Enemigos,cantidad =1):# a mayor cantidad, más aparecen
    if int(enemigos.generador_enemigos*cantidad)%enemigos.v_spawnFU==0:
        select=random.random()
        if select>0.75:
            x=random.randrange(W)
            enemigo = Fuego_angel(x,0,0)
        elif select>0.5:
            y=random.randrange(H)
            enemigo = Fuego_angel(0,y,1)
        elif select>0.25:
            x=random.randrange(W)
            enemigo = Fuego_angel(x,H,0)
            enemigo.vy*=-1
        else:
            y=random.randrange(H)
            enemigo = Fuego_angel(W,H,1)
            enemigo.vx *=-1
        
        enemigos.lista_enemigos_siguen_pj.append(enemigo)





#---------------------- MOVER ENEMIGOS ------------------------

def mover_enemigos_que_siguen_pj(jugador,enemigos:Enemigos):
    nueva_lista = []
    for enemigo in enemigos.lista_enemigos_siguen_pj:
        if enemigo.direccion==0:
            enemigo.posy+=enemigo.vy
            if int(enemigo.posx)>int(jugador.px)+1:
                enemigo.posx-=enemigo.vx
            elif int(enemigo.posx)<int(jugador.px)-1:
                enemigo.posx+=enemigo.vx
            if not(enemigo.posy>H or enemigo.posy<-enemigo.alto):
                nueva_lista.append(enemigo)
        else:
            enemigo.posx+=enemigo.vx
            if int(enemigo.posy)>1+int(jugador.py):
                enemigo.posy-=enemigo.vy
            elif int(enemigo.posy)<int(jugador.py)-1:
                enemigo.posy+=enemigo.vy
            if not(enemigo.posx>W or enemigo.posx<-enemigo.ancho):
                nueva_lista.append(enemigo)
        enemigos.lista_enemigos_siguen_pj = nueva_lista



def mover_enemigos_normal(enemigos:Enemigos):
    nueva_lista = []
    for enemigo in enemigos.lista_enemigos_normal:
        enemigo.posx += enemigo.vx
        enemigo.posy += enemigo.vy
        if not(enemigo.posx<-enemigo.ancho or enemigo.posx > W or enemigo.posy <-enemigo.alto or enemigo.posy > H):
            nueva_lista.append(enemigo)
        enemigos.lista_enemigos_normal = nueva_lista