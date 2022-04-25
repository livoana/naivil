
from rply.lexergenerator import *

class naivilLexerSubStream(object):
    
    def __init__(self, token_list):
        
        self.token_list=token_list
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
            print("Unexpected end of LINE at Line:%s , Column: %s" %(mPosition.lineno,mPosition.colno))
            exit()              
    def expectedEof(self):
        if not self.isEnd():
            tk = self.getCurrent()
            
            mPosition=tk.getsourcepos()
            print("Expected end of LINE at Line:%s , Column: %s"  %(mPosition.lineno,mPosition.colno))
            exit()
    def gotoIndex(self,idx):
        self.idx(idx)
    def getCurrentId(self):
        return self.idx     
    def resetSubstream(self):
        self.idx=0
    def goBack(self):
        self.idx-=1    
    def isEnd(self):
        if self.idx == len(self.token_list):
            return True
        return False