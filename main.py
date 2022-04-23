import pygame
from wave_function import WaveFunction


def main():
    pygame.init()
    pygame.display.set_caption("Wave Function Collapse")
    screen = pygame.display.set_mode((900, 900))

    wave = WaveFunction(25, 25)
    while not wave.has_collapsed:
        wave.collapse()
        wave.draw(screen)
        pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    screen.fill((0, 0, 0))
                    wave = WaveFunction(25, 25)
                    while not wave.has_collapsed:
                        wave.collapse()
                        wave.draw(screen)
                        pygame.display.update()


if __name__ == '__main__':
    main()
