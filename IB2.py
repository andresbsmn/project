import cProfile
import math
import time

import sdl2
import snakeviz

import numpy as np
import sdl2.ext

from levels import *
from playsound import playsound
# Constanten
BREEDTE = 800
HOOGTE = 600
# var aanmaken
global deadline

#
# Globale variabelen
#
global is_horizontaal
global renderer
global list_wall_create
global laser_shot
laser_shot = False
tijd_verstrekentot = 0 #variabele aanmaken
deadline = 10
# positie van de speler
p_speler = np.array([10.0,15.0])


# richting waarin de speler kijkt
r_speler = np.array([0,1])

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
is_texture = False
# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn

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

def levelselect():
    global world_map
    global deadline
    sdl2.ext.init()
    # Maak een venster aan om de game te renderen, wordt na functie ook afgesloten
    window = sdl2.ext.Window("level selectie scherm", size=(BREEDTE, HOOGTE))
    window.show()
    renderer = sdl2.ext.Renderer(window)
    #afbeelding erin
    resources = sdl2.ext.Resources(__file__, "textures")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    achtergrond = factory.from_image(resources.get_path("winkel_start.jpg"))
    errormessage = ""
    message = f'voor level selectie druk "l" \n voor timer aan te passen druk "t"'
    keuze = ''
    moet_afsluiten = False
    while not moet_afsluiten:
        renderer.clear()
        renderer.copy(achtergrond, dstrect=(0,0, window.size[0], window.size[1]))
        if errormessage: #lege string wordt gezien als een false, errormessage krijgt pas waarde bij een error
            message = f'{errormessage}'
        font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:  #nummers gaan van 48(=0) tot 57(=9)
                key = event.key.keysym.sym
                #afsluiten bij kruisje of escape
                if key == sdl2.SDLK_ESCAPE:
                    quit()
                if key == sdl2.SDLK_l:
                    message = f'kies een map door een getal van 1 t.e.m. {aantal_mappen} in te geven'
                    keuze = "level"
                elif key == sdl2.SDLK_t:
                    message = f'kies een tijd door te scrollen'
                    keuze = "timer"
                elif keuze == "level":
                    if key >= 48 and key <= 57:
                        try:
                            world_map = maps[int(chr(key))-1]
                            print(world_map)
                            # return int(chr(key))
                            world_map = maps[int(chr(key))-1]
                            return world_map
                        except:
                            errormessage = f'je hebt een ongeldige waarde ingegeven \n gelieve een waarde tussen 1 en {aantal_mappen} in te geven'
            if keuze == "timer" and event.type == sdl2.SDL_MOUSEWHEEL:
                deadline += event.wheel.y
                message = f'de tijd is nu {deadline}'



                #
                # break
        text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
        renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        renderer.present()
        # window.refresh()

def levelfailed(reden):
    global world_map
    sdl2.ext.init()
    # Maak een venster aan om de game te renderen, wordt na functie ook afgesloten
    window = sdl2.ext.Window("level mislukt", size=(BREEDTE, HOOGTE))
    window.show()
    renderer = sdl2.ext.Renderer(window)
    # afbeelding erin
    resources = sdl2.ext.Resources(__file__, "textures")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    achtergrond = factory.from_image(resources.get_path("winkel_start.jpg"))
    errormessage = ""
    message = f'Game Over, {reden} \n druk op "r" op opnieuw te proberen'
    while True:
        renderer.clear()
        renderer.copy(achtergrond, dstrect=(0, 0, window.size[0], window.size[1]))
        if errormessage:  # lege string wordt gezien als een false, errormessage krijgt pas waarde bij een error
            message = f'{errormessage}'
        font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=30, color=kleuren[3])
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:  # nummers gaan van 48(=0) tot 57(=9)
                key = event.key.keysym.sym
                if key == sdl2.SDLK_r:
                    # message = f'kies een map door een getal van 1 t.e.m. {aantal_mappen} in te geven'
                    sdl2.ext.quit()
                    main()
                if key == sdl2.SDLK_ESCAPE:
                    quit()

        text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
        renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        renderer.present()
        # window.refresh()

def rotatie(alfa, vector):
    #alfa moet in radialen!!!!
    rotatie_matrix = [[np.cos(alfa), -np.sin(alfa)], [np.sin(alfa), np.cos(alfa)]]
    return np.dot(rotatie_matrix, vector)

def verwerk_input(delta):
    global moet_afsluiten
    global r_speler
    global r_cameravlak
    global p_speler
    global laser_shot

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
            #hier nog alles van limitaties ook aanpassen
            if key == sdl2.SDLK_ESCAPE:
                moet_afsluiten = True
            break

        # Analoog aan SDL_KEYDOWN. Dit event wordt afgeleverd wanneer de
        # gebruiker een muisknop indrukt
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            button = event.button.button
            if button == sdl2.SDL_BUTTON_LEFT:
                # ...
                laser_shot = True
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
                rotatie_beweging = (beweging * math.pi/2)/50
                r_speler = rotatie(rotatie_beweging, r_speler)
                #r_speler = rotatie(beweging/100, r_speler)
                r_cameravlak = rotatie((math.pi/2), r_speler)
                continue

    # Polling-gebaseerde input. Dit gebruiken we bij voorkeur om bv het ingedrukt
    # houden van toetsen zo accuraat mogelijk te detecteren
    key_states = sdl2.SDL_GetKeyboardState(None)

    # if key_states[sdl2.SDL_SCANCODE_UP] or key_states[sdl2.SDL_SCANCODE_W]:
    # beweeg vooruit...
    stapverkleiner = 0.05
    #moet querty volgen om een of andere reden
    if key_states[sdl2.SDL_SCANCODE_W]: # komt overeen met Z
        p_speler += (r_speler/(r_speler[0]**2+r_speler[1]**2))*stapverkleiner
    if key_states[sdl2.SDL_SCANCODE_A]: #komt overeen met D
        p_speler += rotatie((3 / 2) * math.pi, r_speler / (r_speler[0] ** 2 + r_speler[1] ** 2)) * stapverkleiner
    if key_states[sdl2.SDL_SCANCODE_D]:
        p_speler += rotatie(math.pi / 2, r_speler / (r_speler[0] ** 2 + r_speler[1] ** 2)) * stapverkleiner
    if key_states[sdl2.SDL_SCANCODE_S]:
        p_speler += rotatie(math.pi, r_speler / (r_speler[0] ** 2 + r_speler[1] ** 2)) * stapverkleiner

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True

def bereken_r_straal(r_speler, kolom):
    #r_straal_kolom = d_camera * r_speler + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak

    r_straal_kolom_x = d_camera * r_speler[0] + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak[0]
    r_straal_kolom_y = d_camera * r_speler[1] + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak[1]

    r_straal_kolom_norm = math.sqrt(r_straal_kolom_x ** 2 + r_straal_kolom_y ** 2)
    r_straal_x = r_straal_kolom_x / r_straal_kolom_norm
    r_straal_y = r_straal_kolom_y / r_straal_kolom_norm
    return np.array([r_straal_x, r_straal_y])

def raycast(p_speler, r_straal):
    global r_speler
    global is_texture
    is_texture = False
    global is_horizontaal
    global blok

    delta_h = 1 / abs(r_straal[0]) #gebruikt x ipv y
    delta_v = 1 / abs(r_straal[1])


    if r_straal[0] < 0:
        d_horizontaal = (p_speler[0] - int(p_speler[0])) * delta_h
    else:
        d_horizontaal = (1 - (p_speler[0] - int(p_speler[0]))) * delta_h
    if r_straal[1] < 0:
        d_verticaal = (p_speler[1] - int(p_speler[1])) * delta_v
    else:
        d_verticaal = (1 - (p_speler[1] - int(p_speler[1]))) * delta_v
    x = 0
    y = 0
    d_muur = 0
    k_muur = kleuren[1]

    while True:
        if d_horizontaal + x * delta_h <= d_verticaal + y * delta_v:
            i_horizontaal_x = p_speler + (d_horizontaal + x * delta_h) * r_straal

            #hier elif tijdelijk toegevoegd, nog verder aanpassen
            # rijen = len(matrix) => hoogte
            # kolommen = len(matrix[0]) => width

            if i_horizontaal_x[0] == len(world_map):
                i_horizontaal_x[0] = len(world_map) - 0.5
            elif i_horizontaal_x[1] == len(world_map[0]):
                i_horizontaal_x[1] = len(world_map[0]) - 0.5

            i_horizontaal_x_rounded_int = (i_horizontaal_x + 0.0005).astype(int)
            x += 1
            is_horizontaal = True

            if r_straal[0] >= 0:
                if world_map[i_horizontaal_x_rounded_int[0], (i_horizontaal_x_rounded_int[1])]:
                    d_muur = math.sqrt((i_horizontaal_x[0] - p_speler[0]) ** 2 + (i_horizontaal_x[1] - p_speler[1]) ** 2)
                    is_texture = True
                    blok = world_map[i_horizontaal_x_rounded_int[0], (i_horizontaal_x_rounded_int[1])]
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (i_horizontaal_x - i_horizontaal_x_rounded_int)
                    break




            elif r_straal[0] < 0:
                if world_map[(i_horizontaal_x_rounded_int[0] - 1, i_horizontaal_x_rounded_int[1])]:
                    d_muur = math.sqrt((i_horizontaal_x[0] - p_speler[0]) ** 2 + (i_horizontaal_x[1] - p_speler[1]) ** 2)
                    is_texture = True
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (i_horizontaal_x - i_horizontaal_x_rounded_int)
                    #textuurcoordinaten_X = (i_horizontaal_x - i_horizontaal_x_rounded_int) * wall.size[0]
                    blok = world_map[(i_horizontaal_x_rounded_int[0] - 1), i_horizontaal_x_rounded_int[1]]
                    break


        else:
            i_verticaal_y = p_speler + (d_verticaal + y * delta_v) * r_straal

            if i_verticaal_y[0] == len(world_map):
                i_verticaal_y[0] = len(world_map) - 0.5
            elif i_verticaal_y[1] == len(world_map[0]):
                i_verticaal_y[1] = len(world_map[0]) - 0.5



            i_verticaal_y_rounded_int = (i_verticaal_y + 0.0005).astype(int)

            is_horizontaal = False
            y += 1
            if r_straal[1] >= 0:
                if world_map[(i_verticaal_y_rounded_int[0]), (i_verticaal_y_rounded_int[1])] :
                    d_muur = math.sqrt((i_verticaal_y[0] - p_speler[0]) ** 2 + (i_verticaal_y[1] - p_speler[1]) ** 2)
                    is_texture = True
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (1-(i_verticaal_y - i_verticaal_y_rounded_int))
                    #textuurcoordinaten_X = (1-(i_verticaal_y - i_verticaal_y_rounded_int)) * wall.size[0]
                    blok = world_map[(i_verticaal_y_rounded_int[0]), (i_verticaal_y_rounded_int[1])]
                    break



            elif r_straal[1] < 0: #omgewisseld: 0 --> 1
                if world_map[i_verticaal_y_rounded_int[0], (i_verticaal_y_rounded_int[1] - 1)]:

                    d_muur = math.sqrt((i_verticaal_y[0] - p_speler[0]) ** 2 + (i_verticaal_y[1] - p_speler[1]) ** 2)
                    is_texture = True
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (1-(i_verticaal_y - i_verticaal_y_rounded_int))
                    #textuurcoordinaten_X = (1-(i_verticaal_y - i_verticaal_y_rounded_int)) * wall.size[0]
                    blok = world_map[i_verticaal_y_rounded_int[0], (i_verticaal_y_rounded_int[1] - 1)]
                    break



    d_muur = d_muur * np.dot(r_speler, r_straal)
    d_muur = round(d_muur, 12)
    return (d_muur, k_muur, is_texture, textuurcoordinaten_X_zondermaalbreedtetextuur, blok)

def create_textures():
    rek = factory.from_image(resources.get_path("rek.png"))
    kassa = factory.from_image(resources.get_path("kassa.png"))
    frigo = factory.from_image(resources.get_path("frigo.png"))
    melkfrigo = factory.from_image(resources.get_path("melkfrigo.png"))
    roodrek = factory.from_image(resources.get_path("roodrek.png"))
    slager = factory.from_image(resources.get_path("slager.png"))
    winkelmuur = factory.from_image(resources.get_path("winkelmuur.png"))
    bakker = factory.from_image(resources.get_path("bakker.png"))

    list_wall = [
        "empty",  # 0
        rek,  # 1
        kassa,  # 2,
        frigo,  # 3
        melkfrigo,  # 4
        roodrek,  # 5
        slager,  # 6
        winkelmuur,  # 7
        bakker  # 8
    ]
    return list_wall


def render_wall(renderer, window, kolom, d_muur, k_muur, is_texture, textuurcoordinaten_X_zondermaalbreedtetextuur, blok, list_wall_create):
    global is_horizontaal
    global wall

    muur = list_wall_create[blok]

    textuurcoordinaten_X = textuurcoordinaten_X_zondermaalbreedtetextuur * muur.size[0]
    hoogte = (HOOGTE) * 1/(d_muur+0.00001) #200/d_muur#(HOOGTE/2) * 1/d_muur
    #hoogte = (HOOGTE / 2) * 1 / d_muur

    if hoogte >= HOOGTE: #hier stond 1/2 naar 1 gezet
        y1 = 0
    else:
        y1 = (HOOGTE - hoogte)/2 #-1 toegevoegd

    if is_texture == True:

        breedte_textuur = muur.size[0]
        hoogte_textuur = muur.size[1]
        if is_horizontaal == True:
            textuur_x = textuurcoordinaten_X[1]
        else:
            textuur_x = textuurcoordinaten_X[0]
        textuur_y = 0
        scherm_x = kolom
        scherm_y = y1


        if hoogte <= HOOGTE:
            renderer.copy(muur, srcrect=(textuur_x, textuur_y, breedte_textuur / 100, hoogte_textuur),dstrect=(scherm_x, scherm_y, 1, hoogte))
        else:
            textuur_y = ((hoogte - HOOGTE) / 2) * (hoogte_textuur / hoogte)
            hoogte_textuur_volledig_scherm = HOOGTE * (hoogte_textuur / hoogte)
            renderer.copy(muur, srcrect=(textuur_x, textuur_y, breedte_textuur / 100, hoogte_textuur_volledig_scherm),
                          dstrect=(scherm_x, scherm_y, 1, HOOGTE))

    else:
        renderer.draw_line((kolom, y1, kolom, HOOGTE - y1), k_muur)


    return

def render_fps(fps, renderer, window):
    message = f'{fps:.2f} fps'
    text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
    renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[0], text.size[1]))

    
def scannergun():
    global laser_shot, laser_shot_rent
    global window
    global renderer
    resources = sdl2.ext.Resources(__file__, "resources")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    scannergun_texture = factory.from_image(resources.get_path("scanner.png"))

    renderer.copy(scannergun_texture, srcrect=(0, 0, scannergun_texture.size[0], scannergun_texture.size[1]),
                  dstrect=(299, 415, scannergun_texture.size[0], scannergun_texture.size[1]))

    # crosshair
    resources = sdl2.ext.Resources(__file__, "resources")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    crosshair_texture = factory.from_image(resources.get_path("crosshair_white.png"))

    renderer.copy(crosshair_texture, srcrect=(0, 0, crosshair_texture.size[0], crosshair_texture.size[1]),
                  dstrect=(380, 277, crosshair_texture.size[0], crosshair_texture.size[1]))

    if laser_shot == True:

        playsound("resources/Scanner_beep_3.mp3")
        resources = sdl2.ext.Resources(__file__, "resources")
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
        laser_texture = factory.from_image(resources.get_path("scanner_laser2.png"))

        renderer.copy(laser_texture, srcrect=(0, 0, laser_texture.size[0], laser_texture.size[1]),
                      dstrect=(381, 298, laser_texture.size[0], laser_texture.size[1]))
        laser_shot = False
    
def timer(delta, renderer, window, deadline):
    global tijd_verstrekentot
    tijd_deadline = deadline
    tijd_verstrekentot += delta
    message = f'je hebt nog {int(deadline - tijd_verstrekentot)} seconden'
    text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
    if tijd_verstrekentot > tijd_deadline:
        message = f'je tijd is op :('
        text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
        levelfailed("tijd was op")
    else:
        renderer.draw_rect((10, text.size[1] * 2, (tijd_verstrekentot / tijd_deadline) * text.size[0], text.size[1]),
                           kleuren[7])

    # renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), window.size[1]/3, text.size[0], text.size[1]))
    renderer.copy(text,
                  dstrect=(10, text.size[1], text.size[0], text.size[1]))

def main():
    global fps_font
    global tijd_verstrekentot
    tijd_verstrekentot = 0
    fps_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])
    world_map = levelselect()
    # print(world_map)
    # Initialiseer de SDL2 bibliotheek
    global laser_shot, laser_shot_rent
    sdl2.ext.init()

    # Maak een venster aan om de game te renderen
    window = sdl2.ext.Window("Project Ingenieursbeleving 2", size=(BREEDTE, HOOGTE))
    window.show()

    # Begin met het uitlezen van input van de muis en vraag om relatieve coordinaten
    sdl2.SDL_SetRelativeMouseMode(True)

    # Maak een renderer aan zodat we in ons venster kunnen renderen
    global renderer
    renderer = sdl2.ext.Renderer(window)
    global resources
    resources = sdl2.ext.Resources(__file__, "resources")
    global factory
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    list_wall_create = create_textures()
    global scannergun_sprite
    scannergun_sprite= factory.from_image(resources.get_path("scanner.png"))
    fps_list = []
    fps = 0

    # Blijf frames renderen tot we het signaal krijgen dat we moeten afsluiten
    while not moet_afsluiten:

        # Onthoud de huidige tijd
        start_time = time.time()

        # Reset de rendering context
        renderer.clear()

        # Render de huidige frame
        color_textures = [factory.from_color(color, (1, 1)) for color in kleuren]
        # ceiling
        renderer.copy(color_textures[4], srcrect=(0, 0, 1, 1), dstrect=(0, 0, window.size[0], window.size[1] / 2))
        # floor
        renderer.copy(color_textures[5], srcrect=(0, 0, 1, 1),dstrect=(0, window.size[1] / 2, window.size[0], window.size[1] / 2))


        for kolom in range(0, window.size[0]):
            r_straal = bereken_r_straal(r_speler, kolom)
            if r_straal[0] ==0 or r_straal[1] == 0:
                continue
            (d_muur, k_muur, is_texture, textuurcoordinaten_X_zondermaalbreedtetextuur,blok) = raycast(p_speler, r_straal)
            render_wall(renderer, window, kolom, d_muur, k_muur, is_texture, textuurcoordinaten_X_zondermaalbreedtetextuur, blok, list_wall_create)


        renderer.copy(scannergun_sprite, srcrect=(0, 0, scannergun_sprite.size[0], scannergun_sprite.size[1]),dstrect=(299, 415, scannergun_sprite.size[0], scannergun_sprite.size[1]))
        end_time = time.time()
        delta = end_time - start_time

        verwerk_input(delta)
        timer(delta, renderer, window, deadline)
        # Teken gemiddelde fps van de laatste 20 frames
        fps_list.append(1/(time.time() - start_time))
        if len(fps_list) == 20:
            fps = np.average(fps_list)
            fps_list = []
        render_fps(fps, renderer, window)
        
        scannergun()
        
        map_weergave = factory.from_image(resources.get_path("Map1.png"))
        positie_persoon_sprite = factory.from_image(resources.get_path("pion_bolletje.png"))
        kaart_genomen = True
        if kaart_genomen == True:
            # mogelijke optimalisatie de hoogte en breedtes als variabelen opslaan of als getallen invullen ipv size opvragen
            renderer.copy(map_weergave, srcrect=(0, 0, map_weergave.size[0], map_weergave.size[1]),dstrect=(20, 20, map_weergave.size[0] * 1.5, map_weergave.size[1] * 1.5))
            positie_pion_x = 22 + ((p_speler[0] / 18) * (map_weergave.size[1] - 4))  # ( 16+(p_speler[0]/18)*(map_weergave.size[0]-5))
            #mss toch gsm ofzo rond zetten dan kan vierkante afbeelding als kaart (niet knippen, naar juiste pixels converteren dus niet pixelconverter online)en Geen rand!!
            # map size breedt en hoogte voorlopig gwn manueel 18 ingevuld
            positie_pion_y = 22 + map_weergave.size[0] - ((p_speler[1] / 18) * (map_weergave.size[0] - 4))  # 16+ map_weergave.size[1]-((p_speler[1]/18)*(map_weergave.size[1]-5))
            renderer.copy(positie_persoon_sprite,srcrect=(0, 0, positie_persoon_sprite.size[0], positie_persoon_sprite.size[1]), dstrect=(positie_pion_y, positie_pion_x, positie_persoon_sprite.size[0] / 4, positie_persoon_sprite.size[1] / 4))

        # Verwissel de rendering context met de frame buffer
        renderer.present()
        # na renderen frame venster verversen
        window.refresh()
    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    #comments met #sv naast wegdoen als je wilt kijken naar snakeviz
    # profiler = cProfile.Profile() # sv
    # profiler.enable() # sv
    main()
    # profiler.disable() # sv
    # stats = pstats.Stats(profiler) # sv
    # stats.dump_stats('data_prof') # sv
