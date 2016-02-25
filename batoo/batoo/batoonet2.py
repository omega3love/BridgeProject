from batoosprites import *
from batoo import *
from pygame import *
import batoomaps
import socket
import threading
from random import random, randint
import sys, os

HOST = '143.248.2.116'
PORT = 50000
DATA_SIZE = 128

class Batoo(object):

    display_size = ( 900, 720 )
    size = ( 11, 11 )
    screen_size = ( 650, 650 )

    xset = board_topleft[0] + board_tile_offset
    yset = board_topleft[1] + board_tile_offset

    board = Board()
    board.rect.topleft = board_topleft
    scoreboard = Scoreboard()
    scoreboard.rect.topleft = ( 0, 0 )
    cursor_mark = Cursor_Marking()

    bmap = batoomaps.sky()
    board.project(bmap)

    font.init()
    scorefont = font.Font(None, 30)

    def __init__(self):

        init()
        mixer.init()
        self.screen = display.set_mode(self.display_size)
        self.clock = time.Clock()
        self.fps = 50
        self.pcm = placement()

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.settimeout(10.0)

        foo = True
        while foo:
            while True:
                try:
                    print 'trying to connect ' + HOST
                    soc.connect( (HOST, PORT) )
                    foo = False
                    print 'Connected!'
                    break
                except socket.timeout:
                    print 'Exceeded time limit'
                    break
                except socket.error:
                    print 'Access denied'
                    time.wait(1000)
                    for ev in event.get():
                        if ev.type == QUIT: exit()

            self.conn = soc

        soc.settimeout(None)

        self.last_data = []
        T = threading.Thread(target = self.read)
        T.start()
        replay = True
        self.game_over = False

        if not self.read_wait() == 'initialize':
            return
        time.wait(1000)

        while replay:
            self.pcm.history = []
            self.screen.fill(WHITE)
            self.board.draw(self.screen)
            self.scoreboard.draw(self.screen)
            display.update()

            self.turn = 1
            self.score = 15
            self.adv_score = 15
            self.score_font = {'mine':None, 'adv':None, 'minepos':None, 'advpos':None}
            self.se = {'place':mixer.Sound("./sound_effects/place.wav"),
                       'catch':mixer.Sound("./sound_effects/catch.wav"),
                       'stir':mixer.Sound("./sound_effects/stir.wav")}
            self.marked_pos = None
            self.hidden = False
            self.hchance = True
            self.scan = False
            self.schance = True
            self.base = []
            self.last_data = []
            time.wait(2000)
            self.get_color()
            print 'your color is ' + self.player
            self.base_build()
            print 'betting started'
            self.betting()
            print 'betting finished'
            while not self.game_over:
                self.update()
            replay = False

        try:
            self.conn.send('quit'.encode('UTF-8'))
        except:
            print 'pipe broken'
        T.join()
        self.conn.close()
        print 'shutting down'

    def read(self):

        while True:
            try:
                data = self.conn.recv(DATA_SIZE)
                data = data.split('*')[0]
            except:
                print 'pipe broken?'
                data = 'quit'
            if data == 'quit':
                self.conn.send('quit'.encode('UTF-8'))
                self.game_over = True
                print 'shutting down at read'
                os._exit(1)
                #break
            elif data not in self.last_data:
                self.last_data.append(data)
                print 'data received! : ' + str(data)
                print 'current last data : ' + str(self.last_data)

            #else:
            #    event.post(event.Event(USEREVENT + 1, {'data':data}))

    def write(self, msg, kind = ''):

        data = kind + ':' + str(msg) + '*' if kind else str(msg) + '*'
        if len(data) <= DATA_SIZE:
            self.conn.send(data.encode('UTF-8'))
        else:
            print 'Data packet size exceeded'
            return
        time.wait(1)

    def read_wait(self):

        while not self.game_over:
            if self.last_data:
                data = self.last_data.pop(0)
                break
            time.wait(1)

        return data

    def update(self):

        self.screen.fill(WHITE)
        self.board.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.score_display()

        if self.turn & 1 == self.order:
            ev = event.wait()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE or ev.type == QUIT:
                self.game_over = True
                return
            elif ev.type == KEYDOWN and ev.key == K_h and not self.hidden and self.hchance:
                self.hidden = True
                self.hchance = False
            elif ev.type == KEYDOWN and ev.key == K_s and not self.scan and self.schance:
                self.scan = True
                self.schance = False
                self.score -= 2
                self.scorefont_update()
            elif ev.type == MOUSEBUTTONUP and ev.button == 1:
                if self.hidden:
                    self.placing(ev.pos, False, 'hidden')
                    self.hidden = False
                else:
                    self.placing(ev.pos)
                    if self.scan:
                        self.scan = False
            elif ev.type == MOUSEMOTION:
                self.placing(ev.pos, True)
        else:
            ev = event.poll()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE or ev.type == QUIT:
                self.game_over = True

        for data in self.last_data[:]:
            if 'history' in data:
                data = eval(data.split('history:')[-1])
                self.pcm_update(data)
                if not data[-1] == 2:
                    self.adjust(data[0], data[1])
                    self.adv_score += 1
            elif 'discovered' in data:
                self.pcm_update('discovered')
            else:
                print data, type(data)
            self.last_data.pop(0)
            self.scorefont_update()

        self.drawing_stones()
        display.update()
        self.clock.tick(self.fps)

    def get_color(self):

        num = random()
        self.write(num)
        adv_num = eval(self.read_wait())
        if num > adv_num:
            self.player = 'B' #black
            self.adv_player = 'W'
        else:
            self.player = 'W'
            self.adv_player = 'B'
        self.scorefont_update()

    def betting(self):

        while not self.game_over:
            #bet_score = input('bet a score(1~15) : ')
            bet_score = randint(1,10)

            self.write(bet_score)
            try:
                adv_bet_score = eval(self.read_wait())
            except:
                print self.last_data

            if bet_score > adv_bet_score:
                self.order = 1 #first
                self.adv_score += bet_score
                break
            elif bet_score < adv_bet_score:
                self.order = 0 #second
                self.score += adv_bet_score
                break
            else:
                continue
        self.scorefont_update()

    def scorefont_update(self):

        if self.player == 'B':
            self.score_font['mine'] = self.scorefont.render(str(self.score), 1, WHITE)
            self.score_font['adv'] = self.scorefont.render(str(self.adv_score), 1, BLACK)
            self.score_font['minepos'] = self.score_font['mine'].get_rect(center = (600, 35))
            self.score_font['advpos'] = self.score_font['adv'].get_rect(center = (50, 35))
        else:
            self.score_font['mine'] = self.scorefont.render(str(self.score), 1, BLACK)
            self.score_font['adv'] = self.scorefont.render(str(self.adv_score), 1, WHITE)
            self.score_font['minepos'] = self.score_font['mine'].get_rect(center = (50, 35))
            self.score_font['advpos'] = self.score_font['adv'].get_rect(center = (600, 35))

    def score_display(self):

        self.screen.blit(self.score_font['mine'], self.score_font['minepos'])
        self.screen.blit(self.score_font['adv'], self.score_font['advpos'])

    def base_build(self):

        while len(self.base) < 3 and not self.game_over:
            self.screen.fill(WHITE)
            self.board.draw(self.screen)
            self.scoreboard.draw(self.screen)
            self.score_display()

            ev = event.poll()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE or ev.type == QUIT:
                self.game_over = True
                return
            elif ev.type == MOUSEBUTTONUP and ev.button == 1:
                grid = self.cursor_marking(ev.pos, self.size, tileSize, 1)
                if grid:
                    base = [ grid, self.player, 3 ]
                    if base not in self.base:
                        self.base.append(base)
                        self.pcm.history.append(base)
            elif ev.type == MOUSEMOTION:
                grid = self.cursor_marking(ev.pos, self.size, tileSize, 1)
                if grid and grid not in [ s[0] for s in self.base ]:
                    self.cursor_mark.draw(self.screen, grid)

            self.drawing_stones()
            display.update()
            self.clock.tick(self.fps)

        self.write(self.base)
        adv_base = eval(self.read_wait())

        self.pcm.history.extend(adv_base)
        base_grid = [ b[0] for b in self.base ]
        adv_base_grid = [ a[0] for a in adv_base ]
        for b in self.base[:]:
            if b[0] in adv_base_grid[:]:
                self.pcm.history.remove(b)
        for a in adv_base[:]:
            if a[0] in base_grid[:]:
                self.pcm.history.remove(a)
        time.wait(1)
        self.scorefont_update()

    def placing(self, pos, marking = False, stone_type = 'normal'):

        markable = self.cursor_marking(pos, self.size, tileSize, 1)
        if markable:
            placable = self.pcm.is_placable(markable, self.player)
            if placable:
                if marking:
                    self.cursor_mark.draw(self.screen, markable)
                else:
                    if placable == 'hidden': #already occupied
                        adv = self.adv_player
                        ind = self.find_stone(markable, adv, 2)
                        self.pcm.history[ind][-1] = 1
                        self.write('discovered')
                    elif not self.scan:
                        s = 1 if stone_type == 'normal' else 2 if stone_type == 'hidden' else 3
                        info = [ markable, self.player, s ]
                        if s != 2:
                            self.adjust(markable, self.player)
                        self.write(info, 'history')
                        self.pcm_update(info)

    def find_stone(self, grid, color, stone_type):

        if grid == 'wherever':
            foo = False
            for h in self.pcm.history:
                if h[1] == color and h[-1] == stone_type:
                    foo = self.pcm.history.index(h)
            return foo

        try:
            return self.pcm.history.index([grid, color, stone_type])
        except:
            return False

    def pcm_update(self, info):

        if info == 'discovered':
            ind = self.find_stone('wherever', self.player, 2)
            self.pcm.history[ind][-1] = 1
            self.adjust(self.pcm.history[ind][0], self.pcm.history[ind][1])
            return

        self.pcm.history.append(info)
        catchable = self.pcm.is_catching(info[0], info[1])
        if catchable:
            catching_list, hidden_catcher = catchable
            for caught in catching_list:
                for stone in self.pcm.history:
                    if stone[0] == caught:
                        color = self.color_toggle(stone[1])
                        if stone[-1] == 1:
                            stone[-1] = 0
                            self.score_update(color, 1)
                        elif stone[-1] == 2:
                            stone[-1] = 0
                            self.write('discovered')
                            self.score_update(color, 1)
                            #notify hidden is caught
                        elif stone[-1] == 3:
                            stone[-1] = 0
                            self.score_update(color, 5)
            for h in hidden_catcher: #hidden is catching
                ind = self.find_stone(*h)
                self.pcm.history[ind][-1] = 1
                self.adjust(self.pcm.history[ind][0], self.pcm.history[ind][1])

        self.se['place'].play()
        self.turn += 1
        if sys._getframe().f_back.f_code.co_name == 'placing':
            self.score += 1
        self.scorefont_update()

    def drawing_stones(self):

        for stone in self.pcm.history:
            if stone[-1] == 1:
                Stone(stone[1], stone[0]).draw(self.screen)
            elif stone[-1] == 2 and self.player == stone[1]:
                Stone(stone[1], stone[0], 'hidden').draw(self.screen)
            elif stone[-1] == 3:
                Stone(stone[1], stone[0], 'base').draw(self.screen)

    def score_update(self, color, num):

        if self.player == color:
            self.score += num
        else:
            self.adv_score += num

    def color_toggle(self, color):

        if color == 'B':
            return 'W'
        else:
            return 'B'

    def adjust(self, grid, color):

        if grid in self.board.plus:
            self.score_update(color, 5)
            self.bmap.plus.remove(grid)
        elif grid in self.board.minus:
            self.score_update(color, -5)
            self.bmap.minus.remove(grid)

        self.board.project(self.bmap)

    def cursor_marking(self, mouse, screenSize, tileSize, gridReturn = 0):

        cursor_range = tileSize/2
        for i in range(screenSize[0]):
            for j in range(screenSize[1]):
                x = self.xset + i*tileSize
                y = self.yset + j*tileSize
                x_range = ( x - cursor_range, x + cursor_range )
                y_range = ( y - cursor_range, y + cursor_range )
                if x_range[0] < mouse[0] <= x_range[1]:
                    if y_range[0] < mouse[1] <= y_range[1]:
                        if gridReturn:
                            return (i+1, j+1)
                        else:
                            return (x, y)

        return False

if __name__ == '__main__':
    Batoo()
    quit()



