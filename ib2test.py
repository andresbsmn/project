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
# d_camera
fov = 45
d_camera = 1/(math.tan(math.radians(fov)/2))
# positie van de speler
start_positie_x = 3
start_positie_y = 3
p_speler = np.array([float(start_positie_x), float(start_positie_y)])

# richting waarin de speler kijkt
r_speler = np.array([1 / math.sqrt(2), 1 / math.sqrt(2)])
# cameravlak
rot90 = [-1, 1] #rotatie matrix voor 90°, al vereenvoudigt
r_cameravlak = rot90 * r_speler #d_camera*r_speler+p_speler als nulpunt


# wordt op True gezet als het spel afgesloten moet worden
moet_afsluiten = False

# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn

world_map = np.array(
    [[2, 2, 2, 2, 2, 2, 2],
     [2, 0, 0, 0, 1, 2, 2],
     [2, 0, 0, 0, 0, 1, 2],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 0, 0, 0, 0, 0, 2],
     [2, 2, 2, 2, 2, 2, 2]]
)

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

def rot(alfa, vector):
    rotmatrix = [[np.cos(alfa), -np.sin(alfa)], [np.sin(alfa), np.cos(alfa)]]
    return np.dot(rotmatrix, vector)
#
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
            if key == sdl2.SDLK_z and p_speler[0]<7 and p_speler[1]<7: #bewegen in richting van muis
                p_speler += (r_speler/(r_speler[0]**2+r_speler[1]**2))*stapverkleiner
            if key == sdl2.SDLK_q and p_speler[0]<7 and p_speler[1]<7:                                      #bewegen loodrecht op richting muis naar links
                p_speler += rot(90, r_speler/(r_speler[0]**2+r_speler[1]**2))*stapverkleiner
            if key == sdl2.SDLK_d and p_speler[0]<7 and p_speler[1]<7:
                p_speler += rot(270, r_speler/(r_speler[0]**2+r_speler[1]**2))*stapverkleiner
            if key == sdl2.SDLK_s and p_speler[0]<7 and p_speler[1]<7:
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
    r_straal_kolom = d_camera*r_speler+(-1+(2*kolom)/BREEDTE)*r_cameravlak
    r_straal_kolom_norm = np.linalg.norm(r_straal_kolom)
    r_straal = r_straal_kolom/r_straal_kolom_norm
    return r_straal


def raycast(p_speler, r_straal):
    # DDA algoritme:
    # stap 0:
    x = 0
    y = 0
    i_verticaal_x = 0
    i_horizontaal_x = 0
    d_horizontaal = 0
    d_verticaal = 0
    # stap 1:
    delta_v = 1 / abs(r_straal[0])
    delta_h = 1 / abs(r_straal[1])
    # stap 2:
    if r_straal[1] < 0:
        d_horizontaal = (p_speler[1] - math.floor(p_speler[1])) * delta_h

    elif r_straal[1] >= 0:
        d_horizontaal = (1 - p_speler[1] + math.floor(p_speler[1])) * delta_h

    if r_straal[0] < 0:
        d_verticaal = (p_speler[0] - math.floor(p_speler[0])) * delta_v
    elif r_straal[0] >= 0:
        d_verticaal = (1 - p_speler[0] + math.floor(p_speler[0])) * delta_v

    # stap 3:
    def test_punt_dicht():
        return d_horizontaal + (x * delta_h) <= d_verticaal + (y * delta_v)

    # stap 4: while nog geen snijpunt doen

    while True:
        a = 0
        if test_punt_dicht():
            i_horizontaal_x_component = int(p_speler[0] + (d_horizontaal + x * delta_h) * r_straal[0])
            i_horizontaal_y_component = y
            x += 1
            if i_horizontaal_x_component >= 7 or i_horizontaal_y_component >= 7:
                return "error", "error"
            if world_map[i_horizontaal_x_component, i_horizontaal_y_component] != 0:
                d_muur = math.sqrt(i_horizontaal_x_component ** 2 + i_horizontaal_y_component ** 2)
                k_muur = kleuren[world_map[i_horizontaal_x_component, i_horizontaal_y_component]]
                break

        else:
            i_verticaal_x_component = x
            i_verticaal_y_component = int(p_speler[1] + (d_verticaal + y * delta_v) * r_straal[1])
            y += 1
            if i_verticaal_x_component >= 7 or i_verticaal_y_component >= 7:
                return "error", "error"

            if not test_punt_dicht() and world_map[i_verticaal_x_component, i_verticaal_y_component] != 0:
                d_muur = math.sqrt(i_verticaal_x_component ** 2 + i_verticaal_y_component ** 2)
                k_muur = kleuren[world_map[i_verticaal_x_component, i_verticaal_y_component]]
                break



        # als intersectie buiten grenzen van level ligt: error returnen
        # stap 5:

        # stap 6 kijken of muur geraakt, indien geraakt d_muur en k_muur returnen, anders terug naar stap 3:
        # afstand dus pythagoras met coordinaten naar intersection die ook effectief muur snijdt
        # if (test_punt_dicht()) and (world_map[i_horizontaal_x_component, i_horizontaal_y_component] != 0):
        #    d_muur = math.sqrt(i_horizontaal_x_component ** 2 + i_horizontaal_y_component ** 2)
        # elif not test_punt_dicht() and (world_map[i_verticaal_x_component, i_verticaal_y_component] != 0):
        #    d_muur = math.sqrt(i_verticaal_x_component ** 2 + i_verticaal_y_component ** 2)
    # if test() and r_straal[y] >= 0:
    #    check(world_map[math.ceil(r_straal[x])])
    # elif test() and r_straal[y] < 0:
    #    check(world_map[math.floor(r_straal[x])])
    # elif not test()  and r_straal[x] < 0:
    #    check(world_map[math.floor(r_straal[x])])
    # elif not test() and r_straal[x] >= 0:
    #    check(world_map[math.ceil(r_straal[x])])
    # als getal 1 dan kleur 1 rood
    if a == 0:
        return (d_muur, k_muur)

def render_kolom(renderer, window, kolom, d_muur, k_muur):
    hoogte =window.size[1]/4 - 2*d_muur
    y1 = int(hoogte) #d_muur
    renderer.draw_line((kolom, y1, kolom, window.size[1]-y1), k_muur)
    renderer.draw_line((kolom, y1+hoogte , kolom, window.size[1]), kleuren[3])
    return
# Initialiseer font voor de fps counter
fps_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])

def render_fps(fps, renderer, window):
    message = f'{fps:.2f} fps'
    text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
    renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 16), 20,text.size[0], text.size[1]))


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
        for kolom in range(0, window.size[0]): #window.size[0] = 800
            r_straal = bereken_r_straal(r_speler, kolom)
            (d_muur, k_muur) = raycast(p_speler, r_straal)
            if d_muur == "error":
                print(p_speler, r_straal)
            else:
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
        window.refresh()

    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()
