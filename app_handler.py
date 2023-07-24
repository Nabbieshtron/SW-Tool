from constants import STATES
from main_menu import Main_menu
from program import Program
from settings import Settings


class AppHandler:
    def __init__(self):
        self.status = STATES.MENU
        self.old_status = STATES.MENU
        self.main_menu = Main_menu()
        self.program = Program()
        self.settings = Settings(self.main_menu, self.program)

    def set_status(self, status):
        self.old_status, self.status = self.status, status

    def revert_status(self):
        self.status, self.old_status = self.old_status, self.status

    def update(self):
        if self.status == STATES.INAPP:
            self.program.update()
        elif self.status == STATES.MENU:
            self.main_menu.update()
