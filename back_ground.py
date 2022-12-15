import pygame
from trolley_car import TargetPoint, TrolleyCar
from people import People, Person
import math

class BackGroundScene:
    '''Creates the screen of the game and hold some background assets'''
    def __init__(self, d_width: int, d_height: int, scale: float = 1,
                car = None, people = None,
                background_path_switched="assets/background_switched.png",
                background_path_not_switched="assets/background_not_switched.png",
                blood_path="assets/blood.png",
                x_path="assets/x.png",
                tick_count=30) -> None:
        self.blood_path = blood_path
        self.width = round(d_width * scale)
        self.height = round(d_height * scale)
        self.scale = scale
        self.screen = pygame.display.set_mode((self.width, self.height,))
        
        self.background_img_switched = pygame.image.load(background_path_switched).convert()
        self.background_img_switched = pygame.transform.scale(self.background_img_switched, (self.width, self.height,))
        self.background_img_not_switched = pygame.image.load(background_path_not_switched).convert()
        self.background_img_not_switched = pygame.transform.scale(self.background_img_not_switched, (self.width, self.height,))
        self.x_img = pygame.image.load(x_path).convert_alpha()
        self.is_switched: bool = False
        self.is_switch_locked: bool = False
        self.switch_operator: Person = None
        self.car: TrolleyCar = car

        self.tick_count = tick_count

        # Hard coding some of the importing postions of image
        self.trolley_start: tuple[int, int] = (13*scale, 80*scale)
        self.trolley_descion_x: int = 250*scale
        '''The point at which the trolley will check the lever'''

        self.trolley_intersection: TargetPoint = TargetPoint(x=255*scale, y=105*scale, time_seconds=5)
        self.trolley_path_switched: list[TargetPoint] = [TargetPoint(x=340*scale, y=75*scale, time_seconds=2), TargetPoint(x=600*scale, y=110*scale, time_seconds=4) ]
        self.trolley_path_not_switched: list[TargetPoint] = [TargetPoint(x=610*scale, y=240*scale, time_seconds=6)]

        self.people: People = people
        


    def show(self) -> None:
        if self.switch_operator:
            if self.car.x >= self.scale*595:
                self.ending()
                return
            self.blank()
            self.car.tick()
        else:
            self.switch_selection()

    def blank(self) -> None:
        face = self.switch_operator.face
        face = pygame.transform.scale(face, (40*self.scale, 40*self.scale,))

        if self.is_switched:
            self.screen.blit(self.background_img_switched, (0,0,))
            self.screen.blit(face, (325*self.scale, 30*self.scale,))
        else:
            self.screen.blit(self.background_img_not_switched, (0,0,))
            self.screen.blit(face, (350*self.scale, 33*self.scale,))
            

        for pos, face, in zip(self.head_positions, self.people_faces):
            self.screen.blit(face, pos)
    
    def switch_selection(self, max_cols=8, d_padding=25) -> None:
        self.screen.fill((255,255,255,))
        padding = d_padding * self.scale
        people = self.people.people
        face_x = 58 * self.scale
        face_y = 66 * self.scale
        running_x = padding
        running_y = padding
        
        self.people_position = []

        i = 0
        while i < len(people):
            face = people[i].face
            face = pygame.transform.scale(face, (face_x, face_y,))
            self.screen.blit(face, (running_x, running_y,))
            
            self.people_position.append(
                ((((running_x), running_y,), (running_x + face_x, running_y + face_y)),
                people[i],)
                )
            
            # check if next row
            if (i + 1) % max_cols == 0:
                # change pos to start of next row
                running_x = padding
                running_y += + face_y + padding
                i += 1
                continue
            # not next row so next col
            running_x += face_x + padding
            i += 1
    
    def check_selection(self, pos):
        if self.switch_operator:
            return

        x, y = pos
        for person_position in self.people_position:
            boundaries, person = person_position
            upper_left, lower_right = boundaries
            if x in range(round(upper_left[0]), round(lower_right[0])) and y in range(round(upper_left[1]), round(lower_right[1])):
                self.switch_operator = person
                self.generate_people_on_tracks()
                return

    def generate_people_on_tracks(self):
        # Getting 6 random people to be on the track
        ## must remove the switch person
        scale = self.scale
        
        self.head_positions = [
                    (477*scale, 197*scale,), # bottom 1
                    (492*scale, 205*scale,), # bottom 2
                    (508*scale, 211*scale,), # bottom 3
                    (528*scale, 214*scale,), # bottom 4
                    (543*scale, 222*scale,), # bottom 5
                    (525*scale, 103*scale,) # top 1
        ]
        self.blood_image = pygame.image.load(self.blood_path).convert_alpha()
        self.blood_image = pygame.transform.scale(self.blood_image, (135*scale, 81*scale,))
        self.blood_positions_not_switched = [
                    (417*scale, 207*scale,), # bottom 1
                    (432*scale, 225*scale,), # bottom 2
                    (448*scale, 231*scale,), # bottom 3
                    (468*scale, 234*scale,), # bottom 4
                    (483*scale, 242*scale,), # bottom 5
        ]
        self.blood_positions_switched = [
            (465*scale, 103*scale,) # top 1
        ]

        self.person_path_switched: Person=  None
        self.people_path_not_switched: list[Person] = []
        self.people_faces = []
        for counter, person in enumerate(self.people.get_n_people(len(self.head_positions), self.switch_operator)):
            face = person.face
            face = pygame.transform.scale(face, (30*scale, 30*scale,))
            face = pygame.transform.rotate(face, 330)
            self.people_faces.append(face)

            
            if counter == len(self.head_positions)-1:
                self.person_path_switched = person
            else:
                self.people_path_not_switched.append(person) 


    def ending(self, d_padding=50):
        padding = d_padding * self.scale
        self.screen.fill((255,255,255,))
        # 254, 290
        # 127, 145

        face_x = 89*self.scale
        face_y = 102*self.scale
        self.x_img = pygame.transform.scale(self.x_img, (face_x + 5, face_y + 5,))

        font = pygame.font.Font('freesansbold.ttf', 20)
        
        # Display switched person
        switched_face = self.person_path_switched.face
        switched_face = pygame.transform.scale(switched_face, (face_x, face_y,))
        self.screen.blit(switched_face, ((self.width - face_x)//2, padding*.5,))

        switched_text = font.render(f'{self.person_path_switched.first_name} {self.person_path_switched.last_name}', True, (0,0,0,), (255, 255, 255,))
        switched_rect = switched_text.get_rect()
        switched_rect.center = (self.width // 2, padding*.5 + face_y,)
        self.screen.blit(switched_text, switched_rect)
        ## putting an x on them if they were killed
        if self.is_switched:
            self.screen.blit(self.x_img, ((self.width - face_x)//2, padding*.5,))


        # Displaying the unswitched path
        running_x = padding*.8
        y_not_switched = padding*1.5 + face_y
        for person in self.people_path_not_switched:
            person_face = person.face
            person_face = pygame.transform.scale(person_face, (face_x, face_y,))
            self.screen.blit(person_face, (running_x, y_not_switched))

            person_text = font.render(f'{person.first_name} {person.last_name}', True, (0,0,0,), (255, 255, 255,))
            person_rect = person_text.get_rect()
            person_rect.center = (running_x + (face_x//2), y_not_switched + face_y,)
            self.screen.blit(person_text, person_rect)
            
            ## putting an x on them if they were killed
            if not self.is_switched:
                self.screen.blit(self.x_img, (running_x, y_not_switched,))

            running_x += padding + face_x
