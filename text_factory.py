import pygame, sys
from pygame.locals import KEYDOWN, K_ESCAPE, RLEACCEL

class Sliders(pygame.sprite.DirtySprite):
    """slding text is an animation and that will be easier with SPRITES of the DIRTY KIND"""

    def __init__(self, posx, posy, images):

        pygame.sprite.DirtySprite.__init__(self)

        self.posx = posx
        self.posy = posy
        self.screenposy = posy
        self.frame = 0
        self.images = []
        self.images[:] = images  # list of images from zoom, fade, rotate
        self.length = len(self.images) - 1
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.posx, self.posy)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # max width and height of a series of images
        self.max_width = self.width
        self.max_height = self.height
        self.done = False
        self.num = -1
        self.xadd = 0  # the number to add to move in x direction
        self.yadd = 0  # the number to add to move in y direction
        self.delay = 20  # after how long the obj starts moving

    #---------------------------------------------------------------------------

    def move(self):

        self.length = len(self.images) - 1

        if self.delay > 0:
            self.delay -= 3

        if self.delay <= 0:
            self.delay = 3
            self.frame += 1

            if self.frame >= self.length:
                self.frame = self.length

            self.image = self.images[self.frame]

            self.posx += self.xadd
            self.posy += self.yadd
            self.rect = self.image.get_rect()
            self.rect.center = (self.posx, self.posy)
            self.dirty = 1

#-------------------------------------------------------------------------------

class Text_Factory():

    """ check the text file in the text_factory folder for all instructions """

    def __init__(self, zoom = None, fade = None, rotate = None, slide = None, text1 = "Level ", text2 = " Complete!", font = None, fontsize = 45,  justify = "C", colour = (255, 50, 64), cycles = 2, frames = 60, reduceX = 4, reduceY = 4, pause = 1500, slowdown = 10, posx = None, posy = None, level = 1, ):

        pygame.init()

        self.screen = pygame.display.get_surface()

        if self.screen == None:

            import os, random

            if sys.platform == 'win32' or sys.platform == 'win64':
                os.environ['SDL_VIDEO_CENTERED'] = '0'# center of screen
                #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 30)#top left corner

            self.screen =pygame.display.set_mode((800, 500), 1, 32)  # demo screen size

            for x in range(100):
                xpos = random.randint(0, 800)
                ypos = random.randint(0, 600)

                #pygame.draw.circle(self.screen, (random.randint(10, 70), random.randint(20, 80), 60), (xpos, ypos), random.randint(10, 40), 0)

        self.back = self.screen.subsurface(self.screen.get_rect()).convert()

        self.screen.blit(self.back, (0, 0))

        pygame.display.set_caption("Magic Mirror: Created by Eddie Tapia")

        self.subsurface = None
        self.background = (0, 0, 0)
        self.alpha = 255
        if posx == None:
            self.posx = self.screen.get_width() / 2
        else:
            self.posx = posx
        if posy == None:
            self.posy = self.screen.get_height() / 2
        else:
            self.posy = posy
        self.center = (self.posx, self.posy)
        self.rect = self.screen.get_rect()
        self.fontsize = fontsize
        self.colour = colour
        self.font = font
        self.renderedfont = pygame.font.Font(font, fontsize)
        self.frames = frames
        self.cycles = cycles
        self.reduceX = reduceX
        self.reduceY = reduceY
        self.pause = pause
        self.slowdown = slowdown  # larger the number, slower the animation
        self.alpha = 255

        self.q = 255 / self.frames  # the quantity by which fade_in or fade_out occurs

        self.angle = 0
        self.increment = 0  # in degrees
        self.fade = fade
        self.rotate = rotate
        self.zoom = zoom  # default is zoom in
        self.slide = slide
        self.jusify = justify

        # offset posx and posy are values that the message will be offset if it has to slide into the screen or slide out of the screen. slide in FROM the value or slide out TO the value.
        # eg: To make the image disappear from the left of the screen it has to move out current_pos + (width / 2) pixels to the left. + values move object right (x) or down (y) and - values move object left (x)  or up (y) .

        self.imagerects = []  # contains rects of original images
        self.imagelist = []  # the images built from the text lines go here
        self.animlist = []  # the processed animations go here direct from the functions
        self.anim_sprites = pygame.sprite.LayeredDirty()  # the sliding text objects
        self.text1 = text1
        self.text2 = text2
        self.level = level
        self.message = (self.text1 + str(self.level) + self.text2)

    #---------------------------------------------------------------------------
    def blit_func(self, image, draw_rect, clear_rect):

        # blit the increasd / reduced image to the screen

        self.screen.blit(image, (draw_rect))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        pygame.time.wait(self.slowdown)  # how long to pause while image displayed

        # now clear the image by pasting the subsurface which we  grabbed earlier
        self.screen.blit((self.subsurface), (clear_rect))

    #---------------------------------------------------------------------------

    def single_or_multi_to_image(self, colour, font, fontsize, message, slide, justify = "C"):
        """make a single image from multiple text lines OR multiple images from
        each line in message
        If slide is ON, each line of text is treated as a single image"""

        # make the font to the given size

        self.renderedfont = pygame.font.Font(font, fontsize)

        text_image_list = []
        x = y = width = height = 0

        for line in message:
            txtimage = self.renderedfont.render(line, True, colour, self.background).convert()
            size = self.renderedfont.size(line)
            height += size[1]
            if size[0] > width:
                width = size[0]
            text_image_list.append(txtimage)  # <- if slide is ON return this list
            #                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        if slide is None:  # slide is OFF so return single image
            # create a new surface to blit the text images
            new_surface = pygame.Surface((width, height))

            for image in text_image_list:
                # now blit the text onto the surface created
                draw_rect = image.get_rect()
                if justify == "L":
                    new_surface.blit(image, (x, y))
                elif justify == "C":
                    draw_rect.midtop = (width / 2, y)
                    new_surface.blit(image, (draw_rect))
                elif justify == "R":
                    draw_rect.topright = (width, y)
                    new_surface.blit(image, (draw_rect))

                y += image.get_height()
            text_image_list = []  # empty the list
            text_image_list.append(new_surface.convert())  # add the single image to the list

        # either way return an imagelist, with a sinlge image or with mutiple images
        return text_image_list

    #---------------------------------------------------------------------------

    def set_colour_key_func(self, surface):

        surface.convert()
        surface.set_colorkey(0, RLEACCEL)

        #  alpha (255 - fully opaque. 0 - fully transparent)
        surface.set_alpha(self.alpha)

        return surface

    #---------------------------------------------------------------------------

    def get_rects(self, image, slide):

        # grab a part of the image the size of the increased / reduced message

        draw_rect = clear_rect = image.get_rect()

        if slide != None:
            clear_rect.center = draw_rect.center
            posx = -image.get_width()
            posy = image.get_height()

        else:
            clear_rect.center = self.center
            posx = newposx = clear_rect[0]
            posy = newposy = clear_rect[1]
            width = clear_rect[2]
            height = clear_rect[3]
            if width > self.screen.get_width(): width = self.screen.get_width()
            if height > self.screen.get_height(): height = self.screen.get_height()
            if posx < 0: newposx = 0
            if posy < 0: newposy = 0

            #print draw_rect, posx, posy, newposx, newposy
        draw_rect = pygame.Rect(newposx, newposy, width, height)

        # grab a rect area of surface image into the subsurface variable
        self.subsurface = self.screen.subsurface(draw_rect).convert_alpha()

        return clear_rect, draw_rect

    #---------------------------------------------------------------------------

    def zoom_func(self, zoom):
        """ The image rendered in the single_or_multi_to_image is reduced in size and  appended to the image list. We end up with an image list in DESCENDING order. To make the image grow in size or Zoom in we reverse the list before blitting. """

        for image in self.imagelist:

            newW = image_width = image.get_width()
            newH = image_height = image.get_height()
            aspectR = newW / newH
            aspect_lok = aspectR
            red = 1

            templist = []

            # make the reduction according to the aspect ratio of image
            while red:  # decrease image size and add to imagelist
                #print newW, newH, newW / newH
                # make a newsurface to the size that image will be shrunk
                newsurface = pygame.Surface((newW, newH))

                # reduce size of image
                pygame.transform.scale(image, (newW, newH), newsurface)
                # colour key
                keyed_surface = self.set_colour_key_func(newsurface)

                # add image to the list
                templist.append(keyed_surface)
                aspect_lok -= 1
                newW -= self.reduceX
                if aspect_lok <= 0:
                    newH -= self.reduceY
                    aspect_lok = aspectR

                if newW <= 2: newW = 2
                if newH <= 2: newH = 2

                if newW == 2 and newH == 2:
                    red = 0

            if zoom == "in":
                templist = list(reversed(templist))

            self.animlist.append(templist)

    #---------------------------------------------------------------------------

    def rotate_func(self, rotate, zoom):

        if rotate == "right": self.increment = -(360 / self.frames)  # default 2 rounds
        elif rotate == "left": self.increment = (360 / self.frames)

        self.angle = 0

        Done = False

        if self.animlist == []:  # animation not done, use self.imagelist and build

            Done = True

            for image in self.imagelist:
                # take each image and make a list of images with rotation LEFT or RIGHT
                templist = []
                # make 1st. image no rotation
                image = self.set_colour_key_func(image)
                templist.append(image)

                # make the required frames with each image and adding them to the sublists

                for r in xrange(self.cycles):

                    for x in xrange(self.frames):

                        self.angle += self.increment
                        rotsurface = pygame.transform.rotate(image, self.angle)
                        rotsurface = self.set_colour_key_func(rotsurface)
                        templist.append(rotsurface)

                # add the sublist to self.animlist
                self.animlist.append(templist)
                self.angle = 0

        elif self.animlist != [] and Done == False: # animation exsists, modify exsisting frames

            for x in xrange(len(self.animlist)):

                temp = self.animlist[x][-1]  # get the last frame

                for y in xrange(len(self.animlist[x]) - 1):

                    rotsurface = pygame.transform.rotate(self.animlist[x][y], self.angle)

                    self.animlist[x][y] = rotsurface

                    self.angle += self.increment

                    self.animlist[x].append(temp)

                self.angle = 0

    #---------------------------------------------------------------------------

    def fade_func(self, fade):

        self.q = 255 / self.frames  # fade amount each frame

        Done = False  # if the 1st. fade routines are complete this is set to True

        if fade == "in":

            self.alpha = 0
            self.q = abs(self.q) #make plus

        elif fade == "out":

            self.alpha = 255
            self.q = - abs(self.q)  # make minus

        if self.animlist == []:  # animation not done, use self.imagelist and build

            for image in self.imagelist:
                # take each image and make a list of images with fade IN or OUT
                templist = []
                setimage = self.set_colour_key_func(image)

                #image.set_alpha(self.alpha)  # make 1st. image fully transparent
                templist.append(setimage)

            # add the rest of the images making the required frames

                for x in xrange((self.frames) + 2):

                    newimage = image.copy()
                    newimage.set_alpha(self.alpha)

                    templist.append(newimage)
                    self.alpha += self.q
                    if self.alpha > 255: self.alpha = 255
                    if self.alpha < 0: self.alpha = 0

                if fade == "in":
                    self.alpha = 0

                elif fade == "out":
                    self.alpha = 255

                #add the sublist to self.animlist
                self.animlist.append(templist)

        elif self.animlist != [] and Done == False:  # animation done externally, Modify exsisting frames

            for animlist in self.animlist:
                for image in animlist:

                    image.set_alpha(self.alpha)

                    self.alpha += self.q

                    if self.alpha >= 255: self.alpha = 255
                    if self.alpha <= 0: self.alpha = 0

                if fade == "in":
                    self.alpha = 0

                elif fade == "out":
                    self.alpha = 255

    #---------------------------------------------------------------------------

    def slide_func(self, slide):
        """The slide function allocates a new position to the image."""

        height_of_all_images = 0
        max_height = max_width = 0

        for i in self.imagelist:

            i_height = i.get_height()
            i_width = i.get_width()

            if i_height > max_height:
                max_height = i_height

            if i_width > max_width:
                max_width = i_width

            height_of_all_images += i_height

        if "in top" in slide or "out bottom" in slide:
            offset_top_image = self.posy + (height_of_all_images / 2)  # offset is the lowest line moving up
        else:
            offset_top_image = self.posy - (height_of_all_images / 2)

        if self.animlist == []:  # no animation. No zoom, roation or fade.

            for image in self.imagelist:
                self.set_colour_key_func(image)

                self.animlist.append([image.convert_alpha()])

        return offset_top_image, max_width, max_height

    #---------------------------------------------------------------------------

    def lowercase(self, word, effect):
        if word is not None:
            word = word.lower()

        funcs = {"zoom": ["in", "out"], "fade": ["in", "out"], "rotate": ["left", "right"], "slide":["in left", "in right", "in top", "in bottom", "out left", "out right", "out top", "out bottom"],}

        if word not in funcs[effect]:
            word = None

        return word

    #---------------------------------------------------------------------------

    def uppercase(self, word, effect):

        word = word.upper()

        if word not in ["L", "C", "R"]:
            word = None

        return word

    #---------------------------------------------------------------------------

    def run(self, zoom = None, fade = None, rotate = None, slide = None, message = None, font = None, fontsize = None, justify = "C", colour = None, frames = None, pause = None, slowdown = None, cycles = None, posx = None, posy = None, reduceX = None, reduceY = None):

        """This is the control routine that runs all the tasks"""
        self.back = self.screen.subsurface(self.screen.get_rect()).convert()
        self.imagelist = []  # clear the imagelist for new building
        self.animlist = []

        if not frames: frames = self.frames
        if not font: font = self.font
        if not fontsize: fontsize = self.fontsize
        if not colour: colour = self.colour
        if not cycles: cycles = self.cycles
        if not frames: frames = self.frames
        if not pause: pause = self.pause
        if not slowdown: slowdown = self.slowdown
        if not posx: posx = self.posx
        if not posy: posy = self.posy
        if not reduceX: reduceX = self.reduceX
        if not reduceY: reducey = self.reduceY

        if not message: message = [self.text1 + str(self.level) + self.text2, ]  # the comma at the end turns the string into a tuple
        #if len(message) == 1:
            #message.append("")  # makes the zoom effect look realistic
        #if zoom == None:
            #zoom = self.zoom
        if not None:
            zoom = self.lowercase(zoom, "zoom")
            print

        #if rotate == None:
            #rotate = self.rotate
        if not None:
            rotate = self.lowercase(rotate, "rotate")

        #if fade == None:
            #fade = self.fade
        if not None:
            fade = self.lowercase(fade, "fade")

        #if slide == None:
            #slide = self.slide
        if not None:
            slide = self.lowercase(slide, "slide")

        #if justify == None:
            #justify = self.justify
        if not None:
            justify = self.uppercase(justify, "justify")

        # by using [:] we can insert all items in the list coming from the function WITHOUT the [].
        self.imagelist[:] = self.single_or_multi_to_image(colour, font, fontsize, message, slide, justify)

        if zoom != None:

            self.zoom_func(zoom)

        if rotate != None:

            self.rotate_func(rotate, zoom)

        if fade != None:

            self.fade_func(fade)

        if slide != None:

            ypos, max_width, max_height = self.slide_func(slide)

        if slide is not None:  # slide is on

            num = 1; delay = 3

            if "in top" in slide or "out bottom"in slide:
                self.animlist = reversed(self.animlist)

            for sublist in self.animlist:

                if "in" in slide:

                    if "left" in slide:  # slide in from LEFT

                        posx = -sublist[0].get_width() # off screen left
                        posy = ypos + max_height
                        txtobj = Sliders(posx, posy, sublist)
                        txtobj.xadd = 10

                    elif "right" in slide:

                        posx = self.screen.get_width() + sublist[0].get_width() / 2  # off screen right
                        posy = ypos + max_height
                        txtobj = Sliders(posx, posy, sublist)
                        txtobj.xadd = -10

                    elif "top" in slide:

                        posx = self.rect.centerx
                        posy = -ypos + max_height
                        txtobj = Sliders(posx, posy, sublist)
                        txtobj.screenposy = ypos  # ypos of text object final posttion
                        txtobj.yadd = 10

                    elif "bottom" in slide:

                        posx = self.rect.centerx
                        posy = self.screen.get_height() + max_height
                        txtobj = Sliders(posx, posy, sublist)
                        txtobj.screenposy = ypos  # ypos of text objects final position
                        txtobj.yadd = -10

                if "out" in slide:

                    posx = self.rect.centerx
                    posy = ypos

                    if "left" in slide:  # slide out to LEFT

                        txtobj = Sliders(posx, posy, sublist)
                        txtobj.xadd = -10

                    elif "right" in slide:  # slide out to LEFT

                        txtobj = Sliders(posx, posy, sublist)
                        txtobj.xadd = 10

                    elif "top" in slide:

                        txtobj = Sliders(posx, posy, sublist)
                        txtobj.yadd = -10

                    elif "bottom" in slide:

                        txtobj = Sliders(posx, posy, sublist)
                        #txtobj.screenposy = ypos  # ypos of text objects final position
                        txtobj.yadd = 10

                txtobj.max_width = max_width
                txtobj.max_height = max_height
                txtobj.num = num
                txtobj.delay = delay

                self.anim_sprites.add(txtobj)

                if "in top" in slide or "out bottom" in slide:
                    ypos -= max_height

                elif "out top" in slide or "in bottom" in slide or "in left" in slide or "in right" in slide or "out left" in slide or "out right" in slide:
                    ypos += max_height

                num += 1

                delay += 15

            # now animate
            #============

            done = False

            frame1wait = True

            while  not done:

                for e in pygame.event.get():
                    if e.type == KEYDOWN and e.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                for obj in self.anim_sprites:

                    obj.move()

                    if "in" in slide:

                        if "left" in slide:

                            if obj.rect.centerx >= self.rect.centerx:
                                obj.rect.center = (self.rect.centerx, obj.posy)
                                if obj.frame == obj.length:
                                    obj.done = True
                            else:
                                obj.done = False

                        elif "right" in slide:

                            if obj.rect.centerx <= self.rect.centerx:
                                obj.rect.center = (self.rect.centerx, obj.posy)
                                if obj.frame == obj.length:
                                    obj.done = True
                            else:
                                obj.done = False

                        elif "top" in slide:

                            if obj.rect.centery >= obj.screenposy:
                                obj.rect.center = (obj.posx, obj.screenposy)
                                if obj.frame == obj.length:
                                    obj.done = True
                            else:
                                obj.done = False

                        elif "bottom" in slide:

                            if obj.rect.centery <=  obj.screenposy:
                                obj.rect.center = (obj.posx, obj.screenposy)
                                if obj.frame == obj.length:
                                    obj.done = True
                            else:
                                obj.done = False


                    elif "out" in slide:

                        if "left" in slide:

                            if obj.rect.centerx <= -obj.width / 2:
                                obj.rect.center = (-obj.width / 2, obj.screenposy)
                                if obj.frame == obj.length:
                                    obj.done = True
                            else:
                                obj.done = False

                        elif "right" in slide:

                            if obj.rect.centerx >= self.screen.get_width() + obj.width / 2:
                                if obj.frame == obj.length:
                                    obj.done = True
                            else:
                                obj.done = False

                        elif "top" in slide:

                            if obj.rect.centery <= -obj.height:
                                if obj.frame == obj.length:
                                    obj.done = True
                            else:
                                obj.done = False

                        elif "bottom" in slide:

                            if obj.rect.centery >= self.screen.get_height() + obj.height / 2:
                                if obj.frame == obj.length:
                                    obj.done = True
                            else:
                                obj.done = False

                if obj.done == True:
                    done = True

                rects = self.anim_sprites.draw(self.screen)

                pygame.display.update(rects)

                pygame.time.wait(40)

                self.anim_sprites.clear(self.screen, self.back)


                if "out" in slide and frame1wait:
                    pygame.time.wait(self.pause)
                    frame1wait = False

            if "in" in slide:  # after the animation is done pause on the last frame only if tha animation

                pygame.time.wait(self.pause)

    #---------------------------------------------------------------------------
        elif slide == None:

            for meslist in self.animlist:

                for image in meslist:

                    draw_rect, clear_rect = self.get_rects(image, slide)

                    self.blit_func(image, draw_rect, clear_rect)

                    if fade == "out" or zoom == "out":

                        if image is meslist[0]:  # hold the first frame
                            pygame.time.wait(self.pause)

                if rotate != None:
                    pygame.time.wait(self.pause)

                if fade == "in" or zoom == "in":  # hold the last frame
                    pygame.time.wait(self.pause)

    #---------------------------------------------------------------------------
    def default(self):

        self.run(zoom = "in")

        self.run(zoom = "out")

    #---------------------------------------------------------------------------

def run_text():
    tf = Text_Factory()
     
    tf.run(zoom = "out", colour= (255,255,255), rotate = None, fade = None, slide = None, message = ["Welcome!!!"," ", "Oh would you look at that!", "It's time for your daily exercise!", "Let us get started with, a routine!"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out right", message = ["Start by stretching"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["and make sure you are ready", "for an intense workout"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out right", message = ["Start by jumping up ", "and down on one foot"])
    tf.run(zoom = None, colour= (255,255,255), rotate = "right", fade = None, slide = None, message = ["alternating your foot each time"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["Now pretend you are playing basketball"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out right", message = ["And pretend you just made", "a three pointer to win", "the NBA championship!"])
    tf.run(zoom = None, colour= (255,255,255), rotate = "left", fade = None, slide = None, message = ["Now stop and sit criss cross applesauce."])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out right", message = ["And raise your hand", "as if you were about"," to ask a question"])
    tf.run(zoom = None, colour= (255,255,255), rotate = "left", fade = None, slide = None, message = ["and yell"," 'I love myselfffff!!!'"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["Now do your favorite yoga stretch!"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["And say 'Ummmm' 'Ummmmm' a couple times."])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["And take a deep breath..."])
    tf.run(zoom = "out", colour= (255,255,255), rotate = None, fade = None, slide = None, message = ["Because now comes the crazy part..."])
    tf.run(zoom = None, colour= (255,255,255), rotate = "right", fade = None, slide = None, message = ["Are you ready????"])
    tf.run(zoom = "out", colour= (255,255,255), rotate = None, fade = None, slide = None, message = ["Just kidding... ", "The workout has ended and you ", "have an upcoming event on your calendar", "Have a great day:)"])

if __name__ == '__main__':

    tf = Text_Factory()

    tf.run(zoom = "out", colour= (255,255,255), rotate = None, fade = None, slide = None, message = ["Welcome!!!"," ", "Oh would you look at that!", "It's time for your daily exercise!", "Let us get started with, a routine!"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out right", message = ["Start by stretching"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["and make sure you are ready", "for an intense workout"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out right", message = ["Start by jumping up ", "and down on one foot"])
    tf.run(zoom = None, colour= (255,255,255), rotate = "right", fade = None, slide = None, message = ["alternating your foot each time"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["Now pretend you are playing basketball"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out right", message = ["And pretend you just made", "a three pointer to win", "the NBA championship!"])
    tf.run(zoom = None, colour= (255,255,255), rotate = "left", fade = None, slide = None, message = ["Now stop and sit criss cross applesauce."])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out right", message = ["And raise your hand", "as if you were about"," to ask a question"])
    tf.run(zoom = None, colour= (255,255,255), rotate = "left", fade = None, slide = None, message = ["and yell"," 'I love myselfffff!!!'"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["Now do your favorite yoga stretch!"])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["And say 'Ummmm' 'Ummmmm' a couple times."])
    tf.run(zoom = None, colour= (255,255,255), rotate = None, fade = None, slide = "out left", message = ["And take a deep breath..."])
    tf.run(zoom = "out", colour= (255,255,255), rotate = None, fade = None, slide = None, message = ["Because now comes the crazy part..."])
    tf.run(zoom = None, colour= (255,255,255), rotate = "right", fade = None, slide = None, message = ["Are you ready????"])
    tf.run(zoom = "out", colour= (255,255,255), rotate = None, fade = None, slide = None, message = ["Just kidding... ", "The workout has ended and you ", "have an upcoming event on your calendar", "Have a great day:)"])