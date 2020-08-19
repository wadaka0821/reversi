import curses

#盤面情報の管理
class Field():
    def __init__(self):
        #盤面の状態を保存（0:なし, -1:黒, 1:白）
        self.field = [[0 for i in range(8)] for j in range(8)]
        #現在のターン数をカウント
        self.turn_num = 0
        #黒白それぞれの石の数をカウント
        self.black = 2
        self.white = 2

        self.field[3][3] = -1
        self.field[3][4] = 1
        self.field[4][3] = 1
        self.field[4][4] = -1

    #指定された座標の色を変更
    def set_col(self, col, y, x):
        if self.check_coor(y, x):
            if col == -1:
                self.white += 1
            else:
                self.black += 1
            self.field[y][x] = col
            return True
        else:
            return False
    
    #指定された座標の色を反転
    def reverse_col(self, y, x):
        if self.check_coor(y, x):
            if self.field[y][x] == -1:
                self.black += 1
                self.white -= 1
            else:
                self.black -= 1
                self.white += 1
            self.field[y][x] *= -1
            return True
        else:
            return False
    
    def get_col(self, y, x):
        if self.check_coor(y, x):
            return self.field[y][x]
        return None

    def get_black(self):
        return self.black
    
    def get_white(self):
        return self.white

    #ターン数を追加
    def add_turn(self):
        self.turn_num += 1

    #指定された座標が正しいか（インデックスエラーにならないか）チェック
    def check_coor(self, y, x):
        if 0 <= y <= 7 and 0 <= x <= 7:
            return True
        return False

#盤面の操作
class Control():
    def __init__(self):
        self.vector = [[-1, -1], [-1, 0], [-1, 1],
                       [0, -1], [0, 0], [0, 1],
                       [1, -1], [1, 0], [1, 1]]
        self.calc = Math()
        
    def set_stone(self, field, col, y, x):
        check_list = self.check_reverse(field, col, y, x)
        if field.get_col(y, x) == 0 and sum(check_list):
            field.set_col(col, y, x)
            self.fill(field, check_list, col, y, x)
            return True
        else:
            return False

    def check_reverse(self, field, col, y, x):
        check_list = [0 for i in range(9)]

        for i in range(len(self.vector)):
            coor = [y, x]
            temp = self.calc.plus(coor, self.vector[i])
            if not field.check_coor(temp[0], temp[1]):
                continue
            elif col*field.get_col(temp[0], temp[1]) != -1:
                continue
            
            temp = self.calc.plus(temp, self.vector[i])
            while field.check_coor(temp[0], temp[1]):
                if col*field.get_col(temp[0], temp[1]) == 1:
                    check_list[i] = 1
                    break
                else:
                    temp = self.calc.plus(temp, self.vector[i])

        return check_list

    def fill(self, field, check_list, col, y, x):
        coor = [y, x]
    
        for i in range(len(check_list)):
            if check_list[i] == 0:
                continue
            temp = self.calc.plus(coor, self.vector[i])
            while col*field.get_col(temp[0], temp[1]) == -1:
                field.reverse_col(temp[0], temp[1])
                temp = self.calc.plus(temp, self.vector[i])

    def endgame(self, field):
        for i in range(8):
            for j in range(8):
                if field.get_col(i, j) == 0:
                    return False
        return True

class Display():
    def __init__(self):
        #self.symbol = ['●', '*', '◯']
        self.symbol = ['B', '*', 'W']
        self.turn_list = ['黒', '白']

    def show(self, field, cursor, turn):
        for i in range(8):
            for j in range(8):
                stdscr.move(2*i, 4*j)
                stdscr.addch(self.symbol[field.get_col(i, j)+1])

        stdscr.move(2*cursor[0], 4*cursor[1])
        stdscr.addch('C')
        stdscr.move(15, 0)
        stdscr.addstr('{} 対 {}'.format(field.get_black(), field.get_white()))
        stdscr.move(16, 0)
        stdscr.addstr('{}の番です'.format(self.turn_list[turn]))


class Player():
    def __init__(self, is_human=True):
        self.is_human = is_human

    def getkey(self, field, col):
        if self.is_human:
            temp = stdscr.getch()
            stdscr.move(17, 0)
            stdscr.addstr(str(temp))
            if temp == curses.KEY_UP:
                return 'u'
            elif temp == curses.KEY_DOWN:
                return 'd'
            elif temp == curses.KEY_LEFT:
                return 'l'
            elif temp == curses.KEY_RIGHT:
                return 'r'
            elif temp == 10:
                return 'e'
            else:
                return None

class Math():
    def __init__(self):
        pass

    def dot(self, li1, li2):
        ans = 0
        if len(li1) != len(li2):
            return None
        else:
            for i in range(len(li1)):
                ans += li1[i] * li2[i]
            return ans

    def scalar(self, li, a):
        return [i*a for i in li]

    def plus(self, li1, li2):
        return [li1[i]+li2[i] for i in range(len(li1))]

    def minus(self, li1, li2):
        return self.plus(li1, self.scalar(li2, -1))

if __name__ == '__main__':
    #初期化
    stdscr = curses.initscr()
    #入力キーのリピートをオフ
    curses.noecho()
    #キー入力後すぐに反応するように設定
    curses.cbreak()
    #キーパッドモードをオン
    stdscr.keypad(True)


    field = Field()
    control = Control()
    display = Display()
    player = [Player(), Player()]
    player1 = Player()
    player2 = Player()

    turn = 0
    coor = [0, 0]

    display.show(field, coor, turn)

    while not control.endgame(field):
        display.show(field, coor, turn)
        key = player[turn].getkey(field, turn*2 - 1)
        stdscr.move(18, 0)
        stdscr.addstr(str(key))
        stdscr.move(19, 0)
        stdscr.addstr(str(coor[0])+str(coor[1]))
        if key == 'u':
            if coor[0] == 0:
                continue
            coor[0] -= 1
        elif key == 'd':
            if coor[0] == 7:
                continue
            coor[0] += 1
        elif key == 'l':
            if coor[1] == 0:
                continue
            coor[1] -= 1
        elif key == 'r':
            if coor[1] == 7:
                continue
            coor[1] += 1
        elif key == 'e':
            if control.set_stone(field, turn*2 - 1, coor[0], coor[1]):
                turn = (turn + 1) % 2


    display.show(field, coor, turn)

    #設定をもとに戻す
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    #終了
    curses.endwin()