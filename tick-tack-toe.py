#import PYGAME
def revert(s):
    if s == 'X':
        return 'O'
    else:
        return 'X'

class field:
    cells = []
    K = 0
    def __init__(self, N, K):
        self.K = K
        self.cells = [['.'] * N for x in range(N)]
    def count_line(self, x, y, dx, dy):
        typ = self.cells[x][y]
        if typ == '.':
            return 0
        X, Y = x, y
        XX, YY = x, y
        while True: #Двигаем X и Y на крайнюю позицию
            try:
                cell = self.cells[X - dx][Y - dy]
                if cell == revert(typ) or X - dx < 0 or Y - dy < 0:
                    break
                X -= dx
                Y -= dy
                #print('1')
            except:
                break
        while True: #Двигаем XX и YY на крайнюю позицию
            try:
                cell = self.cells[XX - dx][YY - dy]
                if (cell in [revert(typ), '.']) or XX - dx < 0 or YY - dy < 0:
                    break
                XX -= dx
                YY -= dy
                #print('2')
            except:
                break
        X_L, Y_L = X, Y
        XX_L, YY_L = XX, YY
        while True: #Двигаем X_L и Y_L на крайнюю позицию
            try:
                cell = self.cells[X_L + dx][Y_L + dy]
                if cell == revert(typ) or X_L + dx < 0 or Y_L + dy < 0:
                    break
                X_L += dx
                Y_L += dy
                #print('3')
            except:
                break
        while True: #Двигаем XX_L и YY_L на крайнюю позицию
            try:
                cell = self.cells[XX_L + dx][YY_L + dy]
                if (cell in [revert(typ), '.']) or XX_L + dx < 0 or YY_L + dy < 0:
                    break
                XX_L += dx
                YY_L += dy
                #print('4')
            except:
                break
        LReached = max(abs(XX_L - XX), abs(YY_L - YY)) + 1
        LLimit = max(abs(X_L - X), abs(Y_L - Y)) + 1
        if LReached >= self.K:
            return 1000000000
        if LLimit < self.K:
            return 0
        return LReached ** 2
    def get_line_count(self, x, y):
        global N
        typ = self.cells[x][y]
        #print(typ)
        #self.out()
        if typ in ['X', 'O']:
            dirs = [[0, 1], [1, 0], [1, 1], [-1, 1]]
            result = 0
            for dirr in dirs:
                result += self.count_line(x, y, dirr[0], dirr[1])
            return result
        return 0
    def get_sit(self, symb):
        res = 0
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j] == symb:
                    rs = self.get_line_count(i, j)
                    res += rs
                    #print(rs, end=' ')
                else:
                    _=0
                    #print('_ ', end='')
            #print()
        return res
    def copy(self):
        cop = field((len(self.cells) + 1) - 1, self.K)
        cop.cells = self.cells.copy()
        return cop
    def place_at(self, x, y, symb):
        if self.cells[x][y] == '.' and symb in ['X', 'O']:
            self.cells[x][y] = symb
            return True
        else:
            return False
    def AI_turn(self, symb, recur=0):
        max_turn = [-999999999999, [-1, -1]]
        any_turn = [-1, -1]
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j] == '.':
                    self.cells[i][j] = symb
                    if symb == 'X':
                        mA = 2
                        mB = 1
                    else:
                        mB = 4
                        mA = 1
                    res = self.get_sit(symb) * mA - self.get_sit(revert(symb)) * mB
                    if recur < 1:
                        is_win_next = self.AI_turn(revert(symb), recur=recur+1)[1]
                    else:
                        is_win_next = None
                    self.cells[i][j] = '.'
                    if is_win_next:
                        if (res > max_turn[0] or is_win_next[0] == symb) and is_win_next[0] != revert(symb):
                            max_turn = [res, [i, j]]
                    else:
                        if res > max_turn[0]:
                            max_turn = [res, [i, j]]
                    any_turn = [i, j]
        self.cells[max_turn[1][0]][max_turn[1][1]] = symb
        r_win = self.get_winner()
        self.cells[max_turn[1][0]][max_turn[1][1]] = '.'
        if max_turn[1] == [-1, -1]:
            return [any_turn, 'NOPE']
        return [max_turn[1], r_win]
    def get_winner(self):
        res = self.get_sit('X') - self.get_sit('O')
        if res >= 1000000:
            #print(res, self.K)
            return 'X wins'
        elif res <= -1000000:
            #print(res, self.K)
            return 'O wins'
        else:
            OK = True
            for raw in self.cells:
                if '.' in ''.join(raw):
                    OK = False
            if OK:
                return 'DRAW'
            else:
                return None
    def out(self):
        for i in range(len(self.cells)):
            print(''.join(self.cells[i]))

try:
    mode_A = input('Chose 1-st player type (BOT or PLAYER) -> ')
    mode_B = input('Chose 2-nd player type (BOT or PLAYER) -> ')

    N = int(input('Field size (one integer) -> '))
    K = int(input('Win-line length -> '))

    game = field(N, K)

    kg = True
    tick = 0
    while kg:
        game.out()
        tick += 1
        if tick % 2 == 1:
            smb = 'X'
        else:
            smb = 'O'
        print(smb, 'turn')
        if ([mode_B, mode_A])[tick % 2] == 'BOT':
            game.place_at(*game.AI_turn(smb)[0], smb)
        elif ([mode_B, mode_A])[tick % 2] == 'PLAYER':
            X = int(input('Enter turn X coordinate -> '))
            Y = int(input('Enter turn Y coordinate -> '))
            res = game.place_at(X, Y, smb)
            while not res:
                print('WRONG INDEXES')
                X = int(input('Enter turn X coordinate -> '))
                Y = int(input('Enter turn Y coordinate -> '))
                res = game.place_at(X, Y, smb)
        else:
            break
        sit = game.get_winner()
        if sit:
            print(sit)
            game.out()
            break
            
except ZeroDivisionError as E:
    print(E)
    print('Сработала защита от дурака')
