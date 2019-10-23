import pygame
import pytmx
import pyscroll
from settings import *
from os import path
#from math import atan2,degrees
import sys

config_name = 'myapp.cfg'
if getattr(sys, 'frozen', False):
    application_path = path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = path.realpath(__file__)
        application_path = path.dirname(app_full_path)
        #running_mode = "Non-interactive (e.g. 'python myapp.py')"
    except NameError:
        application_path = getcwd()
        running_mode = 'Interactive'

#print("running mode: "+running_mode)
FOLDER = application_path
F_img = path.join(FOLDER, "imgs")
F_map = path.join(FOLDER, "maps")
F_font = path.join(FOLDER, "fonts")
vector = pygame.math.Vector2



class Map():
    def __init__(self,folder,file):
        self.tmx = pytmx.load_pygame(path.join(folder,file))
        self.data = pyscroll.data.TiledMapData(self.tmx)
        self.layer = pyscroll.BufferedRenderer  (self.data,
                                                (WIDTH, HEIGHT),
                                                clamp_camera=True)

class Game0bj() :
    def __init__(self, game):
        self.game = game

class Text():
    def __init__(self,size=16,color=COLOR_DEBUG, bkgcolor=COLORS["BLACK"]):
        self.name='Text'
        self.size=size
        #self.font = pygame.font.SysFont("arial", self.size)
        self.font=pygame.font.Font(path.join(F_font,'Inconsolata-Regular.ttf'),self.size)
        self.color = color
        self.bkgcolor = bkgcolor
        self.image = self.font.render(str(''), 1, self.color)
    def draw_text(self,src_txt,target,x=0,y=0):
        for i in range(0,len(src_txt)):
            self.image = self.font.render(src_txt[i], True, self.color,self.bkgcolor)
            target.blit(self.image,(x,y+i*self.size))

class BaseScene():
    def _init_(self):
        self.name='BaseScene'
        pass
    def load_data(self):
        pass
    def new(self):
        pass
    def update(self):
        pass
    def draw_scene(self):
        pass
    def events(self):
        self.key_hit=pygame.key.get_pressed()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (self.key_hit[pygame.K_ESCAPE]):
                self.running = False
                print("Procesado evento de salir")
                #pygame.quit()
                #exit()
        pass
        pass
    def run(self):
        #try:
            while self.running:
                self.events()

                self.draw_scene()

                self.update()
        #except KeyboardInterrupt:
            #if self.running==False:
             #   self.running = False
              #  print("Saliedo...")
               # pygame.quit()
        #pass

######ECS
class Entity():
    def __init__(self):
        self.components = []
    def addComponent(self,source):
        self.components.append(source)
    def removeComponent(self,source):
        self.components.remove(source)

class PointComponent():
    def __init__(self,x,y):
        self.position= vector(x,y)
        self.rotation= 0

class SpriteComponent(pygame.sprite.Sprite):
    def __init__(self,image,group,layer=10,
                x=None,y=None,rotation=None,size=None,
                step=1,animation_type=1,frame_duration=1):
        self._layer = layer
        pygame.sprite.Sprite.__init__(self,group.components[0])
        self.group = group
        if type(image).__name__!='list':
            self.image = pygame.image.load(path.join(F_img,image))
            self.originalimage = self.image
            #self.modify()
            self.rect = self.image.get_rect()
            self.animated= False
        else:
            self.animated=True
            self.keyframes=[]
            self.keyframe_len = len(image)
            print("klen: "+str(self.keyframe_len))
            for i in range(self.keyframe_len):
                self.keyframes.append(pygame.image.load(path.join(F_img,image[i])))
            self.frame = 0
            self.frame_position = 0
            self.frame_step = step #1)beg_to_end|-1)end_to_beg
            self.frame_duration = frame_duration # duracion en frames por key
            self.animation_type = animation_type #1-cycle|2-bounce|3-once
            self.image = self.keyframes[0]      
            self.rect = self.image.get_rect()
    def modify(self,x=None,y=None,rotation=None,size=None):
        if x == None or y == None:
            #x e y positionicionan el centro de la imagen para la rotacion
            pass
        else:
            _w = surface.get_width()
            _h = surface.get_height()
            surface = pygame.Surface((_w*2,_h*2))
            surface.blit(surface,(_w-x,_h-y))
            surface.set_colorkey(WHITE)
        if rotation != None:
            surface = pygame.transform.rotate(surface,rotation)
        if size != None:
            size=size/100
            surface = pygame.transform.scale(surface,(int(surface.get_width()*size),int(surface.get_height()*size)))
        self.image = surface
    def change_layer(self,layer):
        self.group.change_layer(self,layer)
    def change_key(self):
        if self.frame in range(self.keyframe_len-1):
            self.frame += self.frame_step
        else:
            if self.animation_type == 1:
                self.frame = 0
            if self.animation_type == 2:
                self.frame_step = -self.frame_step
                self.frame += self.frame_step

            if self.animation_type == 3:
                pass
    def updateFrame(self):
        self.frame_position += 1
        if self.frame_position == self.frame_duration :
            self.change_key()
            self.frame_position = 0
    def updateSprite(self,rot):
        if self.animated:
            self.image = pygame.transform.rotate(self.keyframes[self.frame], rot)
            self.updateFrame()
        else:
            self.image = pygame.transform.rotate(self.originalimage, rot)
        self.rect = self.image.get_rect()
        
        



class EntitySystem():
    def __init__(self,gameObj,name):
        self.name = name
        self.gameObj = gameObj
        self.list= []
    def addEntity(self,source):
        self.list.append(source)
    def removeEntity(self,source):
        self.list.remove(source)
    def update(self):
        for entity in self.list:
            for component in entity.components: 
                if type(component) is PointComponent:
                    position = component.position
                if type(component) is SpriteComponent:
                    component.updateSprite(0)
                    component.rect.center = position
                    
                if type(component) is pyscroll.PyscrollGroup:
                    component.draw(self.gameObj.screen)
 

class WindowSDL():
    def __init__(self,width=WIDTH,height=HEIGHT):
        _flags = pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.RESIZABLE
        #_flags = pygame.FULLSCREEN
        self.display = pygame.display.set_mode((width, height))#, _flags )
        self.display.set_alpha(None)


