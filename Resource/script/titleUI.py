import pygame
import time
import sys
import ctypes

# 初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

#font = pygame.font.Font("arial", 36)
##同じフォルダー内のResourcesフォルダー内のfontフォルダーにあるのフォントを指定
font = pygame.font.Font("ex05/Resource/font/DotGothic16-Regular.ttf", 36)


# タイトル画面のUI要素
title = font.render("ドンパチゲーム", True, (255, 255, 255))
start = font.render("スタート", True, (255, 255, 255))
score = font.render("スコア", True, (255, 255, 255))
settings = font.render("設定", True, (255, 255, 255))
quit = font.render("やめる", True, (255, 255, 255))

# UI要素の位置
title_rect = title.get_rect(center=(400, 200))
start_rect = start.get_rect(center=(400, 300))
score_rect = score.get_rect(center=(400, 350))
settings_rect = settings.get_rect(center=(400, 400))
quit_rect = quit.get_rect(center=(400, 450))

selected = "start"  # 選択された項目の初期値


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            ##背景を黒にする
            screen.fill((0, 0, 0))
            if event.key == pygame.K_UP:
                if selected == "start":
                    selected = "quit"
                elif selected == "score":
                    selected = "start"
                elif selected == "settings":
                    selected = "score"
                elif selected == "quit":
                    selected = "settings"
            elif event.key == pygame.K_DOWN:
                if selected == "start":
                    selected = "score"
                elif selected == "score":
                    selected = "settings"
                elif selected == "settings":
                    selected = "quit"
                elif selected == "quit":
                    selected = "start"
            elif event.key == pygame.K_RETURN:
                if selected == "start":
                    # UnicodeDecodeError: 'cp932' codec can't decode byte 0x96 in position 2201: illegal multibyte sequenceというエラーが出る
                    # 修正済み

                    exec(open("ex05/Resource/script/main.py", encoding="utf-8").read())
                    pygame.quit()
                    sys.exit()

                elif selected == "score":
                    exec(open("ex05/Resource/script/score.py", encoding="utf-8").read())
                    pygame.quit()
                    sys.exit()

                    pass
                elif selected == "settings":
                    #実装予定
                    
                    pass
                elif selected == "quit":
                    result = ctypes.windll.user32.MessageBoxW(None, "ゲームを終了しますか", "終了確認", 4)
                    if result == 6:
                        pygame.quit()
                        sys.exit()
                    elif result ==7:
                        pass
                    

    # 背景を黒で塗りつぶす
    screen.fill((0, 0, 0))

    # 選択された項目の色を変更
    if selected == "start":
        start = font.render("スタート", True, (255, 0, 0))
    else:
        start = font.render("スタート", True, (255, 255, 255))

    if selected == "score":
        score = font.render("スコア", True, (255, 0, 0))
    else:
        score = font.render("スコア", True, (255, 255, 255))

    if selected == "settings":
        settings = font.render("設定", True, (255, 0, 0))
    else:
        settings = font.render("設定", True, (255, 255, 255))

    if selected == "quit":
        quit = font.render("やめる", True, (255, 0, 0))
    else:
        quit = font.render("やめる", True, (255, 255, 255))

    # UI要素を描画
    screen.blit(title, title_rect)
    screen.blit(start, start_rect)
    screen.blit(score, score_rect)
    screen.blit(settings, settings_rect)
    screen.blit(quit, quit_rect)

    pygame.display.flip()
    clock.tick(60)