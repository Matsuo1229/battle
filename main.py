import asyncio
import json
import pygame

from javascript import WebSocket

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Game")

clock = pygame.time.Clock()

# =========================
# WebSocket
# =========================

SERVER_URL = "wss://jankenserver.my-647.workers.dev/"

ws = WebSocket.new(SERVER_URL)

connected = False

# 自分
player_x = 100
player_y = 250

# 相手
enemy_x = 650
enemy_y = 250

player_speed = 5


# =========================
# WebSocket受信
# =========================

def on_message(event):
    global enemy_x, enemy_y

    try:
        data = json.loads(event.data)

        if data.get("type") == "player":
            enemy_x = data["x"]
            enemy_y = data["y"]

    except Exception as e:
        print("受信エラー:", e)


def on_open(event):
    global connected
    connected = True
    print("WebSocket接続成功")


def on_error(event):
    print("WebSocketエラー")


ws.addEventListener("message", on_message)
ws.addEventListener("open", on_open)
ws.addEventListener("error", on_error)


# =========================
# メインゲーム
# =========================

async def main():

    global player_x
    global player_y

    running = True

    while running:

        # -------------------------
        # イベント
        # -------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


        # -------------------------
        # キー入力
        # -------------------------

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed


        # -------------------------
        # 画面外防止
        # -------------------------

        player_x = max(0, min(WIDTH - 50, player_x))
        player_y = max(0, min(HEIGHT - 50, player_y))


        # -------------------------
        # 自分の位置を送信
        # -------------------------

        if connected:

            try:

                message = json.dumps({
                    "type": "player",
                    "x": player_x,
                    "y": player_y
                })

                ws.send(message)

            except Exception as e:
                print("送信エラー:", e)


        # -------------------------
        # 描画
        # -------------------------

        screen.fill((30, 30, 30))

        # 自分（青）
        pygame.draw.rect(
            screen,
            (0, 120, 255),
            (player_x, player_y, 50, 50)
        )

        # 相手（赤）
        pygame.draw.rect(
            screen,
            (255, 60, 60),
            (enemy_x, enemy_y, 50, 50)
        )


        pygame.display.flip()

        # ブラウザに処理を返す
        await asyncio.sleep(0)

        clock.tick(60)


    pygame.quit()


asyncio.run(main())
