import pygame
import sys
import random

# 初期化
pygame.init()

# 画面設定
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pinpon Game")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# パドルの設定
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 150
PADDLE_SPEED = 5

# ボールの設定
BALL_SIZE = 15
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# パドルの初期位置
left_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# パドル画像の読み込み
left_paddle_img = pygame.image.load('left_paddle.png')
left_paddle_img = pygame.transform.scale(left_paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
right_paddle_img = pygame.image.load('right_paddle.png')
right_paddle_img = pygame.transform.scale(right_paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# ボールの初期位置と速度
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

# スコア
score_left = 0
score_right = 0
font = pygame.font.Font(None, 74)

def move_paddle(paddle, up=True):
    if up and paddle.top > 0:
        paddle.y -= PADDLE_SPEED
    if not up and paddle.bottom < HEIGHT:
        paddle.y += PADDLE_SPEED

def reset_ball():
    ball.center = (WIDTH//2, HEIGHT//2)
    return BALL_SPEED_X * random.choice((1, -1)), BALL_SPEED_Y * random.choice((1, -1))

# ゲームループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # キー入力の処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_paddle(left_paddle, True)
    if keys[pygame.K_s]:
        move_paddle(left_paddle, False)
    if keys[pygame.K_UP]:
        move_paddle(right_paddle, True)
    if keys[pygame.K_DOWN]:
        move_paddle(right_paddle, False)

    # ボールの移動
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # ボールの跳ね返り（上下）
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # ボールの跳ね返り（パドル）
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # スコアの更新
    if ball.left <= 0:
        score_right += 1
        ball_speed_x, ball_speed_y = reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        ball_speed_x, ball_speed_y = reset_ball()

    # 画面の描画
    screen.fill(BLACK)
    # パドル画像の描画
    screen.blit(left_paddle_img, left_paddle)
    screen.blit(right_paddle_img, right_paddle)
    # ボールと中央線
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # スコアの表示
    score_text = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.display.flip()
    pygame.time.Clock().tick(60) 