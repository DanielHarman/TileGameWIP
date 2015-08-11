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
unitFont = pygame.font.SysFont("ariel", 15)

clock = pygame.time.Clock()
pygame.key.set_repeat(2,2)

#startTime = time.clock()

actors = pygame.sprite.Group() #Act like 

playField = classes.tile_field(screen, fieldWidth,  fieldheight, tileWidth, tileHeight)

for x in range(10):
	testSol = classes.soldier(x*30,10,unitFont)
	testEngi = classes.engineer(x*10, 50,unitFont)
	actors.add(testSol)
	actors.add(testEngi)

#Main game loop
while not done:

	mousePosByOffset = (pygame.mouse.get_pos()[0] + screenOffsetX, pygame.mouse.get_pos()[1] + screenOffsetY)

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			done = True

		if event.type == pygame.MOUSEBUTTONDOWN:

			rMouseHeld = False

			if (event.button == 1): #Left click down
				rMouseHeld = True
				sBoxStartPos = mousePosByOffset

				if (actorSelected is True):
					actorSelected = False
					for actor in actors:
						actor.selected = False
						print ("Actor deselected")

			if (event.button == 3): #Right click down
				pass

		if (event.type == pygame.MOUSEBUTTONUP):
			if (event.button == 1): #Left click up

				#if (actorSelected is True):
				#	actorSelected = False
				#	for actor in actors:
				#		actor.selected = False

				if (rMouseHeld is True):

					for actor in actors:

						if (sBoxStartPos[0] -10 <= actor.xPos <= sBoxEndPos[0] + 10):
							actor.selected = True
							actorSelected = True
							print ("Actor selected")

				rMouseHeld = False

			if (event.button == 3):
				for actor in actors:
					if (actor.selected is True or actor.moving is True):
						actor.add_destination(mousePosByOffset[0],mousePosByOffset[1])


		if event.type == pygame.MOUSEMOTION:
			pygame.display.set_caption("RTS WIP Mouse: {0}, Offset Mouse: {1}, OffsetX: {2}, OffsetY: {3}".format(pygame.mouse.get_pos(),mousePosByOffset,screenOffsetX,screenOffsetY))

	#Window scrollin

	if (rMouseHeld):
		sBoxEndPos = mousePosByOffset

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
	actors.update(screenOffsetX,screenOffsetY,screen)
	actors.draw(screen)
	
	if(rMouseHeld is True):
		
		pygame.draw.rect(screen, WHITE, [sBoxStartPos[0]-screenOffsetX,sBoxStartPos[1]-screenOffsetY,sBoxEndPos[0]-sBoxStartPos[0],sBoxEndPos[1]-sBoxStartPos[1]], 1)

	pygame.display.flip() #Update the screen
	clock.tick(60) #Set refresh rate

pygame.quit()