from Constants import EASY, MEDIUM, HARD
from game_logic.strategies.difficult_strategy import DifficultStrategy
from game_logic.strategies.medium_strategy import MediumStrategy
from game_logic.strategies.simple_strategy import SimpleStrategy
from game_logic.strategies.strategycontext import StrategyContext
from play_areas.playground import Playground
from play_areas.not_active_cards import NotActiveCards
from play_areas.player_area import PlayerArea
from Constants import WIN, LOSE


class GameLogic:
    def __init__(self, player: PlayerArea, computer: PlayerArea,
                 main: Playground, not_active_cards: NotActiveCards, difficulty: int):
        self.player = player
        self.computer = computer
        self.playground = main
        self.not_active_cards = not_active_cards
        self.strategy = None
        if difficulty == EASY:
            self.strategy = SimpleStrategy(computer, main, not_active_cards, player)
        elif difficulty == MEDIUM:
            self.strategy = MediumStrategy(computer, main, not_active_cards, player)
        elif difficulty == HARD:
            self.strategy = DifficultStrategy(computer, main, not_active_cards, player)
        self.strategy_context = StrategyContext(self.strategy, self.playground, self.computer)

    def player_move(self, mat_index, held_card) -> bool:

        if len(self.playground.get_cards()[mat_index]) >= 2:
            # There are two played_cards in the mat, so we can't put our card there
            return True

        elif len(self.playground.get_cards()[mat_index]) == 1:
            # There is one card in the mat, so we need to check if the new card can be put there
            return not self.validate_player_defence(
                self.playground.get_cards()[mat_index][-1], held_card)

        elif len(self.playground.get_cards()[mat_index]) == 0:
            # There are no unused_cards in the mat, so we need to check if the new card can be put there
            return not self.validate_player_attack(held_card)

    def validate_player_defence(self, bottom_card, top_card):
        return self.strategy_context.validate_defence_move(bottom_card, top_card)

    def validate_player_attack(self, held_card):
        return self.strategy_context.validate_attack_move(held_card)

    def make_computer_defence_move(self):
        self.player.is_turn = True
        return self.strategy_context.make_computer_move(False)

    def make_computer_attack_move(self):
        self.player.is_turn = True
        return self.strategy_context.make_computer_move(True)

    def computer_take_cards(self):
        # Take the unused_cards from the main area
        cards = self.strategy_context.take_cards_from_main_area()
        # Add the unused_cards to the computer area
        for card in cards:
            card.face_down()
            self.computer.add_new_card(card)

    def finish_player_or_bot_turn(self):

        if self.computer.is_taking:
            self.computer_take_cards()
            self.computer.is_taking = False
            self.player.is_turn = True
        elif self.player.is_turn:
            self.player.is_turn = False

        self.finish_turn()

    def finish_turn(self):
        # First we take unused unused_cards from the not active unused_cards and add them to the computer and player
        # area

        for i in range(6):
            if len(self.not_active_cards.unused_cards) > 0:
                if len(self.player.cards) < 6:
                    card = self.not_active_cards.remove_last_card()
                    card.face_up()
                    self.player.add_new_card(card)
                if len(self.computer.cards) < 6:
                    card = self.not_active_cards.remove_last_card()
                    card.face_down()
                    self.computer.add_new_card(card)

        # We must also remove all cards from the main area
        lst = self.playground.get_and_remove_all_cards()
        # Now add them to the used cards
        for card in lst:
            self.not_active_cards.add_played_card(card)

    def take_all_cards_human(self):
        # Take the unused_cards from the main area
        cards = self.strategy_context.take_cards_from_main_area()
        # Add the unused_cards to the computer area
        for card in cards:
            self.player.add_new_card(card)

    def game_over(self, view_manager, config):
        # Check if the game is over
        if len(self.not_active_cards.get_unused_cards()) == 0 and len(self.player.get_cards()) == 0:
            view_manager.show_win_lose_view(WIN, config)
        elif len(self.not_active_cards.get_unused_cards()) == 0 and len(self.computer.get_cards()) == 0:
            view_manager.show_win_lose_view(LOSE, config)

    def on_update_logic(self, show_btn, hint_text, computer_text):

        # Check if the computer is taking cards
        if self.computer.is_taking:
            self.hint_text = "Add more cards or finish turn"
            if len(self.playground.get_cards()[-1]) == 1:
                self.playground.add_new_sprite()

        # Check if the human player is taking cards
        elif self.player.is_taking:
            self.playground.add_new_sprite()
            if not self.make_computer_attack_move():
                self.player.is_turn = False
                self.player.is_taking = False
                self.finish_turn()

        # If no one is taking cards
        else:
            # Check if there are no cards on the playground
            if len(self.playground.get_cards()[-1]) == 0:
                # If it's the computer's turn, try to attack
                if not self.player.is_turn:
                    computer_text = "Computer attack"
                    if not self.make_computer_attack_move() or len(self.computer.get_cards()) == 0:
                        self.finish_turn()
                        self.player.is_turn = True
                        computer_text = "Computer finished his turn"
                        show_btn = False
                # If it's the human player's turn, show a message
                else:
                    hint_text = "Your turn!\nAttack"

            # Check if there is one card on the playground
            elif len(self.playground.get_cards()[-1]) == 1:
                # If it's the computer's turn, try to defend
                if not self.player.is_turn:
                    computer_text = "Computer defended"
                    if not self.make_computer_defence_move():
                        self.computer.is_taking = True
                        self.player.is_turn = True
                        computer_text = "Computer is taking the cards"
                        if len(self.computer.get_cards()) == 0:
                            self.finish_player_or_bot_turn()
                # If it's the human player's turn, show a message
                else:
                    hint_text = "Your turn!\nDefend or take cards"
                    if len(self.computer.get_cards()) == 0:
                        self.finish_player_or_bot_turn()

            # Check if there are two cards on the playground
            elif len(self.playground.get_cards()[-1]) == 2:
                self.playground.add_new_sprite()

        return show_btn, hint_text, computer_text
