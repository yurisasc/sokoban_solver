import sys

from node import Node


class MyMap:
    # input file symbols
    BOX_SYMBOL = 'B'
    TGT_SYMBOL = 'T'
    PLAYER_SYMBOL = 'P'
    OBSTACLE_SYMBOL = '#'
    FREE_SPACE_SYMBOL = ' '
    BOX_ON_TGT_SYMBOL = 'b'
    PLAYER_ON_TGT_SYMBOL = 'p'
    CORNER_SYMBOL = '+'

    # move symbols (i.e. output file symbols)
    LEFT = 'l'
    RIGHT = 'r'
    UP = 'u'
    DOWN = 'd'

    # render characters
    FREE_GLYPH = '   '
    OBST_GLYPH = 'XXX'
    BOX_GLYPH = '[B]'
    TGT_GLYPH = '(T)'
    PLAYER_GLYPH = '<P>'
    CORNER_GLYPH = '[+]'

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
        possible_positions = {}

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
                elif rows[i][j] == self.BOX_ON_TGT_SYMBOL:
                    box_positions.append((i, j))
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL
                elif rows[i][j] == self.PLAYER_ON_TGT_SYMBOL:
                    player_position = (i, j)
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL

                if rows[i][j] != self.OBSTACLE_SYMBOL:
                    possible_positions[(i, j)] = sys.maxint

        assert len(box_positions) == len(tgt_positions), "Number of boxes does not match number of targets"

        self.x_size = row_len
        self.y_size = num_rows
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = rows
        self.possible_positions = possible_positions
        self.moved_a_box = False
        self.distance_to_goal = self.goal_pull_distance()

        for i in self.distance_to_goal:
            for j in self.distance_to_goal[i]:
                if self.distance_to_goal[i][j] == sys.maxint:
                    rows[j[0]][j[1]] = self.CORNER_SYMBOL

        self.obstacle_map = rows

    def create_root_node(self):
        return Node(self.box_positions, self.tgt_positions, self.player_x, self.player_y, None)

    def goal_pull_distance(self):
        distance_to_goal = {}

        for goal in self.tgt_positions:
            self.possible_positions[goal] = 0
            distance_to_goal[goal] = self.possible_positions

            q = list()
            q.append(goal)

            while q:
                position = q.pop()
                directions = self.get_possible_moves(position)
                for direction in directions:
                    if direction == self.LEFT:
                        boxPosition = (position[0] - 1, position[1])
                        playerPosition = (position[0] - 2, position[1])
                    elif direction == self.DOWN:
                        boxPosition = (position[0], position[1] + 1)
                        playerPosition = (position[0], position[1] + 2)
                    elif direction == self.RIGHT:
                        boxPosition = (position[0] + 1, position[1])
                        playerPosition = (position[0] + 2, position[1])
                    elif direction == self.UP:
                        boxPosition = (position[0], position[1] - 1)
                        playerPosition = (position[0], position[1] - 2)

                    if distance_to_goal[goal][boxPosition] == sys.maxint:
                        if not self.wallAtPosition(boxPosition) and not self.wallAtPosition(playerPosition):
                            distance_to_goal[goal][boxPosition] = distance_to_goal[goal][position] + 1
                            q.append(boxPosition)

        return distance_to_goal

    def wallAtPosition(self, boxPosition):
        return self.obstacle_map[boxPosition[0]][boxPosition[1]] == self.OBSTACLE_SYMBOL

    def get_possible_moves(self, boxPosition):
        moves = []
        if not self.wallAtPosition((boxPosition[0] - 1, boxPosition[1])):
            moves.append(self.LEFT)
        if not self.wallAtPosition((boxPosition[0] + 1, boxPosition[1])):
            moves.append(self.RIGHT)
        if not self.wallAtPosition((boxPosition[0], boxPosition[1] - 1)):
            moves.append(self.UP)
        if not self.wallAtPosition((boxPosition[0], boxPosition[1] + 1)):
            moves.append(self.DOWN)
        return moves