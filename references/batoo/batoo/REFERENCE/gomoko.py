# -*- coding: utf-8 -*-
from pygame import *
time.Clock()
import socket
from toolbox.EasyGame import entry
from toolbox.Menu import slidemenu
import threading
    
class Game(list,object):
    
    blanc = image.load('blanc.png')
    noir = image.load('noir.png')
    board = image.load('board.png')
    
    def __init__(self):
        self.scr = display.set_mode((570,570))
        self.choice = slidemenu(['Make Server','Join Server','Quit'],pos='center',color1=(100,100,100),color2=(200,200,200))[0]
        if self.choice != 'Quit':
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc.settimeout(5.0)
            ### tentatives de connection
            self.is_server = False
            ### si on est server
            if self.choice == 'Make Server':
                self.is_server = True
                soc.bind(('',50007))
                soc.listen(1)
                ### attend un client temps que l'on ne quitte pas
                while True:
                    try:
                        print('awaiting for player connection')
                        self.conn = soc.accept()[0]
                        break
                    except:
                        for ev in event.get():
                            if ev.type == QUIT: exit()
            ### si on est client
            else:
                foo = True # pour break un double-while
                while foo:
                    ### demande l'ip du server temps que celui-ci n'est pas valide ou jusqu'à ce qu'on exit()
                    ip = entry('host ip   : <15,15>',width = 280)
                    if not ip or not ip[0]: print('exit');exit()
                    while True:
                        ### si l'ip est valide, attend la connection temps que l'on exit() pas
                        try:
                            print('try to connect...')
                            soc.connect((ip[0],50007))
                            foo = False
                            print('connected')
                            break
                        except socket.timeout:
                            print('good ip ... ?')
                            break
                        except socket.error:
                            print('...refused')
                            time.wait(1000)
                            for ev in event.get():
                                if ev.type == QUIT:
                                    print('exit game')
                                    exit()
                    self.conn = soc
            soc.settimeout(None)
            ### à partir d'ici, les connections sont établies
            T = threading.Thread(target=self.read)
            T.start()
            self.player = 0
            replay = True
            self.game_over = False
            while replay:
                if self.is_server:
                    playerorder = time.get_ticks()&1
                    self.conn.send(str(playerorder).encode('UTF-8'))
                    self.player = playerorder^1
                else:
                    while not self.game_over:
                        ev = event.wait()
                        if ev.type == USEREVENT+1:
                            if type(ev.data) == int:
                                self.player = ev.data
                                break
                            else: event.post(ev)
                del(self[:])
                self.extend([['_']*19 for foo in range(19)])
                self.winnerspawns = []
                self.scr.blit(Game.board,(0,0))#self.draw_grid()
                display.update()
                self.turn = 120
                self.playable_pos = [(9,9)]
                if self.player == 0:
                    event.post(event.Event(MOUSEBUTTONUP,{'button':1,'pos':(270,270)}))
                self.bigplotpos = None
                while not self.game_over: self.update()
                if self.winnerspawns:
                    self.show_winnerspawns()
                elif not self.turn:
                    display.update(self.scr.fill((255,128,128),(14,14,541,541),BLEND_RGB_ADD))
                    print('tie game')
                elif not self.playable_pos:
                    display.update(self.scr.fill((255,128,128),(14,14,541,541),BLEND_RGB_ADD))
                    print('game stuck')
                else: replay = False
                self.game_over = False
                if replay:
                    while not self.game_over:
                        ev = event.wait()
                        if ev.type == KEYDOWN: break
                        else: event.post(ev)
                    self.scr.fill(0)
                    display.flip()
                    replay = slidemenu(['Replay','Quit'],pos='center',color1=(100,100,100),color2=(200,200,200))[1]^1
        else: exit()
        try: self.conn.send('"quit"'.encode('UTF-8'))
        except: print('pipe broken')
        T.join()
        self.conn.close()
    
    def update(self):
        if self.turn&1 == self.player:
            ev = event.wait()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE or ev.type == QUIT:
                self.game_over = True
                return
            elif ev.type == MOUSEBUTTONUP and ev.button == 1:
                x,y = ev.pos[0]//30,ev.pos[1]//30
                if (x,y) in self.playable_pos:
                    self.put_pawn(x,y)
                    self.conn.send(str((x,y)).encode('UTF-8'))
            elif ev.type == MOUSEMOTION:
                x,y = ev.pos[0]//30,ev.pos[1]//30
                if (x,y) != self.bigplotpos:
                    if self.bigplotpos:
                        X,Y = self.bigplotpos
                        r = self.unplot_(X,Y)
                        self.scr.fill(Color('brown3'),(X*30+12,Y*30+12,5,5))
                        display.update(r)
                    if (x,y) in self.playable_pos:
                        display.update(self.scr.fill(Color('darkred'),(x*30+10,y*30+10,9,9)))
                        self.bigplotpos = (x,y)
                    else: self.bigplotpos = None
        else:
            ev = event.poll()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE or ev.type == QUIT: self.game_over = True
            elif ev.type == USEREVENT+1: self.put_pawn(*ev.data)
            time.wait(1)
            
    def unplot_(self,x,y):
        r = Rect(x*30+10,y*30+10,9,9)
        self.scr.blit(Game.board,r,r)
        return r

    def put_pawn(self,x,y):
        pawn = self.turn&1
        if self.turn&1 == self.player:
            display.update([self.unplot_(*r) for r in self.playable_pos])
        self[x][y] = str(pawn)
        display.update(self.scr.blit(Game.blanc if pawn else Game.noir,(x*30-2,y*30-2)))
        self.actual_pos = x,y
        self.playable_pos = [(x+offx,y+offy) for offx,offy in ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)) if -1<x+offx<19 and -1<y+offy<19 and self[x+offx][y+offy] == '_']
        if not self.playable_pos: self.game_over = True
        if self.turn&1 != self.player:
            display.update([self.scr.fill(Color('brown3'),(X*30+12,Y*30+12,5,5))for X,Y in self.playable_pos])
        self.bigplotpos = None
        if self.is_winner():
            self.game_over = True
            return
        self.turn -= 1
        if not self.turn: self.game_over = True # tie game
        
    def is_winner(self):
        pawn = self.turn&1
        X,Y = self.actual_pos
        invpawn = str(pawn^1)
        pawn = str(pawn)
        row1 = [((X,y),self[X][y])for y in range(19)]+[('',invpawn)]
        row2 = [((x,Y),self[x][Y])for x in range(19)]+[('',invpawn)]
        foo = X-Y
        row3 = [((x,x-foo),self[x][x-foo])for x in range(19)if x-foo<19]+[('',invpawn)]
        foo = X+Y
        row4 = [((x,foo-x),self[x][foo-x])for x in range(19)if foo-x<19]+[('',invpawn)]
        for row in (row1,row2,row3,row4):
            coords,pawns = zip(*row)
            pawns = ''.join(pawns)
            index1 = pawns.find(pawn*5)
            if index1 == -1: continue
            index2 = pawns[index1:].find(pawn+invpawn)
            index2bis = pawns[index1:].find(pawn+'_')
            if -1 < index2 and -1 < index2bis: index2 = min(index2,index2bis)
            else: index2 = max(index2,index2bis)
            if index2 == -1: continue
            self.winnerspawns.extend(coords[index1:index2+index1+1])
        return self.winnerspawns
    
    def show_winnerspawns(self):
        self.scr.fill((128,128,128),(14,14,541,541),BLEND_RGB_ADD if not self.turn&1 else BLEND_RGB_SUB)
        pawn = Game.blanc if self.turn&1 else Game.noir
        [self.scr.blit(pawn,(x*30-2,y*30-2))for x,y in self.winnerspawns]
        display.flip()
    
    def read(self):
        while True:
            try: data = eval(self.conn.recv(8))
            except:
                print('pipe broken')
                data = 'quit'
            if data == 'quit':
                self.game_over = True
                break
            event.post(event.Event(USEREVENT+1,{'data':data}))
        

Game()
quit()
