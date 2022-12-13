import pygame
from back_ground import BackGroundScene

pygame.init()
X = 1422
Y = 744

scene = BackGroundScene(d_width=711, d_height=372, scale=2)
scrn = scene.screen
fpsClock = pygame.time.Clock()
tick_count = 30
pygame.display.set_caption('image')

car = pygame.image.load("assets/trolley_car.png").convert()

car_x, car_y = (0, 0,)
scrn.blit(car, (14,208,))

pygame.display.flip()
status = True

while status:
    # make the empty canvas
    scene.blank()

    # diplay the current place of the car
    scrn.blit(car,(car_x, car_y,))

    # Treat inputs
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            status = False
    
    # Move the position of the car
    target = (484, 266,)
    time_seconds = 5

    car_x += 10

    
    pygame.display.update()
    fpsClock.tick(tick_count)

pygame.quit()
