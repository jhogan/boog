#! /bin/python
# jessehogandeliamariahogan
#vim: set ts=4 sw=4 et
import copy
import os
import curses
import time
import sys
false=False
true=True
class char:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.letter = char

    def str(self):
        return "%s,%s %s" % (self.x, self.y, self.letter)

class board:
    def __init__(self):

        # create matrix with 5 elements for both dimentions
        # to hold char objects
        self.chars=[None]*5
        for i in range(5):
            self.chars[i] = [None] * 5

        y=0
        if false:
            for line in str.split("\n"):
                x=0
                for c in line:
                    self.chars[y][x] = char(x, y, c)
                    x += 1
                y += 1
            
    def isvalid(self):
        for x in range(5):
            for y in range(5):
                c = self.getchar(x,y)
                if c == None or (c.letter.isupper() and c.letter != 'Q'):
                    return false
        return true

    def getchar(self, x, y):
        return self.chars[y][x]

    def setchar(self, x, y, c):
        self.chars[y][x] = char(x, y, c)

    def str(self):
        r=''
        for w in self.words:
            r+= "%s\n" % w.str() 
        return r

class word:
    def __init__(self):
        self.word=[]

    def str(self):
        r=""
        for c in self.word:
            l = c.letter
            if l == 'Q':
                l='qu'
            r+=l
        return r

    def append(self, c):
        self.word.append(c)

    def contains(self, char):
        for c in self.word:
            if c is char:
                return True
        return False
    def pop(self):
        self.word.pop()

    def len(self):
        return len(self.word)

    def graph(self, board):
        r=""
        for x in range(5):
            for y in range(5):
                c = board.getchar(x,y)
                inword=false
                for c0 in self.word:
                    if c.x == c0.x and c.y == c0.y:
                        r += c.letter.upper()
                        inword=true
                        break
                if not inword:
                    r += c.letter.lower()
            r += "\n"
        return r

class words:

    def __init__(self):
        self.words=[]

    def clear(self):
        self.words=[]

    def append(self, word):
        self.words.append(word)
        self.raiseonappend(word)

    def raiseonappend(self, word):
        self.onappend(word)

    def uniqappend(self, word):
        if not self.contains(word):
            self.append(word)
            
    def contains(self, word):
        for w in self.words:
            if word.str() == w.str():
                return true
        return false
    def str(self):
        r=''
        for w in self.words:
            r+= "%s\n" % w.str() 
        return r
    def graph(self, board):
        r=''
        for w in self.words:
            r += "%s\n\n\n\n" % w.graph(board) 
        return r
    def sort(self):
        new=[]
        smalllist=copy.copy(self.words)
        lennew = len(new)
        lenwords = len(self.words)
        while lennew < lenwords:
            smallest=None
            for w in smalllist:
                if smallest == None or w.len() < smallest:
                    smallest = w.len()
                    smallestword = w

            smalllist.remove(smallestword)
            new.append(smallestword)
            lennew += 1
            

        new.reverse()
        self.words=new

class finger:
    def __init__(self, board):
        self.b=board
        self.word=word()
        self.reset()
    def raiseonboardupd(self):
        self.onboardupd(self)

    def reset(self):
        self.startchar=None

    def nextstart(self):
        if self.startchar == None:
            self.startchar = self.b.getchar(0,0)
        else:
            x=self.startchar.x
            y=self.startchar.y

            if   x < 4:
                x += 1
            elif y < 4:
                x = 0
                y += 1
            else:
                return false # we would be at the end

            self.startchar = self.b.getchar(x,y)

        self.x=self.startchar.x
        self.y=self.startchar.y

        #print "starting at (%s,%s)" % (self.x, self.y)

        self.word=word()
        self.word.append(self.b.getchar(self.x, self.y))
        return true

    def mv(self, direction):
        xincr=0
        yincr=0

        d0=direction[0]
        if len(direction) == 2:
            if direction[1] == 'l':
                xincr=-1
            else:
                xincr=1 # assume 'r'

        if  d0 == 'u':
            yincr=-1
        elif d0 == 'd':
            yincr=1
        elif d0 == 'l':
            xincr=-1
        elif d0 == 'r': 
            xincr=1
    
        prevchar = self.b.getchar(self.x, self.y)

        self.x = self.x + xincr
        self.y = self.y + yincr

        if self.x < 0 or self.y < 0 or self.x > 4 or self.y > 4:
            self.x=prevchar.x
            self.y=prevchar.y
            return false

        char = self.b.getchar(self.x, self.y)

        if self.word.contains(char):
            self.x=prevchar.x
            self.y=prevchar.y
            return False
        
        self.word.append(char)

        return true

    def curchar(self):
        return self.b.getchar(self.x, self.y)

    def revert(self):
        self.word.word.pop()
        if len(self.word.word) > 0:
            c = self.word.word[-1]
            self.x = c.x
            self.y = c.y
        else:
            self.x = None
            self.y = None

    def strword(self):
        r=""
        for i in range(self.word.len()):
            l=self.word.word[i].letter
            if l == 'Q':
                l='qu'
            r += l
        return r
                
    def str(self):
        r=""
        for y in range(5):
            for x in range(5):
                char = self.b.getchar(x,y)
                letter = char.letter
                for c in self.word.word:
                    if c is char:
                        letter = letter.upper()
                        
                r += letter + ' '
            r += "\n"
        return r

class boogler:
    def __init__(self, dict, board):
        self.words=words()
        self.dict = dict
        self.b = board 
        self.f = finger(self.b) 
        self.depth = 0

      
    def find(self):
        self.words.clear()
        self.f.reset()
        while self.f.nextstart():
            self.find_()
    def find_(self):
        #print "depth: %s" % self.depth
        self.depth +=1

        if self.dict.startswith(self.f.strword()):
            for d in ('d', 'u', 'l', 'r', 'dl', 'dr', 'ul', 'ur'):
                if self.f.mv(d):
                    #self.f.raiseonboardupd()
                    
                    #print self.f.str()
                    strword = self.f.strword()
                    if len(strword) > 3:
                        #print "--reverting--"
                        #print self.f.str()
                        if self.dict.find(strword):
                            self.words.uniqappend(copy.deepcopy(self.f.word))
                    self.find_()
        self.f.revert()
        self.depth -=1
    def str(self):
        return self.words.str()

    def graph(self):
        return self.words.graph(self.b)
        
class dict:
    def __init__(self, file):
        self.d={}
        self.l=[]
        f = open(file)
        try:
            for w in f:
                if w[0].islower():
                    self.d[w.rstrip()] = ''
                    self.l.append(w.rstrip())
            self.l.sort()
        finally:
            f.close()
    def find(self, k):
            return (k in self.d)

    def len(self):
        return len(self.d)

    def startswith(self, str):
        hi=len(self.l)
        lo=0
        while lo < hi:
            mid = (lo+hi)//2
            word=self.l[mid]
            if word.startswith(str):
                return true
            elif str < word:
                hi = mid
            else:
                lo = mid+1

class cscr:
    def cboard_onenter(self, obj):
        if self.board.isvalid():
            self.msgstat("finding")
            self.boogler.find()
            self.msgstat("sorting")
            self.boogler.words.sort()
            self.msgstat("displaying")
            self.wrdlst.refresh(None)
            self.msgstat(None)
    def wrdlst_onchange(self, c):
        self.cboard.graph(c.word)

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

    def run(self):
        self.msgstat("loading dictionary")
        d = dict('/usr/share/dict')
        self.msgstat()
        self.board = board()
        self.boogler = boogler(d, self.board)
        self.cwidgets=cwidgets()

        # widget: cboard
        cb=cboard(self, self.boogler)
        cb.top = 3
        cb.left = 3
        self.cwidgets.append(cb)
        self.cboard = cb
        cb.onenter = self.cboard_onenter 

        # widget: wrdlst
        h=self.stdscr.getmaxyx()[0]-3
        w=self.stdscr.getmaxyx()[1]-20

        wl = wrdlst(self, self.boogler, 3, 15, w, h )
        wl.onchange = self.wrdlst_onchange
        self.boogler.words.onappend=wl.onappend
        self.cwidgets.append(wl)
        self.wrdlst=wl
        self.cwidgets.show()


    def msgstat(self, msg=None):
        self.stdscr.addstr(0,0, ' ' * 40)
        if msg != None:
            self.stdscr.addstr(0,0, msg, curses.A_REVERSE)
        self.stdscr.refresh()


    def destroy(self):
        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

class cwidgets:
    def __init__(self):
        self.widgets=[]
        self.TAB='\t'
        self._curwidget=None

    def firstwidget(self):
        for w in self.widgets:
            if w.tabord == 0:
                return w
    def lastwidget(self):
        maxwidget = self.firstwidget()
        for w in self.widgets:
            if w.tabord > maxwidget.tabord:
                maxwidget = w
        return maxwidget.tabord

    def curwidget(self, v=None):
        if v!=None:
            self._curwidget=v
        if self._curwidget == None:
            self._curwidget = self.firstwidget()
        return self._curwidget
                
    def show(self):
        while 1:
            w=self.curwidget()
            r = w.setfocus()
            if r == ord("\t"):
                w = self.curwidget(self.next())
            # fixme
            if r == "":
                w = self.curwidget(self.prev())

                
    def prev(self):
        curtab = self.curwidget().tabord
        for w in self.widgets:
            if curtab - 1 == w.tabord:
                return w
        return self.lastwidget()

    def next(self):
        curtab = self.curwidget().tabord
        for w in self.widgets:
            if curtab + 1 == w.tabord:
                return w
        return self.firstwidget()


    def append(self, w):
        if w.tabord == None:
            w.tabord = self.maxtab() + 1
        self.widgets.append(w)

    def maxtab(self):
        max=-1
        for w in self.widgets:
            if max < w.tabord:
                max = w.tabord
        return max

class cwidget:
    def __init__(self, cscr):
        self.cscr=cscr
        self.stdscr=cscr.stdscr
        self.tabord=None

class cboard(cwidget):
    def __init__(self, cscr, boogler):
        self.x=0
        self.y=0
        self.cmdmode=false
        self.top=self.left=0
        self.board=boogler.b
        self.boogler=boogler

        cwidget.__init__(self, cscr)

        boogler.f.onboardupd=self.onboardupd

    def clean(self):
        self.x=self.y=0
        done=false
        while not done:
            c = self.board.getchar(self.x,self.y)
            self.stdscr.addstr(self.offy(), self.offx(), c.letter)
            self.mvnext()
            done = (self.y==0 and self.x==0)

    def cx(self):
        return self.left + self.x
    def cy(self):
        return self.top + self.y
        
    def setfocus(self):
        while 1:
            c = self.stdscr.getch(self.cy(), self.cx())
            if not self.cmdmode:
                if c == curses.KEY_LEFT:
                    self.mv('l')
                elif c == curses.KEY_RIGHT:
                    self.mv('r')
                elif c == curses.KEY_DOWN:
                    self.mv('d')
                elif c == curses.KEY_UP:
                    self.mv('u')
                elif c == 263: # BS
                    self.backspace()
                elif c == 27: # ESC
                    self.cmdmode=true
                elif c == ord("\n"):
                    self.onenter(self)
                elif c == ord("\t"):
                    return c
                elif c in (range(97, 123) + [81]): # [a-zQ]
                    self.stdscr.addstr(self.cy(), self.cx(), chr(c))
                    self.board.setchar(self.x, self.y, chr(c))
                    if self.board.isvalid():
                        self.cscr.msgstat()
                    else:
                        self.cscr.msgstat('board invalid')
                    self.boogler.f.reset()
                    self.mvnext()
            else:
                if c in (curses.KEY_LEFT, ord('h')):
                    self.mv('l')
                elif c in (curses.KEY_RIGHT, ord('l')):
                    self.mv('r')
                elif c in (curses.KEY_DOWN, ord('j')):
                    self.mv('d')
                elif c in (curses.KEY_UP, ord('k')):
                    self.mv('u')
                elif c == ord('a'):
                    self.mvnext()
                    self.cmdmode=false
                elif c == ord('i'):
                    self.cmdmode=false
                
    def mvnext(self):
        if self.x < 4:
            self.mv('r')
        else:
            self.enter()
                
    def enter(self):
        if self.y < 4:
            self.x=0
            self.y+=1
        elif self.x == 4:
            self.x=self.y=0
    def backspace(self):
        if self.x>0:
            self.x -= 1
        elif self.y>0:
            self.x=4
            self.y -=1

    def mv(self, d):
        xincr=yincr=0
        if  d == 'u':
            yincr=-1
        elif d == 'd':
            yincr=1
        elif d == 'l':
            xincr=-1
        elif d == 'r': 
            xincr=1
   
        self.x = self.x + xincr
        self.y = self.y + yincr

        if self.x < 0 or self.y < 0 or self.x > 4 or self.y > 4:
            self.x = self.x - xincr
            self.y = self.y - yincr

    def graph(self, w):
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            for y in range(5):
                for x in range(5):
                    sx=x+3
                    sy=y+3
                    c = self.board.getchar(x,y)
                    inword=false
                    for c0 in w.word:
                        if c.x == c0.x and c.y == c0.y:
                            if c0 is w.word[-1]:
                                cp=curses.color_pair(6)
                            elif c0 is w.word[0]:
                                cp = curses.color_pair(1)
                            else:
                                cp=curses.color_pair(2)
                            inword=true
                            break
                    if not inword:
                       cp=curses.color_pair(0)
                    self.stdscr.addstr(sy, sx, c.letter, cp)
                self.stdscr.refresh()
        

    def onboardupd(self, f):
            return 
            #time.sleep(0)
            self.cscr.wrdlst.updwrd(f.word.str())
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            i=1
            for y in range(5):
                for x in range(5):
                    sx=x+3
                    sy=y+3
                    c = f.b.getchar(x,y)
                    inword=false
                    for c0 in f.word.word:
                        if c.x == c0.x and c.y == c0.y:
                            if c0 is f.word.word[-1]:
                                pass
                                #self.stdscr.addstr(sy, sx, c.letter, curses.color_pair(6))
                            else:
                                pass
                                #self.stdscr.addstr(sy, sx, c.letter, curses.color_pair(i))
                            inword=true
                            if i < 2: i += 1
                            break
                    if not inword:
                        pass
                        #self.stdscr.addstr(sy, sx, c.letter, curses.color_pair(0))
                    self.stdscr.refresh()
class wrdlst(cwidget):
    def __init__(self, cscr, boogler, top, left, width, hight):
        self.boogler=boogler
        self.win=curses.newwin(hight, width, top, left)
        self.win.keypad(1)
        self.win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.win.refresh()
        self.x=self.y=1
        self.page=self.maxpage=0
        self.cellmargin=1
        self._cells=None
        cwidget.__init__(self, cscr)
        self._curcell=None

    def setfocus(self):
        while 1:
            curses.curs_set(0)
            self.curcell()
            c = self.win.getch(0,0)
            if c == ord("\t"):
                curses.curs_set(1)
                return c
            elif c in (curses.KEY_LEFT, ord('h')):
                self.mv('l')
            elif c in (curses.KEY_RIGHT, ord('l')):
                self.mv('r')
            elif c in (curses.KEY_DOWN, ord('j')):
                self.mv('d')
            elif c in (curses.KEY_UP, ord('k')):
                self.mv('u')
            elif c == curses.KEY_NPAGE:
                if self.page < self.maxpage:
                    self.page += 1
                    self.refresh()
                    self.curcell(None, true)
            elif c == curses.KEY_PPAGE:
                if self.page != 0:
                    self.page -= 1
                    self.refresh()
                    self.curcell(None, true)


    def getcell(self, x, y, page):
        for c in self._cells:
            if c.x == x and c.y == y and c.page == page:
                return c
        return None
                
    def curcell(self, c=None, refresh=false):
        if c==None:
            if refresh or self._curcell == None:
                for c in self._cells:
                    #if c.y==0 and c.x==0:
                    if c.page == self.page:
                        self.refresh(c)
                        self._curcell=c
                        self.onchange(c)
                        break
        else:
            self._curcell=c
            self.onchange(c)
            self.refresh(c)
        return self._curcell

    def mv(self, d):
        cc = self.curcell()
        if cc == None: return
        if  d == 'u':
            c = self.getcell(cc.x, cc.y - 1, cc.page)
        elif d == 'd':
            c = self.getcell(cc.x, cc.y + 1, cc.page)
        elif d == 'l':
            c = self.getcell(cc.x - 1, cc.y, cc.page)
        elif d == 'r': 
            c = self.getcell(cc.x + 1, cc.y, cc.page)
        if c != None:
            self.curcell(c)

    def clear(self):
        self._cells=None
        self.win.erase()
        self.win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.win.refresh()
        self.x=self.y=1

    def append(self, w):
        # don't need to use w param
        # we have ref to boogler.words
        #self.refresh(w)
        pass

    def updwrd(self, w):
        #self.win.addstr(self.y+1, self.x, ' ' * 20)
        #self.win.addstr(self.y+1, self.x, w)
        #self.win.refresh()
        pass
        
    def onappend(self,w):
        self.append(w)

    def refresh(self, hlc=None):
        self.x=self.cellmargin
        self.clear()
        cells = self.cells(true) #force refresh
        for col in range(self.columncnt()):
            lastc=None
            for c in cells:
                if c.page == self.page and c.x==col:
                    self.y=c.y+self.cellmargin
                    if hlc != None and hlc.x == c.x and hlc.y == c.y:
                        self.win.addstr(self.y, self.x, c.word.str(), curses.A_REVERSE )
                    else:
                        self.win.addstr(self.y, self.x, c.word.str())
                    lastc=c
            if lastc != None:
                self.x += (lastc.len() + self.cellmargin)
        self.win.refresh()

    def cells(self, refresh=false):
        if self._cells == None or refresh:
            maxyx=self.win.getmaxyx()
            maxy=maxyx[0]
            maxx=maxyx[1]
            self.maxpage=x=y=page=0
            self._cells=[]
            for w in self.boogler.words.words:
                c = wrdlst.cell(w, self)
                c.y=y; c.x=x; c.page=page
                if c.y == maxy-self.cellmargin-2:
                    if self.cellslen(page) > maxx-10:
                        page+=1
                        self.maxpage=page
                        y=x=0
                    else:
                        x+=1
                        y=0
                else:
                    y+=1
                self._cells.append(c)
        return self._cells

    def cellslen(self, page):
        len=0
        for c in self.cells():
            if c.y==0 and c.page == page:
                for colord in range(self.columncnt()):
                    if c.x==colord:
                        len+=(c.len() + self.cellmargin)
                        break
        return len

    def columncnt(self):
        maxx=0
        for c in self.cells():
            if maxx < c.x:
                maxx = c.x
        return maxx+1

    def row(self, ordinal):
        r=[]
        for c in self.cells():
            if c.x == ordinal:
                r.append(c)
        return r


    class cell:
        def __init__(self, word, wrdlst):
            self.word=word
            self.wrdlst=wrdlst
            self.x=self.y=self.page=None

        def str(self):
            return self.word.str()
                
        def len(self):
            maxlen=0
            for c in self.wrdlst.row(self.x):
                #if c.page != self.page: continue
                wrdlen=len(c.word.str())
                if wrdlen > maxlen:
                    maxlen = wrdlen
            return maxlen

c=cscr()
try:
    c.run()
except KeyboardInterrupt:
    c.destroy()
except:
    c.destroy()
    print sys.exc_info()[0]



