import pygame
import time
import sys
import ctypes

# 初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# フォントの読み込み
font_path = "ex05/Resource/font/DotGothic16-Regular.ttf"
font = pygame.font.Font(font_path, 36)

# スコアを読み込むファイルのパス
score_file_path = "ex05/save/score.sdata"

# スコアを読み込む関数
def load_scores(file_path):
    scores = []
    with open(file_path, "r") as file:
        for line in file:
            score = int(line.strip())
            scores.append(score)
    return scores

# スコアを降順に並び替える関数
def sort_scores(scores):
    return sorted(scores, reverse=True)

# スコアを表示する関数
def show_scores(sorted_scores):
    x = 400
    y = 100
    ##スコアという文字を表示
    score_text = font.render("スコア一覧 エスケープキーでタイトル画面へ戻る", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(x, 50))
    screen.blit(score_text, score_rect)
    ##エスケープキーでtitle画面へ戻るという文字を右下に小さく表示

    ##スコアを表示
    for i, score in enumerate(sorted_scores):
        ##iが0のときのif文
        if i == 0:
            score_text = font.render(str(i + 1) +  ":" + "ハイスコア" + ":" + str(score) , True, (255, 255, 0))
            score_rect = score_text.get_rect(center=(x, y + i * 50))
            screen.blit(score_text, score_rect)
        else:
            score_text = font.render(str(i + 1) + ":" + str(score), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(x, y + i * 50))
            screen.blit(score_text, score_rect)

# スコアを読み込み、並び替えて表示する
scores = load_scores(score_file_path)
sorted_scores = sort_scores(scores)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 背景を黒で塗りつぶす
    screen.fill((0, 0, 0))

    # スコアを表示
    show_scores(sorted_scores)

    pygame.display.flip()
    clock.tick(60)

    ##escキーを押したら終了
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        exec(open("ex05/Resource/script/titleUI.py", encoding="utf-8").read())
        pygame.quit()
        sys.exit()
