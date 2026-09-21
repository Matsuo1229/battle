import asyncio
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Game")

# プレイヤー
x = 100
y = 250
speed = 5

running = True


async def main():
    global x, y, running

    while running:

        # ----------------
        # イベント
        # ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ----------------
        # キー入力
        # ----------------
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y -= speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y += speed

        # ----------------
        # 画面外制限
        # ----------------
        x = max(0, min(WIDTH - 50, x))
        y = max(0, min(HEIGHT - 50, y))

        # ----------------
        # 描画
        # ----------------
        screen.fill((30, 30, 30))

        pygame.draw.rect(
            screen,
            (0, 120, 255),
            (x, y, 50, 50)
        )

        # 重要
        pygame.display.flip()

        # ブラウザへ処理を返す
        await asyncio.sleep(0.01)

    pygame.quit()


asyncio.run(main())
