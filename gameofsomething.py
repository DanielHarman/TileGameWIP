import pygame, math, sys, time, classes
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

dimensions = {"height"  :600, "width":700}
 
#Pygame setup and pygame variables
pygame.mixer.pre_init(16000, -16, 1, 512) #For setting up the sound mixer so it works properly with the sounds
pygame.init() #Start pygame

pygame.display.set_caption("IDK right now") #Set the title

size = (dimensions["width"],dimensions["height"])
screen = pygame.display.set_mode(size) #Create the screen
fonts = pygame.font.SysFont("helvetica", 30)

clock = pygame.time.Clock()
pygame.key.set_repeat(2,2)

start_time = time.clock()

playField = classes.tile_field(screen, 32, 32, 30,30)


done = False
while not done:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			done = True

		if event.type == pygame.MOUSEBUTTONDOWN:

			returnID = playField.id_at_pos(pygame.mouse.get_pos())
			clickedEntity = playField.get_entity_from_id(returnID)
			playField.selectedTile = clickedEntity 
			pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}".format(pygame.mouse.get_pos(), playField.selectedTile.ID, len(playField.entityTable)))

		if event.type == pygame.MOUSEMOTION:
			if (playField.selectedTile is None):
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}".format(pygame.mouse.get_pos(), "None", len(playField.entityTable)))
			else:
				pygame.display.set_caption("IDK right now {0}, Selected Tile: {1}, Tile no: {2}".format(pygame.mouse.get_pos(), playField.selectedTile.ID, len(playField.entityTable)))

	screen.fill(BLACK)

	playField.draw()
	pygame.display.flip() #Update the screen
	clock.tick(60) #Set refresh rate

pygame.quit()