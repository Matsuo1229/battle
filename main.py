import asyncio
import pygame


async def main():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygbag Test")

    clock = pygame.time.Clock()

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        pygame.draw.rect(
            screen,
            (50, 150, 255),
            (200, 200, 100, 100)
        )

        pygame.display.flip()

        await asyncio.sleep(0)

        clock.tick(60)

    pygame.quit()


asyncio.run(main())
