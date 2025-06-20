import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = { #移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0 , +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """

    yoko, tate = True, True #初期値:画面内
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate #横方向,縦方向の画面内判定結果を返す


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のSurface作成(爆弾用)
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0)) #黒を透明に設定
    bb_rct = bb_img.get_rect() #爆弾のRectを取得
    bb_rct.centerx = random.randint(0, WIDTH) #横座標の乱数
    bb_rct.centery = random.randint(0, HEIGHT) #縦座標の乱数
    vx, vy = +5, +5 #爆弾の移動速度


    def gameover(screnn: pg.Surface) -> None:
        """
        引数引数:screnn
        戻り値：None
        爆弾にぶつかったら、gameoverにする関数
        """
        bg_img = pg.Surface((1100, 650)) #ブラックアウト
        pg.draw.rect(bg_img,(0, 0, 0),(0 , 0, 1100,0))
        bg_img.set_alpha(150)
        img = pg.image.load("fig/9.png") #こうかとん表示
        fonto = pg.font.Font(None, 80) #画像の表示
        txt = fonto.render("Game Over",True, (255, 255, 255))
        screen.blit(bg_img, [0, 0])
        screen.blit(txt, [355, 300])
        screen.blit(img, [300, 300])
        screen.blit(img, [665, 300])
        pg.display.update()
        time.sleep(5)


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            gameover(screen)
            return 
        screen.blit(bg_img, [0, 0]) 
        
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key , mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾の移動
        yoko, tate = check_bound(bb_rct) #横方向にはみ出ていたら
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct) #爆弾の描画
        
        
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
