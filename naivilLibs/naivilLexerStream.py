
from rply.lexergenerator import *

class naivilLexerStream(object):
    
    def __init__(self, lexer, s):
        self.lexer = lexer
        self.s = s    
        self.token_list=[]
        for l in lexer.lex(self.s):
            self.token_list.append(l)
        self.idx = 0
        
    def useExpectedToken(self,*args): 
        tk = None
        for name in args:
            tk = self.useToken()
            mPosition=tk.getsourcepos()
            if tk.name != name:
                print("Expected \"%s\" at Line:%s , Column: %s , Got \"%s\""%(name,mPosition.lineno,mPosition.colno,tk.name) )
                exit() 
        return tk            
    def useToken(self):
        tk=self.getCurrent()
        self.idx+=1
        return tk
    def getCurrent(self):
        try:
            return self.token_list[self.idx]
        except IndexError:
            mPosition=self.token_list[-1].getsourcepos()
            print("Unexpected end of file at Line:%s , Column: %s" %(mPosition.lineno,mPosition.colno))
            exit()
    def getNext(self):
        try:
            return self.token_list[self.idx+1]
        except IndexError:
            mPosition=self.token_list[-1].getsourcepos()
            print("Unexpected end of file at Line:%s , Column: %s" %(mPosition.lineno,mPosition.colno))
            exit()              
    def expectedEof(self):
        if not self.isEnd():
            tk = self.getCurrent()
            
            mPosition=tk.getsourcepos()
            print("Expected end of file at Line:%s , Column: %s"  %(mPosition.lineno,mPosition.colno))
            exit()
    def rewind(self):
        self.idx-=1
    def gotoIndex(self,idx):
        self.idx(idx)
    def getCurrentId(self):
        return self.idx       
    def reset_count(self):
        self.idx=0 
    def isEnd(self):
        if self.idx == len(self.token_list):
            return True
        return False