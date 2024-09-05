import numpy as np
import pygame
import time
import json
import os

import pygame.locals
import lib.config.default as config
class Player:
    def __init__(self) -> None:
        self.x = 385
        self.y = 285
        self.width = 30
        self.height = 30
        self.skin = pygame.image.load(os.path.join(config.PATH_ASSETS, "skin_1.png"))
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)
        self.jump_speed = 20
        self.jump_on: bool = False
    def jump(self) -> None:
        if not self.jump_on:
            self.jump_on = True
            self.body.y -= self.jump_speed
            self.jump_speed -= 1
            
        
    
        
class Game:
    def __init__(self, name: str = "basic", hard: int = 1, lenght: int = 40) -> None:
        self.name: str = name
        self.hard: int = hard
        self.lenght: int = lenght
        self.level_map = None
        self.left_wall = 0
        self.clock = pygame.time.Clock()
        self.bar_choise: int = 1
        self.bar_on: bool = True
        self.bar_lenght: int = 4
        self.editing_screen = pygame.display.set_mode((800, 600))
        self.player = Player()
        self.starting_pos = (0, 0)
        self.change_x = 0
        self.change_y = 0

        
    
    def make_map(self) -> None:
        self.level_map = np.zeros((20, self.lenght), dtype=int)
           
    def draw_screen(self) -> None:        
        self.editing_screen.fill((0, 0, 0))

        
    def editing_bar(self) -> None:
        if self.bar_on:
            pygame.draw.rect(self.editing_screen, (255, 0, 0), (0, 0, (34 * self.bar_lenght), 34))
            
        for i in range(self.bar_lenght):
            pygame.draw.rect(self.editing_screen, (255, 255, 255), ((32 * i + 2), 2, 30, 30))    
            self.editing_screen.blit(pygame.image.load(os.path.join(config.PATH_ASSETS, 'blocks', f'{i+1}.png')), ((32 * i + 2), 2, 30, 30))   

    def draw_blocks(self) -> None:
        
        for y in range(20):
            for x in range(self.lenght):
                if self.level_map[y][x] > 0:
                    pygame.draw.rect(self.editing_screen, (255, 255, 255), ((x - (self.left_wall / 30)) * 30, y * 30, 30, 30))
                    self.editing_screen.blit(pygame.image.load(os.path.join(config.PATH_ASSETS, "blocks", f"{self.level_map[y][x]}.png")), ((x - (self.left_wall / 30)) * 30, y * 30))
    
    
    def save_map(self) -> None:
        saving_pack = {
            "name": self.name,
            "hard": self.hard,
            "length": self.lenght,
            "level_map": self.level_map.tolist()
        }
        plik = "mapa.json"
        maps = []
        try:
            with open(plik, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
                maps = data
        except FileNotFoundError:
            data = []


        for i, map in enumerate(maps):
            if map["name"] == self.name:
                maps[i] = saving_pack  
                break
        else:
            maps.append(saving_pack)  

        with open(plik, 'w') as f:
            json.dump(maps, f)
            
            
    def editing_loop(self) -> None:
        while True:
            self.draw_screen()
            self.draw_blocks()
            self.editing_bar()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_map()
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = (pos[0] + self.left_wall) // 30, pos[1] // 30
                    self.level_map[y][x] = self.bar_choise

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.left_wall -= 30
                    elif event.key == pygame.K_RIGHT:
                        if 27 + (self.left_wall / 30) < self.lenght:
                            self.left_wall += 30
                    elif event.key == pygame.K_1:
                        self.bar_choise = 1
                    elif event.key == pygame.K_2:
                        self.bar_choise = 2
                    elif event.key == pygame.K_3:
                        self.bar_choise = 3
                    elif event.key == pygame.K_4:
                        self.bar_choise = 4

            self.clock.tick(60)
            pygame.display.flip()
            
        
    def return_maps(self) -> None:
        
        maps = []
        with open("mapa.json", "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                maps = data
            else:
                maps.append(data)

        for map_data in maps:
            name = map_data.get("name", "Unknown")
            hard = map_data.get("hard", "Unknown")
            length = map_data.get("length", "Unknown")
            print(f'''
                    > Name: {name}
                    > Hardness: {hard}
                    > Length: {length}
                    
                    ''')
            
    def map_taker(self, name) -> None:
        maps = []
        with open("mapa.json", "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                maps = data
            else:
                maps.append(data)
            
        for map in maps:
            if map["name"].lower() == name.lower():
                print("map loading...")
                time.sleep(0.3)
                print("loading name...")
                time.sleep(0.3)
                self.name = map["name"]
                print("loading hardnes...")
                time.sleep(0.2)
                self.hard = map["hard"]
                print("loading level...")
                time.sleep(1.1)
                self.level_map = np.array(map["level_map"])
                self.lenght = map["length"]
                print("level loaded...")                    
                break        
        
    def editing_menager(self) -> None:
        step_1 = input("open/create ")
        if step_1.lower() == "open":
            self.return_maps()
        if step_1.lower() == "create":
            name = input("name: ")
            hard = input("hard: ")
            lenght = input("lenght: ")
            self.name = name
            self.hard = int(hard)
            self.lenght = int(lenght)
            self.make_map()
            self.editing_loop()
        step_2 = input("chose map: ")
        self.map_taker(step_2)
        step_3 = input("play/edit ")
        if step_3.lower() == "edit":
            self.editing_loop()
        elif step_3.lower() == "play":
            self.find_start()
            self.loop()
            
    def find_start(self) -> None:
        for x in range(20):
            for y in range(self.lenght):
                if self.level_map[x][y] == 4:
                    self.starting_pos = (x, y)
                    
    def draw(self) -> None:
        for y in range(20):  
            for x in range(self.lenght): 
                if self.level_map[y][x] > 0:  
                    pygame.draw.rect(self.editing_screen, (255, 255, 255), (x*30, y*30, 30, 30))
                    self.editing_screen.blit(pygame.image.load(os.path.join(config.PATH_ASSETS, "blocks", f"{self.level_map[y][x]}.png")), (x*30, y*30))
                    
    def loop(self) -> None:
        while True:
            self.editing_screen.fill((0, 0, 0))
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            pygame.display.flip()
    

lvl = Game()
lvl.editing_menager()

                

                        
        
