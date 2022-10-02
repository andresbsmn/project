import sdl2
import sdl2.ext


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("test", size=(800, 600))
    renderer = sdl2.ext.Renderer(window)
    resources = sdl2.ext.Resources(__file__, "resources")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    wall_texture = factory.from_image(resources.get_path("wood.png"))
    window.show()
    running = True
    while running:
        events = sdl2.ext.get_events()


        renderer.present()


        breedte = wall_texture.size[0]
        hoogte = wall_texture.size[1]
        textuur_x = 0
        textuur_y = 0
        scherm_x = 10
        scherm_y = 100
        renderer.copy(wall_texture,
                      srcrect=(textuur_x, textuur_y, breedte, hoogte),
                      dstrect=(scherm_x, scherm_y, breedte*4, hoogte*4))

        window.refresh()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        window.refresh()
    return 0

run()

