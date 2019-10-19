
#game settings
s=4
WIDTH = 256*s
HEIGHT = 150*s
FPS = 120
FAST_FRAME = FPS / 12
NORMAL_FRAME = FPS / 6
SLOW_FRAME = FPS / 3
TILE = 32
TILERECT = (int(TILE),int(TILE))

#game variables
ENTITY_LIST=[]


#order of render
LAYERS = {	"BOTTOM" : 0,
			"GROUND" : 1,
			"GROUND_LEVEL" : 2,
			"HIP_LEVEL" : 3,
			"SHOULDER_LEVEL" : 4,
			"HEAD_LEVEL" : 5,
			"OVERHEAD" : 6,
			"TOP":7
		}
#player settings


#colors
COLORS ={	"BLACK" : (0,0,0),
			"WHITE" : (255,255,255),
			"RED" : (255,0,0),
			"BLUE" : (0,0,255),
			"LIME" : (0,255,0),
			"YELLOW" : (255,255,0),
			"CYAN" : (0,255,255),
			"MAGENTA" : (255,0,255),
			"SILVER" : (192,192,192),
			"GRAY" : (128,128,128),
			"MAROON" : (128,0,0),
			"OLIVE" : (128,128,0),
			"GREEN" : (0,128,0),
			"PURPLE" : (128,0,128),
			"TEAL" :  (0,128,128),
			"NAVY" : (0,0,128)
		}

COLOR_DEBUG = COLORS["CYAN"]
