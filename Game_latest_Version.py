import math
import time
import pickle
import sdl2
import serial

#als optimalisatie voor frame rate, kan 9600 hogerlr
import numpy as np
import sdl2.ext
COM_POORT='COM14'
from levels import *
from playsound import playsound
persistantfile = "save.pkl"
keuzealgemaakt = False
level = 0
testboolean = True
# Constanten
BREEDTE = 1200
HOOGTE = 900
# var aanmaken


#
# Globale variabelen
win_flags = sdl2.SDL_WINDOW_RESIZABLE #kan window resizen
global is_horizontaal
global renderer
global list_wall_create
laser_shot = False
kaart_genomen = False

levelup = False
render_pizza_in_world = True
pizza_collected = False

apple_collected = False
egg_collected = False
broccoli_collected = False
heartsprite = "heart3.png"
total_hearts_present = 3
aantal = 2

player_hit = False
clerk_dead=False
resources = sdl2.ext.Resources(__file__, "textures")

total_money_present = 0
money1_aantal=0
money2_aantal =0
money3_aantal=0
money4_aantal = 0
money1_collected = False
money2_collected = False
money3_collected = False
money4_collected = False
moneysprite = ""

# coordinaten sprites
pizza_x_coordinaten, pizza_y_coordinaten =         [4, 1.5, 15.5, 6.5],    [5.5, 14.5, 13.5, 3.5]  #
apple_x_coordinaten, apple_y_coordinaten =         [6.5, 10, 16, 2],    [12.5, 11, 9, 7]  #
egg_x_coordinaten, egg_y_coordinaten =             [12, 13.5, 5, 7.5],   [4.5, 11.5, 11, 2.5]  #
broccoli_x_coordinaten, broccoli_y_coordinaten =   [9, 10.5, 6.5, 15.5], [7.5, 2, 15.5, 8.5]  #
munt1_x_coordinaten, munt1_y_coordinaten =         [10, 2, 4, 8],        [10, 2, 10, 11.5]
munt2_x_coordinaten, munt2_y_coordinaten =         [1.5, 7.5, 10, 16.5],       [7, 9, 16, 12.5]
munt3_x_coordinaten, munt3_y_coordinaten =         [12, 13, 13, 11.5],     [1.5, 14.5, 10, 3.5]
munt4_x_coordinaten, munt4_y_coordinaten =         [3, 4, 7, 1.5],         [1.5, 16, 7, 1.5]
gsm_x_coordinaten,gsm_y_coordinaten  = [3, 16, 16.5, 11.5], [16, 9, 1.5, 3.5]
p_kassa_by_level_x = [16.5, 0.5, 1.5, 10.5]
p_kassa_by_level_y = [7.5, 1.5, 1.5, 11.5]

tijd_verstrekentot = 0


deadline_min = 5
deadline_sec = 10
# positie van de speler
p_speler = np.array([9.5, 15.5])

# richting waarin de speler kijkt
r_speler = np.array([0, 1])

# afstand tot cameravlak
d_camera = 1


money1_rendered = True
money2_rendered = True
money3_rendered = True
money4_rendered = True

# middelpunt cameravlak
middelpuntcameravlak = p_speler + d_camera * r_speler

# cameravlak
rotmin90 = np.array([[0, 1], [-1, 0]])  # [cos alfa, -sin afla],[sin alfa, cos alfa] voor -pi/2
r_cameravlak = np.dot(rotmin90, r_speler)

# wordt op True gezet als het spel afgesloten moet worden
moet_afsluiten = False
is_texture = False
exit_allowed = False
# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn
#dit staat in document levels.py

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
    sdl2.ext.Color(252, 210, 153)    #8 = oranje
]

#groottes van alle texturen, sprites... (zodat .size minder tot niet gebruikt)
hud_texture_hoogte = 75
hud_texture_breedte = 800
scannergun_texture_breedte = 606
scannergun_texture_hoogte = 586

crosshair_texture_breedte = 55
crosshair_texture_hoogte = 45

laser_texture_breedte = 50
laser_texture_hoogte = 277
gsm_breedte = 151
gsm_hoogte = 231
tekst_gsm_breedte = 355
tekst_gsm_hoogte = 157
positie_persoon_sprite_breedte = 34
positie_persoon_sprite_hoogte = 34
map_weergave_breedte = 1403
map_weergave_hoogte = [1412, 1416, 1410, 1420]
#map 0, 1, 2, 3 i(breedte altijd dezelfde)
heart_breedtes = [25, 55, 85]
heart_hoogte = 25
money_breedtes = [25, 48, 72, 97]
money_hoogte = 18
#0 : pizza, #1: apple, egg, broccoli, gsmsprite
sprite_breedtes = [35, 35, 30 , 42, 35,150, 100]
sprite_hoogtes = [35, 35, 40, 45, 55,110, 100]

#0: 'empty', #1 rek, kassa, frigo, melkfrigo, roodrek, slager, winkelmuur, bakker
textures_breedtes = ["empty", 1490, 1300, 1180, 1310, 340, 800, 510, 680]
textures_hoogtes = ["empty", 1490, 1300, 1050, 1350, 380, 730 , 510, 670]


personal_records = [0, 0, 0, 0]

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
    start_shopx = BREEDTE / 4
    breedte_shop = BREEDTE / 2
    hoogte_shop = (breedte_shop / shop_afbeelding.size[0]) * shop_afbeelding.size[1]
    start_shopy = HOOGTE - hoogte_shop
    witruimtetussenknop = (BREEDTE / aantal_mappen) / 8
    while not stoppen:
        renderer.clear()
        renderer.fill((0, 0, BREEDTE, HOOGTE), kleuren[7])  # witte achtergrond
        renderer.copy(shop_afbeelding, dstrect=(start_shopx, start_shopy, breedte_shop, hoogte_shop))
        # start knoppen
        renderer.draw_rect((start_shopx, start_shopy - 250, breedte_shop, 100), kleuren[8])
        renderer.copy(sdl2.ext.renderer.Texture(renderer, font.render_text("new game")),
                      dstrect=(start_shopx, start_shopy - 250, breedte_shop, 100))
        renderer.draw_rect((start_shopx, start_shopy-100, breedte_shop, 100), kleuren[1])
        renderer.copy(sdl2.ext.renderer.Texture(renderer, font.render_text("load game")),
                      dstrect=(start_shopx, start_shopy-100, breedte_shop, 100))
        events = sdl2.ext.get_events()
        for event in events:
            key = event.key.keysym.sym
            if event.type == sdl2.SDL_KEYDOWN:  # nummers gaan van 48(=0) tot 57(=9)
                #key = event.key.keysym.sym
                if key == sdl2.SDLK_ESCAPE:
                    quit()
            elif event.type == sdl2.SDL_MOUSEMOTION:
                motion = event.motion
            if key ==sdl2.SDLK_z or key==sdl2.SDLK_s or event.type == sdl2.SDL_MOUSEBUTTONDOWN:  #hier stond elif
                button = event.button.button
                if  key ==sdl2.SDLK_z or  key==sdl2.SDLK_s or button == sdl2.SDL_BUTTON_LEFT:

                    # kijkt of er op  timer knop is geklikt
                    if key ==sdl2.SDLK_z or key ==sdl2.SDLK_s or start_shopx < motion.x < start_shopx + breedte_shop :
                        motion = event.motion #ttttt
                        if key ==sdl2.SDLK_z or start_shopy - 150 > motion.y > start_shopy - 250:  # new game knop
                            startscherm("new_game")
                            stoppen = True
                        if  key==sdl2.SDLK_s or start_shopy-100< motion.y < start_shopy  :
                            startscherm("load_game")
                            stoppen = True

                    # kijkt of er op een lvl knop is geklik
        font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[0])
        text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
        renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        renderer.present()

    renderer.clear()
    sdl2.ext.quit()


def reset_startwaarden():
    global p_speler, r_speler, pizza_collected, apple_collected, egg_collected, broccoli_collected, total_money_present, total_hearts_present, money1_collected, money2_collected, money3_collected, money4_collected, money1_rendered, money2_rendered, money3_rendered, money4_rendered, money1_aantal, money2_aantal, money3_aantal, money4_aantal, kaart_genomen

    r_speler = np.array([0, 1])
    p_speler = np.array([9.5, 15.5])
    pizza_collected = False
    apple_collected = False
    egg_collected = False
    broccoli_collected = False
    total_hearts_present = 3
    total_money_present = 1
    money1_collected = False
    money2_collected = False
    money3_collected = False
    money4_collected = False
    money1_rendered = True
    money2_rendered = True
    money3_rendered = True
    money4_rendered = True
    money1_aantal = 0
    money2_aantal = 0
    money3_aantal = 0
    money4_aantal = 0
    kaart_genomen = False
    renderer.clear



def startscherm(keuze):
    global world_map
    global deadline_min, deadline_sec
    global kaart_gekozen
    global levelup
    global level,money1_aantal,money2_aantal,money3_aantal,money4_aantal
    if keuze == "new_game":
        resetwaarden = {'p_speler': np.array([9.5, 15.5]), 'r_speler': np.array([0, 1]), 'pizza_collected': False,
                        'apple_collected': False, 'egg_collected': False,
                        'broccoli_collected': False,
                        'total_hearts_present': 3, 'total_money_present': 1,
                        'level': 0, 'tijd_verstrekentot': False, 'money1_collected': False, 'money2_collected': False,
                        'money3_collected': False, 'money4_collected': False,
                        'money1_rendered': True, 'money2_rendered': True, 'money3_rendered': True,
                        'money4_rendered': True,
                        'money1_aantal': 0, 'money2_aantal': 0, 'money3_aantal': 0, 'money4_aantal': 0,
                        'kaart_genomen': False
                        }
        save("save")
        testarray = np.array([0, 1])
        globals().update(resetwaarden)



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

    message = f' welkom bij onze winkel!!! \n om te starten klik op de capacitive touch 2 keer \n navigeren tussen levels kan met de groen en blauwe knop \n tijd aanpassen kan met oranje en rode knop'
    keuze = ''
    if not levelup:
        gameinfo = f'gekozen map level {level} \n je hebt {deadline_min} min en {deadline_sec} seconden'
    else:
        gaminfo = f'congrats! new level {level} \n je hebt {deadline_min} min en {deadline_sec} seconden'
        levelup = False
    font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[0])
    infofont = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=10, color=kleuren[0])
    moet_afsluiten = False
    start_shopx = BREEDTE / 4
    breedte_shop = BREEDTE / 2
    hoogte_shop = (breedte_shop / shop_afbeelding.size[0]) * shop_afbeelding.size[1]
    start_shopy = HOOGTE - hoogte_shop
    lvlbuttonxstartwaarde = {}
    witruimtetussenknop = (BREEDTE / aantal_mappen) / 8
    breedte_knop = BREEDTE / aantal_mappen - witruimtetussenknop * 2
    while not moet_afsluiten:
        gameinfo = f'gekozen map level {level + 1} \n je hebt {deadline_min} min en {deadline_sec} seconden'
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
        renderer.draw_rect((BREEDTE / 8, (1 / 2) * HOOGTE, 50, 50), kleuren[8])
        renderer.copy(sdl2.ext.renderer.Texture(renderer, font.render_text("+")),
                      dstrect=(BREEDTE / 8, (1 / 2) * HOOGTE, 50, 50))
        renderer.draw_rect((BREEDTE / 8, (2 / 3) * HOOGTE, 50, 50), kleuren[1])
        renderer.copy(sdl2.ext.renderer.Texture(renderer, font.render_text("-")),
                      dstrect=(BREEDTE / 8, (2 / 3) * HOOGTE, 50, 50))
        if errormessage:  # lege string wordt gezien als een false, errormessage krijgt pas waarde bij een error
            message = f'{errormessage}'
        events = sdl2.ext.get_events()
        for event in events:

            if event.type == sdl2.SDL_MOUSEMOTION:
                motion = event.motion

            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN or event.type==sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                button = event.button.button
                if key== sdl2.SDLK_z or key== sdl2.SDLK_s or button == sdl2.SDL_BUTTON_LEFT :
                    # kijkt of er op  timer knop is geklikt
                    if key== sdl2.SDLK_z or key== sdl2.SDLK_s or BREEDTE / 8 < motion.x < ((BREEDTE / 8) + 50) :
                        geklikt = False
                        change = 0
                        if key== sdl2.SDLK_z or 0.5 * HOOGTE + 50 > motion.y > 0.5 * HOOGTE :  # + knop
                            geklikt = True
                            change = 10
                        if key== (sdl2.SDLK_s or (2 / 3) * HOOGTE < motion.y < (2 / 3) * HOOGTE + 50)  and (deadline_sec > 5 or deadline_min >= 1):
                            geklikt = True
                            change = -10
                        if geklikt:
                            if deadline_min == 1 and deadline_sec == 30 and change == -10:
                                deadline_min = 1
                                deadline_sec = 30
                            else:
                                if deadline_sec == 0 and change == -10:  # -10
                                    deadline_sec = 50  # 59
                                    deadline_min -= 1  # += change
                                elif deadline_sec < 50:  # 59
                                    deadline_sec += change
                                elif deadline_sec == 50 and change == 10:
                                    deadline_sec = 0
                                    deadline_min += 1
                                else:
                                    deadline_sec += change
                                    gameinfo = f'gekozen map level {level} \n je hebt {deadline_min} min en {deadline_sec} seconden'

                    # kijkt of er op een lvl knop is geklikt
                    elif 150 < motion.y < 250:
                        for knop in lvlbuttonxstartwaarde:
                            if lvlbuttonxstartwaarde[knop] < motion.x < lvlbuttonxstartwaarde[knop] + breedte_knop:
                                gekozenlevel = int(knop[-1]) - 1  # want naam knop is knop_<level>
                                level = gekozenlevel
                                world_map = maps[gekozenlevel]
                                kaart_gekozen = gekozenlevel
                                gameinfo = f'gekozen map level {level} \n je hebt {deadline_min} min en {deadline_sec} seconden'



            if event.type == sdl2.SDL_KEYDOWN:  # nummers gaan van 48(=0) tot 57(=9)
                key = event.key.keysym.sym
                # levels met pijltjes, aangepast, levels met q en d voor controller
                if key == sdl2.SDLK_q:#1073741904:  # 1073741904 = linker pijltje; 1073741903 = rechter pijltje
                    level -= 1
                    if level < 0:
                        level = 3
                    kaart_gekozen = level
                    world_map = maps[kaart_gekozen]
                if key == sdl2.SDLK_d:#1073741903:  # 1073741904 = linker pijltje; 1073741903 = rechter pijltje
                    level += 1
                    if level > 3:
                        level = 0
                    kaart_gekozen = level
                    world_map = maps[kaart_gekozen]
                elif key == sdl2.SDLK_ESCAPE:
                    quit()
                elif key == sdl2.SDLK_p:
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
                            gameinfo = f'gekozen map level {level} \n je hebt {deadline_min} min en {deadline_sec} seconden'

                            keuze = ""
                        except:
                            errormessage = f'je hebt een ongeldige waarde ingegeven \n gelieve een waarde tussen 1 en {aantal_mappen} in te geven'

            if keuze == "timer" and event.type == sdl2.SDL_MOUSEWHEEL:
                if deadline_sec > 5 or deadline_min >=1 or event.wheel.y > 0:
                    if deadline_sec == 0 and event.wheel.y < 0:
                        deadline_sec = 59 + (event.wheel.y + 1)
                        deadline_min -= 1
                    elif deadline_sec < 59:
                        deadline_sec += event.wheel.y
                    elif deadline_sec == 59 and event.wheel.y > 0:
                        deadline_sec = 0 + (event.wheel.y - 1)
                        deadline_min += 1
                    else:
                        deadline_sec += event.wheel.y
                        gameinfo = f'gekozen map level {level} \n je hebt {deadline_min} min en {deadline_sec} seconden'


        text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
        gaminfotext = sdl2.ext.renderer.Texture(renderer, infofont.render_text(gameinfo))
        renderer.copy(text, dstrect=(int((BREEDTE - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        renderer.copy(gaminfotext, dstrect=(0, HOOGTE - text.size[1], text.size[0], text.size[1]))
        renderer.present()

    sdl2.ext.quit()
    main()

def exit_level_action():
    global level
    global levelup
    if level == 3:
        message_congrats = f'Proficiat! Alle levels zijn voltooid!'
        level = 0
    else:
        message_congrats = f'Proficiat! Level is voltooid!'
        level += 1
        levelup = True
    reset_startwaarden()
    sdl2.ext.init()
    # Maak een venster aan om de game te renderen, wordt na functie ook afgesloten
    window = sdl2.ext.Window("level voltooid", size=(BREEDTE, HOOGTE))
    window.show()
    renderer = sdl2.ext.Renderer(window)
    # afbeelding erin
    resources = sdl2.ext.Resources(__file__, "resources")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    achtergrond = factory.from_image(resources.get_path("kassa_ticket_res2.png"))

    message_it_took = f'Tijd die je nodig had:'

    time_needed_min = int(tijd_verstrekentot // 60)
    time_needed_sec = int((tijd_verstrekentot / 60 - time_needed_min) * 60)
    message_time_needed = f'{time_needed_min} minuten en {time_needed_sec} seconden.'

    if personal_records[kaart_gekozen] > int(tijd_verstrekentot) or personal_records[kaart_gekozen] == 0:
        personal_records[kaart_gekozen] = int(tijd_verstrekentot)
        message_record = f'Een nieuw record!'
    elif personal_records[kaart_gekozen] == int(tijd_verstrekentot):
        message_record = f'Je verbeterde bijna je record!'
    else:
        message_record = f'Je hebt het level al sneller voltooid!'

    message_current = f'Je huidig record is:'

    current_record_min = int(personal_records[kaart_gekozen] // 60)
    current_record_sec = int((personal_records[kaart_gekozen] / 60 - current_record_min) * 60)
    message_current_record = f'{current_record_min} minuten en {current_record_sec} seconden.'

    message_you_had = f'Je had nog:'

    message_lives = f'Levens over.'

    message_return = f'Druk op "de touch module" om verder te gaan. '

    heartsprite1 = factory.from_image(resources.get_path("heart1.png"))
    heartsprite2 = factory.from_image(resources.get_path("heart2.png"))
    heartsprite3 = factory.from_image(resources.get_path("heart3.png"))
    heartsprites = [heartsprite1, heartsprite2, heartsprite3]
    while True:
        renderer.clear()
        renderer.copy(achtergrond, dstrect=(0, 0, 1200, 900))
        font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=30, color=kleuren[7])
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:  # nummers gaan van 48(=0) tot 57(=9)
                key = event.key.keysym.sym
                if key == sdl2.SDLK_p:
                    renderer.clear()
                    sdl2.ext.quit()
                    startscherm("level_up")
                if key == sdl2.SDLK_ESCAPE:
                    quit()

        if personal_records[kaart_gekozen] > tijd_verstrekentot or personal_records[kaart_gekozen] == 0:
            personal_records[kaart_gekozen] = tijd_verstrekentot

        text_congrats = sdl2.ext.renderer.Texture(renderer, font.render_text(message_congrats))
        renderer.copy(text_congrats, dstrect=(26, 20, text_congrats.size[0], 31))

        text_it_took = sdl2.ext.renderer.Texture(renderer, font.render_text(message_it_took))
        renderer.copy(text_it_took, dstrect=(26, 101, text_it_took.size[0], 31))

        text_time_needed = sdl2.ext.renderer.Texture(renderer, font.render_text(message_time_needed))
        renderer.copy(text_time_needed,
                      dstrect=((700 - text_time_needed.size[0]) / 2, 152, text_time_needed.size[0], 31))

        text_record = sdl2.ext.renderer.Texture(renderer, font.render_text(message_record))
        renderer.copy(text_record, dstrect=((700 - text_record.size[0]) / 2, 203, text_record.size[0], 31))

        text_current = sdl2.ext.renderer.Texture(renderer, font.render_text(message_current))

        renderer.copy(text_current, dstrect=((26, 254, text_current.size[0], 31)))

        text_current_record = sdl2.ext.renderer.Texture(renderer, font.render_text(message_current_record))
        renderer.copy(text_current_record, dstrect=((143, 305, text_current_record.size[0], 31)))

        text_you_had = sdl2.ext.renderer.Texture(renderer, font.render_text(message_you_had))
        renderer.copy(text_you_had, dstrect=((26, 386, text_you_had.size[0], 31)))

        lives_texture = heartsprites[aantal]
        renderer.copy(lives_texture, srcrect=(0, 0, lives_texture.size[0] * 1.5, 37.5),
                      dstrect=((700 - lives_texture.size[0] * 1.5) / 2, 431, lives_texture.size[0] * 1.5, 37.5))

        text_lives = sdl2.ext.renderer.Texture(renderer, font.render_text(message_lives))
        renderer.copy(text_lives, dstrect=((251, 482, text_lives.size[0], 31)))

        text_return = sdl2.ext.renderer.Texture(renderer, font.render_text(message_return))
        renderer.copy(text_return, dstrect=((71, 691, text_return.size[0], 31)))
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
    start_shopx = BREEDTE / 4
    breedte_shop = BREEDTE / 2
    hoogte_shop = (breedte_shop / shop_afbeelding.size[0]) * shop_afbeelding.size[1]
    start_shopy = HOOGTE - hoogte_shop

    font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=30, color=kleuren[3])
    errormessage = ""
    message = f'Game Over, {reden} \n druk op de oranje knop (vooruit) op opnieuw te proberen'
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
                if key == sdl2.SDLK_z or key == sdl2.SDLK_r:
                    sdl2.ext.quit()
                    main()
                if key == sdl2.SDLK_ESCAPE:
                    quit()

        text = sdl2.ext.renderer.Texture(renderer, font.render_text(message))
        renderer.copy(text, dstrect=(int((BREEDTE - text.size[0]) / 2), 20, text.size[0], text.size[1]))
        renderer.present()

def save(option):
    global level,money1_aantal,money2_aantal,money3_aantal,money4_aantal
    global p_speler, r_speler, pizza_collected, apple_collected, egg_collected, broccoli_collected, total_hearts_present, total_money_present, level, tijd_verstrekentot, kaart_genomen

    if option == "save":
        tesaven_waarden = {'p_speler': p_speler, 'r_speler': r_speler, 'pizza_collected': pizza_collected,
                           'apple_collected': apple_collected, 'egg_collected': egg_collected, 'broccoli_collected': broccoli_collected,
                           'total_hearts_present': total_hearts_present, 'money1_aantal': money1_aantal,'money2_aantal':money2_aantal,'money3_aantal':money3_aantal,'money4_aantal':money4_aantal,
                           'level': level, 'tijd_verstrekentot': tijd_verstrekentot, 'kaart_genomen': kaart_genomen, 'money1_collected': money1_collected, 'money2_collected':money2_collected,'money3_collected': money3_collected, 'money4_collected':money4_collected, 'money1_rendered':money1_rendered, 'money2_rendered': money2_rendered, 'money3_rendered':money3_rendered, 'money4_rendered':money4_rendered
                        }
        outfile = open(persistantfile, 'wb')
        pickle.dump(tesaven_waarden, outfile)
        outfile.close()
        print("saven \n")

    elif option == "load":
        infile = open(persistantfile,'rb')
        teladen = pickle.load(infile)
        infile.close()
        globals().update(teladen)
        if total_money_present >= 4:
            total_money_present = 0
        print("laden \n")
    else:
        print('save failed')
        pass



def rotatie(alfa, vector):
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
    global moet_afsluiten
    global r_speler
    global r_cameravlak
    global p_speler
    global laser_shot
    global exit_level
    global s_pressed
    exit_level = False
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
            if key == sdl2.SDLK_t:
                laser_shot = True
                buzzer()
                continue #
            if key == sdl2.SDLK_z and exit_allowed == True:
                playsound("resources/Cash_register.mp3")
                exit_level = True

            if key == sdl2.SDLK_ESCAPE:
                moet_afsluiten = True
                break
#
        # Analoog aan SDL_KEYDOWN. Dit event wordt afgeleverd wanneer de
        # gebruiker een muisknop indrukt
        #elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:

            # button = event.button.button #deze 5 lijntjes is voor linkermuisknop schieten, tijdelijk vervangen door x
            # if button == sdl2.SDL_BUTTON_LEFT:
            #     # ...
            #     laser_shot = True
            #     continue

            #if key == sdl2.SDLK_t:
            #    laser_shot = True
            #    continue
            #if button == sdl2.SDL_BUTTON_RIGHT:ttttttt
            #    save("save")
        # Een SDL_MOUSEWHEEL event wordt afgeleverd wanneer de gebruiker
        # aan het muiswiel draait.
        elif event.type == sdl2.SDL_MOUSEWHEEL :
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
                rotatie_beweging = (beweging * math.pi / 2) /350
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
    # querty
    if key_states[sdl2.SDL_SCANCODE_P]:
        save("save")
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
        s_pressed = True
        pd = p_speler + rotatie(math.pi, r_speler / (r_speler[0] ** 2 + r_speler[1] ** 2)) * stapverkleiner
        if wall_collission(pd):
            p_speler = pd

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True
    #camera draaien
    if key_states[sdl2.SDL_SCANCODE_L]:
        #naar links kijken
        beweging = -5
        rotatie_beweging = (beweging * math.pi / 2) / 50
        r_speler = rotatie(rotatie_beweging, r_speler)
        r_cameravlak = rotatie((math.pi / 2), r_speler)
    if key_states[sdl2.SDL_SCANCODE_R]:
        #naar rechts kijken
        beweging = 5
        rotatie_beweging = (beweging * math.pi / 2) / 50
        r_speler = rotatie(rotatie_beweging, r_speler)
        r_cameravlak = rotatie((math.pi / 2), r_speler)

def vibrator():
    with serial.Serial(COM_POORT, 9600, timeout=1) as ser:
        ser.write(b'v')

def buzzer():
    with serial.Serial(COM_POORT, 9600, timeout=1) as ser:
        ser.write(b'b')

def bereken_r_straal(r_speler, kolom):

    r_straal_kolom_x = d_camera * r_speler[0] + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak[0]
    r_straal_kolom_y = d_camera * r_speler[1] + (-1 + (2 * kolom) / BREEDTE) * r_cameravlak[1]

    r_straal_kolom_norm = math.sqrt(r_straal_kolom_x ** 2 + r_straal_kolom_y ** 2)
    r_straal_x = r_straal_kolom_x / r_straal_kolom_norm
    r_straal_y = r_straal_kolom_y / r_straal_kolom_norm
    return np.array([r_straal_x, r_straal_y])

def heart_display():
    print(total_hearts_present)
    if total_hearts_present == 3:
        ser = serial.Serial(COM_POORT, 9600, timeout=1)
        ser.write(b'0')
    elif total_hearts_present == 2:
        ser = serial.Serial(COM_POORT, 9600, timeout=1)
        ser.write(b'1')
    elif total_hearts_present == 1:
        ser = serial.Serial(COM_POORT, 9600, timeout=1)
        ser.write(b'2')#rllll
    else:
        ser = serial.Serial(COM_POORT, 9600, timeout=1)
        ser.write(b'3')

def collection_array():
    tot = 0
    if pizza_collected == True:
        tot += 1
    if broccoli_collected == True:
        tot += 1
    if egg_collected == True:
        tot += 1
    if apple_collected == True:
        tot += 1
    if tot == 0:
        if kaart_genomen == False:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'4')
        else:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'9')
    if tot == 1:
        if kaart_genomen == False:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'5')
        else:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'a')
    if tot == 2:
        if kaart_genomen == False:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'6')
        else:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'z')
    if tot == 3:
        if kaart_genomen == False:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'7')
        else:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'e')
    if tot == 4:
        if kaart_genomen == False:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'8')
        else:
            ser = serial.Serial(COM_POORT, 9600, timeout=1)
            ser.write(b'r')

def raycast(p_speler, r_straal):
    global r_speler
    global is_texture
    is_texture = False
    global is_horizontaal
    global blok

    delta_h = 1 / abs(r_straal[0])
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
                    blok = world_map[(i_verticaal_y_rounded_int[0]), (i_verticaal_y_rounded_int[1])]
                    break



            elif r_straal[1] < 0:
                if world_map[i_verticaal_y_rounded_int[0], (i_verticaal_y_rounded_int[1] - 1)]:
                    d_muur = math.sqrt((i_verticaal_y[0] - p_speler[0]) ** 2 + (i_verticaal_y[1] - p_speler[1]) ** 2)
                    is_texture = True
                    textuurcoordinaten_X_zondermaalbreedtetextuur = (1 - (i_verticaal_y - i_verticaal_y_rounded_int))
                    blok = world_map[i_verticaal_y_rounded_int[0], (i_verticaal_y_rounded_int[1] - 1)]
                    break

    d_muur = d_muur * np.dot(r_speler, r_straal)

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
    hoogte_t = textures_hoogtes[blok]
    breedte_t = textures_breedtes[blok] - 1

    textuurcoordinaten_X = textuurcoordinaten_X_zondermaalbreedtetextuur * breedte_t
    hoogte = (HOOGTE) * 1 / (d_muur + 0.00001)

    if hoogte >= HOOGTE:
        y1 = 0
    else:
        y1 = (HOOGTE - hoogte) / 2

    if is_texture == True:

        breedte_textuur = breedte_t
        hoogte_textuur = hoogte_t
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
    renderer.copy(text, dstrect=(int((BREEDTE - text.size[0]) / 2), 85, text.size[0], text.size[1]))

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
    global pizza_collected, apple_collected, broccoli_collected, egg_collected
    renderer.copy(scannergun_texture, srcrect=(0, 0, scannergun_texture_breedte, scannergun_texture_hoogte),
                  dstrect=(499, 715, scannergun_texture_breedte, scannergun_texture_hoogte))
    # crosshair
    renderer.copy(crosshair_texture, srcrect=(0, 0, crosshair_texture_breedte, crosshair_texture_hoogte),
                  dstrect=(580, 450, crosshair_texture_breedte, crosshair_texture_hoogte))
    if laser_shot == True:
        playsound("resources/Scanner_beep_3.mp3")
        renderer.copy(laser_texture, srcrect=(0, 0, laser_texture_breedte, laser_texture_hoogte),
                      dstrect=(581, 470, laser_texture_breedte, laser_texture_hoogte))

        # functional scanner
        if d_pizza_kolom_speler <= 1:
            pizza_collected = check_if_object_scanned(tuple_pizza[0] + (tuple_pizza[1] / 2), 450, tuple_pizza[1])
            collection_array()
            laser_shot = False
        if d_apple_kolom_speler <= 1:
            apple_collected = check_if_object_scanned(tuple_apple[0] + (tuple_apple[1] / 2), 450, tuple_apple[1])
            collection_array()
            laser_shot = False
        if d_broccoli_kolom_speler <= 1:
            broccoli_collected = check_if_object_scanned(tuple_broccoli[0] + (tuple_broccoli[1] / 2), 450,
                                                         tuple_broccoli[1])
            collection_array()
            laser_shot = False
        if d_egg_kolom_speler <= 1:
            egg_collected = check_if_object_scanned(tuple_egg[0] + (tuple_egg[1] / 2), 450, tuple_egg[1])
            collection_array()
            laser_shot = False
        else:
            laser_shot = False

# Initialiseer timer
timer_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size = 20, color=kleuren[7])
def timer(delta, renderer, window, deadline_min, deadline_sec):
    timer_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])
    global tijd_verstrekentot
    tijd_verstrekentot += delta
    total_sec = (deadline_min * 60) + deadline_sec
    resterende_tijd = total_sec - int(tijd_verstrekentot)
    display_min = resterende_tijd // 60

    display_sec = int((resterende_tijd / 60 - display_min) * 60 + 0.0001)


    message = f'{display_min}: {display_sec}' #int(deadline_sec - tijd_verstrekentot + 1)
    text = sdl2.ext.renderer.Texture(renderer, timer_font.render_text(message))
    if tijd_verstrekentot > ((deadline_min * 60) + deadline_sec):
        message = f'je tijd is op :('
        text = sdl2.ext.renderer.Texture(renderer, timer_font.render_text(message))
        levelfailed("tijd was op")

    # renderer.copy(text, dstrect=(int((window.size[0] - text.size[0]) / 2), window.size[1]/3, text.size[0], text.size[1]))
    renderer.copy(text, dstrect=(705, 35, text.size[0], text.size[1]))

teller=0

sprite_voor=["voor1.png","voor2.png","voor3.png"]  #0,1,2
sprite_achter=["achter1.png","achter2.png","achter3.png"]
sprite_links=["links1.png","links2.png","links3.png"]
sprite_rechts=["rechts1.png","rechts2.png","rechts3.png"]
sprite_links_voor=["links_voor1.png","links_voor2.png","links_voor3.png"]
sprite_links_achter=["links_achter1.png","links_achter2.png","links_achter3.png"]
sprite_rechts_voor=["rechts_voor1.png","rechts_voor2.png","rechts_voor3.png"]
sprite_rechts_achter=["rechts_achter1.png","rechts_achter2.png","rechts_achter3.png"]
teller=0
def sprite_loop_teller():
    global teller
    if teller<2:
        teller+=1
    else:
        teller=0
    return teller
global angle
angle=0
def nearest_octant(ang):
    if (ang<0):
        res= 8+int(angle/(np.pi/8)+0.5)
    else:
        res=int(angle/(np.pi/8)+0.5)
    if res==8:
        res=0
    return res

def clerk_sprite_selector():
    global angle
    rounded_angle=nearest_octant(angle)

    t=sprite_loop_teller()
    if (rounded_angle == 0):  # rechts       rounded_angle==0   rounded_angle>=np.pi*(-1/8) and rounded_angle<=np.pi*(1/8)
        return sprite_rechts[t]
    elif (rounded_angle == 7):  # rechtsvoor     rounded_angle==(1/4)*np.pi  rounded_angle>np.pi*(1/8) and rounded_angle<np.pi*(3/8)
        return sprite_rechts_voor[t]
    elif (rounded_angle == 6):  # voor     rounded_angle==(1/2)*np.pi rounded_angle>=np.pi*(3/8) and rounded_angle<=np.pi*(5/8)
        return sprite_voor[t]
    elif (rounded_angle == 5):  # linksvoor  rounded_angle==(3/4)*np.pi rounded_angle>np.pi*(5/8) and rounded_angle<np.pi*(7/8)
        return sprite_links_voor[t]
    elif (rounded_angle == 4):  # links      (rounded_angle==np.pi) or (rounded_angle==-np.pi) (rounded_angle>=-np.pi and rounded_angle<=np.pi*(-7/8)) or (rounded_angle>=np.pi*(7/8) and rounded_angle<=np.pi)
        return sprite_links[t]
    elif (rounded_angle == 3):  # linksachter       rounded_angle==(-3/4)*np.pi    rounded_angle>np.pi*(-7/8) and rounded_angle<np.pi*(-5/8)
        return sprite_links_achter[t]
    elif (rounded_angle == 2):  # achter             rounded_angle==(-1/2)*np.pi       rounded_angle>=np.pi*(-5/8) and rounded_angle<=np.pi*(-3/8)
        return sprite_achter[t]
    elif (rounded_angle == 1):  # rechtsachter       rounded_angle==(-1/4)*np.pi rounded_angle>np.pi*(-3/8) and rounded_angle<np.pi*(-1/8)
        return sprite_rechts_achter[t]

def create_sprites_hud():
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
    money_sprite1_wereld = factory.from_image(resources.get_path("money1_wereldsprite.png"))
    heartsprite1 = factory.from_image(resources.get_path("heart1.png"))
    heartsprite2 = factory.from_image(resources.get_path("heart2.png"))
    heartsprite3 = factory.from_image(resources.get_path("heart3.png"))
    heartsprites = [heartsprite1, heartsprite2, heartsprite3]
    gsmsprite = factory.from_image(resources.get_path("gsm.png"))

    return hud_texture, pizza_texture, pizza_gray_texture, apple_texture, apple_gray_texture, egg_texture, egg_gray_texture, broccoli_texture, broccoli_gray_texture, moneysprites, heartsprites, gsmsprite, money_sprite1_wereld

def hud():
    global player_hit, render_pizza_in_world, pizza_collected, apple_collected, egg_collected, broccoli_collected, total_hearts_present, heartsprite, player_hit, total_money_present,  moneysprite
    global money1_collected, money2_collected, money3_collected, money4_collected
    global money1_aantal, money2_aantal, money3_aantal, money4_aantal
    renderer.copy(hud_texture, srcrect=(0, 0, hud_texture_breedte, hud_texture_hoogte),
                  dstrect=(400, 0, hud_texture_breedte, hud_texture_hoogte))

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
        heart_display()
        player_hit = False
    global aantal
    if total_hearts_present:
        aantal = (total_hearts_present - 1)
        heart_texture = heartsprites[aantal]
        renderer.copy(heart_texture, srcrect=(0, 0, heart_breedtes[aantal], heart_hoogte),
                      dstrect=(1090, 30, heart_breedtes[aantal], heart_hoogte))
    else:
        print("game over")
        levelfailed("Levens zijn op!")

    # money

    money_collected = False
    if money1_collected == True:
        money1_aantal = 1
    if money2_collected == True:
        money2_aantal = 1
    if money3_collected == True:
        money3_aantal = 1
    if money4_collected == True:
        money4_aantal = 1

    total_money_present = money1_aantal + money2_aantal + money3_aantal + money4_aantal

    if total_money_present:
        hoeveelheid = total_money_present -1
        money_texture = moneysprites[hoeveelheid]
        renderer.copy(money_texture, srcrect=(0, 0, money_breedtes[hoeveelheid], money_hoogte),dstrect=(885, 35, money_breedtes[hoeveelheid], money_hoogte))

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
    i = kaart_gekozen
    map_weergave = map_weergave_list[i]

    if kaart_genomen == True:
        renderer.copy(gsm, srcrect=(0, 0, gsm_breedte, gsm_hoogte),
                      dstrect=(18, 20, gsm_breedte * 1.2, gsm_hoogte * 1.2))
        renderer.copy(map_weergave, srcrect=(0, 0, map_weergave_breedte, map_weergave_hoogte[i]),
                      dstrect=(30, 50, map_weergave_breedte / 12, map_weergave_hoogte[i] / 12))
        renderer.copy(tekst_gsm, srcrect=(0, 0, tekst_gsm_breedte, tekst_gsm_hoogte),
                      dstrect=(45, 200, tekst_gsm_breedte / 4, tekst_gsm_hoogte / 4))

        positie_pion_x = 30 - (17 / 7) + (
                    (map_weergave_breedte / 12) - (p_speler[1] / 18) * (map_weergave_breedte / 12))

        positie_pion_y = 50 - (17 / 7) + ((p_speler[0] / 18) * (map_weergave_hoogte[i] / 12))

        renderer.copy(positie_persoon_sprite,
                      srcrect=(0, 0, positie_persoon_sprite_breedte, positie_persoon_sprite_hoogte), dstrect=(
                positie_pion_x, positie_pion_y, positie_persoon_sprite_breedte / 7, positie_persoon_sprite_hoogte / 7))

def volgorde_sprite_renderer():
    global z_buffer, laser_shot
    global money1_rendered, money2_rendered, money3_rendered, money4_rendered, money1_collected, money2_collected, money3_collected, money4_collected
    global d_pizza_kolom_speler, d_apple_kolom_speler, d_broccoli_kolom_speler, d_egg_kolom_speler, tuple_pizza, tuple_apple, tuple_broccoli, tuple_egg
    global d_munt1_kolom_speler,d_munt2_kolom_speler ,d_munt3_kolom_speler ,d_munt4_kolom_speler
    global tuple_munt1, tuple_munt2,tuple_munt3,tuple_munt4, tuple_clerk, clerk_sprite
    d_pizza_kolom_speler = math.sqrt(((pizza_x - p_speler[0]) ** 2) + (pizza_y - p_speler[1]) ** 2)
    d_apple_kolom_speler = math.sqrt(((apple_x - p_speler[0]) ** 2) + (apple_y - p_speler[1]) ** 2)
    d_broccoli_kolom_speler = math.sqrt(((broccoli_x - p_speler[0]) ** 2) + (broccoli_y - p_speler[1]) ** 2)
    d_egg_kolom_speler = math.sqrt(((egg_x - p_speler[0]) ** 2) + (egg_y - p_speler[1]) ** 2)
    d_munt1_kolom_speler = math.sqrt(((munt1_x - p_speler[0]) ** 2) + (munt1_y - p_speler[1]) ** 2)
    d_munt2_kolom_speler = math.sqrt(((munt2_x - p_speler[0]) ** 2) + (munt2_y - p_speler[1]) ** 2)
    d_munt3_kolom_speler = math.sqrt(((munt3_x - p_speler[0]) ** 2) + (munt3_y - p_speler[1]) ** 2)
    d_munt4_kolom_speler = math.sqrt(((munt4_x - p_speler[0]) ** 2) + (munt4_y - p_speler[1]) ** 2)
    d_gsm_kolom_speler =   math.sqrt(((gsm_x - p_speler[0])**2)+(gsm_y - p_speler[1])**2)

    if kaart_gekozen!=0:
        clerk_x, clerk_y= clerk_positie(kaart_gekozen)
        d_clerk_kolom_speler= math.sqrt(((clerk_x - p_speler[0])**2)+(clerk_y - p_speler[1])**2)
        list_afstanden = [d_pizza_kolom_speler, d_apple_kolom_speler, d_broccoli_kolom_speler, d_egg_kolom_speler,d_munt1_kolom_speler, d_munt2_kolom_speler, d_munt3_kolom_speler, d_munt4_kolom_speler,d_gsm_kolom_speler,d_clerk_kolom_speler]
    else:
        list_afstanden = [d_pizza_kolom_speler, d_apple_kolom_speler, d_broccoli_kolom_speler, d_egg_kolom_speler, d_munt1_kolom_speler, d_munt2_kolom_speler, d_munt3_kolom_speler, d_munt4_kolom_speler, d_gsm_kolom_speler]

    list_afstanden.sort()
    list_afstanden.reverse()
    for i in range(0, len(list_afstanden)):
        #tuple bevat: beginpunt x, breedte sprite scherm, hoogte sprite scherm en sprite rendered (boolean)
        if list_afstanden[i] == d_pizza_kolom_speler and pizza_collected==False:
            tuple_pizza = sprite_renderer(pizza_x, pizza_y, pizza_texture,0, z_buffer, d_pizza_kolom_speler,1,False)


        elif list_afstanden[i] == d_apple_kolom_speler and apple_collected==False:
            tuple_apple = sprite_renderer(apple_x, apple_y, apple_texture,1, z_buffer, d_apple_kolom_speler,1,False)

        elif list_afstanden[i] == d_egg_kolom_speler and egg_collected==False:
            tuple_egg= sprite_renderer(egg_x, egg_y, egg_texture,2, z_buffer, d_egg_kolom_speler,1,False)

        elif list_afstanden[i] == d_broccoli_kolom_speler and broccoli_collected==False:
            tuple_broccoli = sprite_renderer(broccoli_x, broccoli_y, broccoli_texture,3, z_buffer, d_broccoli_kolom_speler,1,False)

        elif list_afstanden[i] == d_munt1_kolom_speler and money1_collected==False:
            tuple_munt1 = sprite_renderer(munt1_x, munt1_y, money_sprite1_wereld, 5,z_buffer, d_munt1_kolom_speler,1,False)

        elif list_afstanden[i] == d_munt2_kolom_speler and money2_collected==False:
            tuple_munt2 = sprite_renderer(munt2_x, munt2_y, money_sprite1_wereld,5, z_buffer, d_munt2_kolom_speler,1,False)

        elif list_afstanden[i] == d_munt3_kolom_speler and money3_collected==False:
            tuple_munt3 = sprite_renderer(munt3_x, munt3_y, money_sprite1_wereld, 5,z_buffer, d_munt3_kolom_speler,1,False)

        elif list_afstanden[i] == d_munt4_kolom_speler and money4_collected==False:
            tuple_munt4 = sprite_renderer(munt4_x, munt4_y, money_sprite1_wereld,5, z_buffer, d_munt4_kolom_speler,1,False)

        elif list_afstanden[i] == d_gsm_kolom_speler and kaart_genomen ==False:
            tuple_gsm = sprite_renderer(gsm_x, gsm_y, gsmsprite,4, z_buffer, d_gsm_kolom_speler,1,False)
            begintpunt_gsm = tuple_gsm[0]
            if d_gsm_kolom_speler <= 0.5 and begintpunt_gsm != 0:
                collect_gsm()
        if kaart_gekozen!=0:
            if list_afstanden[i]== d_clerk_kolom_speler:
                tuple_clerk = sprite_renderer(clerk_x, clerk_y, clerk_sprite,6, z_buffer,d_clerk_kolom_speler, 5, True)

def munt_collected():
    global money1_collected, money1_rendered, money2_collected, money2_rendered, money3_collected, money3_rendered, money4_collected, money4_rendered
    if money1_rendered == True:
        if tuple_munt1[3] == True:
            collected = money_collector(tuple_munt1, d_munt1_kolom_speler)
            if collected == True:
                money1_rendered = False
                money1_collected = True
    if money2_rendered == True:
        if tuple_munt2[3] == True:
            collected = money_collector(tuple_munt2, d_munt2_kolom_speler)
            if collected == True:
                money2_rendered = False
                money2_collected = True
    if money3_rendered == True:
        if tuple_munt3[3] == True:
            collected = money_collector(tuple_munt3, d_munt3_kolom_speler)
            if collected == True:
                money3_rendered = False
                money3_collected = True
    if money4_rendered == True:
        if tuple_munt4[3] == True:
            collected = money_collector(tuple_munt4, d_munt4_kolom_speler)
            if collected == True:
                money4_rendered = False
                money4_collected = True

def money_collector(tuple, afstand_tot_money):
    # tuple bevat: beginpunt x, breedte sprite scherm, hoogte sprite scherm en sprite rendered (boolean)
    collect_money = False
    beginpunt_money = tuple[0]
    if afstand_tot_money <= 0.5 and beginpunt_money != 0:
        #collect_money(money_rendered, money_collected)
        collect_money = True
    return(collect_money)

def sprite_renderer(sprite_x, sprite_y, sprite, nummber_sprite, z_buffer, d_object_kolom_speler,scale,sprite_bew):
    #waarden op nul zetten, zodat 0 returned als geen kolom weergegeven
    global angle
    sprite_rendered = False
    beginpunt_sprite_x = 0
    breedte_sprite_scherm = 0
    hoogte_sprite_scherm = 0

    p_sprite_x_nieuw = sprite_x - p_speler[0]
    p_sprite_y_nieuw = sprite_y - p_speler[1]
    # determinant van cameramatrix
    determinant_m = r_cameravlak[0] * r_speler[1] - r_cameravlak[1] * r_speler[0]


    u_cameracoordinaten = ((r_speler[1] / determinant_m) * p_sprite_x_nieuw) + (
            (-r_speler[0] / determinant_m) * p_sprite_y_nieuw)
    v_cameracoordinaten = ((-r_cameravlak[1] / determinant_m) * p_sprite_x_nieuw) + (
            (r_cameravlak[0] / determinant_m) * p_sprite_y_nieuw)
    if v_cameracoordinaten==0:
        v_cameracoordinaten+=0.00001
    a = u_cameracoordinaten / v_cameracoordinaten  # positie op x as scherm, dus kolom
    if (sprite_bew==True):
        angle=float(math.atan2(p_sprite_y_nieuw,p_sprite_x_nieuw))

    if (a >= -1) and (a <= 1) and (v_cameracoordinaten >= 0):
        kolom_midden_sprite = (((a + 1) / 2) * BREEDTE)
        hoogte_sprite_wereld = sprite_hoogtes[nummber_sprite]
        breedte_sprite_wereld = sprite_breedtes[nummber_sprite]

        hoogte_sprite_scherm = HOOGTE * (1 / (d_object_kolom_speler * 5)) * scale
        breedte_sprite_scherm = (breedte_sprite_wereld / hoogte_sprite_wereld) * hoogte_sprite_scherm
        beginpunt_sprite_x = kolom_midden_sprite - (breedte_sprite_scherm / 2)

        for kolom_texture_scherm in range(0, int(breedte_sprite_scherm + 0.5)):
            kolom = kolom_texture_scherm + int(beginpunt_sprite_x)
            kolom_texture = (kolom_texture_scherm / breedte_sprite_scherm) * breedte_sprite_wereld
            if(kolom < BREEDTE) and (kolom>=0):

                if z_buffer[kolom] >= d_object_kolom_speler:
                    renderer.copy(sprite, srcrect=(kolom_texture, 0, 1, hoogte_sprite_wereld),dstrect=(kolom, (HOOGTE / 2) - (hoogte_sprite_scherm / 2), 1, hoogte_sprite_scherm))
                    sprite_rendered = True
    else:
        d_object_kolom_speler = 0
    return beginpunt_sprite_x, breedte_sprite_scherm, hoogte_sprite_scherm, sprite_rendered

# checking if we hit an object with our scanner
def check_if_object_scanned(scanobject_x, scanobject_y, breedte):
    if scanobject_x-(breedte/2) <= 600 <= scanobject_x+(breedte/2) and 450 <= scanobject_y <= 495:
        return True
    else:
        return False

def player_hit_by_clerk():
    global player_hit
    global p_speler
    clerk_x, clerk_y = clerk_positie(kaart_gekozen)
    d_clerk = math.sqrt((p_speler[0] - clerk_x) ** 2 + (p_speler[1] - clerk_y) ** 2)
    if d_clerk <= 0.5:
        player_hit = True
        vibrator()
        p_speler = np.array([9.5, 15.5])

def noord(clerk_x):
    clerk_x-=0.05
    return round(clerk_x,2)

def oost(clerk_y):
    clerk_y+=0.05
    return round(clerk_y,2)

def west(clerk_y):
    clerk_y-=0.05
    return round(clerk_y,2)

def zuid(clerk_x):
    clerk_x+=0.05
    return round(clerk_x,2)

#start waarden npc map 2
clerk_x1=15.0
clerk_y1=4.0
#start waarden npc map 3
clerk_x2=12.0
clerk_y2=6.0
#start waarden npc map 4
clerk_x3=15.5
clerk_y3=9.5
clerk_check=True

def clerk_positie(kaart_gekozen):   #fhook      map 1 geeft geen loop want geen vijand.   clerk_x1,clerk_y1,clerk_x2,clerk_y2,clerk_x3,clerk_y3
    if (kaart_gekozen==1): #loop map 2
        global clerk_x1, clerk_y1,clerk_check
        if (clerk_x1>7.5) and (clerk_y1 ==4.0) :  #A
            clerk_x1=noord(clerk_x1)
            clerk_check=True
            return clerk_x1,clerk_y1
        elif (clerk_x1 ==7.5) and (clerk_y1 <15.5) and (clerk_check==True): #B
            clerk_y1=oost(clerk_y1)
            return clerk_x1, clerk_y1
        elif (clerk_x1 > 4.5) and (clerk_y1 ==15.5):  #C
            clerk_x1=noord(clerk_x1)
            clerk_check=False
            return clerk_x1, clerk_y1
        elif (clerk_x1 ==4.5) and (clerk_y1 > 5.5):  #D
            clerk_y1=west(clerk_y1)
            return clerk_x1,clerk_y1
        elif (clerk_x1 < 6.5) and (clerk_y1 ==5.5):  #E
            clerk_x1=zuid(clerk_x1)
            return clerk_x1, clerk_y1
        elif (clerk_x1 ==6.5) and (clerk_y1 >2.0):   #F
            clerk_y1=west(clerk_y1)
            return clerk_x1, clerk_y1
        elif (clerk_x1 <15.0) and (clerk_y1 ==2.0):  #G
            clerk_x1=zuid(clerk_x1)
            return clerk_x1, clerk_y1
        elif (clerk_x1 ==15.0) and (clerk_y1 <4.0):  #H
            clerk_y1=oost(clerk_y1)
            clerk_check=True
            return clerk_x1, clerk_y1

    if (kaart_gekozen==2):  #loop map 3
        global clerk_x2, clerk_y2
        if (clerk_x2!=5.0) and (clerk_y2==6.0):
                clerk_x2=noord(clerk_x2)
                return clerk_x2,clerk_y2
        elif (clerk_x2==5.0) and (clerk_y2!=2.0):
            clerk_y2=west(clerk_y2)
            return clerk_x2,clerk_y2
        elif (clerk_x2!=12.5) and (clerk_y2==2.0):
            clerk_x2=zuid(clerk_x2)
            return clerk_x2,clerk_y2
        elif (clerk_x2==12.5) and (clerk_y2!=6.0):
            clerk_y2=oost(clerk_y2)
            return clerk_x2,clerk_y2

    if (kaart_gekozen==3): #loop map 4
        global clerk_x3, clerk_y3
        if (clerk_x3 !=2.0) and (clerk_y3 ==9.5):
            clerk_x3=noord(clerk_x3)
            return clerk_x3,clerk_y3
        elif (clerk_x3 ==2.0) and (clerk_y3 !=2.0):
            clerk_y3=west(clerk_y3)
            return clerk_x3, clerk_y3
        elif (clerk_x3 !=15.5) and (clerk_y3 ==2.0):
            clerk_x3=zuid(clerk_x3)
            return clerk_x3, clerk_y3
        elif (clerk_x3 == 15.5) and (clerk_y3 !=9.5):
            clerk_y3 = oost(clerk_y3)
            return clerk_x3, clerk_y3


def check_if_level_completed():

    global pizza_collected, broccoli_collected, egg_collected, apple_collected, total_money_present, total_hearts_present, p_kassa_by_level_x, p_kassa_by_level_y, kaart_gekozen, exit_allowed
    d_kassa = math.sqrt((p_speler[0] - p_kassa_by_level_x[kaart_gekozen]) ** 2 + (p_speler[1] - p_kassa_by_level_y[kaart_gekozen]) ** 2)

    if pizza_collected is True and broccoli_collected is True and apple_collected is True and egg_collected is True and total_money_present == 4 and total_hearts_present !=0 and d_kassa <= 1.5:
        exit_allowed = True
        exit_message_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[0])
        message = f'Druk op "e" om het level te voltooien.'
        exit_message = sdl2.ext.renderer.Texture(renderer, exit_message_font.render_text(message))
        renderer.copy(exit_message, dstrect=(400, 400, exit_message.size[0], exit_message.size[1]))
    else:
        exit_allowed = False


def collect_gsm():
    global kaart_genomen
    kaart_genomen = True


def main():
    heart_display()
    collection_array()
    global s_pressed
    s_pressed = False
    global fps_font
    global tijd_verstrekentot
    global keuzealgemaakt
    if not keuzealgemaakt:
        save("load")
        keuzealgemaakt = True
        loadornew()
    tijd_verstrekentot = 0
    fps_font = sdl2.ext.FontTTF(font='CourierPrime.ttf', size=20, color=kleuren[7])

    # Initialiseer de SDL2 bibliotheek
    global kaart_gekozen
    global laser_shot, total_hearts_present, heart1_present, heart2_present, heart3_present, player_hit, total_money_present, pizza_collected, money_collected, moneysprite, heartsprite, broccoli_collected
    sdl2.ext.init()

    global pizza_x, pizza_y, apple_x, apple_y, egg_x, egg_y, broccoli_x, broccoli_y, munt1_x, munt1_y, munt2_x, munt2_y, munt3_x, munt3_y, munt4_x, munt4_y, gsm_x, gsm_y


    pizza_x, pizza_y = pizza_x_coordinaten[kaart_gekozen], pizza_y_coordinaten[kaart_gekozen]  # 299.5
    apple_x, apple_y = apple_x_coordinaten[kaart_gekozen], apple_y_coordinaten[kaart_gekozen]

    egg_x, egg_y = egg_x_coordinaten[kaart_gekozen], egg_y_coordinaten[kaart_gekozen]
    broccoli_x, broccoli_y = broccoli_x_coordinaten[kaart_gekozen], broccoli_y_coordinaten[kaart_gekozen]
    munt1_x, munt1_y = munt1_x_coordinaten[kaart_gekozen], munt1_y_coordinaten[kaart_gekozen]
    munt2_x, munt2_y = munt2_x_coordinaten[kaart_gekozen], munt2_y_coordinaten[kaart_gekozen]
    munt3_x, munt3_y = munt3_x_coordinaten[kaart_gekozen], munt3_y_coordinaten[kaart_gekozen]
    munt4_x, munt4_y = munt4_x_coordinaten[kaart_gekozen], munt4_y_coordinaten[kaart_gekozen]
    gsm_x, gsm_y = gsm_x_coordinaten[kaart_gekozen], gsm_y_coordinaten[kaart_gekozen]
    # global vars voor scanning
    global afstand_tot_sprite
    global beginpunt_broccoli
    global breedte_broccoli
    global hoogte_broccoli
    global z_buffer
    # global money_rendered
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
    global hud_texture, pizza_texture, pizza_gray_texture, apple_texture, apple_gray_texture, egg_texture, egg_gray_texture, broccoli_texture, broccoli_gray_texture, moneysprites, heartsprites, gsmsprite, money_sprite1_wereld
    # sprites hud aanmeken
    hud_texture, pizza_texture, pizza_gray_texture, apple_texture, apple_gray_texture, egg_texture, egg_gray_texture, broccoli_texture, broccoli_gray_texture, moneysprites, heartsprites, gsmsprite, money_sprite1_wereld = create_sprites_hud()
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
        for kolom in range(0, BREEDTE):
            r_straal = bereken_r_straal(r_speler, kolom)
            if r_straal[0] == 0 or r_straal[1] == 0:
                z_buffer.append(100)
                continue
            (d_muur, k_muur, is_texture, textuurcoordinaten_X_zondermaalbreedtetextuur, blok) = raycast(p_speler,
                                                                                                        r_straal)
            z_buffer.append(d_muur)
            render_wall(renderer, window, kolom, d_muur, k_muur, is_texture,
                        textuurcoordinaten_X_zondermaalbreedtetextuur, blok, list_wall_create)

        (d_muur, k_muur, is_texture, textuurcoordinaten_X_zondermaalbreedtetextuur, blok) = raycast(p_speler,r_straal)
        z_buffer.append(d_muur)
        render_wall(renderer, window, kolom, d_muur, k_muur, is_texture,textuurcoordinaten_X_zondermaalbreedtetextuur, blok, list_wall_create)
        if (kaart_gekozen!=0):
            global clerk_sprite
            clerk_string = clerk_sprite_selector()
            clerk_sprite = factory.from_image(resources.get_path(clerk_string))
        volgorde_sprite_renderer()
        scannergun()
        munt_collected()



        end_time = time.time()
        delta = end_time - start_time

        verwerk_input(delta)

        # Teken gemiddelde fps van de laatste 20 frames
        fps_list.append(1 / (time.time() - start_time))
        if len(fps_list) == 20:
            fps = np.average(fps_list)
            fps_list = []
        render_fps(fps, renderer, window)

        hud()
        if level:
            player_hit_by_clerk()
        if kaart_genomen == True:
            kaart_weergeven()


        timer(delta, renderer, window, deadline_min, deadline_sec)


        check_if_level_completed()
        if exit_level == True:
            exit_level_action()

        # Verwissel de rendering context met de frame buffer
        renderer.present()
        # na renderen frame venster verversen
        window.refresh()
    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()

