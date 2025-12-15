import copy
import random

class AIPlayer:
    def __init__(self, player, minimax, heuristic, find_path,
                 difficulty="easy"):
        self.player = player
        self.opponent = "P2" if player == "P1" else "P1"
        self.minimax = minimax
        self.heuristic = heuristic
        self.find_path = find_path
        self.difficulty = difficulty
        if difficulty == "easy":
            self.depth = 1
        elif difficulty == "medium":
            self.depth = 2
        else:  # hard
            self.depth = 4

    def choose_action(self, board):

        actions = self._generate_all_actions(board)
        if self.difficulty == "easy":
            return self._choose_greedy(board, actions)
        best_score = float("-inf")
        best_action = None
        for action in actions:
            simulated_board = self._simulate_action(board, action)
            score = self.minimax(
                board_state=simulated_board,
                depth=self.depth - 1,
                maximizing_player=False,
                ai_player=self.player,
                heuristic_func=self.heuristic,
                find_path_func=self.find_path
            )

            if score > best_score:
                best_score = score
                best_action = action

        return best_action
    def _choose_greedy(self, board, actions): #for easy difficulty
        best_score = float("-inf")
        best_actions = []

        for action in actions:
            simulated_board = self._simulate_action(board, action)
            score = self.heuristic(
                simulated_board,
                self.player,
                self.find_path
            )

            if score > best_score:
                best_score = score
                best_actions = [action]
            elif score == best_score:
                best_actions.append(action)

        return random.choice(best_actions)
    def _generate_all_actions(self, board):
        return (
            self._generate_pawn_moves(board)
            + self._generate_wall_moves(board)
        )

    def _generate_pawn_moves(self, board):
        moves = []
        current_pos = board.pawns[self.player]

        for new_pos in board.get_adjacent_positions(current_pos).values():
            if board.is_valid_move(self.player, new_pos):
                moves.append({"type": "move", "to": new_pos})

        return moves

    def _generate_wall_moves(self, board):
        moves = []

        if board.walls_left[self.player] <= 0:
            return moves

        for x in range(board.GRID_SIZE - 1):
            for y in range(board.GRID_SIZE - 1):
                for orientation in ("H", "V"):
                    if board.can_place_wall(x, y, orientation):
                        if self._wall_keeps_paths(board, x, y, orientation):
                            moves.append({
                                "type": "wall",
                                "x": x,
                                "y": y,
                                "orientation": orientation
                            })

        return moves
    def _simulate_action(self, board, action):
        new_board = copy.deepcopy(board)

        if action["type"] == "move":
            new_board.move_pawn(self.player, action["to"])
        else:
            new_board.place_wall(
                self.player,
                action["x"],
                action["y"],
                action["orientation"]
            )

        return new_board
    def _wall_keeps_paths(self, board, x, y, orientation):
        test_board = copy.deepcopy(board)
        test_board.walls.append((x, y, orientation))

        ai_path = self.find_path(
            self.player,
            test_board.pawns[self.player],
            test_board
        )
        opp_path = self.find_path(
            self.opponent,
            test_board.pawns[self.opponent],
            test_board
        )

        return ai_path is not None and opp_path is not None
