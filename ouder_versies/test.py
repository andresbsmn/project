import math
import time
import pickle

import sdl2

import sdl2.ext

from ouder_versies.levels import *
from playsound import playsound
persistantfile = "save.pkl"
keuzealgemaakt = False
level = 0
global testboolean
testboolean = True
# Constanten
BREEDTE = 800
HOOGTE =  600
# var aanmaken
global deadline
global win_flags
win_flags = sdl2.SDL_WINDOW_RESIZABLE #kan window resizen
#
# Globale variabelen
#
global is_horizontaal
global renderer
global list_wall_create
global laser_shot
laser_shot = False
global kaart_genomen
kaart_genomen = True

levelup = False
render_pizza_in_world = True
pizza_collected = False

apple_collected = False
egg_collected = False
broccoli_collected = False

total_hearts_present = 3

player_hit = False
resources = sdl2.ext.Resources(__file__, "textures")

total_money_present = 1
money_collected = False
moneysprite = ""

# coordinaten sprites
pizza_x_coordinaten, pizza_y_coordinaten = [4, 1.5, 14.5, 7], [5.5, 14.5, 13.5, 3.5]  #
apple_x_coordinaten, apple_y_coordinaten = [6.5, 9.5, 16, 2], [12.5, 7.5, 9, 7]  #

egg_x_coordinaten, egg_y_coordinaten = [12, 12.5, 5, 7.5], [4.5, 10.5, 11, 2.5]  #
broccoli_x_coordinaten, broccoli_y_coordinaten = [9, 10.5, 6.5, 15.5], [7.5, 2, 15.5, 8.5]  #
munt1_x_coordinaten, munt1_y_coordinaten = [10, 2, 3, 8], [10, 2, 12, 11]
munt2_x_coordinaten, munt2_y_coordinaten = [2, 1, 0, 3], [7, 1, 0, 3]
munt3_x_coordinaten, munt3_y_coordinaten = [12, 1, 0, 3], [1, 1, 0, 3]
munt4_x_coordinaten, munt4_y_coordinaten = [3, 1, 0, 3], [1, 1, 0, 3]

tijd_verstrekentot = 0  # variabele aanmaken
deadline = 100
# positie van de speler
p_speler = np.array([9.5, 15.5])

# richting waarin de speler kijkt
r_speler = np.array([0, 1])

# afstand tot cameravlak
d_camera = 1

# middelpunt cameravlak
middelpuntcameravlak = p_speler + d_camera * r_speler

# cameravlak
# r_cameravlak = np.array([-1 / math.sqrt(2), -1 / math.sqrt(2)])
rotmin90 = np.array([[0, 1], [-1, 0]])  # [cos alfa, -sin afla],[sin alfa, cos alfa] voor -pi/2
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

def loadornew():
    sdl2.ext.init()
    window = sdl2.ext.Window("start", size=(BREEDTE, HOOGTE))
    window.show()
    renderer = sdl2.ext.Renderer(window)
    # afbeelding erin
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    shop_afbeelding = factory.from_image(resources.get_path("shop.jpg"))
    font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[0])
    stoppen = False
    message = f'je hebt een save aan level:{level+1}'
    start_shopx = window.size[0] / 4
    start_shopy = window.size[1] - shop_afbeelding.size[1]
    breedte_shop = window.size[0] / 2
    hoogte_shop = window.size[1] / 2
    lvlbuttonxstartwaarde = {}
    witruimtetussenknop = (BREEDTE / aantal_mappen) / 8
    breedte_knop = BREEDTE / aantal_mappen - witruimtetussenknop * 2
    while not stoppen:
        renderer.clear()
        renderer.fill((0, 0, BREEDTE, HOOGTE), kleuren[7])  # witte achtergrond
        # start knoppen timer
        renderer.draw_rect((BREEDTE / 8, (1 / 2) * HOOGTE, 50, 50), kleuren[0])
        renderer.copy(sdl2.ext.renderer.Texture(renderer, font.render_text("new game")),
                      dstrect=(BREEDTE / 8, (1 / 2) * HOOGTE, 50, 50))
        renderer.draw_rect((BREEDTE / 8, (2 / 3) * HOOGTE, 50, 50), kleuren[0])
        renderer.copy(sdl2.ext.renderer.Texture(renderer, font.render_text("load game")),
                      dstrect=(BREEDTE / 8, (2 / 3) * HOOGTE, 50, 50))
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_MOUSEMOTION:
                motion = event.motion
                # print(motion.x, motion.xrel, motion.y, motion.yrel)  # 1ste en 3de nodig
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                button = event.button.button
                if button == sdl2.SDL_BUTTON_LEFT:
                    # print(f'klik op {motion.x, motion.y}')
                    # kijkt of er op  timer knop is geklikt
                    if BREEDTE / 8 < motion.x < ((BREEDTE / 8) + 50):
                        if 0.5 * HOOGTE + 50 > motion.y > 0.5 * HOOGTE:  # new game knop
                            startscherm("new_game")
                            stoppen = True
                        if (2 / 3) * HOOGTE < motion.y < (2 / 3) * HOOGTE + 50 and deadline > 5:
                            startscherm("load_game")
                            stoppen = True

                    # kijkt of er op een lvl knop is geklik
        text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
        renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        renderer.present()
        # window.refresh()
    renderer.clear()
    sdl2.ext.quit()

def reset_startwaarden():
    global p_speler
    global r_speler
    # global render_pizza_in_world
    # global pizza_collected
    # global apple_collected
    # global egg_collected
    # global broccoli_collected
    # global total_money_present
    # global total_hearts_present
    r_speler = np.array([0, 1])
    p_speler = np.array([10.0, 15.0])
    renderer.clear
    #     ik denk dat dit ook moet gereset worden
    #     render_pizza_in_world = True
    #     pizza_collected = False
    #     apple_collected = False
    #     egg_collected = False
    #     broccoli_collected = False
    #     total_hearts_present = 3
    #     total_money_present = 0

def startscherm(keuze):
    global world_map
    global deadline
    global kaart_gekozen
    global levelup
    global level

    if keuze == "new_game":
        resetwaarden = {'p_speler': np.array([9.5, 15.5]), 'r_speler': np.array([0, 1]), 'pizza_collected': False,
                           'apple_collected': False, 'egg_collected': False,
                           'broccoli_collected': False,
                           'total_hearts_present': 3, 'total_money_present': 1,
                           'level': 0, 'tijd_verstrekentot': False
                           }
        save("save")
        testarray = np.array([0, 1])
        globals().update(resetwaarden)
        # print(globals())

        # print(type(testarray), "\n",type(p_speler) )
    kaart_gekozen = level
    world_map = maps[kaart_gekozen]
    if keuze == "load_game":
        return
    sdl2.ext.init()
    # Maak een venster aan om de game te renderen, wordt na functie ook afgesloten
    window = sdl2.ext.Window("level selectie scherm", size=(BREEDTE, HOOGTE), flags=win_flags)
    window.show()
    renderer = sdl2.ext.Renderer(window)
    # afbeelding erin
    resources = sdl2.ext.Resources(__file__, "textures")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    shop_afbeelding = factory.from_image(resources.get_path("shop.jpg"))
    errormessage = ""
    # message = f'om te starten klik "s" \n voor level selectie druk "l" \n voor timer aan te passen druk "t" \n of maak gebruik van de knoppen'
    message = f' welkom bij onze winkel!!! \n om te starten klik "s" \n navigeren kan met de muis of met de pijltjes'
    keuze = ''
    if not levelup:
        gameinfo = f'gekozen map level {level + 1} \n je hebt {deadline} seconden'
    else:
        gameinfo = f'congrats! new level {level + 1} \n je hebt {deadline} seconden'
        levelup = False
    font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[0])
    infofont = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=10, color=kleuren[0])
    moet_afsluiten = False
    start_shopx = window.size[0] / 4
    start_shopy = window.size[1] - shop_afbeelding.size[1]
    breedte_shop = window.size[0] / 2
    hoogte_shop = window.size[1] / 2
    lvlbuttonxstartwaarde = {}
    witruimtetussenknop = (BREEDTE / aantal_mappen) / 8
    breedte_knop = BREEDTE / aantal_mappen - witruimtetussenknop * 2
    while not moet_afsluiten:
        gameinfo = f'gekozen map level {level + 1} \n je hebt {deadline} seconden'
        renderer.clear()
        renderer.fill((0, 0, BREEDTE, HOOGTE), kleuren[7])  # witte achtergrond
        # start knoppen level-selectie
        for i in range(aantal_mappen):
            x_start_knop = ((BREEDTE / aantal_mappen) * i) + witruimtetussenknop
            if level == i:
                renderer.draw_rect((x_start_knop, 150, breedte_knop, 100), kleuren[3])
            else:
                renderer.draw_rect((x_start_knop, 150, breedte_knop, 100), kleuren[0])
            lvlbuttonxstartwaarde[f'knop_{i + 1}'] = x_start_knop
            knoptext = f'level {i + 1}'
            knopmessage = sdl2.ext.renderer.Texture(renderer, font.render_text(knoptext))
            renderer.copy(knopmessage, dstrect=(x_start_knop, 150, breedte_knop, 100))
        renderer.copy(shop_afbeelding, dstrect=(start_shopx, start_shopy, breedte_shop, hoogte_shop))
        # einde knoppen level-selectie

        # start knoppen timer
        renderer.draw_rect((BREEDTE / 8, (1 / 2) * HOOGTE, 50, 50), kleuren[0])
        renderer.copy(sdl2.ext.renderer.Texture(renderer, font.render_text("+")),
                      dstrect=(BREEDTE / 8, (1 / 2) * HOOGTE, 50, 50))
        renderer.draw_rect((BREEDTE / 8, (2 / 3) * HOOGTE, 50, 50), kleuren[0])
        renderer.copy(sdl2.ext.renderer.Texture(renderer, font.render_text("-")),
                      dstrect=(BREEDTE / 8, (2 / 3) * HOOGTE, 50, 50))
        if errormessage:  # lege string wordt gezien als een false, errormessage krijgt pas waarde bij een error
            message = f'{errormessage}'
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_MOUSEMOTION:
                motion = event.motion
                # print(motion.x, motion.xrel, motion.y, motion.yrel)  # 1ste en 3de nodig
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                button = event.button.button
                if button == sdl2.SDL_BUTTON_LEFT:
                    # print(f'klik op {motion.x, motion.y}')
                    # kijkt of er op  timer knop is geklikt
                    if BREEDTE / 8 < motion.x < ((BREEDTE / 8) + 50):
                        geklikt = False
                        change = 0
                        if 0.5 * HOOGTE + 50 > motion.y > 0.5 * HOOGTE:  # + knop
                            geklikt = True
                            change = 1
                        if (2 / 3) * HOOGTE < motion.y < (2 / 3) * HOOGTE + 50 and deadline > 5:
                            geklikt = True
                            change = -1
                        if geklikt:
                            deadline += change
                    # kijkt of er op een lvl knop is geklikt
                    elif 150 < motion.y < 250:
                        for knop in lvlbuttonxstartwaarde:
                            if lvlbuttonxstartwaarde[knop] < motion.x < lvlbuttonxstartwaarde[knop] + breedte_knop:
                                gekozenlevel = int(knop[-1]) - 1  # want naam knop is knop_<level>
                                level = gekozenlevel
                                world_map = maps[gekozenlevel]
                                kaart_gekozen = gekozenlevel


            elif event.type == sdl2.SDL_KEYDOWN:  # nummers gaan van 48(=0) tot 57(=9)
                key = event.key.keysym.sym
                # levels met pijltjes
                if key == 1073741904:  # 1073741904 = linker pijltje; 1073741903 = rechter pijltje
                    level -= 1
                    if level < 0:
                        level = 3
                if key == 1073741903:  # 1073741904 = linker pijltje; 1073741903 = rechter pijltje
                    level += 1
                    if level > 3:
                        level = 0
                elif key == sdl2.SDLK_ESCAPE:
                    quit()
                elif key == sdl2.SDLK_s:
                    keuze = "start"
                    message = f'starting game...'
                    moet_afsluiten = True  # jump naar main achter de lus
                elif key == sdl2.SDLK_l:
                    message = f'kies een map door een getal van 1 t.e.m. {aantal_mappen} in te geven \n klik op "s" om de game te starten'
                    keuze = "level"
                elif key == sdl2.SDLK_t:
                    message = f'kies een tijd door te scrollen'
                    keuze = "timer"
                elif keuze == "level":
                    if key >= 48 and key <= 57:
                        try:
                            kaart_gekozen = (int(chr(key)) - 1)
                            level = int(chr(key)) - 1
                            world_map = maps[level]
                            keuze = ""
                        except:
                            errormessage = f'je hebt een ongeldige waarde ingegeven \n gelieve een waarde tussen 1 en {aantal_mappen} in te geven'

            if keuze == "timer" and event.type == sdl2.SDL_MOUSEWHEEL:
                if deadline > 5 or event.wheel.y > 0:
                    deadline += event.wheel.y
                    # message = f'de tijd is nu {deadline}'

        text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
        gaminfotext = sdl2.ext.renderer.Texture(renderer, infofont.render_text(gameinfo))
        renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        renderer.copy(gaminfotext, dstrect=(0, window.size[1] - text.size[1], text.size[0], text.size[1]))
        renderer.present()
        # window.refresh()
    sdl2.ext.quit()
    main()

def levelcompleted():
    global level
    global levelup
    if level == 3:
        message = f'congrats!!! you beat the game \n klik op "s" om opnieuw te beginnen'
        level = 0
    else:
        message = f'congrats!!! you cleared level {level+1}, \n druk op "s" om verder te spelen'
        level += 1
        levelup = True
    reset_startwaarden()
    sdl2.ext.init()
    # Maak een venster aan om de game te renderen, wordt na functie ook afgesloten
    window = sdl2.ext.Window("levelup", size=(BREEDTE, HOOGTE))
    window.show()
    renderer = sdl2.ext.Renderer(window)
    # afbeelding erin
    resources = sdl2.ext.Resources(__file__, "textures")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    shop_afbeelding = factory.from_image(resources.get_path("shop.jpg"))
    start_shopx = window.size[0] / 4
    start_shopy = window.size[1] - shop_afbeelding.size[1]
    breedte_shop = window.size[0] / 2
    hoogte_shop = window.size[1] / 2

    font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=30, color=kleuren[3])
    errormessage = ""
    while True:
        renderer.clear()
        renderer.fill((0, 0, BREEDTE, HOOGTE), kleuren[7])
        renderer.copy(shop_afbeelding, dstrect=(start_shopx, start_shopy, breedte_shop, hoogte_shop))

        if errormessage:  # lege string wordt gezien als een false, errormessage krijgt pas waarde bij een error
            message = f'{errormessage}'
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:  # nummers gaan van 48(=0) tot 57(=9)
                key = event.key.keysym.sym
                if key == sdl2.SDLK_s:
                    # message = f'kies een map door een getal van 1 t.e.m. {aantal_mappen} in te geven'
                    renderer.clear()
                    sdl2.ext.quit()
                    startscherm("level_up")
                if key == sdl2.SDLK_ESCAPE:
                    quit()

        text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
        renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        renderer.present()

def levelfailed(reden):
    global world_map
    # waarden resetten
    reset_startwaarden()
    sdl2.ext.init()
    # Maak een venster aan om de game te renderen, wordt na functie ook afgesloten
    window = sdl2.ext.Window("level mislukt", size=(BREEDTE, HOOGTE))
    window.show()
    renderer = sdl2.ext.Renderer(window)
    # afbeelding erin
    resources = sdl2.ext.Resources(__file__, "textures")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    shop_afbeelding = factory.from_image(resources.get_path("shop.jpg"))
    start_shopx = window.size[0] / 4
    start_shopy = window.size[1] - shop_afbeelding.size[1]
    breedte_shop = window.size[0] / 2
    hoogte_shop = window.size[1] / 2

    font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=30, color=kleuren[3])
    errormessage = ""
    message = f'Game Over, {reden} \n druk op "r" op opnieuw te proberen'
    while True:
        renderer.clear()
        renderer.fill((0, 0, BREEDTE, HOOGTE), kleuren[7])
        renderer.copy(shop_afbeelding, dstrect=(start_shopx, start_shopy, breedte_shop, hoogte_shop))

        if errormessage:  # lege string wordt gezien als een false, errormessage krijgt pas waarde bij een error
            message = f'{errormessage}'
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

def save(option):
    global level
    global p_speler, r_speler, pizza_collected, apple_collected, egg_collected, broccoli_collected, total_hearts_present, total_money_present, level, tijd_verstrekentot
    # waarden_speler = {'positie': p_speler, 'richting': r_speler, 'pizza':pizza_collected, 'appel': apple_collected, 'egg':egg_collected,'broccoli':broccoli_collected,'hearts':total_hearts_present,'money':total_money_present}
    # waarden_wereld = { 'level': level,'time':tijd_verstrekentot}
    if option == "save":
        tesaven_waarden = {'p_speler': p_speler, 'r_speler': r_speler, 'pizza_collected': pizza_collected,
                           'apple_collected': apple_collected, 'egg_collected': egg_collected, 'broccoli_collected': broccoli_collected,
                           'total_hearts_present': total_hearts_present, 'total_money_present': total_money_present,
                           'level': level, 'tijd_verstrekentot': tijd_verstrekentot
                           }
        outfile = open(persistantfile, 'wb')
        pickle.dump(tesaven_waarden, outfile)
        outfile.close()
        # print(tesaven_waarden, "zijn gesaved \n")
        print("saven \n")
        printvariables()
    elif option == "load":
        infile = open(persistantfile,'rb')
        teladen = pickle.load(infile)
        infile.close()
        globals().update(teladen)
        if total_money_present >= 4:
            total_money_present = 0 #was naar 5 gebugged
        print("laden \n")
        printvariables()
    else:
        print('save failed')
        pass

def printvariables():
    print("printing variables positie, richting, level \n",p_speler, r_speler, level+1)

def rotatie(alfa, vector):
    # alfa moet in radialen!!!!
    rotatie_matrix = [[np.cos(alfa), -np.sin(alfa)], [np.sin(alfa), np.cos(alfa)]]
    return np.dot(rotatie_matrix, vector)


def wall_collission(pd):
    pdx = int(pd[0])
    pdy = int(pd[1])
    if world_map[pdx, pdy] != 0:
        return False
    else:
        return True


def verwerk_input(delta):
    global testboolean
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
            # hier nog alles van limitaties ook aanpassen
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
            if button == sdl2.SDL_BUTTON_RIGHT:
                save("save")
        # Een SDL_MOUSEWHEEL event wordt afgeleverd wanneer de gebruiker
        # aan het muiswiel draait.
        elif event.type == sdl2.SDL_MOUSEWHEEL:
            if event.wheel.y > 0:
                levelcompleted()
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
                rotatie_beweging = (beweging * math.pi / 2) / 50
                r_speler = rotatie(rotatie_beweging, r_speler)
                # r_speler = rotatie(beweging/100, r_speler)
                r_cameravlak = rotatie((math.pi / 2), r_speler)
                continue

    # Polling-gebaseerde input. Dit gebruiken we bij voorkeur om bv het ingedrukt
    # houden van toetsen zo accuraat mogelijk te detecteren
    key_states = sdl2.SDL_GetKeyboardState(None)

    # if key_states[sdl2.SDL_SCANCODE_UP] or key_states[sdl2.SDL_SCANCODE_W]:
    # beweeg vooruit...
    stapverkleiner = 0.05
    # moet querty volgen om een of andere reden
    if key_states[sdl2.SDL_SCANCODE_W]:  # komt overeen met Z
        pd = p_speler + (r_speler / (r_speler[0] ** 2 + r_speler[1] ** 2)) * stapverkleiner
        if wall_collission(pd):
            p_speler = pd
    if key_states[sdl2.SDL_SCANCODE_A]:  # komt overeen met D
        pd = p_speler + rotatie((3 / 2) * math.pi, r_speler / (r_speler[0] ** 2 + r_speler[1] ** 2)) * stapverkleiner
        if wall_collission(pd):
            p_speler = pd
    if key_states[sdl2.SDL_SCANCODE_D]:
        pd = p_speler + rotatie(math.pi / 2, r_speler / (r_speler[0] ** 2 + r_speler[1] ** 2)) * stapverkleiner
        if wall_collission(pd):
            p_speler = pd
    if key_states[sdl2.SDL_SCANCODE_S]:
        pd = p_speler + rotatie(math.pi, r_speler / (r_speler[0] ** 2 + r_speler[1] ** 2)) * stapverkleiner
        if wall_collission(pd):
            p_speler = pd
    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True

def bereken_r_straal(r_speler, kolom):
    # r_straal_kolom = d_camera * r_speler + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak

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

    delta_h = 1 / abs(r_straal[0])  # gebruikt x ipv y
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

            # hier elif tijdelijk toegevoegd, nog verder aanpassen
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
                    d_muur = math.sqrt(
                        (i_horizontaal_x[0] - p_speler[0]) ** 2 + (i_horizontaal_x[1] - p_speler[1]) ** 2)
                    is_texture = True
                    blok = world_map[i_horizontaal_x_rounded_int[0], (i_horizontaal_x_rounded_int[1])]
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (i_horizontaal_x - i_horizontaal_x_rounded_int)
                    break




            elif r_straal[0] < 0:
                if world_map[(i_horizontaal_x_rounded_int[0] - 1, i_horizontaal_x_rounded_int[1])]:
                    d_muur = math.sqrt(
                        (i_horizontaal_x[0] - p_speler[0]) ** 2 + (i_horizontaal_x[1] - p_speler[1]) ** 2)
                    is_texture = True
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (i_horizontaal_x - i_horizontaal_x_rounded_int)
                    # textuurcoordinaten_X = (i_horizontaal_x - i_horizontaal_x_rounded_int) * wall.size[0]
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
                if world_map[(i_verticaal_y_rounded_int[0]), (i_verticaal_y_rounded_int[1])]:
                    d_muur = math.sqrt((i_verticaal_y[0] - p_speler[0]) ** 2 + (i_verticaal_y[1] - p_speler[1]) ** 2)
                    is_texture = True
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (1 - (i_verticaal_y - i_verticaal_y_rounded_int))
                    # textuurcoordinaten_X = (1-(i_verticaal_y - i_verticaal_y_rounded_int)) * wall.size[0]
                    blok = world_map[(i_verticaal_y_rounded_int[0]), (i_verticaal_y_rounded_int[1])]
                    break



            elif r_straal[1] < 0:  # omgewisseld: 0 --> 1
                if world_map[i_verticaal_y_rounded_int[0], (i_verticaal_y_rounded_int[1] - 1)]:
                    d_muur = math.sqrt((i_verticaal_y[0] - p_speler[0]) ** 2 + (i_verticaal_y[1] - p_speler[1]) ** 2)
                    is_texture = True
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (1 - (i_verticaal_y - i_verticaal_y_rounded_int))
                    # textuurcoordinaten_X = (1-(i_verticaal_y - i_verticaal_y_rounded_int)) * wall.size[0]
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


def render_wall(renderer, window, kolom, d_muur, k_muur, is_texture, textuurcoordinaten_X_zondermaalbreedtetextuur,
                blok, list_wall_create):
    global is_horizontaal
    global wall

    muur = list_wall_create[blok]

    textuurcoordinaten_X = textuurcoordinaten_X_zondermaalbreedtetextuur * muur.size[0]
    hoogte = (HOOGTE) * 1 / (d_muur + 0.00001)  # 200/d_muur#(HOOGTE/2) * 1/d_muur
    # hoogte = (HOOGTE / 2) * 1 / d_muur

    if hoogte >= HOOGTE:  # hier stond 1/2 naar 1 gezet
        y1 = 0
    else:
        y1 = (HOOGTE - hoogte) / 2  # -1 toegevoegd

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
            renderer.copy(muur, srcrect=(textuur_x, textuur_y, breedte_textuur / 100, hoogte_textuur),
                          dstrect=(scherm_x, scherm_y, 1, hoogte))
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
    renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 200, text.size[0], text.size[1]))


def scannergun_sprites_create():
    scannergun_texture = factory.from_image(resources.get_path("scanner.png"))
    crosshair_texture = factory.from_image(resources.get_path("crosshair_white.png"))
    laser_texture = factory.from_image(resources.get_path("scanner_laser2.png"))
    return scannergun_texture, crosshair_texture, laser_texture


def scannergun():
    global laser_shot, laser_shot_rent
    global window
    global renderer
    global scannergun_texture, crosshair_texture, laser_texture

    renderer.copy(scannergun_texture, srcrect=(0, 0, scannergun_texture.size[0], scannergun_texture.size[1]),
                  dstrect=(499, 715, scannergun_texture.size[0], scannergun_texture.size[1]))
    # crosshair
    renderer.copy(crosshair_texture, srcrect=(0, 0, crosshair_texture.size[0], crosshair_texture.size[1]),
                  dstrect=(580, 577, crosshair_texture.size[0], crosshair_texture.size[1]))
    if laser_shot == True:
        playsound("../resources/Scanner_beep_3.mp3")
        renderer.copy(laser_texture, srcrect=(0, 0, laser_texture.size[0], laser_texture.size[1]),
                      dstrect=(581, 598, laser_texture.size[0], laser_texture.size[1]))
        laser_shot = False
        # functional scanner
        pizza_collected = check_if_object_scanned(pizza_x, pizza_y)


def timer(delta, renderer, window, deadline):
    global tijd_verstrekentot
    tijd_deadline = deadline
    tijd_verstrekentot += delta
    message = f'je hebt nog {int(deadline - tijd_verstrekentot) + 1} seconden'
    text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
    if tijd_verstrekentot > tijd_deadline:
        message = f'je tijd is op :('
        text = sdl2.ext.renderer.Texture(renderer, fps_font.render_text(message))
        levelfailed("tijd was op")
    else:
        renderer.draw_rect(
            (10, 600 + text.size[1] * 2, (tijd_verstrekentot / tijd_deadline) * text.size[0], text.size[1]), kleuren[7])

    renderer.copy(text, dstrect=(10, 600 + text.size[1], text.size[0], text.size[1]))


def create_sprites_hud():
    # global hud_texture, pizza_texture, pizza_gray_texture, apple_texture, apple_gray_texture, egg_texture, egg_gray_texture, broccoli_texture, broccoli_gray_texture
    hud_texture = factory.from_image(resources.get_path("hud.png"))
    pizza_texture = factory.from_image(resources.get_path("pizza.png"))
    pizza_gray_texture = factory.from_image(resources.get_path("pizza_gray.png"))
    apple_texture = factory.from_image(resources.get_path("apple.png"))
    apple_gray_texture = factory.from_image(resources.get_path("apple_gray.png"))
    egg_texture = factory.from_image(resources.get_path("egg.png"))
    egg_gray_texture = factory.from_image(resources.get_path("egg_gray.png"))
    broccoli_texture = factory.from_image(resources.get_path("broccoli.png"))
    broccoli_gray_texture = factory.from_image(resources.get_path("broccoli_gray.png"))
    moneysprite1 = factory.from_image(resources.get_path("money.png"))
    moneysprite2 = factory.from_image(resources.get_path("money2.png"))
    moneysprite3 = factory.from_image(resources.get_path("money3.png"))
    moneysprite4 = factory.from_image(resources.get_path("money4.png"))
    moneysprites = [moneysprite1, moneysprite2, moneysprite3, moneysprite4]
    heartsprite1 = factory.from_image(resources.get_path("heart1.png"))
    heartsprite2 = factory.from_image(resources.get_path("heart2.png"))
    heartsprite3 = factory.from_image(resources.get_path("heart3.png"))
    heartsprites = [heartsprite1, heartsprite2, heartsprite3]
    return hud_texture, pizza_texture, pizza_gray_texture, apple_texture, apple_gray_texture, egg_texture, egg_gray_texture, broccoli_texture, broccoli_gray_texture, moneysprites, heartsprites


def hud():
    global player_hit, render_pizza_in_world, pizza_collected, apple_collected, egg_collected, broccoli_collected, total_hearts_present, heartsprite, player_hit, total_money_present, money_collected, moneysprite

    renderer.copy(hud_texture, srcrect=(0, 0, hud_texture.size[0], hud_texture.size[1]),
                  dstrect=(400, 0, hud_texture.size[0], hud_texture.size[1]))

    # pizza
    if pizza_collected == True:
        # pizza_collected: breedte = 35, hoogte = 35 (altijd hetzelfde vandaar als constante ingevuld en niet in een aparte variabele gestoken/pizza_collected.size[0] en [1] telkens oproepen)
        renderer.copy(pizza_texture, srcrect=(0, 0, 35, 35), dstrect=(420, 20, 35, 35))
    else:
        # gray pizza
        # pizza_gray_texture: breedte = 35, hoogte = 35
        renderer.copy(pizza_gray_texture, srcrect=(0, 0, 35, 35), dstrect=(420, 20, 35, 35))

    # apple
    if apple_collected == True:
        # apple_texture: breedte = 35, hoogte = 35
        renderer.copy(apple_texture, srcrect=(0, 0, 35, 35), dstrect=(490, 20, 35, 35))
    else:
        # gray apple
        # apple_gray_texture: breedte = 35, hoogte = 35
        renderer.copy(apple_gray_texture, srcrect=(0, 0, 35, 35), dstrect=(490, 20, 35, 35))

    # egg
    if egg_collected == True:
        # egg_texture: breedte = 30, hoogte = 40
        renderer.copy(egg_texture, srcrect=(0, 0, 30, 40), dstrect=(562.5, 17.5, 30, 40))
    else:
        # egg gray
        # egg_gray_texture: breedte = 30, hoogte = 40
        renderer.copy(egg_gray_texture, srcrect=(0, 0, 30, 40), dstrect=(562.5, 17.5, 30, 40))

    # broccoli
    if broccoli_collected == True:
        # broccoli_texture: breedte = 42, hoogte = 45
        renderer.copy(broccoli_texture, srcrect=(0, 0, 42, 45), dstrect=(625, 16, 42, 45))
    else:
        # broccoli gray
        # broccoli_gray_texture: breedte = 42, hoogte = 45
        renderer.copy(broccoli_gray_texture, srcrect=(0, 0, 42, 45), dstrect=(625, 16, 42, 45))

    # hearts
    if player_hit == True:
        total_hearts_present -= 1
        player_hit = False

    if total_hearts_present:
        heart_texture = heartsprites[(total_hearts_present - 1)]
        renderer.copy(heart_texture, srcrect=(0, 0, heart_texture.size[0], heart_texture.size[1]),
                      dstrect=(1090, 30, heart_texture.size[0], heart_texture.size[1]))
    else:
        print("game over")
        # game_over = True

    # money
    if money_collected == True:
        total_money_present += 1
        money_collected = False
        # money_collected = False
    elif total_money_present == 0:
        total_money_present += 1
    if total_money_present:
        money_texture = moneysprites[(total_money_present - 1)]

        renderer.copy(money_texture, srcrect=(0, 0, money_texture.size[0], money_texture.size[1]),
                      dstrect=(885, 35, money_texture.size[0], money_texture.size[1]))

def create_kaart_sprites():
    map0 = factory.from_image(resources.get_path("map0.jpg"))
    map1 = factory.from_image(resources.get_path("map1.jpg"))
    map2 = factory.from_image(resources.get_path("map2.jpg"))
    map3 = factory.from_image(resources.get_path("map3.jpg"))
    map_weergave_list = [map0, map1, map2, map3]
    gsm = factory.from_image(resources.get_path("gsm_test2-BIJGESNEDEN.png"))
    positie_persoon_sprite = factory.from_image(resources.get_path("pion_bolletje.png"))
    tekst_gsm = factory.from_image(resources.get_path("Store_tekst_gsm.jpg"))
    return map_weergave_list, gsm, positie_persoon_sprite, tekst_gsm

def kaart_weergeven():
    global map_weergave_list, gsm, positie_persoon_sprite, tekst_gsm, kaart_gekozen
    # grootte positie_persoon_image is (34, 34)
    # print(map_weergave.size) #1403, 1412

    map_weergave = map_weergave_list[kaart_gekozen]
    if kaart_genomen == True:
        # mogelijke optimalisatie de hoogte en breedtes als variabelen opslaan of als getallen invullen ipv size opvragen
        renderer.copy(gsm, srcrect=(0, 0, gsm.size[0], gsm.size[1]),
                      dstrect=(18, 20, gsm.size[0] * 1.2, gsm.size[1] * 1.2))
        renderer.copy(map_weergave, srcrect=(0, 0, map_weergave.size[0], map_weergave.size[1]),
                      dstrect=(30, 50, map_weergave.size[0] / 12, map_weergave.size[1] / 12))
        # renderer.copy(tekst_gsm, srcrect=(0,0, tekst_gsm.size[0], tekst_gsm.size[1]), dstrect=(50, 500, tekst_gsm.size[0]/4, tekst_gsm.size[1]/4))
        renderer.copy(tekst_gsm, srcrect=(0, 0, tekst_gsm.size[0], tekst_gsm.size[1]),
                      dstrect=(45, 200, tekst_gsm.size[0] / 4, tekst_gsm.size[1] / 4))

        positie_pion_x = 30 - (17 / 7) + (
                    (map_weergave.size[0] / 12) - (p_speler[1] / 18) * (map_weergave.size[0] / 12))
        # kaart positie (0,0) = ((30 - (17/7)),(50 - (17/7)))
        # 22 + ((p_speler[0] / 18) * (map_weergave.size[1] - 4))  # ( 16+(p_speler[0]/18)*(map_weergave.size[0]-5))
        # mss toch gsm ofzo rond zetten dan kan vierkante afbeelding als kaart (niet knippen, naar juiste pixels converteren dus niet pixelconverter online)en Geen rand!!
        # map size breedt en hoogte voorlopig gwn manueel 18 ingevuld
        positie_pion_y = 50 - (17 / 7) + ((p_speler[0] / 18) * (map_weergave.size[1] / 12))
        # print(positie_pion_x, positie_pion_y)
        # 22 + map_weergave.size[0] - ((p_speler[1] / 18) * (map_weergave.size[0] - 4))  # 16+ map_weergave.size[1]-((p_speler[1]/18)*(map_weergave.size[1]-5))
        # waar is potitie, linkerbovenhoek sprite, rechterbovenhoek...
        renderer.copy(positie_persoon_sprite,
                      srcrect=(0, 0, positie_persoon_sprite.size[0], positie_persoon_sprite.size[1]), dstrect=(
                positie_pion_x, positie_pion_y, positie_persoon_sprite.size[0] / 7, positie_persoon_sprite.size[1] / 7))

def sprite_renderer(sprite_x, sprite_y, sprite, z_buffer):
    # zbuffer later nog toevoegen voor overlappingen, en per kolom

    p_sprite_x_nieuw = sprite_x - p_speler[0]
    p_sprite_y_nieuw = sprite_y - p_speler[1]
    # determinant van cameramatrix
    determinant_m = r_cameravlak[0] * r_speler[1] - r_cameravlak[1] * r_speler[0]

    # for sprite_kolom in range(0, breedte_sprite):

    # breedte_sprite_scherm = (breedte_sprite_wereld/hoogte_sprite_wereld)* hoogte_sprite_scherm #"nodig?want zal 1 zijn per kolom maar hoe weten of nog"
    # renderer.copy(broccoli_texture, srcrect=(0, 0, breedte_sprite_wereld, hoogte_sprite_wereld), dstrect=((((a+1)/2)*BREEDTE)-breedte_sprite_scherm/2, HOOGTE/2, 1vc b , hoogte_sprite_scherm))
    u_cameracoordinaten = ((r_speler[1] / determinant_m) * p_sprite_x_nieuw) + (
            (-r_speler[0] / determinant_m) * p_sprite_y_nieuw)
    v_cameracoordinaten = ((-r_cameravlak[1] / determinant_m) * p_sprite_x_nieuw) + (
            (r_cameravlak[0] / determinant_m) * p_sprite_y_nieuw)
    a = u_cameracoordinaten / v_cameracoordinaten  # positie op x as scherm, dus kolom

    if (a >= -1) and (a <= 1) and (v_cameracoordinaten >= 0):
        kolom_midden_sprite = (((a + 1) / 2) * BREEDTE)
        hoogte_sprite_wereld = sprite.size[1]
        breedte_sprite_wereld = sprite.size[0]

        d_object_kolom_speler = math.sqrt(((sprite_x - p_speler[0]) ** 2) + ((sprite_y - p_speler[1]) ** 2))
        hoogte_sprite_scherm = HOOGTE * (1 / (d_object_kolom_speler * 5))
        breedte_sprite_scherm = (breedte_sprite_wereld / hoogte_sprite_wereld) * hoogte_sprite_scherm  # "nodig?want zal 1 zijn per kolom maar hoe weten of nog"
        beginpunt_sprite_x = kolom_midden_sprite - (breedte_sprite_scherm / 2)

        for kolom_texture_scherm in range(0, int(breedte_sprite_scherm + 0.5)):
            kolom = kolom_texture_scherm + int(beginpunt_sprite_x) #+ 0.5)
            kolom_texture = (kolom_texture_scherm / breedte_sprite_scherm) * breedte_sprite_wereld
            if(kolom < BREEDTE):
                if z_buffer[kolom] >= d_object_kolom_speler:
                    renderer.copy(sprite, srcrect=(kolom_texture, 0, 1, hoogte_sprite_wereld),dstrect=(kolom, (HOOGTE / 2) - (hoogte_sprite_scherm / 2), 1, hoogte_sprite_scherm))


# checking if we hit an object with our scanner
def check_if_object_scanned(scanobject_x, scanobject_y):
    global render_pizza_in_world
    if 380 <= scanobject_x <= 435 and 277 <= scanobject_y <= 322:
        render_pizza_in_world = False
        return True


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
    global keuzealgemaakt
    if not keuzealgemaakt:
        save("load")
        keuzealgemaakt = True
        loadornew()
    # startscherm("new_game")
    tijd_verstrekentot = 0
    fps_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])

    # print(world_map)
    # Initialiseer de SDL2 bibliotheek
    global kaart_gekozen
    global laser_shot, total_hearts_present, heart1_present, heart2_present, heart3_present, player_hit, total_money_present, pizza_collected, money_collected, moneysprite, heartsprite
    sdl2.ext.init()

    global pizza_x, pizza_y, apple_x, apple_y, egg_x, egg_y, broccoli_x, broccoli_y, munt1_x, munt1_y, munt2_x, munt2_y, munt3_x, munt3_y, munt4_x, munt4_y

    pizza_x, pizza_y = pizza_x_coordinaten[kaart_gekozen], pizza_y_coordinaten[kaart_gekozen]  # 299.5
    apple_x, apple_y = apple_x_coordinaten[kaart_gekozen], apple_y_coordinaten[kaart_gekozen]

    egg_x, egg_y = egg_x_coordinaten[kaart_gekozen], egg_y_coordinaten[kaart_gekozen]
    broccoli_x, broccoli_y = broccoli_x_coordinaten[kaart_gekozen], broccoli_y_coordinaten[kaart_gekozen]
    munt1_x, munt1_y = munt1_x_coordinaten[kaart_gekozen], munt1_y_coordinaten[kaart_gekozen]
    munt2_x, munt2_y = munt2_x_coordinaten[kaart_gekozen], munt2_y_coordinaten[kaart_gekozen]
    munt3_x, munt3_y = munt3_x_coordinaten[kaart_gekozen], munt3_y_coordinaten[kaart_gekozen]
    munt4_x, munt4_y = munt4_x_coordinaten[kaart_gekozen], munt4_y_coordinaten[kaart_gekozen]

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

    # textures aanmaken
    list_wall_create = create_textures()
    global hud_texture, pizza_texture, pizza_gray_texture, apple_texture, apple_gray_texture, egg_texture, egg_gray_texture, broccoli_texture, broccoli_gray_texture, moneysprites, heartsprites
    # sprites hud aanmeken
    hud_texture, pizza_texture, pizza_gray_texture, apple_texture, apple_gray_texture, egg_texture, egg_gray_texture, broccoli_texture, broccoli_gray_texture, moneysprites, heartsprites = create_sprites_hud()
    global scannergun_sprite, map_weergave_list, gsm, positie_persoon_sprite, tekst_gsm

    # sprites kaart aanmaken
    map_weergave_list, gsm, positie_persoon_sprite, tekst_gsm = create_kaart_sprites()
    global scannergun_texture, crosshair_texture, laser_texture
    # sprites scanner aanmaken
    scannergun_texture, crosshair_texture, laser_texture = scannergun_sprites_create()
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
        renderer.copy(color_textures[4], srcrect=(0, 0, 1, 1), dstrect=(0, 0, BREEDTE, HOOGTE / 2))
        # floor
        renderer.copy(color_textures[5], srcrect=(0, 0, 1, 1), dstrect=(0, HOOGTE / 2, BREEDTE, HOOGTE / 2))
        z_buffer = []
        for kolom in range(0, window.size[0]):
            r_straal = bereken_r_straal(r_speler, kolom)
            if r_straal[0] == 0 or r_straal[1] == 0:
                z_buffer.append(100)
                continue
            (d_muur, k_muur, is_texture, textuurcoordinaten_X_zondermaalbreedtetextuur, blok) = raycast(p_speler,r_straal)
            z_buffer.append(d_muur)
            render_wall(renderer, window, kolom, d_muur, k_muur, is_texture,textuurcoordinaten_X_zondermaalbreedtetextuur, blok, list_wall_create)

        sprite_renderer(pizza_x, pizza_y, pizza_texture, z_buffer)
        sprite_renderer(apple_x, apple_y, apple_texture, z_buffer)
        sprite_renderer(egg_x, egg_y, egg_texture, z_buffer)
        sprite_renderer(broccoli_x, broccoli_y, broccoli_texture, z_buffer)
        moneysprite_1 = moneysprites[0]
        sprite_renderer(munt1_x, munt1_y, moneysprite_1, z_buffer)
        sprite_renderer(munt2_x, munt2_y, moneysprite_1, z_buffer)
        sprite_renderer(munt3_x, munt3_y, moneysprite_1, z_buffer)
        sprite_renderer(munt4_x, munt4_y, moneysprite_1, z_buffer)

        end_time = time.time()
        delta = end_time - start_time
        verwerk_input(delta)
        timer(delta, renderer, window, deadline)
        # Teken gemiddelde fps van de laatste 20 frames
        fps_list.append(1 / (time.time() - start_time))
        if len(fps_list) == 20:
            fps = np.average(fps_list)
            fps_list = []
        render_fps(fps, renderer, window)

        scannergun()
        hud()

        if kaart_genomen == True:
            kaart_weergeven()

        # Verwissel de rendering context met de frame buffer
        renderer.present()
        # na renderen frame venster verversen
        window.refresh()
    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    # comments met #sv naast wegdoen als je wilt kijken naar snakeviz
    # profiler = cProfile.Profile() # sv
    # profiler.enable() # sv
    main()
    # profiler.disable() # sv
    # stats = pstats.Stats(profiler) # sv
    # stats.dump_stats('data_prof') # sv
