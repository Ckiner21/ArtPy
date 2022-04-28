from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import pygame
import buttons
import brush


pygame.init()


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(100, 100, 100)
RED = pygame.Color(255, 0, 0)
PINK = pygame.Color(255, 66, 142)
ORANGE = pygame.Color(255, 111, 0)
YELLOW = pygame.Color(238, 255, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
PURPLE = pygame.Color(162, 0, 255)
all_colors = [BLACK, WHITE, RED, PINK, ORANGE,
             YELLOW, GREEN, BLUE, PURPLE, GREY]


#Create main surface, button pannel
SCR_WIDTH = SCR_HEIGHT = 600
BP_WIDTH = SCR_WIDTH
BP_HEIGHT = SCR_HEIGHT//5
screen = pygame.display.set_mode(size=(SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption("ArtPy by Christian Kiner")
icon = pygame.image.load("Sprites/icon.png").convert_alpha()
pygame.display.set_icon(icon)
button_panel = pygame.Rect((0, SCR_HEIGHT-BP_HEIGHT), (BP_WIDTH, BP_HEIGHT))
canvas = pygame.Surface((SCR_WIDTH, SCR_HEIGHT-BP_HEIGHT))
clock = pygame.time.Clock()
main_brush = brush.Brush()
screen.fill(WHITE)
canvas.fill(WHITE)
pygame.draw.rect(screen, GREY, button_panel)


def set_color(brush_obj: brush.Brush, color: pygame.Color) -> None:
    brush_obj.color = color


def set_radius(brush_obj: brush.Brush, delta_radius: int) -> None:
    new_radius = brush_obj.radius + delta_radius
    if new_radius >= 5 and new_radius <= 30:
        brush_obj.radius = new_radius


def reset_canvas(canvas: pygame.Surface) -> None:
    canvas.fill(WHITE)


# Center buttons on BP
all_buttons = []
BTN_SIZE = (30, 30)
BTN_HEIGHT = SCR_HEIGHT-(BP_HEIGHT//2)-(BTN_SIZE[0]//2)
SPACING = int(1.5 * BTN_SIZE[0])
OFFSET = int((BP_WIDTH - (SPACING * (len(all_colors)+2))) // 2)


# Initialize color buttons
for i, color in enumerate(all_colors[:-1]):
    button = buttons.Button(size=BTN_SIZE, color=color,
                            func=set_color, click_args=[main_brush, color])
    button.draw(screen, (OFFSET+(SPACING*i), BTN_HEIGHT))
    all_buttons.append(button)


# Initialize brush radius buttons
inc_radius = buttons.Button(size=BTN_SIZE, func=set_radius,
                            sprite="Sprites/plus.png",
                            click_args=[main_brush, 5])
inc_radius.draw(screen, (OFFSET+(SPACING*len(all_buttons)), BTN_HEIGHT))
all_buttons.append(inc_radius)
dec_radius = buttons.Button(size=BTN_SIZE, func=set_radius,
                            sprite="Sprites/minus.png",
                            click_args=[main_brush, -5])
dec_radius.draw(screen, (OFFSET+(SPACING*len(all_buttons)), BTN_HEIGHT))
all_buttons.append(dec_radius)


reset = buttons.Button(size=BTN_SIZE, func=reset_canvas,
                       sprite="Sprites/reset.png", click_args=[canvas])
reset.draw(screen, (OFFSET+(SPACING*len(all_buttons)), BTN_HEIGHT))
all_buttons.append(reset)


def main():
    pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
    drawing = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                button = buttons.clicked(all_buttons, event.pos)
                if button is not None:
                    button.click()
                else:
                    drawing = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                drawing = False

        if drawing:
            mouse_pos = pygame.mouse.get_pos()
            if button_panel.collidepoint(mouse_pos) == False:
                pygame.draw.circle(canvas, main_brush.color,
                                    mouse_pos, main_brush.radius)

        screen.blit(canvas, (0,0))
        pygame.display.flip()
        clock.tick(60)


main()
