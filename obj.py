from base_obj import *

class Roach(Actor_Sprite):
    def __init__(self,game,x,y,image,sprite_group,entity_group):
        image = [load_image("0.png"),load_image("1.png")]
        Actor_Sprite.__init__(self,game,x,y,image,sprite_group,entity_group)
        self.hitrect=pg.Rect((x,y),(16,16))
        self.vel = vector(100,0)
        self.rot_speed=200
        self.change_layer(LAYERS["GROUND"])
        self.frame_duration=SLOW_FRAME
        self.step=1

    def update(self):
        Actor_Sprite.update(self)

class Player(Actor_Sprite):
    def __init__(self,game,x,y,image,sprite_group,entity_group):
        self.name='Player'
        image=[load_image("Person_Demo/body.png",size=200)]
        Actor_Sprite.__init__(self,game,x,y,image,sprite_group,entity_group)
        self.hitrect=pg.Rect((x,y),(16,16))
        self.vel = vector(100,0)
        self.rot_speed=200
        self.change_layer(LAYERS["SHOULDER_LEVEL"])

        img_arms=  [
                    load_image("Person_Demo/arm1.png",size=200),
                    load_image("Person_Demo/arm2.png",size=200),
                    load_image("Person_Demo/arm3.png",size=200),
                    load_image("Person_Demo/arm4.png",size=200)
                    ]
        self.sprite_arms=Actor_Sprite(self.game,self.pos.x,self.pos.y,img_arms,self.sprite_group,self.entity_group)
        self.sprite_arms.frame_duration=SLOW_FRAME
        self.sprite_arms.parent=self
        self.sprite_arms.change_layer(LAYERS["HIP_LEVEL"])
        #self.sprite_arms.frame_step=1
        #self.sprite_arms.keyframe_len-=1
        #self.sprite_arms.animation_type=2

        img_extended_arm=[load_image("Person_Demo/armExtended.png",size=200)]
        self.extended_arm=Actor_Sprite(self.game,self.pos.x,self.pos.y,img_extended_arm,self.sprite_group,self.entity_group)
        self.extended_arm.parent=self
        self.extended_arm.change_layer(-1)

        img_head=   [load_image("Person_Demo/head.png",size=200)]
        self.sprite_head=Actor_Sprite(self.game,self.pos.x,self.pos.y,img_head,self.sprite_group,self.entity_group)
        self.sprite_head.change_layer(LAYERS["HEAD_LEVEL"])
        self.sprite_head.parent=self
    def get_keys(self):
        #necesita actualizacion
        if self.game.key_hit[pg.K_d]:
            self.rotate(-self.rot_speed,self.game.delta_time)
        if self.game.key_hit[pg.K_a]:
            self.rotate(self.rot_speed,self.game.delta_time)
        if self.game.key_hit[pg.K_w]:
            self.fwd=1
            self.move_towards(self.game.delta_time)
            self.state("run")
        elif self.game.key_hit[pg.K_s]:
            self.fwd=-1
            self.move_towards(self.game.delta_time)
            self.state("run")
        else:
            self.state("idle")
        if self.game.key_hit[pg.K_SPACE]:
            self.state("hit")
            pass
    def update(self):
        ###Calculo de rotacion de cabeza
        r = -calc_angle(self.sprite_head.rect.center,pg.mouse.get_pos(),self.sprite_group)
        if r<0:
            self.sprite_head.rot= 360+r
        else:
            self.sprite_head.rot= r

        rE = 90 # *2 angulo maximo de vista
        rD = -180
        if self.rot+rE>360 or self.rot-rE<0 :
            #si la rotacion mas el angulo de vista es mayor a 360 o menor a 0
            if self.rot+rE>360:
                r = self.rot+rE-360
                if self.sprite_head.rot>r and self.sprite_head.rot<self.rot-rE:
                    self.sprite_head.rot= 360-abs(-self.sprite_head.rot + rD) + 2*self.rot
            if self.rot-rE<0:
                r=self.rot-rE+360
                if self.sprite_head.rot<r and self.sprite_head.rot>self.rot+rE:
                    self.sprite_head.rot = 360-abs(-self.sprite_head.rot + rD) + 2*self.rot
        elif self.sprite_head.rot<self.rot-rE or self.sprite_head.rot > self.rot+rE:
            self.sprite_head.rot= 360-abs(-self.sprite_head.rot + rD) + 2*self.rot
        ###
        self.get_keys()
        Actor_Sprite.update(self)

        pass
    def state(self,state):
        if state=="run":
            self.sprite_arms.keyframe_len=3
            #if self.sprite_arms.frame>self.sprite_arms.keyframe_len:
             #   self.sprite_arms.frame=0
            self.sprite_arms.updateFrame()
            self.sprite_arms.animation_type=2
            self.extended_arm.change_layer(-1)

            pass
        elif state=="idle":
            self.sprite_arms.frame=2
            self.extended_arm.change_layer(-1)
            pass
        elif state=="hit":
            self.extended_arm.change_layer(LAYERS["HIP_LEVEL"])
            #self.sprite_arms.frame=4
            #self.sprite_arms.animation_type=3
            #self.sprite_arms.keyframe_len=0
        else:
            print("estado no encontrado")
            pass

        pass

def calc_angle(A, B,group):
    from math import atan2, degrees

    return round(degrees(atan2(-A[1]+B[1]+group.view.top, -A[0]+B[0]+group.view.left)))

class Wall(Actor):
    def __init__(self,game,x,y,w,h,entity_group):
        self.name='Wall'
        Actor.__init__(self,game,x,y,entity_group)
        self.hitrect=pg.Rect((x,y),(w,h))
    def collision(self,other):
        other.fwd=-other.fwd
        other.move_towards(self.game.delta_time)
        collisionX(self,other)
        collisionY(self,other)
        pass
    def update(self):
        pass

def collisionX(first,second):
    second.hitrect.centerx=second.pos.x
def collisionY(first,second):
    second.hitrect.centery=second.pos.y
