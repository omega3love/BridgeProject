from batoomap import *
from batoo import *
from pygame import *
import batoomaps
import socket
import threading
from random import random

HOST = '143.248.2.116'
PORT = 50000

class Batoo(object):

    size = ( 11, 11 )
    tileSize = 55
    screen_size = ( (size[0]+1)*tileSize, (size[1]+1)*tileSize )

    board = Board()
    board.rect.center = ( screen_size[0]/2, screen_size[1]/2 )
    cursor_mark = Cursor_Marking(tileSize)

    bmap = batoomaps.sky()
    board.project(bmap)

    def __init__(self):

        init()
        self.screen = display.set_mode(Batoo.screen_size)
        self.clock = time.Clock()
        self.fps = 30
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

        T = threading.Thread(target = self.read)
        T.start()
        replay = True
        self.game_over = False

        while True:
            ev = event.poll()
            if ev.type == USEREVENT+1:
                if ev.data == 'initialize':
                    break
            time.wait(1)
        time.wait(1000)

        while replay:
            self.pcm.history = []
            self.screen.fill(WHITE)
            self.board.draw(self.screen)
            display.update()

            self.turn = 1
            self.score = 0
            self.adv_score = 0
            self.marked_pos = None
            self.hidden = False
            self.base = []
            self.get_color()
            print 'your color is ' + self.player
            self.base_build()
            print 'betting started'
            self.betting()
            print 'betting finished'
            print self.player
            while not self.game_over:
                self.update()

        try:
            self.conn.send('"quit"'.encode('UTF-8'))
        except:
            print 'pipe broken'
        T.join()
        self.conn.close()

    def read(self):

        while True:
            try:
                data = self.conn.recv(100)
            except:
                print 'pipe broken?'
                data = 'quit'
            if data == 'quit':
                self.game_over = True
                break
            event.post(event.Event(USEREVENT + 1, {'data':data}))

    def update(self):

        self.screen.fill(WHITE)
        self.board.draw(self.screen)

        if self.turn & 1 == self.order:
            ev = event.wait()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE or ev.type == QUIT:
                self.game_over = True
                return
            elif ev.type == KEYDOWN and ev.key == K_h and not self.hidden:
                self.hidden = True
            elif ev.type == MOUSEBUTTONUP and ev.button == 1:
                if self.hidden:
                    self.placing(ev.pos, False, 'hidden')
                    self.hidden = False
                else:
                    self.placing(ev.pos)
            elif ev.type == MOUSEMOTION:
                self.placing(ev.pos, True)
        else:
            ev = event.poll()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE or ev.type == QUIT:
                self.game_over = True
            elif ev.type == USEREVENT+1:
                print 'hello', ev.data, type(ev.data)
                try:
                    print 's1'
                    data = eval(ev.data)
                    print 's2'
                    if type(data) == list:
                        self.pcm_update(data)
                    elif type(data) == int:
                        self.adv_score = data
                        print 'hi', self.score, self.adv_score
                except:
                    if 'adjust' in ev.data:
                        adj = ev.data.split(':')
                        if adj[1] == 'plus':
                            self.bmap.plus = eval(adj[2])
                        else:
                            self.bmap.minus = eval(adj[2])
                    else:
                        try:
                            self.pcm_update(ev.data)
                        except:
                            print 'man', ev.data, type(ev.data)
            time.wait(1)

        self.drawing_stones()
        display.update()
        self.clock.tick(self.fps)

    def color_toggle(self, color):

        if color == 'B':
            return 'W'
        else:
            return 'B'

    def get_color(self):

        num = random()
        self.conn.send(str(num).encode('UTF-8'))
        while not self.game_over:
            ev = event.wait()
            if ev.type == USEREVENT + 1:
                adv_num = eval(ev.data)
                break

        if num > adv_num:
            self.player = 'B' #black
        else:
            self.player = 'W'

    def betting(self):

        adv_bet_score = None

        while True:
            #bet_score = input('bet a score(1~15) : ')
            bet_score = 3 
            self.conn.send(str(bet_score).encode('UTF-8'))

            while not self.game_over:
                ev = event.wait()
                if ev.type == USEREVENT + 1:
                    adv_bet_score = eval(ev.data)
                    break

            if bet_score > adv_bet_score:
                self.order = 1 #first
                break
            elif bet_score < adv_bet_score:
                self.order = 0 #second
                self.score += adv_bet_score
                break
            else:
                continue

    def base_build(self):

        while len(self.base) < 3:
            self.screen.fill(WHITE)
            self.board.draw(self.screen)

            ev = event.wait()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE or ev.type == QUIT:
                self.game_over = True
                return
            elif ev.type == MOUSEBUTTONUP and ev.button == 1:
                grid = cursor_marking(ev.pos, self.size, self.tileSize, 1)
                if grid:
                    base = [ grid, self.player, 3 ]
                    if base not in self.base:
                        self.base.append(base)
                        self.pcm.history.append(base)
            elif ev.type == MOUSEMOTION:
                grid = cursor_marking(ev.pos, self.size, self.tileSize, 1)
                if grid and grid not in [ s[0] for s in self.base ]:
                    self.cursor_mark.draw(self.screen, grid)
            elif ev.type == USEREVENT + 1:
                adv_base = eval(ev.data)
            time.wait(1)

            self.drawing_stones()
            display.update()
            self.clock.tick(self.fps)

        self.conn.send(str(self.base).encode('UTF-8'))
        while True:
            try:
                adv_base
                break
            except:
                ev = event.wait()
                if ev.type == USEREVENT + 1:
                    adv_base = eval(ev.data)
                    break
            time.wait(1)

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

    def placing(self, pos, marking = False, stone_type = 'normal'):

        markable = cursor_marking(pos, self.size, self.tileSize, 1)
        if markable:
            placable = self.pcm.is_placable(markable, self.player)
            if placable:
                if marking:
                    self.cursor_mark.draw(self.screen, markable)
                else:
                    if placable == 'hidden': #already occupied
                        adv = self.color_toggle(self.player)
                        ind = self.find_stone(markable, adv, 2)
                        self.pcm.history[ind][-1] = 1
                        self.conn.send('discovered')
                    else:
                        s = 1 if stone_type == 'normal' else 2 if stone_type == 'hidden' else 3
                        info = [ markable, self.player, s ]
                        if s != 2:
                            self.adjust(markable)
                        time.wait(1)
                        self.pcm_update(info)
                        time.wait(1)
                        self.conn.send(str(info).encode('UTF-8'))


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
            self.adjust(self.pcm.history[ind][0])
            return

        self.pcm.history.append(info)
        catchable = self.pcm.is_catching(info[0], info[1])
        if catchable:
            for caught in catchable:
                for stone in self.pcm.history:
                    if stone[0] == caught:
                        if stone[-1] == 1:
                            stone[-1] = 0
                            self.score += 1
                        elif stone[-1] == 2:
                            stone[-1] = 0
                            self.conn.send('discovered')
                            self.score += 1
                            #notify adv's hidden is caught
                        elif stone[-1] == 3:
                            stone[-1] = 0
                            self.score += 5

        time.wait(1)
        self.turn += 1
        self.score += 1
        self.conn.send(str(self.score).encode('UTF-8'))
        time.wait(1)

    def drawing_stones(self):

        for stone in self.pcm.history:
            pos = grid_to_rectcenter(stone[0], self.tileSize)
            if stone[-1] == 1:
                Stone(stone[1], stone[0]).draw(self.screen, pos)
            elif stone[-1] == 2 and self.player == stone[1]:
                Stone(stone[1], stone[0], 'hidden').draw(self.screen, pos)
            elif stone[-1] == 3:
                Stone(stone[1], stone[0], 'base').draw(self.screen, pos)

    def adjust(self, grid):

        if grid in self.board.plus:
            self.score += 5
            self.bmap.plus.remove(grid)
            self.conn.send('adjust:plus:'+str(self.bmap.plus).encode('UTF-8'))
        elif grid in self.board.minus:
            self.score -= 5
            self.bmap.minus.remove(grid)
            self.conn.send('adjust:minus:'+str(self.bmap.minus).encode('UTF-8'))
        self.board.project(self.bmap)

if __name__ == '__main__':
    Batoo()




