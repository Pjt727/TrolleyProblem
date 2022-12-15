from random import shuffle
import pygame

class Person:
    def __init__(self, first_name, last_name, base_path) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.image_path = base_path + last_name + "_" + first_name + ".png"
        self.face = pygame.image.load(self.image_path).convert_alpha()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class People:
    '''Reading people in and getting their picture'''
    def __init__(self,
                people_name_path=".venv/people_info/names.txt",
                people_img_base_path=".venv/people_info/") -> None:
        
        self.people_name_path = people_name_path
        self.people_img_base_path = people_img_base_path
        self.people: list[Person] = []
        with open(self.people_name_path, 'r') as f:
            for line in f.readlines():
                line = line[:-1]
                last_name, first_name = line.split('_')
                self.people.append(Person(first_name=first_name, last_name=last_name, base_path=self.people_img_base_path))
            
    def get_n_people(self, n: int, blacklisted: Person) -> list[Person]:
        ppl = self.people.copy()
        ppl.remove(blacklisted)
        shuffle(ppl)
        return ppl[:n]
