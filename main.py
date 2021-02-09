import random

import numpy
import pygame
import Dot
from Population import Population

pygame.font.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lapirynt")

FPS = 60

CYAN = (90, 90, 200)
BLUE = (0, 0, 255)
YELLOW = (200, 200, 0)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

MIN_SPACE_WIDTH = 40
MAX_SPACE_WIDTH = 100
MIN_OBSTACLE_WIDTH = 100
MAX_OBSTACLE_WIDTH = 350
OBSTACLE_HEIGHT = 30

DEAD = pygame.USEREVENT + 1

INITIAL_VEL = 2
INITIAL_OBS_VEL = 1

OBS = "OBSTACLES"
CHCK = "CHECKPOINTS"

LEVEL = 30

GEN_FONT = pygame.font.SysFont('comicsans', 20)
MODE_FONT = pygame.font.SysFont('comicsans', 30)

goal = pygame.Rect(WIDTH // 2 - 10, 50, 20, 20)


def draw_window(obstacles, checkpoints, mode, gen):
    draw_mode = MODE_FONT.render("mode: " + mode, 1, WHITE)
    draw_gen = GEN_FONT.render("generation: " + str(gen), 1, WHITE)
    WIN.fill(CYAN)
    for obs in obstacles:
        pygame.draw.rect(WIN, GREY, obs)

    for check in checkpoints:
        pygame.draw.rect(WIN, BLUE, check)

    WIN.blit(draw_mode, (WIDTH - draw_mode.get_width() - 10,
                         HEIGHT - MODE_FONT.get_height() - GEN_FONT.get_height() - 20))
    WIN.blit(draw_gen, (WIDTH - draw_gen.get_width() - 10,
                        HEIGHT - GEN_FONT.get_height() - 20))
    pygame.draw.rect(WIN, RED, goal)


def generate_obstacles():

    obstacles = [
        pygame.Rect(WIDTH / 2 - 100, HEIGHT - 150, 200, 20),
        pygame.Rect(100, HEIGHT - 300, 350, 20),
        pygame.Rect(0, HEIGHT - 400, 570, 20),
        pygame.Rect(150, 150, 570, 20),
        pygame.Rect(570, HEIGHT - 400, 20, 100),
        pygame.Rect(450, HEIGHT - 300, 20, 170),
        pygame.Rect(WIDTH / 2 - 100, HEIGHT - 220, 20, 70),
        pygame.Rect(0, HEIGHT - 200, 250, 20),
        pygame.Rect(WIDTH - 250, HEIGHT - 200, 250, 20),
        pygame.Rect(WIDTH / 2 - 100, HEIGHT - 150, 200, 20),
        pygame.Rect(WIDTH / 2 - 100, HEIGHT - 150, 200, 20),
        pygame.Rect(WIDTH / 2 - 100, HEIGHT - 150, 200, 20),
        pygame.Rect(WIDTH / 2 - 100, HEIGHT - 150, 200, 20),
        pygame.Rect(WIDTH / 2 - 100, HEIGHT - 150, 200, 20),


                 ]

    return obstacles


def handle_obstacles(obs_levels, player, vel):
    for obs in obs_levels:
        for o in obs:
            o.y += vel

            if o.colliderect(player):
                pygame.event.post(pygame.event.Event(DEAD))

            if o.y > HEIGHT:
                obs_levels.remove(obs)
                break


def start_shape():
    return numpy.add(pygame.mouse.get_pos(), (0, 0))


def end_shape(shapes, new_shape_pos):
    empty_space = True
    for obs in shapes:
        if obs.colliderect(
                pygame.Rect(pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10, 20, 20)):
            shapes.remove(obs)
            empty_space = False
    if empty_space:
        mouse_pos = numpy.add(pygame.mouse.get_pos(), (0, 0))
        if abs(mouse_pos[0] - new_shape_pos[0]) > abs(mouse_pos[1] - new_shape_pos[1]):
            if mouse_pos[0] < new_shape_pos[0]:
                shapes.append(
                    pygame.Rect(mouse_pos[0], new_shape_pos[1], abs(mouse_pos[0] - new_shape_pos[0]),
                                20))
            else:
                shapes.append(
                    pygame.Rect(new_shape_pos[0], new_shape_pos[1],
                                abs(mouse_pos[0] - new_shape_pos[0]), 20))
        else:
            if mouse_pos[1] < new_shape_pos[1]:
                shapes.append(pygame.Rect(mouse_pos[0], mouse_pos[1],
                                          20, abs(mouse_pos[1] - new_shape_pos[1])))
            else:
                shapes.append(pygame.Rect(new_shape_pos[0], new_shape_pos[1],
                                          20, abs(mouse_pos[1] - new_shape_pos[1])))


def main():
    clock = pygame.time.Clock()
    # obstacles = []
    obstacles = generate_obstacles()
    checkpoints = []
    checkpoints_all = checkpoints
    test = Population(1000)

    run = True
    pause = True
    mode = OBS

    new_obstacle_pos = [0, 0]
    new_checkpoint_pos = [0, 0]

    draw_window(obstacles, checkpoints, mode, test.gen)
    pygame.display.update()
    while run:
        clock.tick(FPS)

        if test.allDotsDead():
            print("all dead - creating new gen")
            # generic algorithm
            test.calculateFitness()
            test.naturalSelection()
            test.mutation()
            checkpoints = checkpoints_all.copy()
        else:
            draw_window(obstacles, checkpoints, mode, test.gen)
            if not pause:
                test.update(obstacles, checkpoints)
            test.show()
            pygame.display.update()
        # loop += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause

                if event.key == pygame.K_m:
                    if mode == OBS:
                        mode = CHCK
                    else:
                        mode = OBS

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == OBS:
                    new_obstacle_pos = start_shape()
                else:
                    new_checkpoint_pos = start_shape()

            if event.type == pygame.MOUSEBUTTONUP:
                if mode == OBS:
                    end_shape(obstacles, new_obstacle_pos)
                else:
                    end_shape(checkpoints, new_checkpoint_pos)
                    checkpoints_all = checkpoints.copy()
                    print(len(checkpoints_all))

        #
        #     if event.type == DEAD:
        #         game_over(level)
        #         run = False
        #         break
        #
        # if obstacles[0].y > 400:
        #     level += 1
        #
        #     obstacles = generate_obstacles()
        #     obs_levels.append(obstacles)
        #
        # if loop % 1500 == 0:
        #     obs_vel += 1
        #     player_vel += 1
        #
        # keys_pressed = pygame.key.get_pressed()
        # handle_movement(player, keys_pressed, player_vel)
        #
        # if loop > 300:
        #     direction = aiify(player, player_vel, obs_levels)
        #     if direction != "":
        #         move(direction, player, player_vel)
        #
        # handle_obstacles(obs_levels, player, obs_vel)
        #
        # if run:
        #     draw_window(player, obs_levels, level)


if __name__ == "__main__":
    main()
