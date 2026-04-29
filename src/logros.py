import pygame,sys
from pygame.locals import *
import pygame_gui
import numpy as np
import random 
import os
from .fondo_y_tiempo import *



def leer_logros(cantidad_logros):
    if not os.path.exists(ARCHIVO_LOGROS) or os.stat(ARCHIVO_LOGROS).st_size != cantidad_logros:
        with open(ARCHIVO_LOGROS,"w") as archivo:
            for i in range(cantidad_logros): archivo.write("0")
    lista_logros = [False]*cantidad_logros
    with open(ARCHIVO_LOGROS,"r") as archivo:
        for i in range(cantidad_logros):
            char = archivo.read(1)
            if char =="1": lista_logros[i] = True
            if char =="0": lista_logros[i] = False
    return lista_logros


class Logros():
    def __init__(self):
        self.logros = { "Wandering Trader": False,
                        "¿El Final? (Fácil)":False,
                        "¿El Final? (Medio)":False,
                        "¿El Final? (Difícil)":False,
                        "Código Pera":False,
                        "Huevos Fritos":False}
        self.descripciones = {"Wandering Trader": "Pierde 2 vidas a manos de las llamas (animal) en una partida",
                        "¿El Final? (Fácil)":"Completa el juego (Fácil)",
                        "¿El Final? (Medio)":"Completa el juego (Medio)",
                        "¿El Final? (Difícil)":"Completa el juego (Difícil)",
                        "Código Pera":"Descubre el código secreto",
                        "Huevos Fritos":"Estréllate contra la cabeza de Vladimir"}
        self.lista_logros = leer_logros(len(self.logros))
        for i in range(len(self.lista_logros)):
            self.logros[list(self.logros.keys())[i]]=self.lista_logros[i]
        self.llamas = 0
        self.dificultad = 0
        self.morse = ""
        self.pera_morse =".--...-..-"
        self.huevo = False
        #texto
        self.etiquetas_logros = []
        self.scroll_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((int(0.25*W), int(0.4*H)), (W/2, H/2)),  # Tamaño visible
            manager=manager
        )
        self.interior_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (1*W, 2*H)),  # Tamaño total del contenido
            manager=manager,
            container=self.scroll_container
        )
        tamaño_alerta = (400,50)
        
        self.alerta_interior_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((W- tamaño_alerta[0], 0), tamaño_alerta),  # Tamaño total del contenido
            manager=manager,
        )
        self.alerta_logro = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect( (0, 0), tamaño_alerta),
            text='Esto no debería salir',
            manager=manager,
            visible=0 , # Oculto al inicio
            container=self.alerta_interior_panel
            )
        self.alerta_visible = False
        self.alerta_tiempo_restante = 0*FPS
        self.alerta_tiempo_visible = 5*FPS
        
    def actualizar_logros(self):
        for etiqueta in self.etiquetas_logros:
            etiqueta.kill()
        self.etiquetas_logros.clear()
        i=0
        textito = ""
        for key in list(self.logros.keys()):
            i+=1
            textito = key+": "
            if self.logros[key]:
                textito+="Obtenido\n"+self.descripciones[key]+"\n\n"
            else: textito+="sin obtener\n"
            etiqueta = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 10 +  i* 40), (0.5*W-20, 120)),
                text= textito,
                manager=manager,
                container=self.interior_panel)
            self.etiquetas_logros.append(etiqueta)
    
    def resetear_cosas_de_logros(self):
        self.llamas = 0
        self.morse = ""
    
    def reescribir_logros(self):
        self.lista_logros = leer_logros(len(self.logros))
        for i in range(len(self.lista_logros)):
            self.logros[list(self.logros.keys())[i]]=self.lista_logros[i]
    
    def alertar_logro(self):
        if self.alerta_visible:
            self.alerta_interior_panel.show()
            self.alerta_tiempo_restante-=1
            if self.alerta_tiempo_restante <= 0:
                self.alerta_visible = False
        else: self.alerta_interior_panel.hide()
    def morse_correcto(self,pausa):
        ret = False
        if not self.logros["Código Pera"] and pausa:
            if self.pera_morse in self.morse: 
                self.logros["Código Pera"] = True
                ret = True
                self.alerta_logro.set_text("Logro desbloqueado: Código Pera")
                self.alerta_visible = True
                self.alerta_tiempo_restante = self.alerta_tiempo_visible
        return ret
    def llameado(self,jugar):
        ret = False
        if not self.logros["Wandering Trader"] and jugar and self.llamas >=2:
            ret = True
            self.logros["Wandering Trader"] = True
            self.alerta_logro.set_text("Logro desbloqueado: Wandering Trader")
            self.alerta_visible = True
            self.alerta_tiempo_restante = self.alerta_tiempo_visible
        return ret
    def termino(self,tiempo,jugar):
        ret = False
        if self.dificultad ==0:
            clave = "¿El Final? (Fácil)"
        elif self.dificultad ==1:
            clave = "¿El Final? (Medio)"
        elif self.dificultad ==2:
            clave = "¿El Final? (Difícil)"
        if not self.logros[clave] and jugar:
            if tiempo>360:
                ret = True
                self.logros[clave] = True
                self.alerta_logro.set_text(f"Logro desbloqueado: {clave}")
                self.alerta_visible = True
                self.alerta_tiempo_restante = self.alerta_tiempo_visible
        return ret
    def huevar(self,jugar):
        ret = False
        if jugar and not self.logros["Huevos Fritos"] and self.huevo:
            ret = True
            self.logros["Huevos Fritos"] = True
            self.alerta_logro.set_text("Logro desbloqueado: Huevos Fritos")
            self.alerta_visible = True
            self.alerta_tiempo_restante = self.alerta_tiempo_visible
        return ret
    def sobreescribir_archivo(self)->None:
        with open(ARCHIVO_LOGROS,"w") as archivo:
            for val in list(self.logros.keys()):
                if self.logros[val]==True:
                    archivo.write("1")
                else: archivo.write("0")
    def vaciar_logros(self)-> None:
        for val in list(self.logros.keys()):
            self.logros[val] = False
        self.sobreescribir_archivo()
    def chequear_logros(self,pausa,jugar,tiempo):
        if self.morse_correcto(pausa) or self.llameado(jugar) or self.termino(tiempo,jugar) or self.huevar(jugar):
            self.sobreescribir_archivo()
            self.reescribir_logros()


logros = Logros()

logros.actualizar_logros()
