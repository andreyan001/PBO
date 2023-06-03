import pygame
import random
import time
from abc import ABC, abstractmethod
from pygame import image

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.Info()
lebar = 1400
tinggi = 800
window = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption("Snake Game")

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
snake_block = 10
snake_speed = 10

class Snake():
    def __init__(self, x1, y1, x1_change = 0,
        y1_change = 0):
        self.x = x1
        self.y = y1
        self.x = x1_change
        self.y = y1_change

    def menu(self):
        title_font = pygame.font.SysFont(None, 64)
        option_font = pygame.font.SysFont(None, 48)
        game_open = True

        while game_open:
            window.fill(black)
            title = title_font.render("Snake Game", True, white)
            play = option_font.render("Play", True, white)
            quit = option_font.render("Quit", True, white)

            window.blit(title, (lebar/2 - title.get_width()/2, 200))
            window.blit(play, (lebar/2 - play.get_width()/2, 300))
            window.blit(quit, (lebar/2 - quit.get_width()/2, 400))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_open = False
                        return game_open
                    elif event.key == pygame.K_q:
                        game_open = True
                        return game_open
                elif event.type == pygame.QUIT:
                    game_open = True
                    pygame.quit()
                    quit()
        
class Food():
    def __init__(self, foodx, foody):
        self.image = pygame.image.load("Makanan.png") 
        self.foodx = foodx
        self.foody = foody

    @abstractmethod
    def makan(self):
        pass

class Game(Snake, Food):
    def __init__(self, x1, y1, x1_change, y1_change, foodx, foody, Length_of_snake = 1):
        super().__init__(x1, y1, x1_change, y1_change)
        self.food = Food(foodx, foody)
        self.x1 = x1
        self.y1 = y1
        self.foodx = foodx
        self.foody = foody
        self.x1_change = x1_change 
        self.y1_change = y1_change 
        self.snake_list = []
        self.Length_of_snake = Length_of_snake

    def menu(self):
        paused = True
        pause_font = pygame.font.SysFont("bahnschrift", 28)
        mesg1 = pause_font.render("Game Paused", True, white)
        mesg2 = pause_font.render("P-Play", True, white)

        while paused:
            window.blit(mesg1, [lebar / 2.5, tinggi / 3 - 20])
            window.blit(mesg2, [lebar / 2.5 + 40, tinggi / 3 + 20])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False

    def our_snake(self):
        self.snake_block = snake_block
        for segment in self.snake_list:
            pygame.draw.rect(window, red, [segment[0], segment[1], snake_block, snake_block])
            pygame.display.update()

    def makan(self):
        food_image = pygame.image.load("Makanan.png")
        window.blit(food_image, (self.foodx, self.foody))
        pygame.display.update()

        for segment in self.snake_list:
            if segment[0] == self.foodx and segment[1] == self.foody:
                self.foodx = round(random.randrange(0, lebar - snake_block) / 10.0) * 10.0
                self.foody = round(random.randrange(0, tinggi - snake_block) / 10.0) * 10.0
                self.Length_of_snake += 1

    def Your_Score(self, score):
        score_font = pygame.font.SysFont("comicsansms", 35)
        self._score = score
        value = score_font.render("Your Score: " + str(self._score), True, yellow)
        window.blit(value, [0, 0])
        pygame.display.update()
        return self._score

    def high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                highscore = int(file.read())
        except FileNotFoundError:
            highscore = 0

        if self.Length_of_snake - 1 > highscore:
            highscore = self.Length_of_snake - 1
            with open("highscore.txt", "w") as file:
                file.write(str(highscore))

        return highscore
    
    def message(self, msg1, msg2, color):
        font_style = pygame.font.SysFont("bahnschrift", 25)
        
        mesg1 = font_style.render(msg1, True, color)
        mesg2 = font_style.render(msg2, True, color)
        mesg3 = font_style.render("High Score : " + str(self.high_score()), True, color)

        window.blit(mesg1, [lebar / 2.5 + 70, tinggi / 3 - 20])
        window.blit(mesg2, [lebar / 2.5, tinggi / 3 + 20])
        window.blit(mesg3, [lebar / 2.5 + 50, tinggi / 3 + 60])

    def gameLoop(self, game_over):
        game_close = False
        music1 = pygame.mixer.Sound("music.mp3")
        music1.play(loops=-1)

        while game_over == False: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x1_change = -snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x1_change = snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_UP:
                        self.y1_change = -snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.y1_change = snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_p:
                        self.menu()

            while game_close == True:
                music1.stop()
                window.fill(black)
                self.message("YOU LOST!", "Press P-Play or Q-Quit", red)
                self.Your_Score(self.Length_of_snake - 1)
                pygame.display.update()
    
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_p:
                            game_over = False
                            self.x1 = lebar / 2
                            self.y1 = tinggi / 2
                            self.x1_change = 0
                            self.y1_change = 0
                            self.foodx = round(random.randrange(0, lebar - snake_block) / 10.0) * 10.0 
                            self.foody = round(random.randrange(0, tinggi - snake_block) / 10.0) * 10.0
                            self.Length_of_snake = 1
                            self.snake_list = []
                            self.gameLoop(game_over)

            if self.x1 >= lebar or self.x1 < 0 or self.y1 >= tinggi or self.y1 < 0:
                game_close = True

            snake_Head = []
            snake_Head.append(self.x1)
            snake_Head.append(self.y1)
            for x in self.snake_list[:-1]:
                if x == snake_Head:
                    game_close = True
            
            self.snake_list.append(snake_Head)

            if len(self.snake_list) > self.Length_of_snake:
                del self.snake_list[0]

            if game_close == True:
                music2 = pygame.mixer.Sound("music2.mp3")
                music2.play()

            clock.tick(snake_speed)

            image1 = pygame.image.load("background.jpg")
            window.blit(image1, [0, 0])
            self.makan()
            self.our_snake()
            self.Your_Score(self.Length_of_snake - 1)
            self.x1 += self.x1_change
            self.y1 += self.y1_change
            pygame.display.update()
            
        pygame.quit()
        quit()

x1 = lebar / 2
y1 = tinggi / 2
x1_change = 0
y1_change = 0
foodx = round(random.randrange(0, lebar - snake_block) / 10.0) * 10.0 
foody = round(random.randrange(0, tinggi - snake_block) / 10.0) * 10.0
LoS = 1

player = Game(x1, y1, x1_change, y1_change, foodx, foody)
snake = Snake(x1, y1)
result = snake.menu()

player.gameLoop(result)
