import asyncio
import json
import pygame
from javascript import WebSocket


# =========================
# 設定
# =========================

SERVER_URL = "wss://my-online-game.my-647.workers.dev"

WIDTH = 800
HEIGHT = 600

FPS = 60

PLAYER_SPEED = 5


# =========================
# pygame
# =========================

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Online Test Game")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)


# =========================
# WebSocket
# =========================

ws = None
connected = False

my_x = 200
my_y = 300

other_x = 600
other_y = 300


def websocket_open(event):
    global connected

    connected = True
    print("WebSocket connected")


def websocket_message(event):
    global other_x
    global other_y

    try:
        data = json.loads(event.data)

        if data.get("type") == "player":
            other_x = data["x"]
            other_y = data["y"]

    except Exception as e:
        print("Receive error:", e)


def websocket_error(event):
    print("WebSocket error")


def websocket_close(event):
    global connected

    connected = False
    print("WebSocket closed")


def connect_server():
    global ws

    print("Connecting...")

    ws = WebSocket.new(SERVER_URL)

    ws.addEventListener("open", websocket_open)
    ws.addEventListener("message", websocket_message)
    ws.addEventListener("error", websocket_error)
    ws.addEventListener("close", websocket_close)


def send_position():
    if not connected:
        return

    data = {
        "type": "player",
        "x": my_x,
        "y": my_y
    }

    try:
        ws.send(json.dumps(data))
    except Exception as e:
        print("Send error:", e)


# =========================
# ゲーム
# =========================

async def main():

    global my_x
    global my_y

    connect_server()

    running = True

    send_timer = 0

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

        # WASD
        if keys[pygame.K_a]:
            my_x -= PLAYER_SPEED

        if keys[pygame.K_d]:
            my_x += PLAYER_SPEED

        if keys[pygame.K_w]:
            my_y -= PLAYER_SPEED

        if keys[pygame.K_s]:
            my_y += PLAYER_SPEED

        # -------------------------
        # 画面外に出ないようにする
        # -------------------------

        my_x = max(0, min(WIDTH - 50, my_x))
        my_y = max(0, min(HEIGHT - 50, my_y))

        # -------------------------
        # 通信
        # -------------------------

        send_timer += 1

        # 約20回/秒
        if send_timer >= 3:

            send_timer = 0

            send_position()

        # -------------------------
        # 描画
        # -------------------------

        screen.fill((30, 30, 30))

        # 自分
        pygame.draw.rect(
            screen,
            (50, 150, 255),
            (my_x, my_y, 50, 50)
        )

        # 相手
        pygame.draw.rect(
            screen,
            (255, 80, 80),
            (other_x, other_y, 50, 50)
        )

        # 接続状態
        if connected:
            text = font.render(
                "CONNECTED",
                True,
                (255, 255, 255)
            )
        else:
            text = font.render(
                "CONNECTING...",
                True,
                (255, 255, 255)
            )

        screen.blit(text, (20, 20))

        pygame.display.flip()

        await asyncio.sleep(0)

        clock.tick(FPS)

    pygame.quit()


asyncio.run(main())
