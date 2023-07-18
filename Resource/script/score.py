
    ##escキーを押したら終了
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        exec(open("ex05/Resource/script/titleUI.py", encoding="utf-8").read())
        pygame.quit()
        sys.exit()