import asyncio
import pygame

pygame.init()

# ゲーム画面
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Game")

clock = pygame.time.Clock()

# プレイヤー
player_x = 100
player_y = 250
player_speed = 5

running = True

async def main():
    global running, player_x, player_y

    while running:

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # キー入力
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed

        # 画面外に出ないようにする
        if player_x < 0:
            player_x = 0

        if player_x > WIDTH - 50:
            player_x = WIDTH - 50

        if player_y < 0:
            player_y = 0

        if player_y > HEIGHT - 50:
            player_y = HEIGHT - 50

        # 背景
        screen.fill((30, 30, 30))

        # 青いプレイヤー
        pygame.draw.rect(
            screen,
            (0, 120, 255),
            (player_x, player_y, 50, 50)
        )

        pygame.display.flip()

        # ★重要
        # ブラウザに処理を返す
        await asyncio.sleep(0)

        clock.tick(60)

    pygame.quit()


asyncio.run(main())
