import asyncio
import pygame
from javascript import WebSocket


# -------------------------
# 設定
# -------------------------
WIDTH = 800
HEIGHT = 500

SERVER_URL = "wss://my-online-game.my-647.workers.dev"

BLUE = (0, 100, 255)
RED = (255, 60, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# -------------------------
# Pygame
# -------------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Battle")

clock = pygame.time.Clock()


# -------------------------
# 自分の位置
# -------------------------
player_x = 200
player_y = 250

PLAYER_SIZE = 50
SPEED = 5


# -------------------------
# 相手の位置
# -------------------------
enemy_x = 550
enemy_y = 250


# -------------------------
# WebSocket
# -------------------------
ws = None
connected = False


def connect_server():
    global ws, connected

    try:
        ws = WebSocket.new(SERVER_URL)

        def on_open(event):
            global connected
            connected = True
            print("WebSocket connected!")

        def on_error(event):
            print("WebSocket error")

        ws.addEventListener("open", on_open)
        ws.addEventListener("error", on_error)

        print("Connecting to server...")

    except Exception as e:
        print("WebSocket error:", e)


def send_position():
    if ws is None:
        return

    if not connected:
        return

    try:
        message = f"{player_x},{player_y}"
        ws.send(message)
    except Exception as e:
        print("Send error:", e)


# -------------------------
# ゲーム
# -------------------------
async def main():

    global player_x
    global player_y
    global enemy_x
    global enemy_y

    connect_server()

    running = True

    while running:

        # -------------------------
        # イベント
        # -------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # -------------------------
        # キーボード
        # -------------------------
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= SPEED

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += SPEED

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= SPEED

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += SPEED

        # 画面外に出ないようにする
        player_x = max(0, min(WIDTH - PLAYER_SIZE, player_x))
        player_y = max(0, min(HEIGHT - PLAYER_SIZE, player_y))

        # -------------------------
        # サーバーへ位置送信
        # -------------------------
        send_position()

        # -------------------------
        # 描画
        # -------------------------
        screen.fill((40, 40, 40))

        # 自分
        pygame.draw.rect(
            screen,
            BLUE,
            (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        )

        # 相手
        pygame.draw.rect(
            screen,
            RED,
            (enemy_x, enemy_y, PLAYER_SIZE, PLAYER_SIZE)
        )

        # 接続状態
        font = pygame.font.Font(None, 32)

        if connected:
            text = font.render("CONNECTED", True, WHITE)
        else:
            text = font.render("CONNECTING...", True, WHITE)

        screen.blit(text, (20, 20))

        pygame.display.flip()

        # ★ Pygbagでは重要
        await asyncio.sleep(0)


asyncio.run(main())
