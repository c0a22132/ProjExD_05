import pygame
import sys
import ctypes

result = ctypes.windll.user32.MessageBoxW(None, "ゲームを実行しますか", "実行確認", 4)

pygame.init()
# ユーザーの選択結果に基づいた処理
if result == 6:  # Yesが選択された場合
    print("Yesが選択されました")
    exec(open("ex05/Resource/script/titleUI.py", encoding="utf-8").read())
    pygame.quit()
    sys.exit()
elif result == 7:  # Noが選択された場合
    ##プログラムを終了する
    print("Noが選択されました")
    result = ctypes.windll.user32.MessageBoxW(None, "プログラムを終了します", "終了", 0)
    pygame.quit()