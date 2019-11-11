from nova import *
#import nova
from random import randrange





def cucaClass(entitySys,SpritesGroup,collisionGroup):
    cuca = Entity()
    cuca.addComponent(PointComponent(randrange(0,WIDTH),randrange(0,HEIGHT),0))
    cuca.addComponent(SpriteComponent(["0.png","1.png"],SpritesGroup,rotation=randrange(0,360)))
    #cuca.addComponent(SpriteComponent(["0.png","1.png"],self.SpritesGroup,rotation=randrange(0,360),size=randrange(1,200)))
    cuca.addComponent(CollisionRectComponent(collisionGroup=collisionGroup))
    
    class behaviour(BehaviourComponent):
        def __init__(self):
            BehaviourComponent.__init__(self,cuca)
        def updateBehaviour(self):
            for component in self.componentsToBehave:
                if type(component) is PointComponent: 
                    component.rotation += 1 
                    pass
    
    cuca.addComponent(behaviour())                        
    entitySys.addEntity(cuca)
    return cuca
    