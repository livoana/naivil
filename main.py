
from naivilLibs.naivilLexer import naivilLexer
from naivilLibs.naivilParser import naivilParser

import argparse

from anytree import  RenderTree
import sys

from naivilLibs.naivilRustTranspiler import naivilRustTranspiler

sys.setrecursionlimit(10000000)

print("Welcome TO NAIVIL COMPILER!")



def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i','--interpreter',action='store_true')
    argparser.add_argument('-c','--compile',action='store_true')
    argparser.add_argument('-v', '--verbose', action='store_true')
    argparser.add_argument('file', nargs='?')
    return argparser.parse_args()

def main():
       
    
    args = parse_args()
    if args.file:
        try:
           f  = open(args.file, "r")        
            
        except:
            print("File not found!")       
            exit()
        text_input = f.read()      
        mLexer = naivilLexer().getLexer()       
        mParser = naivilParser(text_input,mLexer)
        naivilRustTranspiler(mParser.getTree())
        #mInterpreter = naivilInterpreter(mParser.getTree())    
    if args.verbose:
        print(RenderTree(mParser.getTree()))
    
    if args.compile:
        print('Is compile')                     
    if args.interpreter:
        print('Is interpreter')                     
    
    
if __name__ == '__main__':
    main()
