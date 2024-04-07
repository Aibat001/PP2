import pygame, sys
import math

# general game configueration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
objects = []

# color pallete
colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255)
}
current_color = colors['black']

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameObject:
    def update(self, curr_point):
        return

    def draw(self):
        return

class RectButton(GameObject):
    def __init__(self):
        self.width = 50
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - self.width // 2, 20, self.width, self.width)
        self.isButton = True
        self.tool = Rectangle

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 0, 0), self.rect, width=5)

class CircleButton(GameObject):
    def __init__(self):
        self.radius = 25
        self.rect = pygame.draw.circle(screen, (255, 0, 0), (SCREEN_WIDTH // 2 + 3 * self.radius, self.radius + 20),
                                       self.radius)
        self.isButton = True
        self.tool = Circle

    def draw(self, surf):
        pygame.draw.circle(screen, (255, 0, 0), (SCREEN_WIDTH // 2 + 3 * self.radius, self.radius + 20), self.radius,
                           width=5)


# class for Brush button
class BrushButton(GameObject):
    def __init__(self):
        self.width = 50
        self.image = pygame.transform.scale(pygame.image.load('TSIS_8/resources/brush.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topright = (SCREEN_HEIGHT // 2 + self.width, 20)
        self.isButton = True
        self.tool = Pen

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class EraserButton(GameObject):
    def __init__(self):
        self.width = 50
        self.image = pygame.transform.scale(pygame.image.load('TSIS_8/resources/eraser.png'), (self.width, self.width))
        self.rect = self.image.get_rect()
        self.rect.topright = (SCREEN_HEIGHT // 2 + 5.5 * self.width, 20)
        self.isButton = True
        self.tool = Eraser

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class ColorButton(GameObject):
    def __init__(self, *args, **kwargs):
        self.width = 20
        self.color = kwargs['color']
        self.rect = pygame.Rect(*kwargs['pos'], self.width, self.width)

    def draw(self, surf):
        pygame.draw.rect(surf, colors[self.color], self.rect)

class Pen(GameObject):
    def __init__(self, *args, **kwargs):
        self.points: list(Point, ...) = []
        self.image = pygame.transform.scale(pygame.image.load('TSIS_8/resources/brush.png'), (40, 40))
        self.pos = pygame.mouse.get_pos()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos
        self.color = current_color

    def draw(self, surf, *args, **kwargs):
        for id, curr_point in enumerate(self.points[:-1]):
            next_point = self.points[id + 1]
            pygame.draw.line(surf, self.color,
                             (curr_point.x, curr_point.y), (next_point.x, next_point.y), width=5)

    def update(self, curr_point):
        self.points.append(Point(*curr_point))
        self.rect.bottomleft = curr_point
        screen.blit(self.image, self.rect)

class Rectangle(GameObject):
    def __init__(self, init_point, *args, **kwargs):
        self.start_point = Point(*init_point)
        self.end_point = Point(*init_point)
        self.color = current_color
        self.rect = pygame.Rect(self.start_point.x, self.start_point.y, 0, 0)

    def draw(self, surf, *args, **kwargs):
        start_point_x = min(self.start_point.x, self.end_point.x)
        start_point_y = min(self.start_point.y, self.end_point.y)

        end_point_x = max(self.start_point.x, self.end_point.x)
        end_point_y = max(self.start_point.y, self.end_point.y)

        self.rect = pygame.draw.rect(surf, self.color, (start_point_x, start_point_y, end_point_x - start_point_x, end_point_y - start_point_y), width=5)

    def update(self, curr_point):
        self.end_point.x, self.end_point.y = curr_point

class Circle(GameObject):
    def __init__(self, init_point, *args, **kwargs):
        self.center_point = Point(*init_point)
        self.radius = 0
        self.rect = pygame.draw.circle(screen, (0, 0, 0), init_point, self.radius, width=5)
        self.color = current_color

    def draw(self, surf, *args, **kwargs):
        self.rect = pygame.draw.circle(surf, self.color, (self.center_point.x, self.center_point.y), self.radius,
                                       width=5)

    def update(self, curr_point):
        self.radius = math.fabs(curr_point[0] - self.center_point.x)


# class for Eraser tool
class Eraser(GameObject):
    def __init__(self, *args, **kwargs):
        self.pos = pygame.mouse.get_pos()
        self.image = pygame.transform.scale(pygame.image.load('TSIS_8/resources/eraser.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos

    def draw(self, surf):
        for i, obj in enumerate(objects):
            if not hasattr(obj, 'isButton'):
                if obj.rect.collidepoint(self.pos):
                    objects.remove(obj)
                if hasattr(obj, 'points'):
                    for point in obj.points:
                        if self.rect.collidepoint(point.x, point.y):
                            obj.points = []
        return objects

    def update(self, curr_point):
        self.pos = curr_point
        self.rect.bottomright = self.pos
        screen.blit(self.image, self.rect)


def main():
    global objects
    global current_color
    game_obj = GameObject()
    active_obj = game_obj
    curr_shape = Pen
    rect_button = RectButton()
    circle_button = CircleButton()
    eraser_button = EraserButton()
    brush_button = BrushButton()
    red_button = ColorButton(color='red', pos=(100, 20))
    blue_button = ColorButton(color='blue', pos=(120, 20))
    green_button = ColorButton(color='green', pos=(100, 40))
    black_button = ColorButton(color='black', pos=(120, 40))
    objects = [rect_button, circle_button, eraser_button, brush_button, red_button, blue_button, green_button,
               black_button]

    menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 4))

    # main game cycle
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mouse.set_visible(False)

                if rect_button.rect.collidepoint(pygame.mouse.get_pos()):
                    curr_shape = Rectangle
                elif circle_button.rect.collidepoint(pygame.mouse.get_pos()):
                    curr_shape = Circle
                elif eraser_button.rect.collidepoint(pygame.mouse.get_pos()):
                    curr_shape = Eraser
                elif brush_button.rect.collidepoint(pygame.mouse.get_pos()):
                    curr_shape = Pen
                elif red_button.rect.collidepoint(pygame.mouse.get_pos()):
                    current_color = colors[red_button.color]
                elif blue_button.rect.collidepoint(pygame.mouse.get_pos()):
                    current_color = colors[blue_button.color]
                elif green_button.rect.collidepoint(pygame.mouse.get_pos()):
                    current_color = colors[green_button.color]
                elif black_button.rect.collidepoint(pygame.mouse.get_pos()):
                    current_color = colors[black_button.color]
                else:
                    active_obj = curr_shape(init_point=pygame.mouse.get_pos())
                    objects.append(active_obj)

            if event.type == pygame.MOUSEMOTION:
                active_obj.update(curr_point=pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                active_obj = game_obj
                pygame.mouse.set_visible(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    current_color = colors['red']
                if event.key == pygame.K_b:
                    current_color = colors['black']
                if event.key == pygame.K_g:
                    current_color = colors['green']

            for obj in objects:
                if obj == Eraser:
                    objects = obj.draw(screen)
                else:
                    obj.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    main()