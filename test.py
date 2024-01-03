import pygame
from dataclasses import dataclass, field
from typing import Self

class ActivatableComponent:
    # You need Python >=3.11 to use this typehint. If you're on 3.10 or below use Optional["ActivatableComponent"] instead
    active_component: Self | None = None

    def activate(self):
        ActivatableComponent.active_component = self

    def deactivate(self):
        if ActivatableComponent.active_component is self:
            ActivatableComponent.active_component = None
            
    # def update(self):
        # if ActivatableComponent.active_component is self:
            # do whatever

@dataclass
class ListBox(ActivatableComponent):
    color_menu: list[str]
    color_option: list[str]
    rect: pygame.Rect
    font: pygame.Font
    options : list[str]
    amount_showed: int
    main: str = ''
    draw_menu: bool = field(init=False, default=False)
    menu_active: bool = field(init=False, default=False)
    active_option: int = field(init=False, default=-1)
    mscroll_y: int = field(init=False, default=0)
    
    def dispatch_events(self, e):
        if e.type == pygame.MOUSEWHEEL and self.draw_menu:
            # Only works if amount_showed elements in list
            if len(self.options) > self.amount_showed and abs(self.mscroll_y) < (len(self.options)-self.amount_showed):
                # Capping how much is scrolled, e.y returns value depending how fast wheel is moved
                if e.y < 0:
                    self.mscroll_y -=1
                else:
                    self.mscroll_y +=1
            
            # If List end is reached only allows to go up
            if abs(self.mscroll_y) == (len(self.options)-self.amount_showed) and e.y > 0:
                self.mscroll_y +=1
                
            # Blocking scrolling upwards
            if self.mscroll_y > 0:
                self.mscroll_y = 0
            
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos) and ActivatableComponent.active_component is None:
                self.mscroll_y = 0
                self.draw_menu = not self.draw_menu
                ActivatableComponent.activate(self)
            elif self.draw_menu and self.active_option >= 0:
                self.mscroll_y = 0
                self.draw_menu = False
                ActivatableComponent.deactivate(self)
                self.main = self.options[self.active_option]

    def update(self):
        if ActivatableComponent.active_component is self:
            mpos = pygame.mouse.get_pos()
            self.menu_active = self.rect.collidepoint(mpos)
        
            self.active_option = -1
            for i in range(len(self.options)):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                if rect.collidepoint(mpos):
                    self.active_option = i+abs(self.mscroll_y)
                    break

            if not self.menu_active and self.active_option == -1:
                ActivatableComponent.deactivate(self)
                self.draw_menu = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_menu[self.menu_active], self.rect)
        pygame.draw.rect(screen, 'Black', self.rect, 2, 1)
        
        if self.main in self.options:
            msg = self.font.render(self.main, 1, 'Black')
            screen.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options[abs(self.mscroll_y):self.amount_showed+abs(self.mscroll_y)]):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(screen, self.color_option[1 if i+abs(self.mscroll_y) == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                screen.blit(msg, msg.get_rect(center = rect.center))

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
lbox = ListBox(
        color_menu=['Pink', 'Light pink'],
        color_option=['Blue', 'Light blue'],
        rect=pygame.Rect(200,50,100,40),
        font=pygame.font.SysFont('Arial', 26, True),
        main='10',
        options=[str(x) for x in range(1,20)],
        amount_showed=5,
    )
lbox1 = ListBox(
        color_menu=['Pink', 'Light pink'],
        color_option=['Blue', 'Light blue'],
        rect=pygame.Rect(200,90,100,40),
        font=pygame.font.SysFont('Arial', 26, True),
        main='10',
        options=[str(x) for x in range(1,20)],
        amount_showed=5,
    )
    
while running:
    for event in pygame.event.get():
        lbox1.dispatch_events(event)
        lbox.dispatch_events(event)
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill("purple")
    
    lbox1.update()
    lbox.update()
    lbox1.draw(screen)
    lbox.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
    
