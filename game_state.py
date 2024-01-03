import pygame

from abc import ABC, abstractmethod
from types import SimpleNamespace

class GameState(ABC):
    def __init__(self, app, persist):
        """Initialize a game state."""
        self.app = app
        self.persist = persist if persist is not None else SimpleNamespace()
        self.font = pygame.font.Font(None)
        self.running = True

    def reset(self, persist=None):
        """Reset settings when re-running."""
        self.running = True
        if persist:
            self.persist = persist

    def dispatch_events(self, e):
        """Handle user events"""
        if (e.type == pygame.QUIT or
                e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            self.running = False

    @abstractmethod
    def update(self, dt):
        """Update frame by delta time dt."""
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen):
        """Draw current frame to surface screen."""
        raise NotImplementedError