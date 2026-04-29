import pygame,sys
from pygame.locals import *
import pygame_gui
import numpy as np
import random 
import os
from .logros import *
#--------------------------BOTONES ------------------

class Botones():
    def __init__(self):
        self.botones_menu = []
        self.botones_controles = []
        self.botones_pausa = []
        self.botones_derrota = []
        self.botones_dificultad = []
        self.botones_logros = [logros.scroll_container]
        self.lista_listas = [self.botones_menu,self.botones_controles,self.botones_pausa,self.botones_derrota,self.botones_dificultad,self.botones_logros]

    def ocultar_botones(self,lista_de_botones:list[pygame_gui.elements.UIButton]):
        for boton in lista_de_botones:
            boton.hide()

    def revelar_botones(self,lista_de_botones:list[pygame_gui.elements.UIButton]):
        for boton in lista_de_botones:
            boton.show()
    
    def revelar_y_ocultar(self,rev:int):
        for i in range(len(self.lista_listas)):
            if i == rev:
                self.revelar_botones(self.lista_listas[i])
            else: 
                self.ocultar_botones(self.lista_listas[i])

def crear_boton(posición : tuple[int,int],tamaño : tuple[int,int],texto: str,lista_de_botones:list,imagen = 0,manejador=manager):
    
    boton =  pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(posición, tamaño),
    text=texto,
    manager=manejador)
    if imagen!=0:
        boton.set_image(imagen)
    lista_de_botones.append(boton)
    return boton


botones = Botones()

# --------------BOTONES MENU ---------------
boton_jugar = crear_boton((int(0.45*W),int(0.4*H)),(176/a,36/a),"JUGAR",botones.botones_menu)
boton_controles = crear_boton((int(0.413*W),int(0.5*H)),(325/a,52/a),"CONTROLES",botones.botones_menu)
boton_logros = crear_boton((int(0.45*W),int(0.6*H)),(176/a,36/a),"LOGROS",botones.botones_menu)

# --------------BOTONES CONTROLES ---------------
ruta_boton_atras = os.path.join(SPRITES_DIR, "boton_de_atras.png")
img_boton_atras = pygame.image.load(ruta_boton_atras).convert_alpha()
boton_controles_atras = crear_boton((0,0),(64,64),"",botones.botones_controles,img_boton_atras)

# --------------BOTONES PAUSA ---------------
boton_reanudar =  crear_boton( (int(0.45*W),int(0.5*H)), (192,32),"Reanudar",botones.botones_pausa)
boton_volver_al_menu = crear_boton( (int(0.35*W),int(0.6*H)), (470,32),"Volver al Menú Principal",botones.botones_pausa)
boton_reiniciar =  crear_boton( (int(0.45*W),int(0.7*H)), (192,32),"Reiniciar",botones.botones_pausa)


ruta_morsa = os.path.join(SPRITES_DIR, "pera0-c.png")
img_morsa = pygame.image.load(ruta_morsa).convert_alpha()
boton_morse_corto = crear_boton((int(0.1*W),int(0.5*H)),(64,64),".",botones.botones_pausa,img_morsa)
boton_morse_largo = crear_boton((int(0.1*W),int(0.6*H)),(64,64),"_",botones.botones_pausa,img_morsa)

# --------------BOTONES DERROTA ---------------
boton_volver_a_jugar = crear_boton((int(0.45*W),int(0.5*H)),(200,32),"Volver a Jugar",botones.botones_derrota)
boton_derrota_al_menu = crear_boton((int(0.45*W),int(0.6*H)),(200,32),"Volver al menú",botones.botones_derrota)

# --------------BOTONES DIFICULTAD ---------------
boton_dif_facil = crear_boton((int(0.45*W),int(0.4*H)),(200,32),"Fácil",botones.botones_dificultad)
boton_dif_media = crear_boton((int(0.45*W),int(0.5*H)),(200,32),"Media",botones.botones_dificultad)
boton_dif_dificil = crear_boton((int(0.45*W),int(0.6*H)),(200,32),"Difícil",botones.botones_dificultad)
boton_dif_volver_atras = crear_boton((int(0.45*W),int(0.7*H)),(200,32),"Volver al menú",botones.botones_dificultad)

# --------------BOTONES LOGROS ---------------
boton_logros_atras = crear_boton((0,0),(64,64),"",botones.botones_logros,img_boton_atras)
boton_logros_borrar = crear_boton((0,H-64),(180,64),"Borrar Logros Obtenidos",botones.botones_logros)
