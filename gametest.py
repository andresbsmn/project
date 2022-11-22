import math
import time


import numpy as np
import sdl2.ext

from levels import *

# Constanten
BREEDTE = 800
HOOGTE = 600
tijd_verstrekentot = 0 # var aanmaken
deadline = 10
#
# Globale variabelen
#

# positie van de speler
p_speler = np.array([5.0,5.0])


# richting waarin de speler kijkt
r_speler = np.array([0,-1])
#r_speler = np.array([(-1/math.sqrt(2)),(1/math.sqrt(2))])
#r_speler = np.array([0,1])

#afstand tot cameravlak
d_camera = 1

#middelpunt cameravlak
middelpuntcameravlak = p_speler + d_camera * r_speler

#cameravlak
#r_cameravlak = np.array([-1 / math.sqrt(2), -1 / math.sqrt(2)])
rotmin90 = np.array([[0,1], [-1,0]])   #[cos alfa, -sin afla],[sin alfa, cos alfa] voor -pi/2
r_cameravlak = np.dot(rotmin90, r_speler)

# wordt op True gezet als het spel afgesloten moet worden
moet_afsluiten = False

# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn

# keuzenr = int(input(f'kies een map door een getal van 0 t.e.m. {aantal_mappen} in te geven'))

# world_map = np.array(
#     [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
#      [2, 1, 1, 0, 0, 0, 0, 3, 3, 0, 2],
#      [2, 0, 1, 0, 0, 0, 0, 0, 3, 0, 2],
#      [2, 0, 1, 1, 0, 0, 0, 0, 3, 0, 2],
#      [2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2],
#      [2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2],
#      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
#      [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
#      [2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2],
#      [2, 6, 6, 0, 0, 0, 0, 0, 0, 0, 2],
#      [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
# )
# world_map = maps[keuzenr]

# Vooraf gedefinieerde kleuren
kleuren = [
    sdl2.ext.Color(0, 0, 0),  # 0 = Zwart
    sdl2.ext.Color(255, 0, 0),  # 1 = Rood
    sdl2.ext.Color(0, 255, 0),  # 2 = Groen
    sdl2.ext.Color(0, 0, 255),  # 3 = Blauw
    sdl2.ext.Color(64, 64, 64),  # 4 = Donker grijs
    sdl2.ext.Color(128, 128, 128),  # 5 = Grijs
    sdl2.ext.Color(192, 192, 192),  # 6 = Licht grijs
    sdl2.ext.Color(255, 255, 255),  # 7 = Wit
]



sdl2.ext.init()
# Maak een venster aan om de game te renderen
window = sdl2.ext.Window("startscherm", size=(BREEDTE, HOOGTE))
window.show()
renderer = sdl2.ext.Renderer(window)
while True:
    renderer.draw_rect((0,0,100, 100), kleuren[0])
    message = f'kies een map door een getal van 0 t.e.m. {aantal_mappen} in te geven'
    font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[0])
    text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
    renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[1], text.size[0]))
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_KEYDOWN:
            key = event.key.keysym.sym
            print(key == sdl2.SDLK_2)
            print(chr(key), sdl2.SDLK_2)
            print(maps[int(chr(key))])
            sdl2.ext.quit()
            quit()