import arcade

from computer_card_sprites_area import ComputerCardSpritesArea
from main_card_sprites_playing_area import MainCardSpritesPlayingArea
from players_card_sprites_area import PlayersCardSpritesArea


class Utils:

    def __init__(self, player: PlayersCardSpritesArea, computer: ComputerCardSpritesArea,
                 main: MainCardSpritesPlayingArea):
        self.player = player
        self.computer = computer
        self.main = main

    def list_all_mats(self):
        # add all the mats to a list
        all_mats = arcade.SpriteList()
        all_mats.extend(self.player.pile_mat_list)
        all_mats.extend(self.computer.pile_mat_list)
        all_mats.extend(self.main.pile_mat_list)
        return all_mats

    def list_all_usable_mats(self):
        # add all the mats to a list
        all_mats = arcade.SpriteList()
        all_mats.extend(self.player.pile_mat_list)
        all_mats.extend(self.main.pile_mat_list)
        return all_mats

    def list_all_active_cards(self):
        all_cards = [self.player.cards, self.computer.cards, self.main.cards]
        return all_cards
