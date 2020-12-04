import pygame
from pygame.math import Vector2
import random

pygame.init()
pygame.display.set_caption("Snake")

class Snake:
    def __init__(self):
        self.body = [Vector2(10,10), Vector2(11,10)]
        self.direction = Vector2(1,0)
        self.next_block = False

    def draw_snake(self):
        for rect in self.body:
            x_pos = rect.x * cell_size
            y_pos = rect.y * cell_size
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, green, snake_rect)

    def move_snake(self):
        if self.next_block == True:
            copy_body = self.body[:]
            copy_body.insert(0, copy_body[0] + self.direction)
            self.body = copy_body[:]
            self.next_block = False
        else:
            copy_body = self.body[:-1]
            copy_body.insert(0, copy_body[0] + self.direction)
            self.body = copy_body[:]

    def add_block(self):
        self.next_block = True

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, red, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()
        self.score = 0
        self.over = False

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.game_over()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1

        for rect in self.snake.body[1:]:
            if rect == self.fruit.pos:
                self.fruit.randomize()

    def show_score(self):
        # font
        font = pygame.font.Font('freesansbold.ttf', 32)
        # text surface object
        text = font.render('Score: {}'.format(str(self.score)), True, white)
        # rect object for the text surface object
        textRect = text.get_rect()
        # set the center od the rect object
        textRect.center = (cell_size*cell_num - 100, cell_size*cell_num - 60)
        # show text on the screen
        screen.blit(text, textRect)

    def game_over(self):
        if 0 > int(self.snake.body[0].x) or int(self.snake.body[0].x) > cell_num - 1 or int(self.snake.body[0].y) < 0 or int(self.snake.body[0].y) > cell_num - 1:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render("You lost!!!", True, white)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))

            self.snake.body = [Vector2(10,10), Vector2(11,10)]
            self.snake.direction = Vector2(1,0)
            menu()
        for rect in self.snake.body[1:]:
            if self.snake.body[0] == rect:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render("You lost!!!", True, white)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))

                self.snake.body = [Vector2(10,10), Vector2(11,10)]
                self.snake.direction = Vector2(1,0)
                menu()
                    

cell_size = 40
cell_num = 20
WIDTH, HEIGHT = cell_size * cell_num, cell_size * cell_num
screen = pygame.display.set_mode((cell_num * cell_size, cell_num * cell_size))

clock = pygame.time.Clock()

# colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

game = Main()

pygame.time.set_timer(pygame.USEREVENT,100)

def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mainloop()

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Press spacebar to start", True, white)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 300))
        pygame.display.update()

def mainloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.USEREVENT:
                game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if game.snake.direction != Vector2(-1,0):
                        game.snake.direction = Vector2(1,0)
                elif event.key == pygame.K_LEFT:
                    if game.snake.direction != Vector2(1,0):
                        game.snake.direction = Vector2(-1,0)
                elif event.key == pygame.K_UP:
                    if game.snake.direction != Vector2(0,1):
                        game.snake.direction = Vector2(0,-1)
                elif event.key == pygame.K_DOWN:
                    if game.snake.direction != Vector2(0,-1):
                        game.snake.direction = Vector2(0,1)

        screen.fill(black)
        game.draw_elements()
        game.show_score()

        pygame.display.update()
        clock.tick(60)

menu()

pygame.quit()
quit()
