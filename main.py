import pygame
from pygame.locals import *
import math
import time
import random
import os

pygame.init()

width = 1080
height = 720
#Tạo khung hình hiển thị game
display_surf = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bum bum")

pygame.mixer.init()
pygame.mixer.music.load("sound/bg_music.mp3")
pygame.mixer.music.play(-1)

color = {
    'white': (255, 255, 255),
    'bright_white': (255, 255, 200),
    'blue': (0, 0, 255),
    'bright_blue': (117, 156, 255),
    'green': (0, 200, 0),
    'black': (0, 0, 0),
    'bright_green': (0, 255, 0),
    'red': (200,0,0),
    'bright_red': (255,0,0),
    'yellow': (200,200,0),
    'bright_yellow': (255,255,0),
}

explode_list = []
for i in range(8):
    explode_list.append('picture/' + 'explode_' + str(i+1) + '.png')
explode_img = []
for img in explode_list:
    set_img = pygame.transform.scale2x(pygame.image.load(img).convert_alpha(), )
    set_img.set_colorkey(color['black'])
    explode_img.append(set_img)

bg = pygame.image.load('picture/bg.jpg').convert_alpha()
bullet_image = pygame.image.load("picture/bullet.png").convert_alpha()
game_over_img = pygame.image.load("picture/game_over.jpg").convert_alpha()
big_star_image = pygame.image.load("picture/bigstar.png").convert_alpha()
small_star_image = pygame.image.load("picture/smallstar.png").convert_alpha()
paddle_image = pygame.image.load("picture/paddle.png").convert_alpha()
menu_img = pygame.image.load("picture/menu.jpg").convert_alpha()

score_list = []

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
        display_surf.blit(bullet_image, (self.x, self.y))

class ScoreBoard:
    def __init__(self, x, y, score, size):
        self.x = x
        self.y = y
        self.score = score
        self.size = size
        self.font = pygame.font.Font(None, self.size)
        self.high_score = 0
    def display(self):
        display_high_score = self.font.render(" Best score " + str(self.high_score), True, color['white'])
        display_score = self.font.render(' Score ' + str(self.score), True, color['white'])
        display_surf.blit(display_score, (self.x, self.y))
        display_surf.blit(display_high_score, (self.x, self.y + 20))

class Game:
    def __init__(self, star, paddle, bullet, scoreboard, level):
        self.star = star
        self.paddle = paddle
        self.bullet = bullet
        self.score_board = scoreboard
        self.hard = level
        self.explode = False
        self.lost_star = (0, 0)
        self.check = 0
        self.img = 0
    def draw_arena(self):
        display_surf.blit(bg, (0, 0))
        self.paddle.draw()
        for draw_star in self.star:
            draw_star.draw()
        for bullet in self.bullet:
            display_surf.blit(bullet_image, (bullet.x, bullet.y))
        if self.explode:
            for img in explode_img:
                display_surf.blit(img, self.lost_star)
                pygame.display.update()
                fps_clock.tick(100)
            self.explode = False
        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        resume_btn = Button(0, 0, 80, 30, "Pause", "yellow", "PAUSE", mousepos, click)
        resume_btn.draw()

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

class Button:
    def __init__(self, x, y, w, h, text, color, button_name, mouse_pos,click):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.button_name = button_name
        self.mouse_pos = mouse_pos
        self.click = click
    def button_function(self):
        if self.button_name == "TRY AGAIN" or self.button_name == "PLAY":
            Main()
        elif self.button_name == "QUIT":
            pygame.quit()
        elif self.button_name == "PAUSE":
            pause()
        elif self.button_name == "MENU":
            if pygame.mixer.Channel(1).get_busy():
                pygame.mixer.Channel(1).stop()
            main_menu()

    def draw(self):
        if self.x + self.w > self.mouse_pos[0] > self.x and self.y + self.h > self.mouse_pos[1] > self.y:
            pygame.draw.rect(display_surf, color['bright_' + self.color], (self.x, self.y, self.w, self.h), 0)
            if self.click[0] == 1:
                self.button_function()
        else:
            pygame.draw.rect(display_surf, color[self.color], (self.x, self.y, self.w, self.h), 0)

        font = pygame.font.Font(None, 20)
        button_text = font.render(self.text, True, color['black'])
        display_surf.blit(button_text, (self.x + 5, self.y + 5))

def pause():
    pause_check = True

    display_surf.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    pause_text = font.render("PAUSE", True, color['white'])
    display_surf.blit(pause_text, (100, height/2))
    msg = font.render("Press R to continue", True, color['white'])
    display_surf.blit(msg, (200, height/2 + 60))

    while pause_check:
        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        menu_btn = Button(width - 80, 0, 80, 30, "Main Menu", "white", "MENU", mousepos, click)
        quit_but = Button(width - 80, 50, 80, 30, "Quit", "red", "QUIT", mousepos, click)

        menu_btn.draw()
        quit_but.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    pause_check = False

        pygame.display.update()
        fps_clock.tick(500)

def main_menu():
    while True:
        flag = False
        display_surf.blit(menu_img, (0, 0))

        font = pygame.font.Font(None, 175)
        menu_text = font.render("Shoot that Star !!!", True, color['white'])
        display_surf.blit(menu_text, (0, 0))

        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        play_btn = Button(350, height/2, 80, 50, "Shoooot", "blue", "PLAY", mousepos, click)
        quit_but = Button(700, height/2, 80, 50, "Quit", "red", "QUIT", mousepos, click)

        play_btn.draw()
        quit_but.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                flag = True

        if flag:
            break

        pygame.display.update()
        fps_clock.tick(fps)

def Main():
    level = [x for x in range(50, 550, 50)]
    check_sound = True
    paddle = Paddle(width/2 ,height - 78, 100, 78, 1)
    stars = []
    bullets = []
    score_board = ScoreBoard(800, 40, 0, 25)
    game = Game(stars, paddle, bullets, score_board, 0.1)
    game.paddle.speed = game.hard * 20

    while True:
        if len(score_list) > 0:
            best_score = score_list[0]
            for score in score_list:
                if score > best_score:
                    best_score = score

            game.score_board.high_score = best_score
        else:
            game.score_board.high_score = game.score_board.score

        if game.score_board.score in level:
            game.hard += 0.1
            level.remove((game.score_board.score))

        if len(game.star) <= game.hard * 10:
            game.star.append(Stars(60, 92, random.randint(game.paddle.w/2, width - game.paddle.w/2), 0, game.hard * 2))

        flag = False
        for check_star in game.star:
            if check_star.hit_paddle(game.paddle) or check_star.hit_floor():
                score_list.append(game.score_board.score)
                display_surf.blit(game_over_img, (0,0))

                font = pygame.font.Font(None, 20)
                game_over = font.render("GAME OVER", True, color['black'])
                your_score = font.render("Your score: " + str(game.score_board.score), True, color['black'])
                high_score = font.render("High score: " + str(game.score_board.high_score), True, color['black'])
                display_surf.blit(game_over, (width / 2, height / 2))
                display_surf.blit(game_over, (width / 2, height / 2))
                display_surf.blit(your_score, (width / 2, height / 2 + 20))
                display_surf.blit(high_score, (width / 2, height / 2 + 40))

                mousepos = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                try_again_but = Button(width / 2, height / 2 + 60, 80, 30, "Try again", "green", "TRY AGAIN", mousepos, click)
                menu_but = Button(width / 2, height / 2 + 100, 80, 30, "Menu", "white", "MENU", mousepos, click)
                quit_but = Button(width / 2, height / 2 + 140, 80, 30, "Quit", "red", "QUIT", mousepos, click)

                try_again_but.draw()
                menu_but.draw()
                quit_but.draw()

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
                        game.lost_star = (check_star.x, check_star.y + check_star.h/2)
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
                            game.bullet.append(Bullet(game.paddle.x + game.paddle.w/2, game.paddle.y, 20, 83, 10))
                            pygame.mixer.Channel(2).set_volume(1)
                            pygame.mixer.Channel(2).queue(pygame.mixer.Sound('sound/shoot.wav'))
                game.draw_arena()
                game.update()
        if flag:
            break

        pygame.display.update()
        fps_clock.tick(fps)

if __name__ == '__main__':
    main_menu()