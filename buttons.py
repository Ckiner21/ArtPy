import pygame


class Button:
    def __init__(self, name=None, sprite=None, size=None, color=None,
            func=None, click_args=None, click_kwargs=None, **kwargs):
        if sprite is not None:
            self.sprite = pygame.image.load(sprite)
            if sprite.endswith(".png"):
                self.sprite = self.sprite.convert_alpha()
            if size is None:
                size = self.sprite.get_size()
            self.sprite = pygame.transform.scale(self.sprite, size)
        else:
            self.sprite = pygame.Surface(size)
            if color is not None:
                self.sprite.fill(color)

        self.rect = self.sprite.get_rect()
        self.name = name
        self.color = color
        self.func = func
        self.args = click_args
        self.kwargs = click_kwargs

    def draw(self, surface, dest=(0,0)):
        surface.blit(self.sprite, dest)
        self.rect.left, self.rect.top = dest

    def click(self, *args, **kwargs):
        click_args = args
        click_kwargs = kwargs
        if self.func is not None:
            if self.args is not None:
                click_args = self.args
            if self.kwargs is not None:
                click_kwargs = self.kwargs
            return_val = self.func(*click_args, **click_kwargs)
            if return_val is not None:
                return return_val


def clicked(button_list, point) -> int:
    if type(button_list) == Button:  # Allows user to pass either one button or a list
        button_list = [button_list]
    for button in button_list:
        if button.rect.collidepoint(point):
            return button
    return None
