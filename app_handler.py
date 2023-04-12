from main_menu import Main_menu
from program import Program
from settings import Settings
from enum import Enum


class App_handler:
    status = Enum("status", ["MENU", "INAPP", "SETTINGS"])

    def __init__(self):
        self.status = App_handler.status.MENU
        self.old_status = App_handler.status.MENU
        self.main_menu = Main_menu()
        self.program = Program()
        self.settings = Settings(self.main_menu, self.program)

    def set_status(self, status):
        self.old_status, self.status = self.status, status

    def revert_status(self):
        self.status, self.old_status = self.old_status, self.status

    def update(self):
        if self.status == App_handler.status.INAPP:
            self.program.update()
        elif self.status == App_handler.status.MENU:
            self.main_menu.update()
