import pygame as pg
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
vector = pg.math.Vector2

def init_screen(width, height):

    _flags = pg.DOUBLEBUF | pg.FULLSCREEN | pg.RESIZABLE
    #_flags = pg.FULLSCREEN
    screen = pg.display.set_mode((width, height))#, _flags )
    screen.set_alpha(None)
    return screen

def load_image(image,x = None,y = None,rotation = None,size = None):
    #!Modificar para aceptar imagenes con tiles y separarlas
    #!Necesita canales alpha para transparencias
    surface = pg.image.load(path.join(F_img,image))
    if x == None or y == None:
        #x e y posicionan el centro de la imagen para la rotacion
        pass
    else:
        _w = surface.get_width()
        _h = surface.get_height()
        surface = pg.Surface((_w*2,_h*2))
        surface.blit(surface,(_w-x,_h-y))
        surface.set_colorkey(WHITE)
    if rotation != None:
        surface = pg.transform.rotate(surface,rotation)
    if size != None:
        size=size/100
        surface = pg.transform.scale(surface,(int(surface.get_width()*size),int(surface.get_height()*size)))
        #surface.set_alpha(None)
    return surface

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

class Point():
    def __init__(self, x, y):
        self.pos = vector(x, y)
        self.vel = vector(0,0)
        #self.dir= vector(0,0)
        self.rot = 0
        self.fwd=1
    def move_towards(self,dt):
        #movimiento hacia adelante o atras, respecto a la rotacion
        self.pos += self.fwd*self.vel.rotate(-self.rot) * dt

    """NO ANDAN
    def move_absolute(self,grade,dt):
        #movimiento en direccion al angulo
        self.pos += self.vel.rotate(grade) * dt
        #self.dir.from_polar((0,self.rot))
    def move_strafe(self,grade,dt):
        #movimiento relativo con la rotacion
        self.pos += self.vel.rotate(self.rot+grade) * dt"""

    def rotate(self,factor,dt):
        if self.rot<0:
            self.rot = 360+(factor* dt)
        if self.rot>360:
            self.rot=0
        else:
            self.rot += (factor* dt)
    def update(self):
        pass

class Actor(Game0bj,Point):
    #un actor es una entidad manipulable dentro del juego.
    def __init__(self,game,x,y,entity_group=None,parent=None):
        Game0bj.__init__(self,game)
        Point.__init__(self,x,y)
        self.parent=parent
        if entity_group!=None:
            entity_group.add(self)
            self.entity_group=entity_group
        self.hitrect=pg.Rect((x,y),TILERECT)
        #self.rect=self.hitrect
    def collision(self,other):
        pass
    def update(self):
        pass

class Sprite(pg.sprite.Sprite,Game0bj):
    #Imagen con rect(), layers, rotacion, animacion y q se puede pegar en la
    #pantalla de forma estatica UNICAMENTE usando draw(),por lo q su layer debe
    # ser oculto.
    #No instanciar directamente, solo funca con Actor_Sprite.
    def __init__(self,game,image,sprite_group,step=1,animation_type=1,frame_duration=1,layer=LAYERS["HIP_LEVEL"]):
        Game0bj.__init__(self,game)
        self.name='Sprite'
        self._layer = layer
        if sprite_group!=None:
            self.sprite_group = sprite_group
            pg.sprite.Sprite.__init__(self,self.sprite_group)
        else:
            pg.sprite.Sprite.__init__(self)
        if type(image).__name__=='list':
            self.animated=True
            self.keyframe = image
            self.frame = 0
            self.keyframe_len = len(self.keyframe)-1
            self.frame_pos = 0
            self.frame_step = step #1)beg_to_end|-1)end_to_beg
            self.frame_duration = frame_duration # duracion en frames por key
            self.animation_type = animation_type #1-cycle|2-bounce|3-once
            self.image = self.keyframe[0]
        else:
            self.animated=False
            self.image=image
        self.rect = self.image.get_rect()
        if self.animated:
            self.originalimage = image[0]
        else:
            self.originalimage= image
    def change_layer(self,layer):
        self.sprite_group.change_layer(self,layer)
    def change_key(self):
        if self.frame > 0  and self.frame < self.keyframe_len :
            self.frame += self.frame_step
        else:
            if self.animation_type == 1:
                self.frame = 0
            if self.animation_type == 2:
                self.frame_step = -self.frame_step
                self.frame += self.frame_step

            if self.animation_type == 3:
                pass
    def draw(self,dest,x=0,y=0):
        #usado para pegar sprites en la pantalla,no en el escenario
        dest.blit(self.image,(x,y))
        self.update()
    def updateFrame(self):
        self.frame_pos += 1
        if self.frame_pos == self.frame_duration :
            self.change_key()
            self.frame_pos = 0
    def updateSprite(self):
        if self.animated:
            #if self.frame
            self.image = pg.transform.rotate(self.keyframe[self.frame], self.rot)
            self.updateFrame()
        else:
            self.image = pg.transform.rotate(self.originalimage, self.rot)
        self.rect = self.image.get_rect()
        pass
    def update(self):
        self.updateSprite()

class Actor_Sprite(Actor,Sprite):
    #un actor_sprite es un actor con un sprite asociado,ideal para sprites dentro del juego
    def __init__(self,game,x,y,image,sprite_group,entity_group):
        self.name='Actor_Sprite'
        Sprite.__init__(self,game,image,sprite_group)
        Actor.__init__(self,game,x,y,entity_group)
    def update(self):
        Sprite.update(self)
        #Actor.update(self)
        self.rect.center = self.pos
        self.hitrect.center=self.pos
        if self.parent != None:
            self.rect.center = self.parent.pos
            self.rot=self.parent.rot

class Entity_Group():
    # para updatear estados
    def __init__(self):
        self.name='Entity_Group'
        self.list=[]
        #self.list_names=[]
        self.text=Text(size=12)
    def add(self,source):
        #self.list_names.append(str(type(source))+'_'+str(len(self.list)))
        self.list.append(source)
    def remove(self,source):
        self.list.remove(source)
    def update(self):
        for entity in self.list:
            entity.update()
    def draw_debug(self,dest,group):
        for entity in self.list:
            rect=(entity.hitrect.left-group.view.left, entity.hitrect.top-group.view.top, entity.hitrect.width, entity.hitrect.height)
            self.text.draw_text([str(type(entity))],dest,rect[0],rect[1])
            pg.draw.circle(dest, COLOR_DEBUG,( int(entity.pos.x-group.view.left),int(entity.pos.y-group.view.top) ), 3,1)
            pg.draw.rect(dest,COLOR_DEBUG,rect,1)
            #Rect del sprite
            #rect=(entity.rect.left-group.view.left, entity.rect.top-group.view.top, entity.rect.width, entity.rect.height)
            #pg.draw.rect(dest,COLORS["BLACK"],rect,1)
    def collide_all_vs_one(self,one):
        self.remove(one)
        for entity in self.list:
            if one.hitrect.colliderect(entity.hitrect):
                if entity.parent!=one:
                    entity.collision(one)
                    pass
        self.add(one)

class Text():
    def __init__(self,size=16,color=COLOR_DEBUG, bkgcolor=COLORS["BLACK"]):
        self.name='Text'
        self.size=size
        #self.font = pg.font.SysFont("arial", self.size)
        self.font=pg.font.Font(path.join(F_font,'Inconsolata-Regular.ttf'),self.size)
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
        self.key_hit=pg.key.get_pressed()
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (self.key_hit[pg.K_ESCAPE]):
                self.running = False
                print("Procesado evento de salir")
                #pg.quit()
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
               # pg.quit()
        #pass

######ECS
class Entity():
    def __init__(self):
        self.components = []
    def add(self,source):
        self.components.append(source)
    def remove(self,source):
        self.components.remove(source)

class PointComponent():
    def __init__(self,x,y):
        self.pos= vector(x,y)

class SpriteComponent(pg.sprite.Sprite):
    def __init__(self,image,group,layer=4):
        self._layer = layer
        pg.sprite.Sprite.__init__(self,group)
        self.group = group
        self.image = image
        self.rect = self.image.get_rect()
        
    def render(self,surface,pos):
        self.rect.center = pos
        self.group.draw(surface)
        pass

class EntitySystem():
    def __init__(self,name,gameObj):
        self.name = name
        self.gameObj = gameObj
        self.list= []
    def add(self,source):
        self.list.append(source)
    def remove(self,source):
        self.list.remove(source)
    def update(self):
        for entity in self.list:
            for component in entity.components:
                #print(type(component)) 
                if type(component) is PointComponent:
                    pos = component.pos
                if type(component) is SpriteComponent:
                    component.render(self.gameObj.screen,pos)
                    
                    #print("a")
                #print(component) 



