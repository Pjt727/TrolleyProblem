import pygame
from back_ground import BackGroundScene
from trolley_car import TrolleyCar
from people import People

pygame.init()
X = 1422
Y = 744
pygame.display.set_mode((X, Y,))
people = People()
scene = BackGroundScene(d_width=711, d_height=372, scale=2, people=people)
scrn = scene.screen
fpsClock = pygame.time.Clock()
tick_count = 30
pygame.display.set_caption('image')

car: TrolleyCar = TrolleyCar(scene=scene)
scene.car = car
pygame.display.flip()
status = True

while status:
    # make the empty canvas
    scene.show()

    # Treat inputs
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            status = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                scene = BackGroundScene(d_width=711, d_height=372, scale=2, people=people)
                car: TrolleyCar = TrolleyCar(scene=scene)
                scene.car = car
                continue
            if e.key == pygame.K_s:
                if not scene.is_switch_locked:
                    scene.is_switched = not scene.is_switched
                continue
            if not car.target_queue: # if at start then add target to the intersection
                s_x, s_y = scene.trolley_start
                if car.x == s_x and car.y == s_y:
                    car.add_target(scene.trolley_intersection)
        if e.type == pygame.MOUSEBUTTONDOWN:
            scene.check_selection(pygame.mouse.get_pos())


    
    pygame.display.update()
    fpsClock.tick(tick_count)

pygame.quit()
