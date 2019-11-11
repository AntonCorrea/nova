
#from nova import *
from classes import *

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
        self.collisionGroup = []
        self.SpritesGroup = Entity()
        self.SpritesGroup.addComponent(pyscroll.PyscrollGroup(map_layer=self.map.layer))
        #Grupos de entidades para actualizar
        self.entitySys = EntitySystem(self,'primerGrupo')
        self.entitySys.addEntity(self.SpritesGroup)
        cuca = []
        for i in range(0,20):
            cuca.append(cucaClass(self.entitySys,self.SpritesGroup,self.collisionGroup))
        
        self.hud=Text()


    def update(self):
        self.delta_time = self.clock.tick(FPS) / 1000
        self.map.layer.center(pygame.mouse.get_pos())#la camara(el mapa) mira hacia el target
        self.entitySys.update()
        pass


    def draw_scene(self):

        

        self.hud.draw_text(['fps: '+str(self.clock.get_fps())[0:4]],self.screen)
        
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
