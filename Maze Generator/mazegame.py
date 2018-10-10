"""
Game by Joshua Chang and Animesh KC

Maze game
"""

import pygame
from pygame.locals import *
import time as t
from mazebuilder import *


class Background:
    """
    Background class for the maze
    - initialises a random array of arrays for use in constructing the maze
    - loads images for the walls and the finish block
    - opens the pygame window
    - builds the maze by placing pygame rects in the proper places
    - places the finish block at the bottom left corner of the maze

    The background window and block sizes are dynamic in that the dimensions of the pictures that are loaded for the
    blocks can be changed without breaking the code

    The player image should not be bigger than the blocks
    """
    def __init__(self, rows, columns):
        self.maze = Maze(rows, columns)

        # unrandomised test maze

        # self.b = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        #           [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        #           [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        #           [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        #           [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        #           [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        #           [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        #           [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        #           [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        #           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        #           [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        #           [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        #           [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        #           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.b = self.maze.random_maze

        # pre surface type setting
        self.bg_surf = pygame.display.set_mode((0, 0), pygame.HWSURFACE)

        # loading end image
        self.end = pygame.image.load("end.png").convert()
        # self.end_rect = self.end.get_rect()

        # loading block image and block rect
        self.block = pygame.image.load("block.png").convert()
        self.block_rect = self.block.get_rect()

        # finding image pixel dimensions from pygame.Rect's built in methods
        self.block_width = self.block_rect.width
        self.block_height = self.block_rect.height

        # the maze dimensions in the number of blocks
        self.width = len(self.b[0])
        self.height = len(self.b)

        # the maze dimensions in the number of pixels
        self.maze_width = self.width * self.block_width
        self.maze_height = self.height * self.block_height

        # opening the correct size window calculated from the size and number of the blocks
        self.bg_surf = pygame.display.set_mode((self.maze_width, self.maze_height), pygame.HWSURFACE)
        pygame.display.set_caption("MazeGame")

        # initialising the list to store all the different rects that make up the walls
        self.rect_list = list()
        # for each value in the array,
        for y in range(self.height):
            for x in range(self.width):
                # add a rect to the rect list at the position where there is a 1 in the background array
                if self.b[y][x] == 1:
                    self.rect_list.append(Rect(x * self.block_width, y * self.block_height,
                                               self.block_width, self.block_height))
                # initialising the rect for the finish block
                elif self.b[y][x] == 3:
                    self.end_rect = Rect(x * self.block_width, y * self.block_height,
                                         self.block_width, self.block_height)
        # self.rect_list.append(Rect(0, 0, self.block_width, self.block_height))

    def draw(self):
        """
        printing the walls and the finish block to the pygame window
        """
        # for each item in the array of arrays
        for y in range(self.height):
            for x in range(self.width):
                # draw a wall at a 1
                if self.b[y][x] == 1:
                    self.bg_surf.blit(self.block, (x * self.block_width, y * self.block_height))
                # draw the finish at 3
                elif self.b[y][x] == 3:
                    self.bg_surf.blit(self.end, (x * self.block_width, y * self.block_height))


class Player:
    """
    Player class for the cursor
    - loads the rects and the image for the player

    The player image can also be altered
    """
    def __init__(self):
        # loading image, converting into surface and rect
        self.character = pygame.image.load("player.png").convert()
        # loading player rect
        self.char_rect = self.character.get_rect()
        # finding dimensions of the player
        self.width = self.char_rect.width
        self.height = self.char_rect.height

        '''
        the player consists of 5 different rects:
          the main rect where the player image is blited onto
          the 2 rects at the left and right edges of the main rect
          the 2 rects at the top and bottom edges of the main rect
        the 4 subrects have a thickness of 1 pixel. they are used for collision detection
        '''
        self.char_rect_left = pygame.Rect(0, 1, 1, self.height-2)
        self.char_rect_top = pygame.Rect(1, 0, self.width-2, 1)
        self.char_rect_right = pygame.Rect(self.width-1, 1, 1, self.height-2)
        self.char_rect_bottom = pygame.Rect(1, self.height-1, self.width-2, 1)

        # initialising the heading or direction of the player
        self.heading = 5

    def move(self, heading):
        """
        moving all 5 of the player rects depending on the heading
        """
        if heading == 6:  # right
            self.char_rect.move_ip(1, 0)
            self.char_rect_left.move_ip(1, 0)
            self.char_rect_top.move_ip(1, 0)
            self.char_rect_right.move_ip(1, 0)
            self.char_rect_bottom.move_ip(1, 0)
        if heading == 2:  # down
            self.char_rect.move_ip(0, 1)
            self.char_rect_left.move_ip(0, 1)
            self.char_rect_top.move_ip(0, 1)
            self.char_rect_right.move_ip(0, 1)
            self.char_rect_bottom.move_ip(0, 1)
        if heading == 4:  # left
            self.char_rect.move_ip(-1, 0)
            self.char_rect_left.move_ip(-1, 0)
            self.char_rect_top.move_ip(-1, 0)
            self.char_rect_right.move_ip(-1, 0)
            self.char_rect_bottom.move_ip(-1, 0)
        if heading == 8:  # up
            self.char_rect.move_ip(0, -1)
            self.char_rect_left.move_ip(0, -1)
            self.char_rect_top.move_ip(0, -1)
            self.char_rect_right.move_ip(0, -1)
            self.char_rect_bottom.move_ip(0, -1)
        return True


class Menu:
    """
    Menu class for the start screen
    - starts the menu screen
    - text input for determining the dimensions of the maze
    - runs the game
    - prints the win screen (if won)
    """
    def __init__(self):
        # initialising the font
        self.font = pygame.font.SysFont("Times New Roman", 30)
        # starting the start screen
        self.start = self.Start(self.font)

        if self.start.exit_game:
            # exit button at start pressed
            self.exit_game = True
            return

        # starting the game class
        self.game = self.Game(self.start.rows, self.start.columns)
        # initial screen draw
        self.game.game_render()
        # logic for game loops
        self.game.running = True
        self.exit_game = False

        # main game loop
        while self.game.running:
            pygame.event.pump()
            # pause so cursor doesnt move too fast
            t.sleep(0.00017)

            if self.game.check_key_press():
                # if any keys have been pressed
                self.game.check_collision()
                self.game.game_render()

        if self.game.won:
            self.win = self.Win(self.font)
            if self.win.exit_game:
                self.exit_game = True

        else:
            # quit the game
            self.exit_game = True

    class Start:
        """
        Start class for drawing the start menu screen
        - Variables for maze dimensions can be entered here
        """
        def __init__(self, font):
            # logic for start screen loop
            self.stop = False
            # if escape button has been pressed
            self.exit_game = False
            # open up the start window
            self.start_screen = pygame.display.set_mode((854, 480), pygame.HWSURFACE)
            pygame.display.set_caption("MazeGame: Welcome!")
            self.font = font

            # default maze dimensions
            self.rows = 22
            self.columns = 22

            # start and exit buttons
            self.start_button = self.font.render("Start", False, (255, 255, 255))
            self.exit_button = self.font.render("Exit", False, (255, 255, 255))

            self.button = pygame.image.load("button.png").convert()
            # loading player rect
            self.start_rect = self.button.get_rect(center=(600, 300))
            self.exit_rect = self.button.get_rect(center=(600, 340))

            # text boxes for entering dimensions of the maze

            self.block = pygame.image.load("block.png").convert()
            x = 0
            y = 0

            # start screen loop
            while not self.stop:
                pygame.event.pump()
                self.start_screen.fill((54, 57, 62))

                # print button background
                self.start_screen.blit(self.button, self.start_rect)
                self.start_screen.blit(self.button, self.exit_rect)

                # print button text
                self.start_screen.blit(self.start_button, (self.start_rect.left + 20, self.start_rect.top))
                self.start_screen.blit(self.exit_button, (self.exit_rect.left + 24, self.exit_rect.top))

                # print animation
                t.sleep(0.0001)
                self.start_screen.blit(self.block, (x, y))

                x += 2
                y += 1

                if x > self.start_screen.get_width():
                    x = 0
                if y > self.start_screen.get_height():
                    y = 0

                # update screen
                pygame.display.flip()

                # check keyboard and mouse
                key_press = pygame.key.get_pressed()
                self.mouse_pos = pygame.mouse.get_pos()
                self.mouse_key = pygame.mouse.get_pressed()

                # type dimensions in

                # if escape is pressed or if the exit button is clicked
                if key_press[K_ESCAPE] or (self.exit_rect.collidepoint(self.mouse_pos) and self.mouse_key[0]):
                    # exit the game
                    self.stop = True
                    self.exit_game = True

                if self.start_rect.collidepoint(self.mouse_pos) and self.mouse_key[0]:
                    # change to default maze dimensions if required
                    if self.rows < 2:
                        self.rows = 9
                    if self.columns < 2:
                        self.columns = 9

                    # exit out of start menu
                    self.stop = True

        def type(self):  #
            """
            for typing in the dimensions of the maze
            """

    class Game:
        """
        Game class for most of the game logic
        - Background and Player classes are initialised here
        """

        def __init__(self, rows, columns):
            # background and player initialisation
            self.background = Background(rows, columns)
            self.player = Player()

            # placing the player in the proper spot down and right one block
            x = self.background.block_rect.width
            y = self.background.block_rect.height
            self.player.char_rect.move_ip(x, y)
            self.player.char_rect_left.move_ip(x, y)
            self.player.char_rect_top.move_ip(x, y)
            self.player.char_rect_right.move_ip(x, y)
            self.player.char_rect_bottom.move_ip(x, y)

            # if the game is running and if you have won or not
            self.running = True
            self.won = False

        def game_render(self):
            """
            updates the screen by making the screen black and redrawing all the walls, the finish block and the player
            """
            # fill black
            self.background.bg_surf.fill((54, 57, 62))
            # draw walls and the finish block
            self.background.draw()
            # draw player
            self.background.bg_surf.blit(self.player.character, self.player.char_rect)
            # updated window
            pygame.display.flip()

        def check_key_press(self):
            """
            checks the keyboard for key presses and moves the player if directions have been input
            """
            # get key presses
            keys = pygame.key.get_pressed()
            moved = False
            self.player.heading = 5

            if keys[K_RIGHT]:
                moved = self.player.move(6)
            elif keys[K_LEFT]:
                moved = self.player.move(4)
            if keys[K_DOWN]:
                moved = self.player.move(2)
            elif keys[K_UP]:
                moved = self.player.move(8)

            if keys[K_ESCAPE]:
                # escape was pressed: exit the game
                self.running = False

            return moved

        def check_collision(self):
            """
            checks if the player has collided with walls or the finish block
            """
            if self.player.char_rect.collidelist(self.background.rect_list) > 0:
                # there is a collision
                if self.player.char_rect_right.collidelist(self.background.rect_list) > 0:
                    self.player.move(4)
                if self.player.char_rect_bottom.collidelist(self.background.rect_list) > 0:
                    self.player.move(8)
                if self.player.char_rect_left.collidelist(self.background.rect_list) > 0:
                    self.player.move(6)
                if self.player.char_rect_top.collidelist(self.background.rect_list) > 0:
                    self.player.move(2)

            if self.player.char_rect.colliderect(self.background.end_rect):
                # player has reached the end and won
                self.won = True
                self.running = False

    class Win:
        def __init__(self, font):
            # game has been finished
            # logic for win screen loop
            self.stop = False
            # open up the finish window
            self.win_screen = pygame.display.set_mode((854, 480), pygame.HWSURFACE)
            pygame.display.set_caption("MazeGame: Congratulations!")
            self.font = font

            # retry and exit buttons
            self.retry_button = self.font.render("Retry", True, (255, 255, 255))
            self.exit_button = self.font.render("Exit", True, (255, 255, 255))

            self.button = pygame.image.load("button.png").convert()

            self.retry_rect = self.button.get_rect(center=(340, 300))
            self.exit_rect = self.button.get_rect(center=(510, 300))

            # text to display
            win_text = self.font.render("Congratulations, you win!", True, (255, 255, 255))

            # win screen loop
            while not self.stop:
                pygame.event.pump()
                # clear screen
                self.win_screen.fill((54, 57, 62))
                self.win_screen.blit(win_text, (270, 150))

                # print button background
                self.win_screen.blit(self.button, self.retry_rect)
                self.win_screen.blit(self.button, self.exit_rect)

                # print button text
                self.win_screen.blit(self.retry_button, (self.retry_rect.left + 17, self.retry_rect.top))
                self.win_screen.blit(self.exit_button, (self.exit_rect.left + 24, self.exit_rect.top))
                pygame.display.flip()

                key_press = pygame.key.get_pressed()
                self.mouse_pos = pygame.mouse.get_pos()
                self.mouse_key = pygame.mouse.get_pressed()

                # if escape is pressed or if the exit button is clicked
                if key_press[K_ESCAPE] or (self.exit_rect.collidepoint(self.mouse_pos) and self.mouse_key[0]):
                    # exit the game
                    self.stop = True
                    self.exit_game = True

                # retry button was pressed
                if self.retry_rect.collidepoint(self.mouse_pos) and self.mouse_key[0]:
                    self.stop = True
                    self.exit_game = False


if __name__ == "__main__":
    pygame.init()
    # if quit game is pressed, maze will be False
    while True:
        menu = Menu()
        # once menu exits and maze is still True, it means try again was pressed
        if menu.exit_game:
            break
        del menu

    pygame.quit()
