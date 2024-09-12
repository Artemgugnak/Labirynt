from pygame import *
from color import *

#константи
window_width = 1000
window_height = 900
display.set_caption('labirint lol')
window = display.set_mode((window_width, window_height))
game = True

#основа обєктів проекту
class GameSprite(sprite.Sprite):
    def __init__(self, img, player_x, player_y, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, player_x, player_y, width, height, player_x_speed, player_y_speed):
        GameSprite.__init__(self, img, player_x, player_y, width, height)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        if player.rect.x <= window_width - 80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for platforms in platforms_touched:
                self.rect.right = min(self.rect.right, platforms.rect.left)
        elif self.x_speed < 0:
            for platforms in platforms_touched:
                self.rect.left = max(self.rect.left, platforms.rect.right)
        if player.rect.y <= window_height - 80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.y_speed > 0:
            for platforms in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, platforms.rect.top)
        elif self.y_speed < 0:
            for platforms in platforms_touched:
                self.rect.top = max(self.rect.top, platforms.rect.bottom)
                
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right - 25, self.rect.centery - 16, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def __init__(self, img, player_x, player_y, width, height, player_speed):
        GameSprite.__init__(self,img, player_x, player_y, width, height)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= window_width - 80:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, img, player_x, player_y, width, height, player_speed):
        GameSprite.__init__(self, img, player_x, player_y, width, height)
        self.speed = player_speed
        
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > window_width + 10:
            self.kill()

class Enemy1(GameSprite):
    side = 'left'

    def __init__(self, img, player_x, player_y, width, height, player_speed):
        GameSprite.__init__(self, img, player_x, player_y, width, height)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= - 30:
            self.side = 'right'
        if self.rect.x >= window_width - 380:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player('Hero.png', 50, 50, 100, 100, 5, 5)
monster1 = Enemy('monster.png',800, 750, 50, 100, 3)
monster2 = Enemy1('monster.png', 500, 270, 80, 80, 3)
finish = GameSprite('end.png', 800, 800, 100, 50)

walls = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

wall1 = Wall(0, 0, 30, window_height, Silver)
wall2 = Wall(0, 0, window_width, 30, Silver)
wall3 = Wall(200, 200, window_width - 400, 30, Silver)
wall4 = Wall(200, 600, window_width - 400, 30, Silver)
wall5 = Wall(200, 200, 30, 200, Silver)
wall6 = Wall(500, 400, 30, 200, Silver)
wall7 = Wall(600, 0, 30, 200, Silver)

walls.add(wall1)
walls.add(wall2)
walls.add(wall3)
walls.add(wall4)
walls.add(wall5)
walls.add(wall6)
walls.add(wall7)

monsters.add(monster1)
monsters.add(monster2)

win = False
while game:
    time.delay(17)
    
    #щоб програма закриваласся
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.y_speed = -5
            elif e.key == K_s:
                player.y_speed = 5
            elif e.key == K_a:
                player.x_speed = -5
            elif e.key == K_d:
                player.x_speed = 5
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                player.y_speed = 0
            elif e.key == K_s:
                player.y_speed = 0
            elif e.key == K_a:
                player.x_speed = 0
            elif e.key == K_d:
                player.x_speed = 0
    if not win:
        window.fill((255, 255, 255))
        bullets.draw(window)
        monsters.draw(window)
        bullets.update()
        monsters.update()
        player.reset()
        player.update()
        finish.reset()
        walls.draw(window)

        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(bullets, walls, True, False)

        if sprite.collide_rect(player, finish):
            win = True
            img = image.load('win.jpg')
            window.blit(transform.scale(img, (window_width, window_height)), (0,0))
        if sprite.spritecollide(player, monsters, False):
            win = True
            img = image.load('game_over.jpg')
            window.blit(transform.scale(img, (window_width, window_height)), (0,0))

        display.update()