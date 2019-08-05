

class SokobanMap:
    """
    Instance of a Sokoban game map.

    COMP3702 2019 Assignment 1 Support Code

    Last updated by njc 05/08/19
    """

    # input file symbols
    BOX_SYMBOL = 'B'
    TGT_SYMBOL = 'T'
    PLAYER_SYMBOL = 'P'
    OBSTACLE_SYMBOL = '#'
    FREE_SPACE_SYMBOL = ' '

    # move symbols (i.e. output file symbols)
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'

    # render characters
    #FREE_GLYPH = '\u0020'
    #FREE_GLYPH = '  '
    FREE_GLYPH = ' '

    #OBST_GLYPH = '\u2573'
    #OBST_GLYPH = '\u25AE'
    #OBST_GLYPH = '\u2B1B'
    OBST_GLYPH = '#'

    #BOX_GLYPH = '\u22A0'
    #BOX_GLYPH = '\u26CB'
    BOX_GLYPH = 'B'

    #TGT_GLYPH = '\u25A2'
    #TGT_GLYPH = '\u2BCC'
    TGT_GLYPH = 'T'

    #PLAYER_GLYPH = '\u26C4'
    PLAYER_GLYPH = 'P'

    def __init__(self, filename):
        """
        Build a Sokoban map instance from the given file name
        :param filename:
        """
        f = open(filename, 'r')

        rows = []
        for line in f:
            if len(line.strip()) > 0:
                rows.append(list(line.strip()))

        f.close()

        row_len = len(rows[0])
        for row in rows:
            assert len(row) == row_len, "Mismatch in row length"

        num_rows = len(rows)

        box_positions = []
        tgt_positions = []
        player_position = None
        for i in range(num_rows):
            for j in range(row_len):
                if rows[i][j] == self.BOX_SYMBOL:
                    box_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL
                elif rows[i][j] == self.TGT_SYMBOL:
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL
                elif rows[i][j] == self.PLAYER_SYMBOL:
                    player_position = (i, j)
                    rows[i][j] = self.FREE_SPACE_SYMBOL

        assert len(box_positions) == len(tgt_positions), "Number of boxes does not match number of targets"

        self.x_size = row_len
        self.y_size = num_rows
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = rows

    def apply_move(self, move):
        """
        Apply a player move to the map.
        :param move: 'L', 'R', 'U' or 'D'
        :return: True if move was successful, false if move could not be completed
        """
        # basic obstacle check
        if move == self.LEFT:
            if self.obstacle_map[self.player_y][self.player_x - 1] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x - 1
                new_y = self.player_y

        elif move == self.RIGHT:
            if self.obstacle_map[self.player_y][self.player_x + 1] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x + 1
                new_y = self.player_y

        elif move == self.UP:
            if self.obstacle_map[self.player_y - 1][self.player_x] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x
                new_y = self.player_y - 1

        else:
            if self.obstacle_map[self.player_y + 1][self.player_x] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x
                new_y = self.player_y + 1

        # pushed box collision check
        if (new_y, new_x) in self.box_positions:
            if move == self.LEFT:
                if self.obstacle_map[new_y][new_x - 1] == self.OBSTACLE_SYMBOL or (new_y, new_x - 1) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x - 1
                    new_box_y = new_y

            elif move == self.RIGHT:
                if self.obstacle_map[new_y][new_x + 1] == self.OBSTACLE_SYMBOL or (new_y, new_x + 1) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x + 1
                    new_box_y = new_y

            elif move == self.UP:
                if self.obstacle_map[new_y - 1][new_x] == self.OBSTACLE_SYMBOL  or (new_y - 1, new_x) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x
                    new_box_y = new_y - 1

            else:
                if self.obstacle_map[new_y + 1][new_x] == self.OBSTACLE_SYMBOL or (new_y + 1, new_x) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x
                    new_box_y = new_y + 1

            # update box position
            self.box_positions.remove((new_y, new_x))
            self.box_positions.append((new_box_y, new_box_x))

        # update player position
        self.player_x = new_x
        self.player_y = new_y

        return True

    def render(self):
        """
        Render the map's current state to terminal
        """
        for r in range(self.y_size):
            line = ''
            for c in range(self.x_size):
                symbol = self.FREE_GLYPH
                if self.obstacle_map[r][c] == self.OBSTACLE_SYMBOL:
                    symbol = self.OBST_GLYPH
                if (r, c) in self.tgt_positions:
                    symbol = self.TGT_GLYPH
                # box or player overwrites tgt
                if (r, c) in self.box_positions:
                    symbol = self.BOX_GLYPH
                if self.player_x == c and self.player_y == r:
                    symbol = self.PLAYER_GLYPH
                line += symbol
            print(line)

        print('\n\n')







