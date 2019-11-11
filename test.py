import pygame
from nova import *
from random import randrange

display = pygame.display.set_mode((1000, 1000))#, _flags )

if __name__ == "__main__":
    pygame.init()
    hud = Text() 
    running = True
    clock = pygame.time.Clock()
    while running:
        delta=clock.tick(FPS) / 1000
        key_hit=pygame.key.get_pressed()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (key_hit[pygame.K_ESCAPE]):
                running = False
                print("Procesado evento de salir")
        hud.draw_text(['fps: '+str(clock.get_fps())[0:4]],display)
        for i in range(0,20):
            pygame.draw.rect(display,(0,255,255),(randrange(0,1000),randrange(0,1000),randrange(0,1000),randrange(0,1000)),1)

        pygame.display.update(display.get_rect())
        	