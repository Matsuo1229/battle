import asyncio
import json
import pygame

from javascript import WebSocket
from pyodide.ffi import create_proxy


# =========================
# Cloudflare Worker
# =========================

SERVER_URL = "wss://my-online-game.my-647.workers.dev"


# =========================
# Pygame
# =========================

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Online Battle")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)


# =========================
# プレイヤー
# =========================

my_x = 200
my_y = 250

enemy_x = 600
enemy_y = 250

speed = 5

connected = False


# =========================
# WebSocket
# =========================

ws = WebSocket.new(SERVER_URL)


def websocket_open(event):
    global connected

    connected = True
    print("WebSocket connected")

    # 最初の位置を送信
    send_position()


def websocket_error(event):
    global connected

    connected = False
    print("WebSocket error")


def websocket_close(event):
    global connected

    connected = False
    print("WebSocket closed")


def websocket_message(event):
    global enemy_x
    global enemy_y

    try:
        data = json.loads(str(event.data))

        # 相手の座標
        if data.get("type") == "position":

            # 自分のメッセージを受け取った場合は無視
            if data.get("player") == "me":
                return

            enemy_x = int(data["x"])
            enemy_y = int(data["y"])

            print("Enemy:", enemy_x, enemy_y)

    except Exception as e:
        print("Receive error:", e)


# JavaScriptのイベントにPython関数を登録
open_proxy = create_proxy(websocket_open)
error_proxy = create_proxy(websocket_error)
close_proxy = create_proxy(websocket_close)
message_proxy = create_proxy(websocket_message)

ws.onopen = open_proxy
ws.onerror = error_proxy
ws.onclose = close_proxy
ws.onmessage = message_proxy


# =========================
# 座標送信
# =========================

def send_position():

    if not connected:
        return

    try:

        data = {
            "type": "position",
            "player": "me",
            "x": my_x,
            "y": my_y
        }

        ws.send(json.dumps(data))

    except Exception as e:

        print("Send error:", e)


# =========================
# メインループ
# =========================

async def main():

    global my_x
    global my_y

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

        if keys[pygame.K_w]:
            my_y -= speed

        if keys[pygame.K_s]:
            my_y += speed

        if keys[pygame.K_a]:
            my_x -= speed

        if keys[pygame.K_d]:
            my_x += speed


        # 画面外に出ないようにする

        my_x = max(0, min(750, my_x))
        my_y = max(0, min(550, my_y))


        # -------------------------
        # 座標を送信
        # -------------------------

        send_timer += 1

        if send_timer >= 3:

            send_position()

            send_timer = 0


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
            (255, 70, 70),
            (enemy_x, enemy_y, 50, 50)
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


        # Pygbagでは重要
        await asyncio.sleep(0)

        clock.tick(60)


    ws.close()

    pygame.quit()


# =========================
# 起動
# =========================

asyncio.run(main())
