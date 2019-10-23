
from nova import *
from random import randrange

class Game(BaseScene):
    def __init__(self):
        pygame.init()
        self.screen = WindowSDL().display
        #self.screen = init_screen(WIDTH, HEIGHT)
        #pygame.display.set_caption("DEMO")
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_data() #precacheo de recursos
        self.new() #inicialisacion de recursos

        pass

    def load_data(self):
        #CARGAR RECURSOS
        self.map = Map(F_map, "LevelDemo2.tmx")
        pass

    def new(self):
        self.map.data.convert_surfaces(self.screen,True)
        #Grupo de elementos a dibujar
        self.toggleDebug=False
        self.SpritesGroup = Entity()
        self.SpritesGroup.addComponent(pyscroll.PyscrollGroup(map_layer=self.map.layer))
        #Grupos de entidades para actualizar
        self.entitySys = EntitySystem(self,'primerGrupo')
        self.entitySys.addEntity(self.SpritesGroup)
              
        for i in range(0,100):
            cuca = Entity()
            cuca.addComponent(PointComponent(randrange(0,WIDTH),randrange(0,HEIGHT)))
            cuca.addComponent(SpriteComponent(["0.png","1.png"],self.SpritesGroup,rotation=randrange(0,360),size=randrange(1,200)))
            #cuca.addComponent(SpriteComponent("0.png",self.SpritesGroup,rotation=randrange(0,360),size=randrange(1,200)))
            self.entitySys.addEntity(cuca)
        
        self.hud=Text()


    def update(self):
        self.delta_time = self.clock.tick(FPS) / 1000
        #self.map.layer.center(self.player.pos)#la camara(el mapa) mira hacia el target
        pass


    def draw_scene(self):

        self.entitySys.update()

        self.hud.draw_text(['fps: '+str(self.clock.get_fps())[0:4]],self.screen)
        
        if self.toggleDebug==True:
            self.group_all_entities.draw_debug(self.screen,self.group_all_sprites)

        pygame.display.update(self.screen.get_rect())
        pass
    def events(self):
        BaseScene.events(self)
        pass


game = Game()

if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption('N O V A.')
    #intro.run()
    if game.running==True:
        game.run()
        pygame.quit()
