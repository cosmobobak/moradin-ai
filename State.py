from random import choice

class State:
    def __init__(self, inputG=None):
        if inputG != None:
            self.node = [m for m in inputG.node]
            self.movecount = inputG.turn
            self.stack = [m for m in inputG.stack]
        else:
            self.node = [0b000000000, 0b000000000]
            self.movecount = 0
            self.stack = []

    def __hash__(self):
        return self.node[0] + (self.node[1] << 9)

    def __eq__(self, other):
        return self.node[0] == other.node[0] and self.node[1] == other.node[1]

    def pos_filled(self, i):
        if ((self.node[0] & (1 << i)) != 0):
            return True
        elif ((self.node[1] & (1 << i)) != 0):
            return True
        return False

    # only valid to use if self.pos_filled() returns True:
    def player_at(self, i):
        if ((self.node[0] & (1 << i)) != 0):
            return True
        else:
            return False

    def is_full(self):
        for i in range(9):
            if not self.pos_filled(i):
                return False
        return True

    def __repr__(self):
        builder = ""
        for x in range(3):
            for y in range(3):
                if (self.pos_filled(x * 3 + y)):
                    if (self.player_at(x * 3 + y)):
                        builder += "X "
                    else:
                        builder += "0 "
                else:
                    builder += ". "
            builder += '\n'
        builder += '\n'
        return builder

    def play(self, i):
        #  n ^ (1 << k) is a binary XOR where you flip the kth bit of n
        self.node[self.movecount & 1] ^= (1 << i)
        
        self.stack.append(i)

    # only valid directly after a move, do not unplay on root, or unplay twice in a row:
    def unplay(self):
        i = self.stack.pop()
        self.movecount -= 1
        self.node[self.movecount & 1] ^= (1 << i)

    def push(self, i):
        self.play(i)

    def pop(self):
        self.unplay()

    def evaluate(self):
        self.nodes += 1  # increment nodes
        #  check first diagonal
        if (self.pos_filled(0) and self.pos_filled(4) and self.pos_filled(8)):
            if (self.player_at(0) == self.player_at(4) and self.player_at(4) == self.player_at(8)):
                if (self.player_at(0)):
                    return 1
                else:
                    return -1

        #  check second diagonal
        if (self.pos_filled(2) and self.pos_filled(4) and self.pos_filled(6)):
            if (self.player_at(2) == self.player_at(4) and self.player_at(4) == self.player_at(6)):
                if (self.player_at(2)):
                    return 1
                else:
                    return -1

        #  check rows
        for i in range(3):
            if (self.pos_filled(i * 3) and self.pos_filled(i * 3 + 1) and self.pos_filled(i * 3 + 2)):
                if (self.player_at(i * 3) == self.player_at(i * 3 + 1) and self.player_at(i * 3 + 1) == self.player_at(i * 3 + 2)):
                    if (self.player_at(i * 3)):
                        return 1
                    else:
                        return -1

        #  check columns
        for i in range(3):
            if (self.pos_filled(i) and self.pos_filled(i + 3) and self.pos_filled(i + 6)):
                if (self.player_at(i) == self.player_at(i + 3) and self.player_at(i + 3) == self.player_at(i + 6)):
                    if (self.player_at(i)):
                        return 1
                    else:
                        return -1
        return 0

    def is_game_over(self):
        return self.is_full() or (self.evaluate() != 0)

    def legal_moves(self):
        return [m for m in range(9) if not self.pos_filled(m)]

    def random_play(self):
        self.play(choice(self.legal_moves()))
