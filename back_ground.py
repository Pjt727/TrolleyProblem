import pygame

class BackGroundScene:
    '''Creates the screen of the game and hold some background assets'''
    def __init__(self, d_width: int, d_height: int, scale: float = 1, background_path= "assets/background.png") -> None:
        self.width = d_width * scale
        self.height = d_height * scale
        self.scale = scale
        self.screen = pygame.display.set_mode((self.width, self.height,))
        self.background_path = background_path
        
        self.background_img = pygame.image.load(background_path).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height,))
    
    def blank(self) -> None:
        self.screen.blit(self.background_img, (0,0,))
