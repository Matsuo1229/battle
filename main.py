import asyncio
import json
import pygame
from javascript import WebSocket

pygame.init()

# =========================
# ゲーム設定
# =========================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Game")

clock = pygame.time.Clock()

# =========================
# Cloudflare WebSocket
# =========================

SERVER_URL = "wss://my-online-game.my-647.workers.dev"

ws = WebSocket.new(SERVER_URL)

connected = False

# =========================
# 自分のプレイヤー
# =========================

player_x = 100
player_y = 250

player_speed = 5

# =========================
# 相手のプレイヤー
# =========================

enemy_x = 650
enemy_y = 250


# =========================
# WebSocket接続
# =========================

def on_open(event):
    global connected

    connected = True
    print("WebSocket connected")


# =========================
# 相手からデータを受信
# =========================

def on_message(event):
    global enemy_x
    global enemy_y

    try:
        data = json.loads(str(event.data))

        if data.get("type") == "player":

            enemy_x = int(data["x"])
            enemy_y = int(data["y"])

    except Exception as e:
        print("受信エラー:", e)


# =========================
# エラー
# =========================

def on_error(event):
    print("WebSocket error")


# =========================
# 接続イベント登録
# =========================

ws.addEventListener("open", on_open)
ws.addEventListener("message", on_message)
ws.addEventListener("error", on_error)


# =========================
# ゲーム
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
        # 画面外に出ない
        # -------------------------

        player_x = max(0, min(WIDTH - 50, player_x))
        player_y = max(0, min(HEIGHT - 50, player_y))


        # -------------------------
        # Cloudflareへ自分の位置を送信
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


        # =========================
        # 描画
        # =========================

        screen.fill((30, 30, 30))

        # 自分
        pygame.draw.rect(
            screen,
            (0, 120, 255),
            (player_x, player_y, 50, 50)
        )

        # 相手
        pygame.draw.rect(
            screen,
            (255, 60, 60),
            (enemy_x, enemy_y, 50, 50)
        )


        # 接続状態
        font = pygame.font.Font(None, 32)

        if connected:
            text = font.render("CONNECTED", True, (0, 255, 0))
        else:
            text = font.render("CONNECTING...", True, (255, 255, 0))

        screen.blit(text, (20, 20))


        pygame.display.flip()

        # ブラウザに処理を返す
        await asyncio.sleep(0)

        clock.tick(60)


    pygame.quit()


asyncio.run(main())
