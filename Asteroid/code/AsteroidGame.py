import pygame, sys
from pygame.locals import QUIT
from random import randint, uniform

#Global Setup
pygame.init()
WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroid Shooter')
pygame.mouse.set_visible(False)

#Function
def laser_update(laser_list, lspeed):
    for rect in laser_list:
        rect.y -= lspeed;
        if rect.bottom < 0:
            laser_list.remove(rect)

def asteroid_update(asteroid_list, speed = 2):
    for asteroid_tuple in asteroid_list:
        direction = asteroid_tuple[1]
        asteroid_rect = asteroid_tuple[0]
        asteroid_rect.center += direction * speed
        if asteroid_rect.top > WINDOW_HEIGHT:
            asteroid_list.remove(asteroid_tuple)


#Ship
ship_surf = pygame.image.load('../sprites/Ship.png')
ship_surf_scaled = pygame.transform.scale(ship_surf,(64,64))
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

#BG
bg_surf = pygame.image.load("../sprites/Stage.jpg")

#Laser
laser_surf = pygame.image.load('../sprites/betalaser.png')
laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
laser_list = []
lspeed = 10

#Asteroid
asteroid_surf = pygame.image.load('../sprites/asteroid.png')
asteroid_list = []

asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 250) #Spawn Rate

clock = pygame.time.Clock()

#Declare Variables

#Game Loop
while True:
    #Close Game Event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #print("Laser!")
                laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
                laser_list.append(laser_rect)
                print(laser_list)
                
        if event.type == asteroid_timer:
            #Logic for asteroid, appens to list
            pos_x = randint(-100, WINDOW_WIDTH+100)
            pos_y = randint(-120, -70)
            asteroid_rect = asteroid_surf.get_rect(center = (pos_x,pos_y))
            direction = pygame.math.Vector2(uniform(-0.5,1),1)
            asteroid_list.append((asteroid_rect,direction))
            
    clock.tick(200)
            
    #Section 1 - Sprites & Surfaces
            #Background, Player, Incoming Objects, Projectiles, Text
    display_surface.fill((0,0,0))
    display_surface.blit(bg_surf,(0,0))
    display_surface.blit(ship_surf_scaled,ship_rect)
            
    #Section 2 - Controls & Inputs
                    #Movement (Mouse), Projectiles (Buttons)
    ship_rect.center = pygame.mouse.get_pos()
            
    #Section 3 - Game Logic, Interactions & Updates
                    #Mandatory: Movement Code For Player, List of Enemies, Iteration, Collisions
                    #Extra: Score, Lives, Splitting?, Audio
    
    laser_update(laser_list, lspeed)
    
    #Collision
    for asteroid_tuple in asteroid_list:
        asteroid_rect = asteroid_tuple[0]
        if ship_rect.colliderect(asteroid_rect):
            pygame.quit()
            sys.exit()
    
    #Laser Collission
    for asteroid_tuple in asteroid_list:
        for laser in laser_list:
            if asteroid_tuple[0].colliderect(laser_rect):
                asteroid_list.remove(asteroid_tuple)
                laser_list.remove(laser_rect)
    
    for rect in laser_list:
        display_surface.blit(laser_surf,rect)
    
    asteroid_update(asteroid_list)
    for asteroid_tuple in asteroid_list:
        display_surface.blit(asteroid_surf, asteroid_tuple[0])
    
        

    #Final Visual Update For User
    pygame.display.update()