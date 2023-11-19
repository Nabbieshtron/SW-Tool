import pygame
import json
from constants import DISPLAY_SIZES


class App:
    def __init__(self, title, screen, fps):
        """Initialize the app framework."""
        self.title = title
        self.screen = None
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

        self._states = None
        self._state = None
        self._state_stack = []
        self._dt_max = 3 / fps

        pygame.init()

    def next_state(self, state, persist):
        """Switch state.

        If the new state is None, return to a previously stacked state, if one
        exists, otherwise end the app.
        """
        # If we don't have a follow up state, but there are states in the
        # stack, continue these, otherwise finish the game loop.
        if state is None:
            if self._state_stack:
                self._state = self._state_stack.pop()
                return
            else:
                self.running = False
                return

        # We do have a follow up state
        self._state = self._states[state]
        self._state.reset(persist)
    
    def set_window(self, state:str, resizable=False):
        if self._state == self._states[state]:
            if resizable:
                self.screen = pygame.display.set_mode(DISPLAY_SIZES[state], pygame.RESIZABLE)
            else:
                self.screen = pygame.display.set_mode(DISPLAY_SIZES[state])

    def save_to_disk(self, data, path):
        with open(path, 'r') as file:
            try:
                old = json.load(file)
                old.update(data)
            except json.JSONDecodeError:
                old = data
        
        with open(path, 'w') as file:
            json.dump(old, file, indent=4)
        
    def load_from_disk(self, path):
        pass
        
    def dispatch_events(self):
        """Delegate events to current state."""
        for e in pygame.event.get():
            self._state.dispatch_event(e)

    def update(self, dt):
        """Call update method of current state.

        If the current state running property is False, exit the app.

        If the current state returns a tuple of (next_state, persist), switch
        states.
        """
        res = self._state.update(dt)

        if not self._state.running:
            self.running = False
            return

        if res:
            next_state, persist = res
            self.next_state(next_state, persist)

    def draw(self):
        """Call draw method of current state."""
        self._state.draw(self.screen)

    def run(self, state, states):
        """The game loop."""

        self._states = states
        self._state = self._states[state]
        
        # Set window size
        self.set_window('main_menu', True)
        
        while self.running:
            dt = min(self.clock.tick(self.fps) / 1000.0, self._dt_max)

            self.dispatch_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()

    def push(self, substate):
        """push the current state onto the stack, run the new one.

            self.persist.state.push(pause_screen)

        once the sub state finishes, control is returned to the previous state.
        persist is merged to provide results.
        """

        self._state_stack.append(self._state)
        self._state = substate