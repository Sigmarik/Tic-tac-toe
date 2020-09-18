class field:
    cells = []
    K = 0
    def __init__(self, N, K):
        self.K = K
        self.cells = [['.'] * N for x in range(N)]
    def get_line_count(self, x, y):
        global N
        typ = self.cells[x][y]
        dirs = [[0, 1], [1, 0], [1, 1]]
        maxx = 0
        for dirr in dirs:
            counter = 0
            for i in range(0, self.K):
                cell = self.cells[x + dirr[0] * i, y + dirr[1] * i]
                if cell not in [typ, '.']:
                    is_wrong = False
                    for j in range(1, self.K - i + 2):
                        cellr = self.cells[x + dirr[0] * -j, y + dirr[1] * -j]
                        if cellr not in [typ, '.']:
                            is_wrong = True
                            break
                    if (not is_wrong) and counter > maxx:
                        return 
    def get_sit(self, symb):
        for i in range()

mode = int(input('Chose player count (0, 1 or 2) -> '))

N = int(input('Enter board size -> '))
K = int(input('Enter win-line size -> '))

if K > N:
    print('WARNING!!! Win-line longer then field!')
    input()
else:
    
