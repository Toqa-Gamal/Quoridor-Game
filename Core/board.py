class Board:
    GRID_SIZE = 9    
    MAX_WALLS = 10     

    def __init__(self, ai_opponent=False):
        self.ai_opponent = ai_opponent

       
        self.pawns = {
            "P1": (4, 0),   
            "P2": (4, 8)    
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

    def get_adjacent_positions(self, pos):
        """Returns the 4 orthogonal neighbor cells."""
        r, c = pos
        moves = {
            "up": (r - 1, c),
            "down": (r + 1, c),
            "left": (r, c - 1),
            "right": (r, c + 1)
        }
        return moves

    def is_wall_blocking(self, pos, new_pos):
        """Checks if any wall blocks movement between pos -> new_pos."""
        r1, c1 = pos
        r2, c2 = new_pos

        if r1 == r2:
  
            if c2 > c1:

                return ("V", r1, c1 + 1) in self._wall_edges()
            else:

                return ("V", r1, c1) in self._wall_edges()

        if c1 == c2:
            if r2 > r1:

                return ("H", r1 + 1, c1) in self._wall_edges()
            else:

                return ("H", r1, c1) in self._wall_edges()

        return False

    def is_valid_move(self, player, new_pos):
        """Check if moving the pawn to new_pos is legal."""
        if not self.inside_board(new_pos):
            return False

        current_pos = self.pawns[player]

  
        if new_pos not in self.get_adjacent_positions(current_pos).values():
            return False


        if self.is_wall_blocking(current_pos, new_pos):
            return False


        other_player = "P2" if player == "P1" else "P1"
        if new_pos == self.pawns[other_player]:
            return False

        return True

    def move_pawn(self, player, new_pos):
        """Apply pawn movement if valid."""
        if self.is_valid_move(player, new_pos):
            self.pawns[player] = new_pos
            self._switch_turn()
            return True
        return False
    
    def can_place_wall(self, x, y, orientation):
        """Check if wall placement is legal."""
  
        if orientation == 'H':
            if x < 0 or x >= self.GRID_SIZE - 1 or y < 0 or y >= self.GRID_SIZE - 1:
                return False
        elif orientation == 'V':
            if x < 0 or x >= self.GRID_SIZE - 1 or y < 0 or y >= self.GRID_SIZE - 1:
                return False

        for wx, wy, o in self.walls:
            if (wx, wy, o) == (x, y, orientation):
                return False

    
        if orientation == "H":
            if (x, y, "V") in self.walls or (x, y + 1, "V") in self.walls:
                return False

        if orientation == "V":
            if (x, y, "H") in self.walls or (x + 1, y, "H") in self.walls:
                return False

        return True

    def place_wall(self, player, x, y, orientation):
        """Place wall if allowed."""
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

    def _wall_edges(self):
        """
        Convert walls into blocked edges.
        Used for movement checking.
        """
        edges = set()

        for x, y, orientation in self.walls:
            if orientation == "H":
                edges.add(("H", x, y))
            else: 
                edges.add(("V", x, y))

        return edges
