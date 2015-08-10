import pygame, math, sys, time, classes
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

dimensions 		= {"height"  :720, "width":1280}

tileWidth 		= 20 #px
tileHeight 		= tileWidth #for now

fieldWidth  	= 64 #tiles
fieldheight 	= fieldWidth #For now too

#Variables for screen scrolling 
screenOffsetX	= 0
screenOffsetY 	= 0
scrollSpeed 	= 10
scrollArea		= 15
scrollBoundary  = 75

done 			= False
rMouseHeld		= False
actorSelected 	= False

sBoxStartPos 	= (0,0)
sBoxEndPos		= (0,0)
 
#Pygame setup and pygame variables
pygame.mixer.pre_init(16000, -16, 1, 512) #For setting up the sound mixer so it works properly with the sounds
pygame.init() #Start pygame

size = (dimensions["width"],dimensions["height"])
screen = pygame.display.set_mode(size) #Create the screen
fonts = pygame.font.SysFont("helvetica", 30)

clock = pygame.time.Clock()
pygame.key.set_repeat(2,2)

#startTime = time.clock()

actors = pygame.sprite.Group() #Act like 

playField = classes.tile_field(screen, fieldWidth,  fieldheight, tileWidth, tileHeight)

for x in range(10):
	testSol = classes.soldier(x*10,10)
	testEngi = classes.engineer(x*10, 50)
	actors.add(testSol)
	actors.add(testEngi)

#Main game loop
while not done:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			done = True

		if event.type == pygame.MOUSEBUTTONDOWN:

			if (event.button == 1):

				if (actorSelected is True and rMouseHeld is False):
					for actor in actors:
						if (actor.selected is True):
							actor.add_destination(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],screenOffsetX, screenOffsetY) #Add destination can work for building for waypoints

				if (rMouseHeld is False):
					sBoxStartPos = pygame.mouse.get_pos()
				
				rMouseHeld = True

				for actor in actors:
					if ((actor.xPos - screenOffsetX <= pygame.mouse.get_pos()[0] <= (actor.xPos - screenOffsetX + actor.spriteSize[0] )) and (actor.yPos - screenOffsetY <= pygame.mouse.get_pos()[1] <= (actor.yPos -screenOffsetY + actor.spriteSize[1]))):
						actor.selected = True
						actorSelected = True
						print ("Selected: " + str(actor))

					elif ((sBoxStartPos[0] <= actor.xPos - screenOffsetX <= sBoxEndPos[0])):
						actor.selected = True
						actorSelected = True
						print ("Selected: " + str(actor))

			elif (event.button == 3):
				for actor in actors:
					actor.selected = False
				actorSelected = False

			#returnID = playField.id_at_pos(pygame.mouse.get_pos())
			#clickedEntity = playField.get_entity_from_id(returnID)
			#playField.selectedTile = clickedEntity 

			if (playField.selectedTile is None):
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}, Rend:{3}".format(pygame.mouse.get_pos(), "None", len(playField.entityTable), playField.renderCount))
			else:
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}, Rend: {3}".format(pygame.mouse.get_pos(), playField.selectedTile.ID, len(playField.entityTable), playField.renderCount))

		if (event.type == pygame.MOUSEBUTTONUP):
			if (event.button == 1):
				rMouseHeld = False

		if event.type == pygame.MOUSEMOTION:
			if (playField.selectedTile is None):
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}, Rend:{3}".format(pygame.mouse.get_pos(), "None", len(playField.entityTable), playField.renderCount))
			else:
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}, Rend: {3}".format(pygame.mouse.get_pos(), playField.selectedTile.ID, len(playField.entityTable), playField.renderCount))

	if (rMouseHeld is True):
		sBoxEndPos = pygame.mouse.get_pos()
	#Window scrollin

	if ((0 <= pygame.mouse.get_pos()[0] <= scrollArea) and not (screenOffsetX < -scrollBoundary)):
		screenOffsetX -= scrollSpeed

	if ((0 <= pygame.mouse.get_pos()[1] <= scrollArea) and not (screenOffsetY < -scrollBoundary)):
		screenOffsetY -= scrollSpeed

	if ((dimensions["width"] - scrollArea <= pygame.mouse.get_pos()[0] <= dimensions["width"]) and not ((screenOffsetX + dimensions["width"]) > ((tileWidth)*fieldWidth) + scrollBoundary)):
		screenOffsetX += scrollSpeed

	if ((dimensions["height"] - scrollArea <= pygame.mouse.get_pos()[1] <= dimensions["height"]) and not ((screenOffsetY + dimensions["height"]) > ((tileHeight)*fieldheight) + scrollBoundary)):
		screenOffsetY += scrollSpeed

	screen.fill(BLACK)

	playField.draw(screenOffsetX, screenOffsetY, dimensions)
	actors.update(screenOffsetX,screenOffsetY)
	actors.draw(screen)
	
	if(rMouseHeld is True):
		
		pygame.draw.rect(screen, WHITE, [sBoxStartPos[0],sBoxStartPos[1],sBoxEndPos[0]-sBoxStartPos[0],sBoxEndPos[1]-sBoxStartPos[1]], 1)

	pygame.display.flip() #Update the screen
	clock.tick(60) #Set refresh rate

pygame.quit()