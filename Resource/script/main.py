
import pygame
import random
import sys
import json

# ゲームの画面サイズ
WIDTH = 480
HEIGHT = 600

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# 敵クラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy_image = pygame.image.load(f"ex05/Resource/image/neco1.png")
        self.enemy_size = random.randint(30, 50)  #画像のサイズの値の設定
        self.image = pygame.transform.scale(self.enemy_image, (self.enemy_size, self.enemy_size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -35)
        self.speedy = random.randrange(1, 9)
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -35)
            self.speedy = random.randrange(1, 9)
        if self.enemy_size <= 35:  
            sircle_enemy = pygame.transform.scale(pygame.image.load(f"ex05/Resource/image/neco2.png"), (self.enemy_size, self.enemy_size))
            if self.speedy >= 7:  #特定の速さ以上だと画像を回転落下させる
                self.image = pygame.transform.rotate(sircle_enemy, self.rect.y + self.speedy)  #画像を移動に合わせて回転
            else:
                self.image = pygame.transform.rotate(sircle_enemy, 0)  #回転阻止
            

# 弾クラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# 初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("縦型シューティングゲーム")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# スコア関連の変数
score = 0
score_font = pygame.font.Font("ex05/Resource/font/DotGothic16-Regular.ttf", 20)

# FPS関連の変数
show_fps = False
fps_font = pygame.font.Font("ex05/Resource/font/DotGothic16-Regular.ttf", 15)

# フォントの設定
font_name = "ex05/Resource/font/DotGothic16-Regular.ttf"

# テキストを描画する関数
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# ゲームオーバー画面を表示する関数
def show_game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, "Game Over", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Rキーを押してリトライ", 24, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Eキーを押してタイトル画面へ", 24, WIDTH // 2, HEIGHT // 2 + 30)
    draw_text(screen, "Score: {}".format(score), 30, WIDTH // 2, HEIGHT // 2 + 50)


    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_e:
                    exec(open("ex05/Resource/script/titleUI.py", encoding="utf-8").read())


# ゲームループ
running = True
game_over = False
last_score_update = pygame.time.get_ticks()  # 最後にスコアを更新した時刻
score_update_interval = 1000  # スコアを更新する間隔（ミリ秒）
while running:
    clock.tick(60)

    if game_over:
        show_game_over_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for _ in range(8):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        score = 0  # スコアを初期化

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_F1:
                show_fps = not show_fps  # F1キーでFPS表示の切り替え

    # 更新処理
    all_sprites.update()

    # 弾と敵の当たり判定
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit_enemy in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        score += 10  # スコアを追加

    # プレイヤーと敵の当たり判定
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        game_over = True

    # スコアを更新
    current_time = pygame.time.get_ticks()
    if current_time - last_score_update >= score_update_interval:
        score += 1
        last_score_update = current_time
        

    # 描画処理
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, "Score: {}".format(score), 18, WIDTH - 50, 10)  # スコアを描画

    # FPSを表示
    if show_fps:
        fps = int(clock.get_fps())
        draw_text(screen, "FPS: {}".format(fps), 18, 50, 10)  # FPSを描画

    pygame.display.flip()


