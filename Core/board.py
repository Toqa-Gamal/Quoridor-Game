from Core.pathfinding import find_path

class Board:
    GRID_SIZE = 9
    MAX_WALLS = 10

    def __init__(self, ai_opponent=False):
        self.ai_opponent = ai_opponent

        self.pawns = {
            "P1": (0, 4),
            "P2": (8, 4)
        }

      
        self.walls = []

        self.walls_left = {
            "P1": self.MAX_WALLS,
            "P2": self.MAX_WALLS
        }

        self.current_player = "P1"

  

    def inside_board(self, pos):
        r, c = pos
        return 0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE

    def is_adjacent(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

    def get_adjacent_positions(self, pos):
        r, c = pos
        return {
            "up": (r - 1, c),
            "down": (r + 1, c),
            "left": (r, c - 1),
            "right": (r, c + 1)
        }


    def _wall_edges(self):
        edges = set()
        for x, y, o in self.walls:
            edges.add((o, x, y))
        return edges

    def is_wall_blocking(self, pos, new_pos):
        r1, c1 = pos
        r2, c2 = new_pos

        # Horizontal move
        if r1 == r2:
            if c2 > c1:
                return ("V", r1, c1 + 1) in self._wall_edges()
            else:
                return ("V", r1, c1) in self._wall_edges()

        # Vertical move
        if c1 == c2:
            if r2 > r1:
                return ("H", r1 + 1, c1) in self._wall_edges()
            else:
                return ("H", r1, c1) in self._wall_edges()

        return False


    def is_jump_move(self, current, opponent, new_pos):
        if not self.is_adjacent(current, opponent):
            return False

        dr = opponent[0] - current[0]
        dc = opponent[1] - current[1]
        jump_pos = (opponent[0] + dr, opponent[1] + dc)

        if new_pos != jump_pos:
            return False

        if not self.inside_board(jump_pos):
            return False

        if self.is_wall_blocking(current, opponent):
            return False

        if self.is_wall_blocking(opponent, jump_pos):
            return False

        return True

    def is_diagonal_move(self, current, opponent, new_pos):
        if not self.is_adjacent(current, opponent):
            return False

        dr = opponent[0] - current[0]
        dc = opponent[1] - current[1]

        jump_pos = (opponent[0] + dr, opponent[1] + dc)

   
        if self.inside_board(jump_pos) and not self.is_wall_blocking(opponent, jump_pos):
            return False

        diagonals = []
        if dr == 0: 
            diagonals = [
                (opponent[0] - 1, opponent[1]),
                (opponent[0] + 1, opponent[1])
            ]
        elif dc == 0: 
            diagonals = [
                (opponent[0], opponent[1] - 1),
                (opponent[0], opponent[1] + 1)
            ]

        if new_pos not in diagonals:
            return False

        if not self.inside_board(new_pos):
            return False

        if self.is_wall_blocking(opponent, new_pos):
            return False

        return True

    def is_valid_move(self, player, new_pos):
        if not self.inside_board(new_pos):
            return False

        current = self.pawns[player]
        opponent_player = "P2" if player == "P1" else "P1"
        opponent = self.pawns[opponent_player]

   
        if self.is_adjacent(current, new_pos):
            if new_pos != opponent and not self.is_wall_blocking(current, new_pos):
                return True


        if self.is_jump_move(current, opponent, new_pos):
            return True

  
        if self.is_diagonal_move(current, opponent, new_pos):
            return True
        

        return False

    def move_pawn(self, player, new_pos):
        if self.is_valid_move(player, new_pos):
            self.pawns[player] = new_pos
            self._switch_turn()
            return True
        return False



    def can_place_wall(self, x, y, orientation):
        if orientation not in ("H", "V"):
            return False

        if x < 0 or x >= self.GRID_SIZE - 1 or y < 0 or y >= self.GRID_SIZE - 1:
            return False

        if (x, y, orientation) in self.walls:
            return False
        
        
   
        if orientation == "H":
            if (x, y, "V") in self.walls or (x, y + 1, "V") in self.walls:
                return False
        else:
            if (x, y, "H") in self.walls or (x + 1, y, "H") in self.walls:
                return False

        return True

    def place_wall(self, player, x, y, orientation):
        if self.walls_left[player] <= 0:
            return False

        if self.can_place_wall(x, y, orientation):
            self.walls.append((x, y, orientation))
            self.walls_left[player] -= 1
            self._switch_turn()
            return True

        return False

    def _switch_turn(self):
        self.current_player = "P2" if self.current_player == "P1" else "P1"
