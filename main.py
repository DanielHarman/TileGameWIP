import pygame, math, sys, time, classes
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

dimensions = {"height"  :720, "width":1280}
 
#Pygame setup and pygame variables
pygame.mixer.pre_init(16000, -16, 1, 512) #For setting up the sound mixer so it works properly with the sounds
pygame.init() #Start pygame

size = (dimensions["width"],dimensions["height"])
screen = pygame.display.set_mode(size) #Create the screen
fonts = pygame.font.SysFont("helvetica", 30)

clock = pygame.time.Clock()
pygame.key.set_repeat(2,2)

start_time = time.clock()

tileWidth 	= 20 #px
tileHeight 	= tileWidth #for now

fieldWidth  = 64 #tiles
fieldheight = fieldWidth #For now too

playField = classes.tile_field(screen, fieldWidth,  fieldheight, tileWidth, tileHeight)

#Variables for screen scrolling 
screenOffsetX	= 0
screenOffsetY 	= 0
scrollSpeed 	= 10
scrollArea		= 15
scrollBoundary  = 75

done = False

while not done:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			done = True

		if event.type == pygame.MOUSEBUTTONDOWN:

			returnID = playField.id_at_pos(pygame.mouse.get_pos())
			clickedEntity = playField.get_entity_from_id(returnID)
			playField.selectedTile = clickedEntity 

			if (playField.selectedTile is None):
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}, Rend:{3}".format(pygame.mouse.get_pos(), "None", len(playField.entityTable), playField.renderCount))
			else:
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}, Rend: {3}".format(pygame.mouse.get_pos(), playField.selectedTile.ID, len(playField.entityTable), playField.renderCount))

		if event.type == pygame.MOUSEMOTION:
			if (playField.selectedTile is None):
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}, Rend:{3}".format(pygame.mouse.get_pos(), "None", len(playField.entityTable), playField.renderCount))
			else:
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}, Rend: {3}".format(pygame.mouse.get_pos(), playField.selectedTile.ID, len(playField.entityTable), playField.renderCount))

	#Window scrolling

	if ((0 <= pygame.mouse.get_pos()[0] <= scrollArea) and not (screenOffsetX < -scrollBoundary)):
		screenOffsetX -= scrollSpeed

	if ((0 <= pygame.mouse.get_pos()[1] <= scrollArea) and not (screenOffsetY < -scrollBoundary)):
		screenOffsetY -= scrollSpeed

	print (((tileWidth-1)*fieldWidth + scrollBoundary) )
	print ("//")
	print (screenOffsetX + dimensions["width"])

	if ((dimensions["width"] - scrollArea <= pygame.mouse.get_pos()[0] <= dimensions["width"]) and not ((screenOffsetX + dimensions["width"]) > ((tileWidth)*fieldWidth) + scrollBoundary)):
		screenOffsetX += scrollSpeed

	if ((dimensions["height"] - scrollArea <= pygame.mouse.get_pos()[1] <= dimensions["height"]) and not ((screenOffsetY + dimensions["height"]) > ((tileHeight)*fieldheight) + scrollBoundary)):
		screenOffsetY += scrollSpeed

	screen.fill(BLACK)

	playField.draw(screenOffsetX, screenOffsetY, dimensions)

	pygame.display.flip() #Update the screen
	clock.tick(60) #Set refresh rate

pygame.quit()