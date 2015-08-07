import pygame
from enum import Enum

#Vars = camelCase
#Classes/Obj = underscores

BLACK 	= (0,0,0)
WHITE 	= (255,255,255)
RED 	= (255,0,0)
GREEN 	= (0,128,20)
BLUE 	= (0,0,255)


class ttype(Enum):
	
	ground 		= 0
	soldier 	= 1
	monster 	= 2
	barracks	= 3
	spawner 	= 4

	def get_type_colour(tileType):

		if (tileType is ttype.ground):
			return GREEN
		else:
			return WHITE

class tile_entity(pygame.sprite.Sprite):
	
	def __init__(self, ID, width, height, tileType=ttype.ground, colour=GREEN):
		pygame.sprite.Sprite.__init__(self)

		self.ID			= ID
		self.tileType 	= tileType
		self.colour 	= colour
		self.width 		= width
		self.height 	= height
		self.xpos		= 0
		self.ypos		= 0

		self.blinkOn 	= False

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(self.colour)
		self.image.set_colorkey(self.colour)

		self.rect = self.image.get_rect()

	def update(self, widthOffset, heightOffset, screen, screenDimensions):


		self.xpos = widthOffset
		self.ypos = heightOffset

		if (self.blinkOn):
			self.colour = BLUE
		else:
			self.colour = ttype.get_type_colour(self.tileType)


		if ((0 - self.width <= self.xpos <= screenDimensions["width"] + self.width) and (0 - self.height <= self.ypos <= screenDimensions["height"] + self.height )):

			pygame.draw.rect(screen, self.colour, [widthOffset, heightOffset, self.width-1, self.height-1])
			self.debugRender = 1
			
		else:
			self.debugRender = 0

	def change_type(self, tileType):

		self.tileType = tileType

class tile_field(object):

	def __init__(self, screen, fieldWidth, fieldHeight, tileWidth=10, tileHeight=10):

		self.entityTable 	= []
		self.screen			= screen
		self.fieldWidth 	= fieldWidth
		self.fieldHeight 	= fieldHeight
		self.tileWidth 		= tileWidth
		self.tileHeight 	= tileHeight
		self.selectedTile 	= None
		self.blinkDel 		= 0
		self.renderCount 	= 0

		counterID = 0

		for heightPoint in range(self.fieldHeight):
			for widthPoint in range(self.fieldWidth):
				self.entityTable.append(tile_entity(counterID, self.tileWidth, self.tileHeight))
				counterID += 1



	def id_at_pos(self, pos):

		for entity in self.entityTable:

			if (entity.xpos <= pos[0] <= (entity.xpos + entity.width)):
				if (entity.ypos <= pos[1] <= (entity.ypos + entity.height)):
					print ("ID: {3} xPos: {0} eWidth: {1} mPos: {2}".format(entity.xpos, entity.width, pos[0], entity.ID))
					print ("ID: {3} yPos: {0} eHeight: {1} mPos: {2}".format(entity.ypos, entity.height, pos[1], entity.ID))
					return entity.ID
					break

	def get_entity_from_id(self, ID):

		for entity in self.entityTable:
			if(entity.ID == ID):
				return entity
				break

	def draw(self, screenOffsetX, screenOffsetY, screenDimensions):

		widthOffset 	= 0 -screenOffsetX
		heightOffset 	= 0 -screenOffsetY
		flip 			= False
		counter 		= 0
		self.renderCount = 0

		if (not self.selectedTile is None):
			if(self.blinkDel >= 60):
				self.selectedTile.blinkOn = not self.selectedTile.blinkOn
				self.blinkDel = 0

		self.blinkDel += 1 

		for entity in self.entityTable:

			if (not (entity is self.selectedTile)):
				entity.blinkOn = False

			
			entity.update(widthOffset, heightOffset, self.screen, screenDimensions)

			self.renderCount += entity.debugRender

			#Counters and offset updates
			widthOffset += self.tileWidth
			counter += 1

			if (counter == self.fieldWidth):

				flip = not flip

				heightOffset  += self.tileHeight
				widthOffset = 0 -screenOffsetX
				counter = 0
		
