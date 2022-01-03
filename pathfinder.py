import pygame
import sys
from math import sqrt, floor
from collections import Counter

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 800))
font = pygame.font.SysFont("arial", bold=True, size=30)

visited = []
visited_objects = []

mover_coords = []
goal_reached = False
final_path_coords = []
visual_path_coords = []
winner = None

width_squares = 50
gap = 800 / width_squares

current_blue = 50


class Visited:

    def __init__(self, x, y, blue):
        self.x = x
        self.y = y
        self.blue = blue
        self.width= gap/3

    def draw(self):
        self.width -= 0.1
        pygame.draw.circle(screen, (0, 0, self.blue), (self.x+gap/2, self.y+gap/2), self.width)


def dist(x1, y1, x2, y2):

    return sqrt((x1-x2)**2 + (y1-y2)**2)


class Goal:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.goal = pygame.Rect(self.x, self.y, gap, gap)
        self.follow_mouse = False

    def draw(self):
        if self.follow_mouse:
            mx, my = pygame.mouse.get_pos()
            mx = floor(mx / gap) * gap
            my = floor(my / gap) * gap

            self.x = mx
            self.y = my

        self.goal = pygame.Rect(self.x, self.y, gap, gap)
        pygame.draw.rect(screen, (0, 180, 0), self.goal)

    def click(self):
        mx, my = pygame.mouse.get_pos()
        mx = floor(mx / gap) * gap
        my = floor(my / gap) * gap

        if self.goal.collidepoint(mx, my):
            self.follow_mouse = not self.follow_mouse


class Start:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start = pygame.Rect(self.x, self.y, gap, gap)
        self.follow_mouse = False

    def draw(self):
        if self.follow_mouse:
            mx, my = pygame.mouse.get_pos()
            mx = floor(mx / gap) * gap
            my = floor(my / gap) * gap

            self.x = mx
            self.y = my

        self.start = pygame.Rect(self.x, self.y, gap, gap)
        pygame.draw.polygon(screen, (0, 0, 200), [(self.x, self.y), (self.x + gap, self.y + gap / 2), (self.x, self.y + gap)], 5)

    def click(self):
        mx, my = pygame.mouse.get_pos()
        mx = floor(mx / gap) * gap
        my = floor(my / gap) * gap

        if self.start.collidepoint(mx, my):
            self.follow_mouse = not self.follow_mouse


class Mover:

    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.width = gap
        self.height = gap
        self.mover = pygame.Rect(self.x, self.y, self.width, self.height)
        self.path_coords = []
        self.found = False
        self.created = False
        self.childs = []
        self.parent = parent

    def track_path(self):
        self.path_coords.append((self.x, self.y))
        if self.parent is not None:
            self.path_coords += self.parent.track_path()

        return self.path_coords

    def move(self):
        global goal_reached, winner, coord_counts
        if (self.x, self.y) == (goal.x, goal.y):
            self.found = True
            goal_reached = True
            winner = self

        if not goal_reached:

            if not self.created:
                if self.y > 0:
                    ux, uy = self.x, self.y - gap
                    coord_counts = Counter(mover_coords)

                    if (ux, uy) not in obs_coords and coord_counts[(ux, uy)] < 1:
                        m = Mover(ux, uy, self)
                        mover_list.append(m)
                        self.childs.append(m)
                        mover_coords.append((ux, uy))
                        if (ux, uy) not in visited:
                            visited.append((ux, uy))
                            visited_objects.append(Visited(ux, uy, current_blue))

                if self.y < 800 - gap:
                    dx, dy = self.x, self.y + gap

                    if (dx, dy) not in obs_coords and coord_counts[(dx, dy)] < 1:
                        m = Mover(dx, dy, self)
                        mover_list.append(m)
                        self.childs.append(m)
                        mover_coords.append((dx, dy))
                        if (dx, dy) not in visited:
                            visited.append((dx, dy))
                            visited_objects.append(Visited(dx, dy, current_blue))

                if self.x > 0:
                    lx, ly = self.x - gap, self.y

                    if (lx, ly) not in obs_coords and coord_counts[(lx, ly)] < 1:
                        m = Mover(lx, ly, self)
                        mover_list.append(m)
                        self.childs.append(m)
                        mover_coords.append((lx, ly))
                        if (lx, ly) not in visited:
                            visited.append((lx, ly))
                            visited_objects.append(Visited(lx, ly, current_blue))

                if self.x < 800 - gap:
                    rx, ry = self.x + gap, self.y

                    if (rx, ry) not in obs_coords and coord_counts[(rx, ry)] < 1:
                        m = Mover(rx, ry, self)
                        mover_list.append(m)
                        self.childs.append(m)
                        mover_coords.append((rx, ry))
                        if (rx, ry) not in visited:
                            visited.append((rx, ry))
                            visited_objects.append(Visited(rx, ry, current_blue))

                self.created = True


class Obs:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.obs = pygame.Rect(self.x, self.y, gap, gap)

    def draw(self):
        self.obs = pygame.Rect(self.x, self.y, gap, gap)
        pygame.draw.rect(screen, (0, 0, 0), self.obs)

    def delete(self):
        mx, my = pygame.mouse.get_pos()

        if self.obs.collidepoint(mx, my):
            obs_coords.remove((self.x, self.y))
            obs_list.remove(self)
            return True

        return False


dest_x, dest_y = 800 - gap, 800 - gap

start = False
obs_list = []
obs_coords = []

tracked = False
pressing_down = False
pressing_down_right = False

goal = Goal(dest_x, dest_y)
start_obj = Start(0, 0)

start_x = 0
start_y = 0

"""BUTTONS"""

button_reset = pygame.Rect(850, 150, 100, 50)
button_set_start = pygame.Rect(850, 250, 100, 50)


def reset():
    global start, goal_reached, current_blue, mover_list, tracked, start_obj, goal
    start = False
    goal_reached = False
    tracked = False
    current_blue = 50

    goal = Goal(dest_x, dest_y)
    start_obj = Start(0, 0)

    mover_coords.clear()

    final_path_coords.clear()
    visual_path_coords.clear()
    visited_objects.clear()
    visited.clear()

    obs_list.clear()
    obs_coords.clear()


while True:

    """CHANGING THE STARTING POINT IN MOVER LIST"""

    if not start:
        mover_list = [Mover(start_obj.x, start_obj.y, None)]

    coord_counts = Counter(mover_coords)
    mover_list.reverse()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                pressing_down = False

            elif e.button == 3:
                pressing_down_right = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                pressing_down = True

                """GETTING GOAL AND STARTING POINT TO FOLLOW MOUSE"""
                goal.click()
                start_obj.click()

                """PRESSING BUTTONS"""
                x, y = pygame.mouse.get_pos()

                if button_reset.collidepoint(x, y):
                    reset()

                if button_set_start.collidepoint(x, y):
                    start = True

            elif e.button == 3 and not goal_reached:
                # mx, my = pygame.mouse.get_pos()
                # mx = floor(mx / gap) * gap
                # my = floor(my / gap) * gap
                #
                # goal.x = mx
                # goal.y = my

                pressing_down_right = True

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                start = True

            if e.key == pygame.K_ESCAPE and not start and len(obs_list) > 0:
                obs_list.pop(-1)
                obs_coords.pop(-1)

    screen.fill((255, 255, 255))

    if pressing_down:
        mx, my = pygame.mouse.get_pos()
        mx = floor(mx / gap) * gap
        my = floor(my / gap) * gap

        if (mx, my) not in obs_coords and not start and mx < 800 and (mx, my) != (start_x, start_y) and (mx, my) != (goal.x, goal.y) and (mx, my) != (start_obj.x, start_obj.y):
            obs_list.append(Obs(mx, my))
            obs_coords.append((mx, my))

    elif pressing_down_right:

        for obs in obs_list:
            if obs.delete():
                break

    """DRAW OBS"""

    for obs in obs_list:
        obs.draw()

    """DRAW LINES"""

    xx = gap
    yy = gap

    for i in range(width_squares - 1):
        pygame.draw.line(screen, (0, 0, 0), (xx, 0), (xx, 800))
        pygame.draw.line(screen, (0, 0, 0), (0, yy), (800, yy))

        xx += gap
        yy += gap

    """VISITED SQUARES"""

    if not goal_reached:
        for obj in visited_objects:
            obj.draw()

    """GOAL AND START"""

    goal.draw()
    start_obj.draw()

    """MOVERS"""

    og_count = len(mover_list) - 1

    if start:
        for count, mover in enumerate(mover_list):
            if not goal_reached:
                mover.move()
            if count >= og_count:
                break

    if goal_reached and not tracked:
        final_path_coords = winner.track_path()
        tracked = True
        final_path_coords.reverse()

    if tracked and len(final_path_coords) > 0:
        visual_path_coords.append(final_path_coords.pop(0))

    if goal_reached:
        for coord in visual_path_coords:
            pygame.draw.rect(screen, (0, 180, 0), (coord[0], coord[1], round(gap), round(gap)))

    """DRAWIG BUTTONS"""

    pygame.draw.rect(screen, (0, 200, 0), button_reset)
    text = font.render("Reset", True, (0, 0, 0))
    screen.blit(text, (button_reset.x + 15, button_reset.y + 8))

    pygame.draw.rect(screen, (0, 200, 0), button_set_start)
    text = font.render("Find", True, (0, 0, 0))
    screen.blit(text, (button_set_start.x + 20, button_set_start.y + 8))

    if start:
        clock.tick(round(width_squares/2))

    current_blue += 2
    current_blue = min(255, current_blue)

    pygame.display.flip()
