import pygame
from pygame.locals import *
import math
import time
import random

width = 1080
height = 720
#Tạo khung hình hiển thị game
display_surf = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bum bum")

bg = pygame.image.load("bg.jpg").convert_alpha()
bullet_image = pygame.image.load("bullet.png").convert_alpha()
game_over_img = pygame.image.load("game_over.jpg").convert_alpha()
big_star_image = pygame.image.load("bigstar.png").convert_alpha()
small_star_image = pygame.image.load("smallstar.png").convert_alpha()
paddle_image = pygame.image.load("paddle.png").convert_alpha()
explode_img = pygame.image.load("soulsplode.png").convert_alpha()

white = (255, 255, 255)
gray = (114, 106, 106)
green = (0, 200, 0)
black = (0, 0, 0)
bright_green = (0, 255, 0)

fps = 200 #Số frame trên giây
fps_clock = pygame.time.Clock()

class Stars:
    def __init__(self, w, h, x, y, speed):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.speed = speed
    def draw(self):
        display_surf.blit(big_star_image, (self.x, self.y))
    def move(self):
        self.y = self.y + self.speed
    def hit_paddle(self, paddle):
        if paddle.x - self.w <= self.x <= paddle.x + paddle.w\
            and self.y + self.h >= paddle.y:
            return True
        else:
            return False
    def hit_floor(self):
        if self.y >= (height - self.h):
            return True
        else:
            return False
    def hit_bullet(self, bullet):
        if bullet.x - self.w <= self.x <= bullet.x + bullet.w\
            and self.y >= bullet.y - self.h:
            return True
        else:
            return False

class Paddle:
    def __init__(self, x, y, w, h, speed):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.speed = speed
        self.dr = 1
    def draw(self):
        display_surf.blit(paddle_image, (self.x, self.y))
    def move(self):
        if self.x + self.dr*self.speed >= 0 and self.x + self.w + self.dr*self.speed <= width:
            self.x += self.dr*self.speed

class Bullet:
    def __init__(self, x, y, w, h, speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
    def move(self):
        self.y -= self.speed
    def draw(self):
        screen.blit(bullet_image, (self.x, self.y))

class ScoreBoard:
    def __init__(self, x, y, score, size):
        self.x = x
        self.y = y
        self.score = score
        self.size = size
        self.font = pygame.font.Font(None, self.size)
    def display(self):
        display_score = self.font.render(' Score ' + str(self.score), True, white)
        display_surf.blit(display_score, (self.x, self.y))

class Game:
    def __init__(self, star, paddle, bullet, scoreboard):
        self.star = star
        self.paddle = paddle
        self.bullet = bullet
        self.score_board = scoreboard
    def draw_arena(self):
        display_surf.blit(bg, (0, 0))
        self.paddle.draw()
        for draw_star in self.star:
            draw_star.draw()
        for bullet in self.bullet:
            display_surf.blit(bullet_image, (bullet.x, bullet.y))
        self.score_board.display()
    def update(self):
        for move_star in self.star:
            move_star.move()
        for b in range(len(self.bullet)):
            self.bullet[b].move()

        for bullet in self.bullet:
            if bullet.y < 0:
                self.bullet.remove(bullet)
        self.paddle.move()

def Main():
    pygame.init()

    paddle = Paddle(width/2 ,height - 78, 100, 78, 1)
    stars = []
    bullets = []
    score_board = ScoreBoard(800, 40, 0, 25)
    game = Game(stars, paddle, bullets, score_board)
    while True:
        if len(game.star) <= 2:
            game.star.append(Stars(60, 92, random.randint(game.paddle.w/2, width - game.paddle.w/2), 0, 0.1))

        flag = False
        for check_star in game.star:
            if check_star.hit_paddle(game.paddle) or check_star.hit_floor():
                display_surf.blit(game_over_img, (0,0))

                font = pygame.font.Font(None, 20)
                game_over = font.render("GAME OVER", True, black)
                display_surf.blit(game_over, (width / 2, height / 2))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        flag = True
                break
            else:
                for bullet in game.bullet:
                    if check_star.hit_bullet(bullet):
                        #display_surf.blit(explode_img, (bullet.x, bullet.y))
                        game.star.remove(check_star)
                        game.bullet.remove(bullet)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        flag = True
                    elif event.type == KEYDOWN:
                        print(1)
                        if event.key == pygame.K_a:
                            game.paddle.dr = -1
                        elif event.key == pygame.K_d:
                            game.paddle.dr = 1
                        elif event.key == pygame.K_SPACE:
                            game.bullet.append(Bullet(game.paddle.x + game.paddle.w/2, game.paddle.y, 10, 42, 5))

                if flag:
                    break
                print("fuck")
                game.draw_arena()
                game.update()

        pygame.display.update()
        fps_clock.tick(fps)

if __name__ == '__main__':
    Main()