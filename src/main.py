import pygame,sys
from pygame.locals import *
import pygame_gui
import numpy as np
import random 
import os
from .jugador import *
from .enemigos import *
from .poderes import *
from .botones import *

jugador = Jugador()
backup_jugador = Jugador()
partida = Partida()

enemigos_facil = Enemigos(40,120,6,100)
enemigos_media = Enemigos(30,105,9,85)
enemigos_dificil = Enemigos(25,90,12,70)

enemigos= enemigos_facil #Defino al elegir la dificultad

etapas = Etapas()
decoraciones = Decoraciones(a)

#                --------------------------    DERROTA ------------------
def perder(jugador :Jugador,partida:Partida):

    if not jugador.invulnerable:
        jugador.vidas-=1
        if jugador.vidas==0:
            SCREEN.fill(DERROTA)
            partida.juego=False
        else:
            jugador.t_invul=FPS #1 segundo de invulnerabilidad


def resetear_variables_a_inicio(jugador:Jugador,partida:Partida,poderes :Poderes,enemigos:Enemigos,etapas:Etapas,decoraciones:Decoraciones):
    global primer_frame_de_muerte
    jugador.t_invul=backup_jugador.t_invul
    jugador.vidas=backup_jugador.vidas
    jugador.escudos=backup_jugador.escudos
    jugador.px=backup_jugador.px
    jugador.py=backup_jugador.py
    jugador.tiempo_dash=backup_jugador.tiempo_dash
    partida.derrota=False
    partida.reloj=partida.empieza*FPS
    partida.juego=True
    partida.manejar_musica(1)
    enemigos.lista_enemigos_normal=[]
    enemigos.lista_enemigos_siguen_pj=[]
    poderes.lista_poderes = []
    enemigos.Vladimir = False
    etapas.num_etapa = 0
    decoraciones.texto_puntaje=0
    primer_frame_de_muerte = True


def menu_derrota(partida:Partida, decoraciones:Decoraciones):
    SCREEN.fill(DERROTA)
    botones.revelar_y_ocultar(3)
    decoraciones.tiempo_sobrevivido = partida.tiempo
    if not partida.derrota:
        partida.derrota=True


def recargarPantalla(jugador:Jugador,partida:Partida,poderes:Poderes,enemigos:Enemigos,etapas:Etapas,decoraciones:Decoraciones):
    manager.update(RELOJ.get_time() / 1000)
    logros.alertar_logro()
    if partida.menu_principal:
        etapas.num_etapa = 0
        mover_fondo(partida,etapas)
        if partida.menu_controles:
            botones.revelar_y_ocultar(1)
            for i in decoraciones.texto_controles:
                SCREEN.blit(i[0],(i[1],i[2]))
            
        elif partida.menu_dificultad:
            botones.revelar_y_ocultar(4)
        elif partida.menu_logros:
            botones.revelar_y_ocultar(5)
        else:
            SCREEN.blit(decoraciones.Oh_pera,(int(0.2*W),int(0.2*H)))
            botones.revelar_y_ocultar(0)
    elif partida.menu_pausa:
        botones.revelar_y_ocultar(2)
        menu_pausa(partida,decoraciones)
    else:
        if partida.juego:
            botones.revelar_y_ocultar(-1)
            if etapas.num_etapa<10:
                SCREEN.blit(jugador.image,(int(jugador.px),int(jugador.py)))
                if jugador.escudo!=0:SCREEN.blit(jugador.escudo_im[4*jugador.escudo//poderes.duracion_escudo],(int(jugador.px),int(jugador.py)))
                for enemigo in enemigos.lista_enemigos_normal:
                    SCREEN.blit(enemigo.image,(enemigo.posx,enemigo.posy))
                for enemigo in enemigos.lista_enemigos_siguen_pj:
                    SCREEN.blit(enemigo.image,(enemigo.posx,enemigo.posy))
                for poder in poderes.lista_poderes:
                    SCREEN.blit(poder.image,(poder.posx,poder.posy))
                for i in range(jugador.vidas-1):
                    SCREEN.blit(jugador.imagen_vida_extra,((jugador.ancho+0.01*W)*i,0.01*i))
                for i in range(jugador.escudos):
                    SCREEN.blit(jugador.imagen_escudo,((jugador.ancho+0.01*W)*i,0.01*i+jugador.alto))
        else:
            SCREEN.blit(decoraciones.texto_perdiste,decoraciones.pos_texto_perdiste)
            decoraciones.texto_puntaje=decoraciones.fuente_dos.render(f"Tiempo sobrevivido: {int(partida.tiempo)}s",False,COLOR_TEXTO) #Lo tengo que hacer acá para que se actualice el tiempo
            SCREEN.blit(decoraciones.texto_puntaje,decoraciones.pos_texto_puntaje)
    pygame.mixer.music.set_volume(partida.vol)
    manager.draw_ui(SCREEN)
    pygame.display.update()


def chequear_eventos(event,enemigos = enemigos,botones:Botones = botones,logros:Logros = logros,partida:Partida = partida):
    if event.type==pygame.QUIT:
        partida.ejecutar=False
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #---------menu -----
        if event.ui_element == botones.botones_menu[0]:
            partida.menu_dificultad = True
        elif event.ui_element == botones.botones_menu[1]:
            partida.menu_controles = True
        elif event.ui_element == botones.botones_menu[2]:
            partida.menu_logros = True
            logros.actualizar_logros()
        #------controles ---------
        elif event.ui_element == botones.botones_controles[0]:
            partida.menu_controles = False
        #------pausa ------
        elif event.ui_element == botones.botones_pausa[0]:
            partida.menu_pausa = False
            partida.manejar_musica(4)
        elif event.ui_element == botones.botones_pausa[1]:
            partida.juego = False
            partida.menu_pausa = False
            partida.menu_principal = True
            partida.manejar_musica(0)
        elif event.ui_element == botones.botones_pausa[2]:
            partida.menu_pausa = False
            resetear_variables_a_inicio(jugador,partida,poderes,enemigos,etapas,decoraciones)
        elif event.ui_element == botones.botones_pausa[3]:
            logros.morse+="."
            partida.manejar_musica(".")
        elif event.ui_element == botones.botones_pausa[4]:
            logros.morse+="-"
            partida.manejar_musica("-")
        #---- derrota ----
        elif event.ui_element == botones.botones_derrota[0]:
            resetear_variables_a_inicio(jugador,partida,poderes,enemigos,etapas,decoraciones)
        elif event.ui_element == botones.botones_derrota[1]:
            partida.menu_principal = True
            partida.manejar_musica(0)
        #---dificultad ----
        elif event.ui_element == botones.botones_dificultad[0]:
            partida.menu_dificultad = False
            partida.menu_principal = False
            partida.dificultad = 0
            logros.dificultad = 0
            enemigos.copiar_a_otro(enemigos_facil)
            resetear_variables_a_inicio(jugador,partida,poderes,enemigos,etapas,decoraciones)
        elif event.ui_element == botones.botones_dificultad[1]:
            partida.menu_dificultad = False
            partida.menu_principal = False
            partida.dificultad = 1
            logros.dificultad = 1
            enemigos.copiar_a_otro(enemigos_media)
            resetear_variables_a_inicio(jugador,partida,poderes,enemigos,etapas,decoraciones)
        elif event.ui_element == botones.botones_dificultad[2]:
            partida.menu_dificultad = False
            partida.menu_principal = False
            partida.dificultad = 2
            logros.dificultad = 2
            enemigos.copiar_a_otro(enemigos_dificil)
            resetear_variables_a_inicio(jugador,partida,poderes,enemigos,etapas,decoraciones)
        elif event.ui_element == botones.botones_dificultad[3]:
            partida.menu_dificultad = False
            partida.menu_principal = True
        #----logros------
        elif event.ui_element == botones.botones_logros[1]:
            partida.menu_logros = False
        elif event.ui_element == botones.botones_logros[2]:
            logros.vaciar_logros()
            logros.actualizar_logros()
            logros.resetear_cosas_de_logros()


primera = True #usado para que se reproduzca la música en el menú
primer_frame_de_muerte = True
while partida.ejecutar:
    #fps
    RELOJ.tick(FPS)
    logros.chequear_logros(partida.menu_pausa,partida.juego,partida.tiempo)
    #bucle
    for event in pygame.event.get():
        manager.process_events(event)
        chequear_eventos(event)
    if partida.menu_principal:
        if primera:
            primera = False
            partida.manejar_musica(0)
    elif not partida.menu_pausa:
        if partida.juego:
            partida.tiempo=partida.reloj/FPS
            partida.reloj=((partida.empieza*1000+pygame.mixer.music.get_pos())*FPS)//1000            
            movimiento(jugador,partida)
            if partida.reloj%poderes.tiempos_aparicion==0:
                aparecer_poder(poderes)
            actualizar_poderes(jugador,poderes)
            enemigos.generador_enemigos+=1
            mover_enemigos_normal(enemigos)
            mover_enemigos_que_siguen_pj(jugador,enemigos)
            if chequear_colision(jugador,enemigos):
                perder(jugador,partida)
            if etapas.num_etapa in [0,1,3,4,6,8,9,10]:
                mover_fondo(partida,etapas)
            
            if etapas.num_etapa == 0:
                crear_llama(enemigos)
            
            if etapas.num_etapa==1:
                if partida.reloj<etapas.e1_final:
                    crear_angel(enemigos)
            
            if etapas.num_etapa>=2 and etapas.num_etapa<=10 and not enemigos.Vladimir:
                crear_vladimir(enemigos)
            if etapas.num_etapa==2:
                if partida.reloj<etapas.e2_pausa:
                    momento=fondo_etapa_tres(partida,etapas)
                    if momento != -1 : 
                        if fondo_enemigo(jugador,enemigos,momento):
                            perder(jugador,partida)
                else:
                    fondo_etapa_tres(partida,etapas)
            
            if etapas.num_etapa==3:
                if partida.reloj < etapas.etapa_3_fuegos:
                    crear_nota(partida,enemigos,etapas)
                else:
                    crear_fuego(enemigos)
            
            if etapas.num_etapa==4 or etapas.num_etapa==6:
                crear_fuego(enemigos)
            if etapas.num_etapa==5 or etapas.num_etapa==7:
                if partida.reloj < etapas.entre_7y8:
                    momento=fondo_etapa_cinco_y_siete(partida,etapas)
                    crear_nota(partida,enemigos,etapas,1/2)
                    if colision_fondo_final(jugador,enemigos.lista_fondos[momento]):
                        perder(jugador,partida)
            if etapas.num_etapa==8:
                crear_fuego(enemigos,1/4)
                crear_nota(partida,enemigos,etapas,1/5)
            if etapas.num_etapa == 10:
                enemigos.lista_enemigos_normal=[]
                enemigos.lista_enemigos_siguen_pj =[]
                enemigos.Vladimir = False #No cambia pero por las dudas
            if partida.reloj >etapas.termina: 
                partida.menu_principal=True
                resetear_variables_a_inicio(jugador,partida,poderes,enemigos,etapas,decoraciones)
                partida.manejar_musica(0)
            chequear_etapa(partida,etapas)
        else:
            if primer_frame_de_muerte:
                primer_frame_de_muerte = False
                partida.manejar_musica(2)
            menu_derrota(partida,decoraciones)
    recargarPantalla(jugador,partida,poderes,enemigos,etapas,decoraciones)


pygame.quit()
