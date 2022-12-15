from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from back_ground import BackGroundScene
import pygame

class TrolleyCar:
    '''Car stuff'''
    def __init__(self, scene: BackGroundScene, car_path="assets/trolley_car.png") -> None:
        self.scene = scene
        self.x, self.y = scene.trolley_start
        self.image = pygame.image.load(car_path).convert()

        self.target_queue : list[TargetPoint] = []


    def tick(self) -> None:
        # adding blood
        self.add_blood()

        self.scene.screen.blit(self.image, (self.x, self.y,))

        # check to see the car has passed the the intersection
        if self.x >= self.scene.trolley_descion_x - 3:
            if not self.scene.is_switch_locked:
                self.scene.is_switch_locked = True
                if self.scene.is_switched:
                    tars = self.scene.trolley_path_switched
                else:
                    tars = self.scene.trolley_path_not_switched
                for tar in tars:
                    self.add_target(tar)
        

        if not self.target_queue: # no targets in queue list
            return
        
        # Iterate based off of the the first target in queue
        current_target = self.target_queue[0]
        if self.is_close_to(tar_x=current_target.x, tar_y=current_target.y):
            self.target_queue.remove(current_target)
        
        x_iter, y_iter = current_target.iters
        self.x += x_iter
        self.y += y_iter

    def add_target(self, target: TargetPoint) -> None:
        start_x = self.x
        start_y = self.y
        if self.target_queue: # start x will be at the last target
            last_target = self.target_queue[-1]
            start_x = last_target.x
            start_y = last_target.y
        
        target.iters: tuple[int, int] = self.iters(start_x, start_y, target)
        self.target_queue.append(target)

    def add_blood(self) -> None:
        if not self.scene.is_switch_locked:
            return
        
        blood_to_add = None
        if self.scene.is_switched:
            blood_to_add = self.scene.blood_positions_switched
        else:
            blood_to_add = self.scene.blood_positions_not_switched
        
        for blood_pos in blood_to_add:
            blood_x, blood_y = blood_pos
            if self.x < blood_x:
                continue
            self.scene.screen.blit(self.scene.blood_image, blood_pos)



    def iters(self, start_x, start_y, target: TargetPoint) -> tuple[float, float]:

        tick = self.scene.tick_count
        x_iter = (target.x - start_x) / (target.time_seconds*tick)
        y_iter = (target.y - start_y) / (target.time_seconds*tick)
        return x_iter, y_iter

    def is_close_to(self, tar_x, tar_y, plus_or_minus=5) -> bool:
        return round(self.x) in range(tar_x-plus_or_minus, tar_x+plus_or_minus) \
            and round(self.y) in range(tar_y-plus_or_minus, tar_y+plus_or_minus)

class TargetPoint:
    def __init__(self, x: int, y: int, time_seconds: float = 5):
        self.x = x
        self.y = y
        self.time_seconds = time_seconds
        self.tick_counter = 0
        self.iters: tuple[int, int] = (0,0,)
    
    def __str__(self) -> str:
        return f"x: {self.x} | y: {self.y} | iters: {self.iters}"
