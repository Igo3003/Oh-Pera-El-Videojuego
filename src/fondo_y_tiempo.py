import pygame, sys
from pygame.locals import *
import pygame_gui
import numpy as np
from .config import *
import os
pygame.init()
a = 1.3
W, H = int(1920 / a), int(1080 / a)
SCREEN = pygame.display.set_mode((W, H))
manager = pygame_gui.UIManager((W, H))
pygame.display.set_caption("Juegoooo")

ruta_icono = os.path.join(SPRITES_DIR, "pera0.png")
icono = pygame.image.load(ruta_icono).convert_alpha()
pygame.display.set_icon(icono)
pygame.display.set_caption("Oh Pera! El Videojuego")

# PALETA
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
BANCO = (240, 240, 240)
PIEL = (255, 200, 180)
DERROTA = (255, 200, 200, 50)
PAUSA = (200, 255, 200, 50)
COLOR_TEXTO = (0, 0, 0)

# Tiempo
FPS = 30
const_tiempo = 60 / FPS
RELOJ = pygame.time.Clock()
raiz = np.sqrt(2) / 2

class Partida:
    def __init__(self):
        self.vol = 0.3
        self.menu_principal = True
        self.menu_controles = False
        self.menu_pausa = False
        self.menu_dificultad = False
        self.menu_logros = False
        self.dificultad = 0
        self.ejecutar = True
        self.juego = True
        self.click = False
        self.derrota = False
        self.empieza = 0
        self.reloj = self.empieza * FPS
        self.tiempo = self.reloj / FPS

        # musica
        self.ruta_cancion = os.path.join(AUDIO_DIR, "P gang pera3.85(8-bit).mp3")
        self.ruta_musica_intro = os.path.join(AUDIO_DIR, "P gang pera3.85(8-bit)-inicio.mp3")
        self.ruta_audio_muerte = os.path.join(AUDIO_DIR, "audio_muerte(8-bit).mp3")
        self.morse_corto = pygame.mixer.Sound(os.path.join(AUDIO_DIR, "morse_corto.wav"))
        self.morse_largo = pygame.mixer.Sound(os.path.join(AUDIO_DIR, "morse_largo.wav"))

        self.fondox = 0
        self.fondo = [
            os.path.join(SPRITES_DIR, "fondo-c.jpg"),
            os.path.join(SPRITES_DIR, "fondo1-c.jpg"),
            [
                os.path.join(SPRITES_DIR, "vladimir_fondo_0.png"),
                os.path.join(SPRITES_DIR, "vladimir_fondo_R.png"),
                os.path.join(SPRITES_DIR, "vladimir_fondo_G.png"),
                os.path.join(SPRITES_DIR, "vladimir_fondo_B.png"),
            ],
            os.path.join(SPRITES_DIR, "calabozo-c.jpg"),
            [
                os.path.join(SPRITES_DIR, "fondo_etapa5a.png"),
                os.path.join(SPRITES_DIR, "fondo_etapa5b.png"),
                os.path.join(SPRITES_DIR, "fondo_etapa5c.png"),
                os.path.join(SPRITES_DIR, "fondo_etapa5d.png"),
                os.path.join(SPRITES_DIR, "fondo_etapa5e.png"),
            ],
            os.path.join(SPRITES_DIR, "melodica_en_llamas-c.png")
        ]
        self.mov_fondox = 2

    def get_fondo(self, index, subindex=None):
        if subindex is None:
            if isinstance(self.fondo[index], str):
                self.fondo[index] = pygame.image.load(self.fondo[index]).convert()
                self.fondo[index] = pygame.transform.scale(self.fondo[index],(W,H))
            return self.fondo[index]
        else:
            if isinstance(self.fondo[index][subindex], str):
                self.fondo[index][subindex] = pygame.image.load(self.fondo[index][subindex]).convert()
                self.fondo[index][subindex] = pygame.transform.scale(self.fondo[index][subindex],(W,H))
            return self.fondo[index][subindex]

    def manejar_musica(self, num): #0: intro, 1: juego, 2: derrota, 3: pausa, 4: despausa, - o . : morse
        pygame.mixer.music.set_volume(self.vol)
        if num == 0:
            pygame.mixer.music.load(self.ruta_musica_intro)
            pygame.mixer.music.play(-1)
        elif num == 1:
            pygame.mixer.music.load(self.ruta_cancion)
            pygame.mixer.music.play(1, self.empieza)
        elif num == 2:
            pygame.mixer.music.load(self.ruta_audio_muerte)
            pygame.mixer.music.play(1)
        elif num == 3:
            pygame.mixer.music.pause()
        elif num == 4:
            pygame.mixer.music.unpause()
        elif num == ".":
            self.morse_corto.play()
        elif num == "-":
            self.morse_largo.play()


class Etapas:
    def __init__(self):
        self.num_etapa = 0
        
        self.inicio_etapa_0 = 0
        self.inicio_etapa_1 = 57.5*FPS
        self.e1_final = 100*FPS
        self.inicio_etapa_2 = 108*FPS
        self.e2_ataque = 114.8*FPS
        self.e2_tiempo_animacion = 240*FPS/140
        self.e2_pausa = 155.95*FPS
        self.inicio_etapa_3 = 164.51*FPS
        self.etapa_3_fuegos = 221.08*FPS
        self.inicio_etapa_4 = 269.08*FPS
        self.inicio_etapa_5 = 281.08*FPS
        self.reloj_entre_etapas = 3*FPS
        self.inicio_etapa_6 = 293.08*FPS
        self.inicio_etapa_7 = 305.08*FPS
        self.entre_7y8 = 317.08*FPS
        self.inicio_etapa_8 = 320.08*FPS
        self.etapa_final = 344.08*FPS
        self.deja_de_moverse = 355.87 * FPS
        self.aparece_final = 363.37 * FPS
        self.termina = 367 * FPS


class Decoraciones():
    def __init__(self,a):
        #texto_derrota
        self.fuente=pygame.font.SysFont("euphorig",int(0.08*W))
        self.fuente_dos=pygame.font.SysFont("euphorig",int(0.04*W))
        self.texto_perdiste=self.fuente.render("PER(A)DISTE",False,COLOR_TEXTO)
        self.txt_ctr=(int((0.3+0.176)*W),int((0.3+0.047)*H))
        self.texto_puntaje=0

        #texto menu principal
        self.Oh_pera=self.fuente.render("Oh Pera! El videojuego",False,COLOR_TEXTO,DERROTA)
        

        #texto pausa
        self.pausado = self.fuente.render("PAUSA",False,COLOR_TEXTO,PAUSA)

        #texto derrota
        self.texto_perdiste=self.fuente.render("PER(A)DISTE",False,COLOR_TEXTO)
        self.pos_texto_perdiste = (int(0.35*W),int(0.2*H))
        self.pos_texto_puntaje = (int(0.36*W),int(0.4*H))

        x_inputs=int(0.25*W)
        y_inputs=0.2
        dif_inputs=0.05
        self.texto_controles=[[self.fuente_dos.render("Moverse: Flechas/WASD",False,COLOR_TEXTO,DERROTA),x_inputs,int(y_inputs*W)],
                        [self.fuente_dos.render("Dash: Espacio ",False,COLOR_TEXTO,DERROTA),x_inputs,int((y_inputs+dif_inputs)*W)],
                        [self.fuente_dos.render("Escudo: E",False,COLOR_TEXTO,DERROTA),x_inputs,int((y_inputs+dif_inputs*2)*W)],
                        [self.fuente_dos.render("Bajar/Subir Volumen: V/B",False,COLOR_TEXTO,DERROTA),x_inputs,int((y_inputs+dif_inputs*3)*W)],
                        [self.fuente_dos.render("Pausa: Esc",False,COLOR_TEXTO,DERROTA),x_inputs,int((y_inputs+dif_inputs*4)*W)]]


def modulo(num):
    if num<0:
        num=-num
    return num




def menu_pausa(partida:Partida,decoraciones:Decoraciones):
    global a
    SCREEN.fill(PAUSA)
    SCREEN.blit(decoraciones.pausado,(int(0.4*W),int(0.2*H)))





#ver en qué etapa estamos

def chequear_etapa(partida:Partida, etapas:Etapas):
    if partida.reloj >=etapas.deja_de_moverse: 
        etapas.num_etapa = 10
    elif partida.reloj >=etapas.etapa_final: 
        etapas.num_etapa = 9
    elif partida.reloj >=etapas.inicio_etapa_8: 
        etapas.num_etapa = 8
    elif partida.reloj >=etapas.inicio_etapa_7: 
        etapas.num_etapa = 7
    elif partida.reloj >=etapas.inicio_etapa_6: 
        etapas.num_etapa = 6
    elif partida.reloj >=etapas.inicio_etapa_5: 
        etapas.num_etapa = 5
    elif partida.reloj >=etapas.inicio_etapa_4: 
        etapas.num_etapa = 4
    elif partida.reloj >=etapas.inicio_etapa_3: 
        etapas.num_etapa = 3
    elif partida.reloj >=etapas.inicio_etapa_2: 
        etapas.num_etapa = 2
    elif partida.reloj >=etapas.inicio_etapa_1: 
        etapas.num_etapa = 1


#     ------------MOVER FONDO -------------

def mover_fondo(partida: Partida, etapas: Etapas):
    if etapas.num_etapa in [0, 1, 4, 6, 8, 9]:
        fondo_en_lista = etapas.num_etapa
        if etapas.num_etapa in [4, 6, 8, 9]:
            fondo_en_lista = 1
        partida.get_fondo(fondo_en_lista)
        fondo = partida.fondo[fondo_en_lista]
        fx_rel = partida.fondox % fondo.get_rect().width
        SCREEN.blit(fondo, (fx_rel - fondo.get_rect().width, 0))
        partida.fondox -= partida.mov_fondox
        if fx_rel < W:
            SCREEN.blit(fondo, (fx_rel, 0))
    elif etapas.num_etapa == 3:
        SCREEN.blit(partida.get_fondo(3), (0, 0))
    elif etapas.num_etapa == 10:
        SCREEN.fill(NEGRO)
        if partida.reloj > etapas.aparece_final:
            SCREEN.blit(partida.get_fondo(5), (0, 0))


def fondo_etapa_tres(partida: Partida, etapas : Etapas):
    retornar = -1
    if partida.reloj < etapas.e2_ataque or partida.reloj > etapas.e2_pausa:
        SCREEN.blit(partida.get_fondo(2, 0), (0, 0))
    elif (partida.reloj - etapas.e2_ataque) % etapas.e2_tiempo_animacion < (1.5 / 8) * etapas.e2_tiempo_animacion:
        SCREEN.blit(partida.get_fondo(2, 1), (0, 0))
        retornar = 0
    elif (partida.reloj - etapas.e2_ataque) % etapas.e2_tiempo_animacion < (3 / 8) * etapas.e2_tiempo_animacion:
        SCREEN.blit(partida.get_fondo(2, 0), (0, 0))
    elif (partida.reloj - etapas.e2_ataque) % etapas.e2_tiempo_animacion < (4.5 / 8) * etapas.e2_tiempo_animacion:
        SCREEN.blit(partida.get_fondo(2, 2), (0, 0))
        retornar = 1
    elif (partida.reloj - etapas.e2_ataque) % etapas.e2_tiempo_animacion < (6 / 8) * etapas.e2_tiempo_animacion:
        SCREEN.blit(partida.get_fondo(2, 0), (0, 0))
    elif (partida.reloj - etapas.e2_ataque) % etapas.e2_tiempo_animacion < (7 / 8) * etapas.e2_tiempo_animacion:
        SCREEN.blit(partida.get_fondo(2, 3), (0, 0))
        retornar = 2
    else:
        SCREEN.blit(partida.get_fondo(2, 0), (0, 0))
    return retornar


def fondo_etapa_cinco_y_siete(partida:Partida, etapas:Etapas):
    if etapas.num_etapa == 5:
        reloj_inicio_etapa = etapas.inicio_etapa_5
    else:
        reloj_inicio_etapa = etapas.inicio_etapa_7

    reloj_entre_fotos = (etapas.inicio_etapa_6 - etapas.inicio_etapa_5) // 4
    tiempo_relativo = partida.reloj - reloj_inicio_etapa
    if partida.reloj <= etapas.entre_7y8:
        if tiempo_relativo <= reloj_entre_fotos:
            SCREEN.blit(partida.get_fondo(4, 1), (0, 0))
            momento = 0
        elif tiempo_relativo < reloj_entre_fotos * 2:
            SCREEN.blit(partida.get_fondo(4, 2), (0, 0))
            momento = 1
        elif tiempo_relativo < reloj_entre_fotos * 3:
            SCREEN.blit(partida.get_fondo(4, 3), (0, 0))
            momento = 2
        else:
            SCREEN.blit(partida.get_fondo(4, 4), (0, 0))
            momento = 3
    else: 
        SCREEN.blit(partida.get_fondo(4, 0), (0, 0))
        momento = -1

    return momento

def mouse_hover(mouse,centro_elemento,ancho_y_alto):
    ejex = mouse[0]-centro_elemento[0]<= ancho_y_alto[0]/2 and mouse[0]-centro_elemento[0]>= -ancho_y_alto[0]/2
    ejey = mouse[1]-centro_elemento[1]<= ancho_y_alto[1]/2 and mouse[1]-centro_elemento[1]>= -ancho_y_alto[1]/2
    return ejex and ejey

def mouse_toca(mouse,centro_elemento,ancho_y_alto):
    click = False
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN: 
            click ==True
    return mouse_hover(mouse,centro_elemento,ancho_y_alto) and click

