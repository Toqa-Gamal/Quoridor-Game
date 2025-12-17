class Wall:
    @staticmethod
    def wall_edges(x, y, orientation, grid_size):
        """
        Returns the two blocked edges created by a wall at (x, y) with orientation 'H' or 'V'.
        Each edge is a frozenset of two adjacent positions.
        """
        if orientation == "H":
            a1, b1 = (x, y), (x + 1, y)
            a2, b2 = (x, y + 1), (x + 1, y + 1)
        elif orientation == "V":
            a1, b1 = (x, y), (x, y + 1)
            a2, b2 = (x + 1, y), (x + 1, y + 1)
        else:
            return set()

        edges = set()
        for a, b in [(a1, b1), (a2, b2)]:
            if 0 <= a[0] < grid_size and 0 <= a[1] < grid_size and \
               0 <= b[0] < grid_size and 0 <= b[1] < grid_size:
                edges.add(frozenset((a, b)))
        return edges

    @staticmethod
    def crosses_existing_wall(x, y, orientation, existing_walls):
        """
        Checks if placing a wall at (x, y, orientation) would cross any existing wall.
        """
        if orientation == "H":
            return (x, y, "V") in existing_walls or (x, y + 1, "V") in existing_walls
        elif orientation == "V":
            return (x, y, "H") in existing_walls or (x + 1, y, "H") in existing_walls
        return False

    @staticmethod
    def is_wall_within_bounds(x, y, orientation, grid_size):
        """
        Checks if the wall anchor is within valid bounds for placement.
        """
        return (
            orientation in ("H", "V") and
            0 <= x < grid_size - 1 and
            0 <= y < grid_size - 1
        )
