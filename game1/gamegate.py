import pygame
import random
import math

# Pygameの初期化
pygame.init()

# グローバル設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_LIFE = 3

# ゲーム画面の設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# タイトルとアイコン
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('image/ufo.png')
pygame.display.set_icon(icon)

# BGMのロードと再生
pygame.mixer.music.load('music/background_music.mp3')
pygame.mixer.music.play(-1)  # ループ再生

# 効果音をロード
shoot_sound = pygame.mixer.Sound('music/shoot.ogg')

# ボス戦BGMとゲームクリアBGMをロード
boss_bgm = 'music/boss_battle.ogg'
game_clear_bgm = 'music/game_clear_bgm.wav'

# 背景画像のロード
background = pygame.image.load('image/space_background.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# プレイヤーの設定
player_size = (50, 50)
playerImg = pygame.image.load('image/spaceship.png')
playerImg = pygame.transform.scale(playerImg, player_size)
playerX = 370
playerY = 480
playerX_change = 0

# 弾の設定
bullet_size = (15, 15)
bulletImg = pygame.image.load('image/bullet.png')
bulletImg = pygame.transform.scale(bulletImg, bullet_size)
bulletX = 0
bulletY = 480
bulletY_change = 5  # 弾のスピードを少し遅く
bullet_state = "ready"  # ready - 発射可能, fire - 発射中

# 敵の設定
enemy_speed_factor = 2
enemy_size = (32, 32)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    original_enemy_image = pygame.image.load('image/alien.png')
    small_enemy_image = pygame.transform.scale(original_enemy_image, enemy_size)
    enemyImg.append(small_enemy_image)
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1 / enemy_speed_factor)
    enemyY_change.append(40 / enemy_speed_factor)

# ボスキャラの設定
boss_size = (100, 100)
bossImg = pygame.image.load('image/boss.png')
bossImg = pygame.transform.scale(bossImg, boss_size)
bossX = 300
bossY = 50
bossX_change = 2
boss_hp = 10
boss_active = False

# ボス弾の設定
boss_bullet_size = (20, 20)
boss_bulletImg = pygame.image.load('image/boss_bullet.png')
boss_bulletImg = pygame.transform.scale(boss_bulletImg, boss_bullet_size)
boss_bulletX = 0
boss_bulletY = 0
boss_bulletY_change = 0.5
boss_bullet_state = "ready"

# 爆発画像のロード
explosionImg = pygame.image.load('image/explosion.png')
boss_explosionImg = pygame.image.load('image/boss_explosion.png')

# スコアの設定
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# ゲームオーバーおよびゲームクリアの管理
game_over = False
game_clear = False

# プレイヤーの描画
def player(x, y):
    screen.blit(playerImg, (x, y))

# 敵の描画
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# ボスの描画
def boss(x, y):
    screen.blit(bossImg, (x, y))

# 爆発描画
def explosion(x, y):
    screen.blit(explosionImg, (x, y))

def boss_explosion(x, y):
    screen.blit(boss_explosionImg, (x, y))

# 弾の発射
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    shoot_sound.play()

# ボス弾の発射
def fire_boss_bullet(x, y):
    global boss_bullet_state
    boss_bullet_state = "fire"
    screen.blit(boss_bulletImg, (x + 50, y + 100))

# 当たり判定
def isCollision(objX, objY, bulletX, bulletY, radius=27):
    distance = math.sqrt((math.pow(objX - bulletX, 2)) + (math.pow(objY - bulletY, 2)))
    return distance < radius

# スコア表示
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# ゲームオーバー表示
def show_game_over():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    game_over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))
    continue_text = font.render("Press ENTER to continue", True, (255, 255, 255))
    screen.blit(continue_text, (200, 350))

# ゲームクリア表示
def show_game_clear():
    clear_font = pygame.font.Font('freesansbold.ttf', 64)
    game_clear_text = clear_font.render("GAME CLEAR!!", True, (255, 255, 255))
    screen.blit(game_clear_text, (200, 250))

# ゲームリセット
def reset_game():
    global playerX, playerY, bulletY, bullet_state, score_value, boss_active, boss_hp, game_clear
    playerX = 370
    playerY = 480
    bulletY = 480
    bullet_state = "ready"
    score_value = 0
    boss_active = False
    boss_hp = 10
    game_clear = False

    # 通常BGMに戻す
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/background_music.mp3')
    pygame.mixer.music.play(-1)

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)

# ゲームループ
running = True
while running:
    screen.blit(background, (0, 0))  # 背景を描画

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over or game_clear:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()
                game_over = False
                game_clear = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not game_over and not game_clear:
        # プレイヤーの移動
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # 弾の移動
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

            # 弾が画面外に出たらリセット
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

        # 敵の移動と処理
        for i in range(num_of_enemies):
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= 736:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]

            # 敵との当たり判定
            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                explosion(enemyX[i], enemyY[i])
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # ボス戦
        if score_value >= 20 and not boss_active:
            boss_active = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load(boss_bgm)
            pygame.mixer.music.play(-1)

        if boss_active:
            bossX += bossX_change
            if bossX <= 0 or bossX >= 700:
                bossX_change *= -1

            if isCollision(bossX, bossY, bulletX, bulletY, radius=50):
                bulletY = 480
                bullet_state = "ready"
                boss_hp -= 1
                boss_explosion(bossX, bossY)
                if boss_hp <= 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(game_clear_bgm)
                    pygame.mixer.music.play()
                    game_clear = True

            boss(bossX, bossY)

        # スコアが30でゲームクリア
        if score_value >= 30:
            game_clear = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load(game_clear_bgm)
            pygame.mixer.music.play()

        player(playerX, playerY)
        show_score(textX, textY)

    elif game_over:
        show_game_over()

    elif game_clear:
        show_game_clear()

    pygame.display.update()

pygame.quit()
