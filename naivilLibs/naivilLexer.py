from rply import LexerGenerator

class naivilLexer():
    def __init__(self):
        self.nLexer = LexerGenerator()
    
    def defineTokens(self):
        
        self.nLexer.add('COMMENT', r'#.*')
        
        self.nLexer.add('VAR','var')
        
        self.nLexer.add('FUNCTION','func') 
        
        self.nLexer.add('RUST_NATIVE','rust')
        
        self.nLexer.add('IF','if')
        self.nLexer.add('ELSE','else')
        self.nLexer.add('ELSEIF','elseif')
        
        self.nLexer.add('FOR','for')
     
        self.nLexer.add('WHILE','while')
        self.nLexer.add('BREAK','break')
        self.nLexer.add('SWITCH','switch')
        self.nLexer.add('CASE','case')
        
        self.nLexer.add('VARIABLE_TYPE',r'int32|int64|int128|bigint')
        self.nLexer.add('VARIABLE_TYPE',r'float')
        self.nLexer.add('VARIABLE_TYPE',r'str')
        self.nLexer.add('VARIABLE_TYPE',r'void')
        
        self.nLexer.add('IN','in')
        
        self.nLexer.add('STRING', r'"(\\"|[^"])*"')
        self.nLexer.add('STRING', r"'(\\'|[^'])*'")
        self.nLexer.add('NUMBER', r'\d+\.\d+')
        self.nLexer.add('NUMBER', r'\d+')
        self.nLexer.add('NAME', r'[a-zA-Z_]\w*')
                     
        self.nLexer.add('ARITHMETIC_OPERATOR', r'[\^\+\*\-\/%]')   
        self.nLexer.add('COMPARISON_OPERATOR', r'<=|>=|==|!=|<|>') 
        self.nLexer.add('BOOLEAN_OPERATOR', r'\|\||&&')           
        self.nLexer.add('RANGE_OPERATOR', r'\.\.\.|\.\.')      
        
        self.nLexer.add('NOT', '!')                  
        
        self.nLexer.add('ASSIGN', '=')
        
        self.nLexer.add('(', r'\(')
        self.nLexer.add(')', r'\)')
        self.nLexer.add('[', r'\[')
        self.nLexer.add(']', r'\]')
        self.nLexer.add('{', r'\{')
        self.nLexer.add('}', r'\}')
        
        self.nLexer.add('TRUE', 'True')
        self.nLexer.add('FALSE', 'False')
        
        self.nLexer.add('COLON', ':')
        self.nLexer.add('SEMICOLON', ';')
        self.nLexer.add('COMMA', ',')
        
        # Ignore spaces
        self.nLexer.ignore('\s+')
       
        
    
    def getLexer(self):
        self.defineTokens()
        return self.nLexer.build()        