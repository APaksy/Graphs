import pygame as pg
import app


# Click '+' to add node
# Left click and hold to drag nodes
# Right click and drag on node to draw edge
# Click on edge/node to select
# Press '-' when selected to delete
# Type when edge selected to edit length
# Press enter to print graph representation (nodes are represented by id so might not match the numbers on the UI nodes)


pg.init()
displaySize = (1200, 750)
BG = pg.display.set_mode(displaySize)
DISPLAY = pg.Surface(displaySize, pg.SRCALPHA)
clock = pg.time.Clock()

appObj = app.App()


run = True
while run:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            appObj.mouse_down(event.pos, event.__dict__['button'])

        if event.type == pg.MOUSEBUTTONUP:
            appObj.mouse_up(event.pos, event.__dict__['button'])

        if event.type == pg.MOUSEMOTION:
            appObj.mouse_move(event.pos)

        if event.type == pg.KEYDOWN:
            appObj.key_down(event.key)
            

    appObj.update()

    BG.fill((130, 130, 130, 0))
    DISPLAY.fill((130, 130, 130, 0))
    appObj.display(DISPLAY)
    BG.blit(DISPLAY, (0, 0))
    pg.display.flip()
    clock.tick(144)

    
