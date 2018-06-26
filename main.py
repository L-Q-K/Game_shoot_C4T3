import pygame
from pygame.locals import *
import math
import time
import random
import os

width = 1080
height = 720
#Tạo khung hình hiển thị game
display_surf = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bum bum")

pygame.mixer.init()
pygame.mixer.music.load("sound/bg_music.mp3")
pygame.mixer.music.play(-1)

white = (255, 255, 255)
gray = (114, 106, 106)
green = (0, 200, 0)
black = (0, 0, 0)
bright_green = (0, 255, 0)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)

explode_list = []
for i in range(8):
    explode_list.append('picture/' + 'explode_' + str(i+1) + '.png')
explode_img = []
for img in explode_list:
    set_img = pygame.image.load(img).convert_alpha()
    set_img.set_colorkey(black)
    explode_img.append(set_img)


bg = pygame.image.load('picture/bg.jpg').convert_alpha()
bullet_image = pygame.image.load("picture/bullet.png").convert_alpha()
game_over_img = pygame.image.load("picture/game_over.jpg").convert_alpha()
big_star_image = pygame.image.load("picture/bigstar.png").convert_alpha()
small_star_image = pygame.image.load("picture/smallstar.png").convert_alpha()
paddle_image = pygame.image.load("picture/paddle.png").convert_alpha()

fps = 200 #Số frame trên giây
fps_clock = pygame.time.Clock()

def explosion(x, y, size=50):

    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for img in explode_img:
            display_surf.blit(img, (x, y))

            pygame.display.update()
            fps_clock.tick(10)

        explode = False

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
        display_surf.blit(bullet_image, (self.x, self.y))

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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explode_img[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explode_img):
                self.kill()
            else:
                center = self.rect.center
                self.image = explode_img[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Game:
    def __init__(self, star, paddle, bullet, scoreboard, level, explode):
        self.star = star
        self.paddle = paddle
        self.bullet = bullet
        self.score_board = scoreboard
        self.hard = level
        # self.explode = explode
    def draw_arena(self):
        display_surf.blit(bg, (0, 0))
        self.paddle.draw()
        for draw_star in self.star:
            draw_star.draw()
        for bullet in self.bullet:
            display_surf.blit(bullet_image, (bullet.x, bullet.y))
        # if self.explode:
        #     for img in explode_img:
        #         display_surf.blit(img, (300, 300))
        #         pygame.display.update()
        #         fps_clock.tick(10)

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

    level = [x for x in range(50, 550, 50)]
    check_sound = True
    paddle = Paddle(width/2 ,height - 78, 100, 78, 1)
    stars = []
    bullets = []
    score_board = ScoreBoard(800, 40, 0, 25)
    game = Game(stars, paddle, bullets, score_board, 0.1, False)
    game.paddle.speed = game.hard * 15

    while True:
        game.explode = False
        if game.score_board.score in level:
            game.hard += 0.1
            level.remove((game.score_board.score))

        if len(game.star) <= game.hard * 10:
            game.star.append(Stars(60, 92, random.randint(game.paddle.w/2, width - game.paddle.w/2), 0, game.hard))

        flag = False
        for check_star in game.star:
            if check_star.hit_paddle(game.paddle) or check_star.hit_floor():
                display_surf.blit(game_over_img, (0,0))
                font = pygame.font.Font(None, 20)
                game_over = font.render("GAME OVER", True, black)
                display_surf.blit(game_over, (width / 2, height / 2))
                if check_sound:
                    check_sound = False
                    pygame.mixer.Channel(1).set_volume(1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound/Die.wav'))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        flag = True
                break
            else:
                for bullet in game.bullet:
                    if check_star.hit_bullet(bullet):
                        game.score_board.score += 10
                        game.explode = True
                        pygame.mixer.Channel(0).set_volume(0.5)
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/star_shoot.wav'))
                        game.star.remove(check_star)
                        game.bullet.remove(bullet)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        flag = True
                    elif event.type == KEYDOWN:
                        if event.key == pygame.K_a:
                            game.paddle.dr = -1
                        elif event.key == pygame.K_d:
                            game.paddle.dr = 1
                        elif event.key == pygame.K_SPACE:
                            pygame.mixer.Channel(2).set_volume(1)
                            pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/shoot.wav'))
                            game.bullet.append(Bullet(game.paddle.x + game.paddle.w/2, game.paddle.y, 20, 83, 10))


                game.draw_arena()
                game.update()
        if flag:
            break

        pygame.display.update()
        fps_clock.tick(fps)

if __name__ == '__main__':
    Main()