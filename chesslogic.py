class ChessLogic:
    def canBishop(self, x1, y1, x2, y2):
        if abs(x2 - x1) != abs(y2 - y1):
            return False
        i = (y2 - y1) // abs(y2 - y1)
        j = (x2 - x1) // abs(x2 - x1)
        x1 += j
        y1 += i
        while x1 != x2 and y1 != y2:
            if self.board[y1][x1] != 0:
                return False
            x1 += j
            y1 += i
        return True
    def canRook(self, x1, y1, x2, y2):
        if x2 == x1:
            i = (y2 - y1) // abs(y2 - y1)
            j = 0
        elif y2 == y1:
            j = (x2 - x1) // abs(x2 - x1)
            i = 0
        else:
            return False
        x1 += j
        y1 += i
        while x1 != x2 or y1 != y2:
            if self.board[y1][x1] != 0:
                return False
            x1 += j
            y1 += i
        return True
    def canMove(self, p1, p2):
        x1 = p1[1]
        y1 = p1[0]
        x2 = p2[1]
        y2 = p2[0]
        p = self.board[y1][x1]
        if p == 0 or p[1] != self.turn or (self.board[y2][x2] != 0 and self.board[y2][x2][1] == self.turn) or (x1 == x2 and y1 == y2):
            return False
        elif p[0] == 'P':
            if self.board[y2][x2] == 0 and x1 == x2 and\
                ((p[1] == 'w' and (y1 - y2 == 1 or (y1 == 6 and y1 - y2 == 2))) or \
                (p[1] == 'b' and (y2 - y1 == 1 or (y1 == 1 and y2 - y1 == 2)))):
                return True
            if self.board[y2][x2] != 0 and abs(x1 - x2) == 1 and\
                ((p[1] == 'w' and y1 - y2 == 1) or \
                (p[1] == 'b' and y2 - y1 == 1)):
                return True
        elif p[0] == 'R':
            return self.canRook(x1, y1, x2, y2)
        elif p[0] == 'B':
            return self.canBishop(x1, y1, x2, y2)
        elif p[0] == 'Q':
            return self.canRook(x1, y1, x2, y2) or self.canBishop(x1, y1, x2, y2)
        elif p[0] == 'K':
            if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                return True
        elif p[0] == 'N':
            if (abs(x1 - x2) == 2 and abs(y1 - y2) == 1) or (abs(x1 - x2) == 1 and abs(y1 - y2) == 2):
                return True
        return False