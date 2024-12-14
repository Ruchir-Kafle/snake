import pygame
from sys import exit
import copy
import math
import random


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption("Snake")       

        self.clock = pygame.time.Clock()

        # Tile settings
        # Tiles
        self.tiles = 15
        # Getting the middle tile of the board so that the snake can be placed there
        self.middle_tile = math.floor(self.tiles / 2)
        # Taking the board pixel size and dividing it by how many tiles for size of each tile
        self.tile_size = 800 / self.tiles

        # Creating board lists
        self.board = []
        self.new_board = []

        # Creating the actual board using tile settings
        # First for loop makes the rows
        # Second for loop makes columns
        for _ in range(0, self.tiles):
            new_list = []

            for _ in range(0, self.tiles):
                new_list.append(0)
            
            self.board.append(new_list)
            self.new_board.append(new_list)

        # Making the middle tile of the board the snake
        self.board[self.middle_tile][self.middle_tile] = 1
        self.new_board[self.middle_tile][self.middle_tile] = 1
        
        # Default velocity
        self.velocity = [0,0]

        # Last snake block
        self.last = 1
        
        # Creating food on game start
        self.food()

    def user_input(self):
        # User inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Setting constant velocity depending on what key the user presses
                if event.key == pygame.K_w:
                    if self.velocity != [0, 1]:
                        self.velocity = [0, -1]
                    
                elif event.key == pygame.K_a:
                    if self.velocity != [1, 0]:
                        self.velocity = [-1, 0]

                elif event.key == pygame.K_s:
                    if self.velocity != [0, -1]:
                        self.velocity = [0, 1]

                elif event.key == pygame.K_d:
                    if self.velocity != [-1, 0]:
                        self.velocity = [1, 0]

    def food(self):
        # Getting a random y and x for the food
        random_y = random.randint(0, self.tiles - 1)
        random_x = random.randint(0, self.tiles - 1)

        # If random_y and random_x correspond to a non-empty tile, re-run
        # Else make the tile a food tile
        if self.board[random_y][random_x] != 0:
            self.food()
        else:
            self.board[random_y][random_x] = "food"

    def locate(self, tile_number):
        for i, row in enumerate(self.new_board):
            for j, tile in enumerate(row):
                if tile_number:
                    if tile == tile_number:
                        return [i, j]
                    
    def print_board(self, board):
        for i in board:
            for j in i:
                if j == "food":
                    print("f", end=" ")
                elif j == 0:
                    print("-", end=" ")
                else:
                    print(j, end=" ")
            
            print("")
        
        print("\n")

    def movement(self, velocity, tile_number):
        # First for loop gets each row in the board and the index of the row
        # Second for loop gets each individual tile in the board and it's index
        # We loop through self.new_board so that we can change all the values one at a time while not disrupting
        # original values.
        for i, row in enumerate(self.new_board):
            for j, tile in enumerate(row):
                # If tile is the head of the snake and the next tile is within board limits,
                # Increment position by velocity
                if tile == tile_number:
                    if tile_number == 1:
                        if (i + velocity[1] < self.tiles and i + velocity[1] > -1):
                            if (j + velocity[0] < self.tiles and j + velocity[0] > -1):
                                
                                if self.board[i+velocity[1]][j+velocity[0]] == "food":
                                    y, x = self.locate(self.last)

                                    if self.last == 1:
                                        y_increment = velocity[1] * -1
                                        x_increment = velocity[0] * -1
                                    else:
                                        previous_y, previous_x = self.locate(self.last - 1)
                                        
                                        y_increment = y - previous_y
                                        x_increment = x - previous_x

                                    self.last += 1
                                    self.board[y + y_increment][x + x_increment] = self.last
                                    self.food()

                                    print(self.board)
                                    # self.print_board(self.board)

                                    self.new_board = copy.deepcopy(self.board)

                                self.board[i][j] = 0
                                self.board[i+velocity[1]][j+velocity[0]] = 1

                                self.movement([0,0], 2)
                                self.new_board = copy.deepcopy(self.board)
                    else:
                        y, x = self.locate(tile - 1)
                        self.board[y][x] = tile
                        self.board[i][j] = 0

                        self.movement([0,0], tile+1)

    def loop(self):
        while True:
            # Checking for user input
            self.user_input()

            # Moving the snake
            self.movement(self.velocity, 1)
            
            # Getting every tile in the board
            for i, row in enumerate(self.board):
                for j, tile in enumerate(row):
                    # Making the tile and it's rectangle
                    tile_surf = pygame.Surface((self.tile_size, self.tile_size))
                    tile_rect = tile_surf.get_rect(topleft=((j*self.tile_size),(i*self.tile_size)))

                    # Checking the tile type and coloring based on the tile it is
                    if tile == 0:
                        if (i + j) % 2 == 0:
                            tile_surf.fill((68, 65, 190))
                        else:
                            tile_surf.fill((70, 152, 185))
                    elif tile == "food":
                        tile_surf.fill((255,0,0))
                    else:
                        tile_surf.fill((0,200,0))

                    # Drawing the tile to the screen using its respective rectangle
                    self.screen.blit(tile_surf, tile_rect)

            # Updating the display
            self.update()

    def update(self):
        # Simply updating the display
        pygame.display.update()
        self.clock.tick(10)

# This if statement will fire if the name of the file is main
if __name__ == "__main__":
    # Making a Game object so that we can start the game
    start_game = Game()
    start_game.loop()