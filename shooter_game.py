#Создай собственный Шутер!
#Добавить: меню, уровни сложности и новый тип появления бонусов

from pygame import *
from random import *
import time as timer

lost = 0
score = 0
num_fire = 0
rel_time = False
paused = False
count_p = 0
play_m = True
menu = True
c_dif = 'n'
btn_new_game = Rect(550, 300, 300, 60)
btn_dif = Rect(550, 400, 300, 60)
btn_menu = Rect(550, 300, 300, 60)
btn_continue = Rect(550, 300, 300, 60)
btn_restart = Rect(550, 400, 300, 60)
btn_quit = Rect(550, 500, 300, 60)

window = display.set_mode((1400, 1000))
display.set_caption('Шутер')
display.set_icon(image.load('Media/black-hole.png'))

background = transform.scale(image.load('Media/galaxy.jpg'), (1400, 1000))

bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, speed, x_cor, y_cor, width, height):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullets(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y <= 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 1290:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullets('Media/bullet.png', 20, self.rect.centerx, self.rect.top, 10, 30) 
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 1000:
            lost += 1
            self.rect.y = -50
            self.rect.x = randint(0, 1300)     
            self.speed = randint(2, 5) 

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 1000:
            self.rect.y = -50
            self.rect.x = randint(0, 1300)     
            self.speed = randint(5, 17) 

class Bonus1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -90:
            self.speed = 1
        elif self.rect.y > 1000:
            self.rect.y = -1000
            self.rect.x = randint(0, 1300)
        else:
            self.speed = randint(5, 17)

class Bonus2(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < -90:
            self.speed = 1
        elif self.rect.x > 1400:
            self.rect.x = -1000
            self.rect.y = randint(100, 300)
        else:
            self.speed = randint(3, 10)
      

monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    m = Enemy('Media/ufo.png', randint(2, 5), randint(0, 1300), -50, 100, 65)
    monsters.add(m)

for i in range(4):
    a = Asteroid('Media/asteroid.png', randint(2, 10), randint(0, 1300), -50, 100, 65)
    asteroids.add(a)

life_bonus1 = Bonus1('Media/medkit.png', 10, randint(0, 1300), randint(-1500, -700), 100, 100)

reload_bonus = Bonus1('Media/bullets.png', 10, randint(0, 1300), randint(-1500, -700), 100, 100)

reset_bonus = Bonus1('Media/arrow.png', 10, randint(0, 1300), randint(-1500, -700), 100, 100)

life_bonus2 = Bonus2('Media/medkit.png', 5, randint(-1500, -700), randint(100, 300), 100, 100)

player = Player('Media/rocket.png', 10, 700, 830, 100, 150)

font.init()

font1 = font.Font(None, 108)
font2 = font.Font(None, 55)
font3 = font.Font(None, 30)

game = True

clock = time.Clock()
mixer.init()

mixer.music.load('Media/space.ogg')
mixer.music.set_volume(0.25)
mixer.music.play()

shot = mixer.Sound('Media/fire.ogg')
shot.set_volume(0.25)

lose_text = font1.render(f'Вы проиграли!', True, (255, 255, 255))
win_text = font1.render(f'Вы выиграли!', True, (255, 255, 255))
reload_text = font2.render(f'Идёт перезарядка...', True, (200, 50, 50))

def reset_game():
    global lost, score, num_fire, rel_time, health, paused, n_final
    lost = 0
    score = 0
    num_fire = 0
    rel_time = False
    health = 100
    paused = False
    n_final = True
    bullets.empty()
    monsters.empty()
    asteroids.empty()
    for i in range(5):
        m = Enemy('Media/ufo.png', randint(2, 5), randint(0, 1300), -50, 100, 65)
        monsters.add(m)
    for i in range(4):
        a = Asteroid('Media/asteroid.png', randint(2, 10), randint(0, 1300), -50, 100, 65)
        asteroids.add(a)
    for b in [life_bonus1, reload_bonus, reset_bonus]:
        b.rect.x, b.rect.y = randint(0, 1300), randint(-1500, -700)
    life_bonus2.rect.x, life_bonus2.rect.y = randint(-1500, -700), randint(100, 300)
    player.rect.x, player.rect.y = 700, 830

def draw_button(surface, rect, text, font, base_color, hover_color, mx, my):
    is_hover = rect.collidepoint(mx, my)
    if is_hover:
        color = hover_color
    else:
        color = base_color
    draw.rect(surface, color, rect)
    draw.rect(surface, (255, 255, 255), rect, 2)
    txt_surf = font.render(text, True, (255, 255, 255))
    txt_rect = txt_surf.get_rect()
    txt_rect.center = rect.center  # Автоматическое центрирование текста в кнопке
    surface.blit(txt_surf, txt_rect)
    return is_hover

n_final = True
while game:
    mx, my = mouse.get_pos()
    for events in event.get():
            if events.type == QUIT:
                game = False
            if events.type == KEYDOWN:
                if events.key == K_SPACE:
                    if num_fire < 5 and not rel_time:
                        player.fire()
                        shot.play()
                        num_fire += 1
                    elif num_fire >= 5 and not rel_time:
                        rel_time = True
                        begin_rel = timer.time()
                if events.key == K_ESCAPE:
                    play_m = not play_m
                    paused = not paused
                    if not play_m:
                        mixer.music.stop()
                    else:
                        mixer.music.play()
            if events.type == MOUSEBUTTONDOWN and paused and n_final:
                if btn_continue.collidepoint(events.pos):
                    play_m = not play_m
                    if not play_m:
                        mixer.music.stop()
                    else:
                        mixer.music.play()
                    paused = False
                elif btn_restart.collidepoint(events.pos):
                    reset_game()
                    play_m = not play_m
                    if not play_m:
                        mixer.music.stop()
                    else:
                        mixer.music.play()
                elif btn_quit.collidepoint(events.pos):
                    game = False
            if events.type == MOUSEBUTTONDOWN and menu:
                if btn_new_game.collidepoint(events.pos):
                    menu = False
                elif btn_dif.collidepoint(events.pos):
                    if c_dif == 'n':
                        c_dif = 'e'
                    elif c_dif == 'e':
                        c_dif = 'h'
                    elif c_dif == 'h':
                        c_dif = 'n'
                elif btn_quit.collidepoint(events.pos):
                    game = False
            if events.type == MOUSEBUTTONDOWN and not n_final:
                if btn_restart.collidepoint(events.pos):
                    n_final = True
                    reset_game()
                elif btn_menu.collidepoint(events.pos):
                    n_final = True
                    menu = True
                elif btn_quit.collidepoint(events.pos):
                    game = False

    if n_final and not paused and not menu:
        if count_dif_change == 0:
            if c_dif == 'n':
                health = 100
                rel_dif_time = 3
                lost_lose = 1000
            elif c_dif == 'e':
                health = 130
                rel_dif_time = 2
                lost_lose = 30
            elif c_dif == 'h':
                health = 70
                rel_dif_time = 5
                lost_lose = 10
            count_dif_change += 1
        count_p = 0
        window.blit(background, (0, 0))
        player.reset()
        life_bonus1.reset()
        reload_bonus.reset()
        reset_bonus.reset()
        life_bonus2.reset()
        player.update()
        life_bonus1.update()
        reload_bonus.update()
        reset_bonus.update()
        life_bonus2.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        lost_text = font1.render(f'Пропущено: {lost}', True, (255, 255, 255))
        score_text = font1.render(f'Счёт: {score}', True, (255, 255, 255))
        if sprite.spritecollide(player, asteroids, True) or sprite.spritecollide(player, monsters, True):
            health -= 30
            if health <= 0:
                health = 0
                window.blit(lose_text, (400, 200))
                n_final = False
        
        if sprite.spritecollide(life_bonus2, bullets, True):
            health += 10
            if health > 100:
                health = 100

        if sprite.collide_rect(player, life_bonus1):
            health += 20
            if health > 100:
                health = 100
            life_bonus1.rect.y = -1000

        if health >= 67:
            health_text = font1.render(f'{health}', True, (50, 200, 50))
            window.blit(health_text, (1250, 40))
        elif health < 67 and health > 33:
            health_text = font1.render(f'{health}', True, (150, 200, 50))
            window.blit(health_text, (1250, 40))
        elif health <= 34:
            health_text = font1.render(f'{health}', True, (200, 50, 50))
            window.blit(health_text, (1250, 40))

        if sprite.collide_rect(player, reload_bonus):
            num_fire = -20
            reload_bonus.rect.y = -1000

        if sprite.collide_rect(player, reset_bonus):
            lost = 0
            reset_bonus.rect.y = -1000

        if rel_time:
            cur_rel = timer.time()
            if cur_rel - begin_rel < rel_dif_time:
                window.blit(reload_text, (455, 900))
            else:
                num_fire = 0
                rel_time = False
                
        collide_list = sprite.groupcollide(bullets, monsters, True, True)

        for spr in collide_list:
            score += 1
            m = Enemy('Media/ufo.png', randint(2, 10), randint(0, 1300), -50, 100, 65)
            monsters.add(m)

        if lost >= lost_lose:
            window.blit(lose_text, (400, 200))
            n_final = False
            
        if score >= 20:
            window.blit(win_text, (400, 200))
            n_final = False
        
        lost_text = font1.render(f'Пропущено: {lost}', True, (255, 255, 255))
        score_text = font1.render(f'Счёт: {score}', True, (255, 255, 255))

        window.blit(score_text, (40, 20))
        window.blit(lost_text, (40, 100))

    if paused:
        overlay = Surface(window.get_size(), SRCALPHA)
        overlay.fill((0, 0, 0, 75))
        if count_p < 1:
            window.blit(overlay, (0, 0))
            count_p += 1
        pause_text = font1.render(f'Остановлено', True, (255, 255, 255))
        window.blit(pause_text, (455, 900))
        draw_button(window, btn_continue, 'Продолжить', font2, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_restart, "Заново", font2, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_quit, "Выйти", font2, (70, 130, 180), (100, 180, 230), mx, my)
    
    elif not n_final:
        draw_button(window, btn_restart, "Заново", font2, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_menu, "В меню", font2, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_quit, "Выйти", font2, (70, 130, 180), (100, 180, 230), mx, my)
    
    elif menu:
        count_dif_change = 0
        overlay = Surface(window.get_size(), SRCALPHA)
        overlay.fill((0, 0, 0, 75))
        window.blit(overlay, (0, 0))
        pause_text = font1.render(f'Главное меню', True, (255, 255, 255))
        window.blit(pause_text, (455, 900))
        draw_button(window, btn_new_game, 'Новая игра', font2, (70, 130, 180), (100, 180, 230), mx, my)
        if c_dif == 'n':
            draw_button(window, btn_dif, 'Сложность: нормальная', font3, (70, 130, 180), (100, 180, 230), mx, my)
        elif c_dif == 'e':
            draw_button(window, btn_dif, 'Сложность: лёгкая', font3, (70, 130, 180), (100, 180, 230), mx, my)
        elif c_dif == 'h':
            draw_button(window, btn_dif, 'Сложность: повышенная', font3, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_quit, "Выйти", font2, (70, 130, 180), (100, 180, 230), mx, my)

    clock.tick(60)
    display.update()
    