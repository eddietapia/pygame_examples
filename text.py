user = 'David Beckham'

demo = [["Welcome "+ user + "! Let us begin the game."], ["Oh would you look at that!"],["It's time for your daily exercise!", "Let us get started with, your daily routine!"], ["Start by stretching", "and making sure you are ready for"," an intense workout"], ["start by jumping up and down on one foot", "alternating your foot each time"], ["Now pretend you are playing basketball"], ["Now stop and sit criss cross applesauce.", "And raise your hand ", "as if you were still in third grade. ", "and yell 'I love myself'"], ["Now do your favorite yoga stretch!", "And say 'Ummmm' 'Ummmmm' three times.", "And take a deep breath", "Because now comes the crazy part...", "it in your game or any other programe", "where you would like to have","a fancy text display."], ["when learning Python I sometimes found that", "most modules did not have", "a good help file", "or a demo highlighting the abilities", "of the program.", "That is why I decided","to incorporate a detailed help text file", "and a demo with all the possible routines."]]
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, RLEACCEL
from text_factory import Text_Factory
from flist import flist

tf = Text_Factory()

screen = pygame.display.get_surface()

back = screen.subsurface(screen.get_rect()).convert()

txtvar = 0

for num, item in enumerate(flist):
    tf = Text_Factory()

    txt = demo[txtvar]

    col1 = (50, 90, 250)
    col2 = (150, 230, 20)
    grey = (80, 80, 80)
    black = (0, 0, 0)

    posx = 0

    renderedfont = pygame.font.Font(None, 30)

    txt0 = renderedfont.render("efx no: ", True, col1, back)
    efx0 = renderedfont.render(str(num), True, col2, black)

    txt1 = renderedfont.render("  zoom = ", True, col1, black)
    """if item[0] == None:
        efx1 = renderedfont.render(str(item[0]), True, grey, black)
    else:
        efx1 = renderedfont.render(str(item[0]), True, col2, black)

    txt2 = renderedfont.render("  fade = ", True, col1, black)
    if item[1] == None:
        efx2 = renderedfont.render(str(item[1]), True, grey, black)
    else:
        efx2 = renderedfont.render(str(item[1]), True, col2, black)

    txt3 = renderedfont.render("  rotate = ", True, col1, black)
    if item[2] == None:
        efx3 = renderedfont.render(str(item[2]), True, grey, black)
    else:
        efx3 = renderedfont.render(str(item[2]), True, col2, black)

    txt4 = renderedfont.render("  slide = ", True, col1, black)
    if item[3] == None:
        efx4 = renderedfont.render(str(item[3]), True, grey, black)
    else:
        efx4 = renderedfont.render(str(item[3]), True, col2, black)"""

    efx1 = renderedfont.render(str(item[0]), True, grey, black)

    txt2 = renderedfont.render("  fade = ", True, col1, black)

    efx2 = renderedfont.render(str(item[2]), True, black, black)

    txt3 = renderedfont.render("  fade = ", True, col1, black)
    efx3 = renderedfont.render(str(item[2]), True, black, black)

    txt4 = renderedfont.render("  slide = ", True, col1, black)
    efx4 = renderedfont.render(str(item[3]), True, black, black)


    efximgs= [txt0, efx0, txt1, efx1, txt2, efx2, txt3, efx3, txt4, efx4]

    for x, m in enumerate(efximgs):
        efximgs[x].set_colorkey( (0,0, 0), RLEACCEL )

    screen.blit(back, (0, 0))

    for img in efximgs:
        screen.blit(img, (posx, 0))
        posx += img.get_width()

    tf.run(zoom = item[0], fade = item[1], rotate = item[2], slide = item[3], message = txt)

    txtvar += 1
    if txtvar >= len(demo):
        txtvar = 0

