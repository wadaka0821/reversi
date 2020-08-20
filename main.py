import curses
import copy
import time

#盤面情報の管理
class Field():
    def __init__(self):
        self.field_height = 8
        self.field_width = 8
        #盤面の状態を保存（0:なし, -1:黒, 1:白）
        self.field = [[0 for i in range(self.field_width)] for j in range(self.field_height)]
        #現在のターン数をカウント
        self.turn_num = 0
        #黒白それぞれの石の数をカウント
        self.black = 2
        self.white = 2

        #盤面の初期設定
        self.field[3][3] = -1
        self.field[3][4] = 1
        self.field[4][3] = 1
        self.field[4][4] = -1

    #指定された座標の色を変更
    def set_col(self, col, y, x):
        if self.check_coor(y, x):
            #石の数をカウント
            if col == -1:
                self.black += 1
            else:
                self.white += 1
            #石の色を変更
            self.field[y][x] = col
            return True
        else:
            return False
    
    #指定された座標の色を反転
    def reverse_col(self, y, x):
        if self.check_coor(y, x):
            #石の数をカウント
            if self.field[y][x] == -1:
                self.black -= 1
                self.white += 1
            else:
                self.black += 1
                self.white -= 1
            #石の色を反転
            self.field[y][x] *= -1
            return True
        else:
            return False
    
    #指定された座標の色を返す
    def get_col(self, y, x):
        if self.check_coor(y, x):
            return self.field[y][x]
        return None

    #黒の石の個数を返す
    def get_black(self):
        return self.black
    
    #白の石の個数を返す
    def get_white(self):
        return self.white

    #ターン数を追加
    def add_turn(self):
        self.turn_num += 1

    #指定された座標が正しいか（インデックスエラーにならないか）チェック
    def check_coor(self, y, x):
        if 0 <= y <= self.field_height-1 and 0 <= x <= self.field_width-1:
            return True
        return False

#盤面の操作
class Control():
    def __init__(self):
        self.vector = [[-1, -1], [-1, 0], [-1, 1],
                       [0, -1], [0, 0], [0, 1],
                       [1, -1], [1, 0], [1, 1]]
        #基本のベクトル演算に使用
        self.calc = Math()
        
    #指定された座標に石を設置
    def set_stone(self, field, col, y, x):
        #反転させる石がある方向を調べる
        check_list = self.check_reverse(field, col, y, x)
        #反転させる石があれば石を設置、反転させる
        if field.get_col(y, x) == 0 and sum(check_list) > 0:
            field.set_col(col, y, x)
            self.fill(field, check_list, col, y, x)
            return True
        else:
            return False

    #反転させる石がある方向を調べる
    def check_reverse(self, field, col, y, x):
        check_list = [0 for i in range(len(self.vector))]

        for i in range(len(self.vector)):
            coor = [y, x]
            temp = self.calc.plus(coor, self.vector[i])
            if not field.check_coor(temp[0], temp[1]):
                continue
            elif col*field.get_col(temp[0], temp[1]) != -1:
                continue
            
            temp = self.calc.plus(temp, self.vector[i])
            while field.check_coor(temp[0], temp[1]):
                stdscr.move(25, 0)
                stdscr.addstr(' '.join([str(i) for i in temp]))
                stdscr.refresh()
                if col*field.get_col(temp[0], temp[1]) == 1:
                    check_list[i] = 1
                    break
                else:
                    temp = self.calc.plus(temp, self.vector[i])

        return check_list

    #挟まれた石の反転
    def fill(self, field, check_list, col, y, x):
        coor = [y, x]
    
        for i in range(len(check_list)):
            if check_list[i] == 0:
                continue
            temp = self.calc.plus(coor, self.vector[i])
            while col*field.get_col(temp[0], temp[1]) == -1:
                field.reverse_col(temp[0], temp[1])
                temp = self.calc.plus(temp, self.vector[i])

    #ゲームが終了するか調べる
    def endgame(self, field):
        for i in range(field.field_height):
            for j in range(field.field_width):
                if field.get_col(i, j) == 0:
                    return False
        return True

    #プレイヤーの置く場所があるかチェック
    def check_set(self, field, col):
        for i in range(field.field_height):
            for j in range(field.field_width):
                if field.get_col(i, j) != 0:
                    continue
                if sum(self.check_reverse(field, col, i, j)) > 0:
                    return True
        return False

class Display():
    def __init__(self):
        #self.symbol = ['●', '*', '◯']
        self.symbol = ['B', '*', 'W']
        self.turn_list = ['黒', '白']

    def show(self, field, cursor, turn):
        for i in range(field.field_height):
            for j in range(field.field_width):
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
        self.que = list()

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
            elif temp == 113:
                return 'q'
            else:
                return None
        else:
            if len(self.que) != 0:
                stdscr.move(26, 0)
                stdscr.addstr(' '.join(self.que))
                stdscr.refresh()
                #time.sleep(5)
                return self.que.pop()
            else:
                self.que = self.cpu(field, col)
                return self.que.pop()

    def cpu(self, field, col):
        evaluate_list = self.evaluate(field, col)

        index = evaluate_list.index(max(evaluate_list))
        stdscr.move(27, 0)
        stdscr.addstr(' '.join([str(i) for i in evaluate_list]))
        stdscr.refresh()
        
        y, x = int(index/field.field_height), index%field.field_height

        move = ['d' for i in range(y)]
        for i in range(x):
            move.append('r')
        move.append('e')
        move.reverse()

        return move
    
    def evaluate(self, field, col):
        evaluate_list = [0 for i in range(field.field_height*field.field_width)]
        
        for i in range(field.field_height):
            for j in range(field.field_width):
                field_temp = copy.deepcopy(field)
                
                if field.get_col(i, j) != 0 or not control.set_stone(field_temp, col, i, j):
                    evaluate_list[i*field.field_height + j] = -1
                    continue
                if col == -1:
                    evaluate_list[i*field.field_height + j] = field_temp.get_black() - field.get_black()
                elif col == 1:
                    evaluate_list[i*field.field_height + j] = field_temp.get_white() - field.get_white()

                if [i, j] in [[0, 0], [0, 7], [7, 0], [7, 7]]:
                    evaluate_list[i*field.field_height + j] += 100

        return evaluate_list

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

    #Fieldクラスのインスタンス生成
    field = Field()
    #Controlクラスのインスタンス生成
    control = Control()
    #Displayクラスのインスタンス生成
    display = Display()
    player = [Player(), Player(False)]

    turn = 0
    #カーソルの座標
    coor = [0, 0]

    display.show(field, coor, turn)

    while not control.endgame(field):
        stdscr.refresh()
        #stdscr.move(21, 0)
        #stdscr.addstr('check')
        if not control.check_set(field, turn*2 - 1):
            turn = (turn + 1) % 2
            continue
        display.show(field, coor, turn)
        stdscr.refresh()
        key = player[turn].getkey(field, turn*2 - 1)
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
                coor[0] = 0
                coor[1] = 0
        elif key == 'q':
            break


    display.show(field, coor, turn)

    #設定をもとに戻す
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    #終了
    curses.endwin()