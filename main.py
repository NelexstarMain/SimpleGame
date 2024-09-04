import numpy as np
import pygame
import time
import json

class Level:
    def __init__(self, name: str = "basic", hard: int = 1, lenght: int = 40) -> None:
        self.name: str = name
        self.hard: int = hard
        self.lenght: int = lenght
        self.level_map = np.zeros((20, self.lenght), dtype=np.uint8)
        self.left_wall = 0
        self.clock = pygame.time.Clock()
        self.bar_choise: int = 1
        self.bar_on: bool = True
        self.bar_lenght: int = 3
        self.editing_screen = None
        self.editing_screen_on = False

        
    def map_editing(self) -> None:
        
        def make_screen(self) -> None:
            self.editing_screen = pygame.display.set_mode((800, 600))
            self.editing_screen_on = True
            
        def draw_screen(self) -> None:
            if self.editing_screen_on == False:
                make_screen(self)
            
            self.editing_screen.fill((0, 0, 0))

            
        def editing_bar(self) -> None:
            if self.bar_on:
                pygame.draw.rect(self.editing_screen, (255, 0, 0), (0, 0, (34 * self.bar_lenght), 34))
                
            for i in range(self.bar_lenght):
                pygame.draw.rect(self.editing_screen, (255, 255, 255), ((32 * i + 2), 2, 30, 30))    
                self.editing_screen.blit(pygame.image.load(f"{i+1}.png"), ((32 * i + 2), 2, 30, 30))   

        def draw_blocks(self) -> None:
            
            for y in range(20):
                for x in range(self.lenght):
                    if self.level_map[y][x] > 0:
                        pygame.draw.rect(self.editing_screen, (255, 255, 255), ((x - (self.left_wall / 30)) * 30, y * 30, 30, 30))
                        self.editing_screen.blit(pygame.image.load(f"{self.level_map[y][x]}.png"), ((x - (self.left_wall / 30)) * 30, y * 30))
        
        
        def save_map(self) -> None:
            saving_pack = {
                "name": self.name,
                "hard": self.hard,
                "length": self.lenght,
                "level_map": self.level_map.tolist()
            }
            plik = "mapa.json"
            try:
                with open(plik, 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {}

            data.update(saving_pack)
            with open(plik, 'w') as f:
                json.dump(data, f)
            
                
                
        def editing_loop(self) -> None:
            while True:
                draw_screen(self)
                draw_blocks(self)
                editing_bar(self)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save_map(self)
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

                self.clock.tick(60)
                pygame.display.flip()
                
          
        def return_maps() -> None:
            
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
                
        def map_taker(name) -> None:
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
                    time.sleep(1.4)
                    self.level_map = np.array(map["level_map"])
                    self.lenght = map["length"]
                    print("level loaded...")                    
                    break        
            
        def editing_menager(self) -> None:
            step_1 = input("open/create ")
            if step_1.lower() == "open":
                return_maps()
            step_2 = input("chose map: ")
            map_taker(step_2)
            step_3 = input("play/edit ")
            if step_3.lower() == "edit":
                editing_loop(self)
                

        editing_menager(self)  
            
lvl = Level()
lvl.map_editing()

                

                        
        
