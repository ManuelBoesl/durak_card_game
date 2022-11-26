import arcade

from gui.screen_configuration import ScreenConfiguration
from gui.views.difficulty_level import DifficultyView
from gui.views.rules_screen import RulesView
from gui.views.start_screen import MenuView
from gui.views.views import GameView

from gui.views.win_lose_screen import WinLoseView


class ViewManager(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(ViewManager, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.view = None
        self.config = ScreenConfiguration()
        self.__rules_view = RulesView(self.config)

    def show_game_view(self, difficulty):
        arcade.get_window().show_view(GameView(self.config, difficulty))

    def show_rules_view(self):
        arcade.get_window().show_view(self.__rules_view)

    def show_difficulty_view(self):
        arcade.get_window().show_view(DifficultyView(self.config))

    def show_menu_view(self):
        arcade.get_window().show_view(MenuView(self.config))

    # def show_win_view(self):
    #     arcade.get_window().show_view(WinView(self.config))
    #
    # def show_lose_view(self):
    #     arcade.get_window().show_view(LoseView(self.config))

    def show_win_lose_view(self, status):
        arcade.get_window().show_view(WinLoseView(self.config, status))


