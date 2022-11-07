import math
import time


import numpy as np
import sdl2.ext

# Constanten
BREEDTE = 800
HOOGTE = 600

#
# Globale variabelen
#

# positie van de speler
p_speler = np.array([3,3])

#print(p_speler[0])

# richting waarin de speler kijkt
r_speler = np.array([1,0])
#r_speler = np.array([(-1/math.sqrt(2)),(1/math.sqrt(2))])
#r_speler = np.array([0,1])

#afstand tot cameravlak
d_camera = 1

#middelpunt cameravlak
middelpuntcameravlak = p_speler + d_camera * r_speler
#print(middelpuntcameravlak)

#cameravlak
#r_cameravlak = np.array([-1 / math.sqrt(2), -1 / math.sqrt(2)])
rotmin90 = np.array([[0,1], [-1,0]])
r_cameravlak = np.dot(rotmin90, r_speler)
#print(r_cameravlak)

# wordt op True gezet als het spel afgesloten moet worden
moet_afsluiten = False

# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn
world_map = np.array(
    [[2, 2, 2, 2, 2, 5, 5],
     [2, 1, 0, 0, 0, 0, 5],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 3, 0, 0, 0, 0, 2],
     [2, 2, 2, 2, 2, 2, 2]]
)
#print(world_map[1,3])
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


#
# Verwerkt alle input van het toetsenbord en de muis
#
# Argumenten:
# @delta       Tijd in milliseconden sinds de vorige oproep van deze functie
#
def rot(alfa, vector):
    alfa = alfa * math.pi / 180
    rotmatrix = [[np.cos(alfa), -np.sin(alfa)], [np.sin(alfa), np.cos(alfa)]]
    return np.dot(rotmatrix, vector)

def verwerk_input(delta):
    global moet_afsluiten
    global r_speler
    global r_cameravlak
    global p_speler

    # Handelt alle input events af die zich voorgedaan hebben sinds de vorige
    # keer dat we de sdl2.ext.get_events() functie hebben opgeroepen
    events = sdl2.ext.get_events()
    for event in events:
        # Een SDL_QUIT event wordt afgeleverd als de gebruiker de applicatie
        # afsluit door bv op het kruisje te klikken
        if event.type == sdl2.SDL_QUIT:
            moet_afsluiten = True
            break
        # Een SDL_KEYDOWN event wordt afgeleverd wanneer de gebruiker een
        # toets op het toetsenbord indrukt.
        # Let op: als de gebruiker de toets blijft inhouden, dan zien we
        # maar 1 SDL_KEYDOWN en 1 SDL_KEYUP event.
        elif event.type == sdl2.SDL_KEYDOWN:
            key = event.key.keysym.sym
            if key == sdl2.SDLK_ESCAPE:
                moet_afsluiten = True
            stapverkleiner = 0.05
            if key == sdl2.SDLK_z and p_speler[0]<world_map.shape[0] and p_speler[1]<world_map.shape[1]: #bewegen in richting van muis
                p_speler = p_speler + (r_speler/(r_speler[0]**2+r_speler[1]**2))*stapverkleiner
            if key == sdl2.SDLK_d and p_speler[0]<world_map.shape[0] and p_speler[1]<world_map.shape[1]:                                      #bewegen loodrecht op richting muis naar links
                p_speler = p_speler + rot(90, r_speler/(r_speler[0]**2+r_speler[1]**2))*stapverkleiner
            if key == sdl2.SDLK_q and p_speler[0]<world_map.shape[0] and p_speler[1]<world_map.shape[1]:
                p_speler = p_speler + rot(270, r_speler/(r_speler[0]**2+r_speler[1]**2))*stapverkleiner
            if key == sdl2.SDLK_s and p_speler[0]<world_map.shape[0] and p_speler[1]<world_map.shape[1]:
                p_speler += rot(180, r_speler/(r_speler[0]**2+r_speler[1]**2))*stapverkleiner
            break

        # Analoog aan SDL_KEYDOWN. Dit event wordt afgeleverd wanneer de
        # gebruiker een muisknop indrukt
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            button = event.button.button
            if button == sdl2.SDL_BUTTON_LEFT:
                # ...
                continue
        # Een SDL_MOUSEWHEEL event wordt afgeleverd wanneer de gebruiker
        # aan het muiswiel draait.
        elif event.type == sdl2.SDL_MOUSEWHEEL:
            if event.wheel.y > 0:
                # ...
                continue
        # Wordt afgeleverd als de gebruiker de muis heeft bewogen.
        # Aangezien we relative motion gebruiken zijn alle coordinaten
        # relatief tegenover de laatst gerapporteerde positie van de muis.
        elif event.type == sdl2.SDL_MOUSEMOTION:
            # Aangezien we in onze game maar 1 as hebben waarover de camera
            # kan roteren zijn we enkel geinteresseerd in bewegingen over de
            # X-as
            if event.motion.xrel > 1 or event.motion.xrel < -1:
                beweging = event.motion.xrel
                r_speler = rot(beweging/100, r_speler)
                r_cameravlak = rot(90, r_speler)
                continue

    # Polling-gebaseerde input. Dit gebruiken we bij voorkeur om bv het ingedrukt
    # houden van toetsen zo accuraat mogelijk te detecteren
    key_states = sdl2.SDL_GetKeyboardState(None)

    # if key_states[sdl2.SDL_SCANCODE_UP] or key_states[sdl2.SDL_SCANCODE_W]:
    # beweeg vooruit...

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True


def bereken_r_straal(r_speler, kolom):

    # print(r_speler)
    #r_straal_kolom = d_camera * r_speler + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak
    #print(r_straal_kolom)
    r_straal_kolom_x = d_camera * r_speler[0] + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak[0]
    #if kolom == 134:
        #print(r_straal_kolom_x)
    #print(r_straal_kolom_x)
    r_straal_kolom_y = d_camera * r_speler[1] + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak[1]
    #if kolom == 134:
        #print(r_straal_kolom_y)
    #print(r_straal_kolom_y)
    #print(" ")


    #print("x: ", r_straal_kolom_x, "y:", r_straal_kolom_y)
    r_straal_kolom_norm = math.sqrt(r_straal_kolom_x ** 2 + r_straal_kolom_y ** 2)
    #print(r_straal_kolom_norm)
    r_straal_x = r_straal_kolom_x / r_straal_kolom_norm
    #print(r_straal_x)
    r_straal_y = r_straal_kolom_y / r_straal_kolom_norm
    #print(r_straal_y)



    # r_straal_kolom = d_camera*r_speler+(-1+(2*kolom)/BREEDTE)*r_cameravlak
    # r_straal_kolom_norm = np.linalg.norm(r_straal_kolom)
    # r_straal = r_straal_kolom/r_straal_kolom_norm
    #print (r_straal_x)
    return np.array([r_straal_x, r_straal_y])


def raycast(p_speler, r_straal):
    global r_speler
    delta_h = 1 / abs(r_straal[0]) #gebruikt x ipv y
    delta_v = 1 / abs(r_straal[1])
    #print(delta_v)
    if r_straal[0] < 0:
        d_horizontaal = (p_speler[0] - int(p_speler[0])) * delta_h
        #d_horizontaal = (p_speler[1] - math.floor(p_speler[1])) * delta_h
        #print("hit")
    else:
        d_horizontaal = (1 - (p_speler[0] - int(p_speler[0]))) * delta_h
        #d_horizontaal = (1 - p_speler[1] + math.floor(p_speler[1])) * delta_h
        #print("hit2")
        #print(d_horizontaal)
    if r_straal[1] < 0:
        d_verticaal = (p_speler[1] - int(p_speler[1])) * delta_v
        #d_verticaal = (p_speler[0] - math.floor(p_speler[0])) * delta_v
        #print("hit3")
    else:
        d_verticaal = (1 - (p_speler[1] - int(p_speler[1]))) * delta_v
        #d_verticaal = (1 - p_speler[0] + math.floor(p_speler[0])) * delta_v
        #print("hit4")
        #print(d_verticaal)

    x = 0
    #print(x)
    y = 0
    #print(y)
    wall_boundaryfound = False
    d_muur = 0
    k_muur = kleuren[1]
    while True:
        #print(x)
        #print(y)
        #print(r_straal)
        #print(d_horizontaal)
        #print(d_verticaal)
        #print(delta_h)
        #print(delta_v)
        if d_horizontaal + x * delta_h <= d_verticaal + y * delta_v:
            #print("hit")
            i_horizontaal_x = p_speler + (d_horizontaal + x * delta_h) * r_straal
            #print(i_horizontaal_x)
            #i_horizontaal_x_rounded_float = np.round_(i_horizontaal_x)
            #print(i_horizontaal_x_rounded_float)
            i_horizontaal_x_rounded_int = i_horizontaal_x.astype("i")
            #print(i_horizontaal_x_rounded_int)
            x += 1
            #print(x)
            #print(r_straal[0])
            if r_straal[0] >= 0:
                #print("hit")
                #print(i_horizontaal_x_rounded_int[0])
                #print(i_horizontaal_x_rounded_int[1] + 1) #indien dit het geval kijken we in [5,5] terwijl we in [5,4] moeten kijken => +1 moet weg!
                #print(world_map[i_horizontaal_x_rounded_int[0], (i_horizontaal_x_rounded_int[1])])
                if world_map[i_horizontaal_x_rounded_int[0], (i_horizontaal_x_rounded_int[1])] :
                    #print(world_map[i_horizontaal_x_rounded_int[0] + 1, (i_horizontaal_x_rounded_int[1])])
                    #print("hit")
                    d_muur  = math.sqrt((i_horizontaal_x[0]-p_speler[0])**2 + (i_horizontaal_x[1]-p_speler[1])**2)
                    #print(d_muur)
                    k_muur = kleuren[world_map[i_horizontaal_x_rounded_int[0], (i_horizontaal_x_rounded_int[1])]]
                    #print(k_muur)
                    break
                    #return (d_muur, k_muur)
                #else:
                    #print("not hit")

            elif r_straal[0] < 0:
                if world_map[(i_horizontaal_x_rounded_int[0] - 1, i_horizontaal_x_rounded_int[1])]:
                    d_muur = math.sqrt((i_horizontaal_x[0]-p_speler[0])**2 + (i_horizontaal_x[1]-p_speler[1])**2)
                    k_muur = kleuren[world_map[(i_horizontaal_x_rounded_int[0] - 1, i_horizontaal_x_rounded_int[1])]]
                    break
                    #return (d_muur, k_muur)

        else:
            #print("hit2")
            i_verticaal_y = p_speler + (d_verticaal + y * delta_v) * r_straal
            #print(i_verticaal_y)
            #i_verticaal_y_rounded_float = np.round_(i_verticaal_y)
            #print(i_verticaal_y_rounded_float)
            i_verticaal_y_rounded_int = i_verticaal_y.astype("i")
            #print(i_verticaal_y_rounded_int)
            y += 1
            #print(y)
            #print(r_straal[0])
            if r_straal[1] >= 0:
                #print("hit")
                #print(world_map[(i_verticaal_y_rounded_int[0] + 1), i_verticaal_y_rounded_int[1]]) #hier kijken we in [6,4] maar we moeten in [5,5] kijken
                if i_verticaal_y_rounded_int[0] >= 7 or i_verticaal_y_rounded_int[1] >= 7:
                    print(i_verticaal_y_rounded_int)
                    quit()
                if world_map[i_verticaal_y_rounded_int[0], i_verticaal_y_rounded_int[1]]:
                    #print("hit")
                    d_muur = math.sqrt((i_verticaal_y[0]-p_speler[0])**2 + (i_verticaal_y[1]-p_speler[1])**2)
                    k_muur = kleuren[world_map[(i_verticaal_y_rounded_int[0]), i_verticaal_y_rounded_int[1]]]
                    break
                    #return (d_muur, k_muur)

            elif r_straal[1] < 0: #omgewisseld: 0 --> 1
                if world_map[i_verticaal_y_rounded_int[0], i_verticaal_y_rounded_int[1] - 1]:
                    d_muur = math.sqrt((i_verticaal_y[0]-p_speler[0])**2 + (i_verticaal_y[1]-p_speler[1])**2)
                    k_muur = kleuren[world_map[i_verticaal_y_rounded_int[0], i_verticaal_y_rounded_int[1] - 1]]
                    break
                    #return (d_muur, k_muur)
    d_muur = d_muur * np.dot(r_speler, r_straal)
    d_muur = round(d_muur, 12)
    #print(d_muur)
    return (d_muur, k_muur)

def render_kolom(renderer, window, kolom, d_muur, k_muur):
    #print("in render: ",d_muur)
    hoogte = (HOOGTE/2) * 1/d_muur
    if d_muur < 1/2:
        y1 = 0
    else:
        y1 = (HOOGTE - hoogte)/2
    #print("hoogte: ", hoogte)
    #print()
    renderer.draw_line((kolom, y1, kolom, HOOGTE-y1), k_muur) #renderer.draw_line((kolom, 300, kolom, 1/d_muur), k_muur) #renderer.draw_line((kolom, 0, kolom, window.size[1]), kleuren[1])
    return

# Initialiseer font voor de fps counter
fps_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])


def render_fps(fps, renderer, window):
    # message = f'{fps:.2f} fps'
    # text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
    # renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20,
    #                              text.size[0], text.size[1]))

    message = f'{fps:.2f} fps \n {p_speler} position \n {r_speler}kijkrichting '
    text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
    renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 16), 20,
                                 text.size[0], text.size[1]))



def main():
    # Initialiseer de SDL2 bibliotheek
    sdl2.ext.init()

    # Maak een venster aan om de game te renderen
    window = sdl2.ext.Window("Project Ingenieursbeleving 2", size=(BREEDTE, HOOGTE))
    window.show()

    # Begin met het uitlezen van input van de muis en vraag om relatieve coordinaten
    sdl2.SDL_SetRelativeMouseMode(True)

    # Maak een renderer aan zodat we in ons venster kunnen renderen
    renderer = sdl2.ext.Renderer(window)

    fps_list = []
    fps = 0

    # Blijf frames renderen tot we het signaal krijgen dat we moeten afsluiten
    while not moet_afsluiten:

        # Onthoud de huidige tijd
        start_time = time.time()

        # Reset de rendering context
        renderer.clear()

        # Render de huidige frame
        for kolom in range(0, window.size[0]):
            #if kolom == 400:
                #print("half")
            #print(kolom)
            r_straal = bereken_r_straal(r_speler, kolom)
            if r_straal[0] ==0 or r_straal[1] == 0:
                continue
            (d_muur, k_muur) = raycast(p_speler, r_straal)
            render_kolom(renderer, window, kolom, d_muur, k_muur)

        end_time = time.time()
        delta = end_time - start_time

        verwerk_input(delta)

        # Teken gemiddelde fps van de laatste 20 frames
        fps_list.append(1/(time.time() - start_time))
        if len(fps_list) == 20:
            fps = np.average(fps_list)
            fps_list = []
        render_fps(fps, renderer, window)

        # Verwissel de rendering context met de frame buffer
        renderer.present()

    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()