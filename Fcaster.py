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

#d_camera
fov=90
d_camera=1/(math.tan(math.radians(fov)/2))
# positie van de speler
p_speler = np.array([3 + 1 / math.sqrt(2), 4 - 1 / math.sqrt(2)])

# richting waarin de speler kijkt
r_speler = np.array([1 / math.sqrt(2), -1 / math.sqrt(2)])

# cameravlak
r_cameravlak = np.array([-1 / math.sqrt(2), -1 / math.sqrt(2)])

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
#
def verwerk_input(delta):
    global moet_afsluiten

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
            if key == sdl2.SDLK_q:
                moet_afsluiten = True
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
            beweging = event.motion.xrel
            continue

    # Polling-gebaseerde input. Dit gebruiken we bij voorkeur om bv het ingedrukt
    # houden van toetsen zo accuraat mogelijk te detecteren
    key_states = sdl2.SDL_GetKeyboardState(None)

    # if key_states[sdl2.SDL_SCANCODE_UP] or key_states[sdl2.SDL_SCANCODE_W]:
    # beweeg vooruit...

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True


def bereken_r_straal(r_speler, kolom):
    r_straal = np.zeros(2)
    r_straal_kolom=d_camera*r_speler+(-1+(2*kolom)/BREEDTE)*r_cameravlak
    r_straal_kolom_norm=np.linalg.norm(r_straal_kolom)
    r_straal = r_straal_kolom/r_straal_kolom_norm


def raycast(p_speler, r_straal):
    d_muur = 0
    k_muur = kleuren[0]
    return (d_muur, k_muur)


def render_kolom(renderer, window, kolom, d_muur, k_muur):
    renderer.draw_line((kolom, 0, kolom, window.size[1]), kleuren[1])
    return


# Initialiseer font voor de fps counter
fps_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])


def render_fps(fps, renderer, window):
    message = f'{fps:.2f} fps'
    text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
    renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20,
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
            r_straal = bereken_r_straal(r_speler, kolom)
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
        window.refresh()

    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()
