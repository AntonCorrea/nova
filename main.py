
from obj import *
from random import randrange
class Game(BaseScene):

    def __init__(self):
        pg.init()
        self.screen = init_screen(WIDTH, HEIGHT)
        pg.display.set_caption("DEMO")
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data() #precacheo de recursos
        self.new() #inicialisacion de recursos

        pass

    def load_data(self):
        #CARGAR RECURSOS
        self.anim_coin=[    load_image("coin (1).png"),
        		            load_image("coin (2).png"),
                	    	load_image("coin (3).png"),
                        ]
        self.img_person=[   load_image("Person_Demo.png")]
        self.img_demo=[     load_image("TileDemo.png")]

        self.map = Map(F_map, "LevelDemo2.tmx")

        pass

    def new(self):
        self.map.data.convert_surfaces(self.screen,True)
        #Grupo de elementos a dibujar
        self.toggleDebug=False
        self.group_all_sprites = pyscroll.PyscrollGroup(map_layer=self.map.layer)
        #Grupos de entidades para actualizar
        self.group_all_entities = Entity_Group()
        ###
        self.entitySys = EntitySystem('primerGrupo',self)
        #self.spriteECS = SpriteComponent(load_image("0.png"),self.group_all_sprites)
        #self.spriteECS.rect.x = 100
        #self.spriteECS.rect.y = 100
        #self.entitySys.add(self.spriteECS)
        cuca = Entity()
        cuca.add(PointComponent(500,500))
        cuca.add(SpriteComponent(load_image("0.png"),self.group_all_sprites))
        self.entitySys.add(cuca)
        
        #Entidades
        self.hud=Text()
        """
        #self.sprite = Sprite(self.anim_coin,self.group_all_sprites)
        #self.sprite.change_layer(0)
        self.actor = Actor_Sprite(self,100,300,self.anim_coin,self.group_all_sprites,self.group_all_entities)

        for tile_object in self.map.tmx.objects:
            if tile_object.name=='wall':
                Wall(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height,self.group_all_entities)
"""
        self.player = Player(self,100,200,None,self.group_all_sprites,self.group_all_entities)
        """
        self.roach = Roach(self,200,200,None,self.group_all_sprites,self.group_all_entities)

        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill((20,20,20))
        self.light_mask = pg.image.load(path.join(F_img, "light.png")).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, (50,50))
        self.light_rect = self.light_mask.get_rect()
"""

    def update(self):
        self.delta_time = self.clock.tick(FPS) / 1000
        self.map.layer.center(self.player.pos)#la camara(el mapa) mira hacia el target
        self.group_all_entities.update()
        
        #self.spriteECS.rect = self.player.rect
        self.group_all_entities.collide_all_vs_one(self.player)

        pass

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill((20,20,20))
        rect=(self.player.hitrect.left-self.group_all_sprites.view.left, self.player.hitrect.top-self.group_all_sprites.view.top, self.player.hitrect.width, self.player.hitrect.height)
        self.light_rect.centerx = rect[0]
        self.light_rect.centery = rect[1]
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pg.BLEND_MULT)

    def draw_scene(self):

        #self.group_all_sprites.draw(self.screen)
        self.entitySys.update()
        #self.render_fog()
        self.hud.draw_text([    'fps: '+str(self.clock.get_fps())[0:4],
                                'pos: '+str(self.player.pos),
                                'h_rot: '+str(self.player.sprite_head.rot),
                                'p_rot: '+str(self.player.rot)]
                                ,self.screen)
        
        if self.toggleDebug==True:
            self.group_all_entities.draw_debug(self.screen,self.group_all_sprites)

        pg.display.update(self.screen.get_rect())
        pass
    def events(self):
        BaseScene.events(self)
        if self.key_hit[pg.K_f]:
            print("intro")
            intro.__init__()
            intro.run()
        if self.key_hit[pg.K_g]:
            if self.toggleDebug==True:
                print("debug desactivado")
                self.toggleDebug=False
            else:
                print("debug activado")
                self.toggleDebug=True
            pass

class IntroScreen(BaseScene):
    def __init__(self):
        pg.init()
        self.screen = init_screen(WIDTH, HEIGHT)
        pg.display.set_caption("Intro")
        self.running = True
        self.new()
    def new(self):
        self.text = Text()
        self.time=0
    def update(self):
        if self.time>400:
            self.running=False
            self.time=0
        else:
            self.time+=1
    def draw_scene(self):
        self.screen.fill(COLORS["BLACK"])
        self.text.color=COLORS["BLUE"]
        self.text.draw_text(    ["Demo presentada por:",
                                "Antonio Correa"],
                                self.screen,WIDTH/2-100,HEIGHT/2)
        self.text.color=COLORS["WHITE"]
        self.text.draw_text(    ["Demo presentada por:",
                                "Antonio Correa"],
                                self.screen,WIDTH/2-95,HEIGHT/2+5)
        pg.display.update(self.screen.get_rect())

intro= IntroScreen()
game = Game()
if __name__ == "__main__":

    pg.init()
    pg.display.set_caption('N O V A.')
    #intro.run()
    if game.running==True:
        game.run()
        pg.quit()
