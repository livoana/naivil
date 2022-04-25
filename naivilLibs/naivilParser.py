
from anytree import Node

from naivilLibs.naivilLexerStream import naivilLexerStream
from naivilLibs.naivilLexerSubStream import naivilLexerSubStream

class naivilParser():
    
    def __init__(self,text_input,lexer):
        self.lexerStream = naivilLexerStream(lexer,text_input)
        self.root = Node("Env",parent=None)
        
        self.functionParsers(self.lexerStream,self.root)
      
    def getTree(self):
        return self.root
    
    # FUNCTION PARSE METHODS
    
    def functionParsers(self,lexStream,node):
        
        functions = Node("FUNCTIONS",parent=node)
        while not lexStream.isEnd():
            if lexStream.useToken().name == "FUNCTION":
                
                try:
                    f_type = lexStream.useExpectedToken("VARIABLE_TYPE")
                    f_name = lexStream.useExpectedToken("NAME")
                    source_pos = f_name.getsourcepos()
                    mNode=Node(f_name.value,functions,idx=lexStream.getCurrentId(),token=f_name,returnType=f_type)
                    self.functionParamsParser(lexStream,mNode)
                    self.functionBodyParser(lexStream,mNode)
                    
                except:    
                    print("No functions found error!!!")
                    exit()
    def functionParamsParser(self,lexStream,node):
        mParams=Node("Params",node)
        try:
            lexStream.useExpectedToken("(")
        except:
            exit()
        last = None
        while not lexStream.isEnd():
            tk = lexStream.useToken()
            if tk.name == "NAME":
                Node(tk.value,mParams,token=tk,type=last)  
            if tk.name ==")":
                break     
            last = tk
    
    def functionBodyParser(self,lexStream,node):
        mBody = Node("Body",node)        
        
        try:
            lexStream.useExpectedToken("{")
        except:
            exit()
        
        while not lexStream.isEnd():
            currentToken = lexStream.useToken()
            
            if (currentToken.name == "}") and (lexStream.getCurrent().value == ";"):
                    break     
            else:
                if ((currentToken.name == "RUST_NATIVE") and lexStream.getCurrent().name =="STRING"):
                    name = lexStream.useExpectedToken("STRING")
                    Node("RUST_NATIVE",mBody,tk=name,type=name)
                    lexStream.useExpectedToken("SEMICOLON")
                    pass
                elif ((currentToken.name == "VAR") and lexStream.getCurrent().name =="NAME"):
                    name = lexStream.useExpectedToken("NAME")
                    type = lexStream.useExpectedToken("VARIABLE_TYPE")
                    Node("VARIABLE",mBody,value=name.value,tk=name,type=type)
                    lexStream.useExpectedToken("SEMICOLON")
                    pass
                
                elif ((currentToken.name == "NAME") and lexStream.getCurrent().value =="="):
                    
                    lexStream.useExpectedToken("ASSIGN")
                    expected_list=['ARITHMETIC_OPERATOR','NAME','NUMBER','STRING','(',')','COMMA']
                    param_list = self.readUntillToken(lexStream,";",expected_list)
                    if len(param_list)==0:
                        print("Unexpected token near {%s} at Line: %s, Column: %s"%(currentToken.value,currentToken.getsourcepos().lineno,currentToken.getsourcepos().colno))
                        exit()
                    mAssignNode = Node("ASSIGN",mBody)
                    mLeftNode=Node("left",mAssignNode)
                    mRightNode=Node("right",mAssignNode)
                    Node("VALUE",mLeftNode,value=currentToken.value,token=currentToken)
                    if(len(param_list)==1):
                        Node('VALUE',mRightNode,value=param_list[0].value,token=param_list[0])
                    elif(len(param_list)>1):
                        
                        self.parseExpression(param_list,mRightNode)
                elif((currentToken.name == 'FOR')and lexStream.getCurrent().value =='('):
                    condition = self.readBetweenBrackets(lexStream,"(",")",None)
                    forBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    self.parseForStatement(condition,forBody,mBody)
                                            
                elif ((currentToken.name == "NAME") and lexStream.getCurrent().value =="("):
                    expected_list=['ARITHMETIC_OPERATOR','NAME','NUMBER','STRING','(',')','COMMA']
                    
                    param_list = self.readBetweenBrackets(lexStream,"(",")",expected_list)
                    self.parseCallFunction(currentToken,param_list,mBody)
                elif((currentToken.name == 'IF')and lexStream.getCurrent().value =='('):
                    condition = self.readBetweenBrackets(lexStream,"(",")",None)
                    ifBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    elseBody = None
                    if(lexStream.getCurrent().name=="ELSE"):
                        lexStream.useExpectedToken("ELSE")
                        elseBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    self.parseIfStatement(condition,ifBody,elseBody,mBody) 
                elif((currentToken.name == 'WHILE')and lexStream.getCurrent().value =='('):
                    condition = self.readBetweenBrackets(lexStream,"(",")",None)
                    whileBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    self.parseWhileStatement(condition,whileBody,mBody)
                
    # FOR STATEMENT METHODS
    def parseForStatement(self,condition,forBody,mNode):
        mForNode = Node("FOR STATEMENT",mNode)
        mForCondition = Node("Condition",mForNode)
        mForBody = Node('Body',mForNode)
        self.parseForCondition(condition,mForCondition)
        self.parseForBody(forBody,mForBody)   
    def parseForCondition(self,param_list,mNode):  
        condition_list = []
        left  = []
        right = []
        for p in range(len(param_list)):
            
            if param_list[p].name=="IN":
              
              left=param_list[0:p]
              right=param_list[p+1:len(param_list)]  
        Node("INDEX",mNode,value=left[0].value,range_low=right[2].value,range_high=right[4].value)
        pass
    def conditionSubparser(self,param_list,mNode):
        lexStream = naivilLexerSubStream(param_list)
        left = []
        right= []
        operator = []
        while not lexStream.isEnd():
            currentToken = lexStream.useToken()
            if ((currentToken.name == "NAME") and lexStream.getCurrent().value == "="):
                mAssignNode = Node("ASSIGN",mNode)
                mLeftNode=Node("left",mAssignNode)
                mRightNode=Node("right",mAssignNode)
                left.append(currentToken)
                operator.append(lexStream.useExpectedToken("ASSIGN"))
                while not lexStream.isEnd():
                    right.append(lexStream.useToken())
                
                Node("VALUE",mLeftNode,value=currentToken.value,token=currentToken)
                if(len(right)==1):
                    Node('VALUE',mRightNode,value=right[0].value,token=right[0])
                elif(len(right)>1):
                    self.parseExpression(right,mRightNode)    
                break                           
                
            elif ((currentToken.name == "NAME") and lexStream.getCurrent().name =="COMPARISON_OPERATOR"):
                mComparisonNode = Node("COMPARISON_OPERATOR",mNode,value=lexStream.getCurrent().value)
                mLeftNode=Node("left",mComparisonNode)
                mRightNode=Node("right",mComparisonNode)
                left.append(currentToken)
                operator.append(lexStream.useExpectedToken("COMPARISON_OPERATOR"))
                while not lexStream.isEnd():
                    right.append(lexStream.useToken())
                Node("VALUE",mLeftNode,value=currentToken.value,token=currentToken)
                if(len(right)==1):
                    Node('VALUE',mRightNode,value=right[0].value,token=right[0])
                elif(len(right)>1):
                    self.parseExpression(right,mRightNode)    
                break                                    
    def parseForBody(self,param_list,mBody):
        lexStream = naivilLexerSubStream(param_list)
        while not lexStream.isEnd():
            currentToken = lexStream.useToken()
            
            if (currentToken.name == "}") and (lexStream.getCurrent().value == ";"):
                    break     
            else:
                if ((currentToken.name == "NAME") and lexStream.getCurrent().value =="="):
                    lexStream.useExpectedToken("ASSIGN")
                    expected_list=['ARITHMETIC_OPERATOR','NAME','NUMBER','STRING','(',')']
                    param_list = self.readUntillToken(lexStream,";",expected_list)
                    if len(param_list)==0:
                        print("Unexpected token near {%s} at Line: %s, Column: %s"%(currentToken.value,currentToken.getsourcepos().lineno,currentToken.getsourcepos().colno))
                        exit()
                    mAssignNode = Node("ASSIGN",mBody)
                    mLeftNode=Node("left",mAssignNode)
                    mRightNode=Node("right",mAssignNode)
                    Node("VALUE",mLeftNode,value=currentToken.value,token=currentToken)
                    if(len(param_list)==1):
                        Node('VALUE',mRightNode,value=param_list[0].value,token=param_list[0])
                    elif(len(param_list)>1):
                        
                        self.parseExpression(param_list,mRightNode)
                                        
                elif ((currentToken.name == "NAME") and lexStream.getCurrent().value =="("):
                    expected_list=['ARITHMETIC_OPERATOR','NAME','NUMBER','STRING','(',')',"COMMA"]
                    param_list = self.readBetweenBrackets(lexStream,"(",")",expected_list)
                    self.parseCallFunction(currentToken,param_list,mBody)
                elif((currentToken.name == 'IF')and lexStream.getCurrent().value =='('):
                    condition = self.readBetweenBrackets(lexStream,"(",")",None)
                    ifBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    elseBody = None
                    if(lexStream.getCurrent().name=="ELSE"):
                        lexStream.useExpectedToken("ELSE")
                        elseBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    self.parseIfStatement(condition,ifBody,elseBody,mBody)   
    
    # WHILE STATEMENT METHODS
    
    def parseWhileStatement(self,condition,whileBody,mNode):
        mWhileNode = Node("WHILE STATEMENT",mNode)
        mWhileCondition = Node("Condition",mWhileNode)
        mWhileBody = Node('Body',mWhileNode)
        self.parseWhileCondition(condition,mWhileCondition)
        self.parseWhileBody(whileBody,mWhileBody)        
    def parseWhileCondition(self,param_list,mNode):
        subStream=naivilLexerSubStream(param_list)
        operand_list=[]
     
        while not subStream.isEnd():
            currentToken = subStream.useToken()
            if(subStream.isEnd()):
                temp_list =[]
                temp_list.append(currentToken)
                operand_list.append(temp_list)
            else:
                if currentToken.name=="NAME" and subStream.getCurrent().name=='(':
                    temp_list = []
                    temp_list.append(currentToken)
                    while True:
                        currentToken = subStream.useToken()
                        temp_list.append(currentToken)
                        if currentToken.name==')':
                            operand_list.append(temp_list)
                            break
                else: # to do brackets
                    temp_list =[]
                    temp_list.append(currentToken)
                    operand_list.append(temp_list)
        self.evaluateWhileCondition(operand_list,mNode)
        pass       
    def evaluateWhileCondition(self,operandList,mNode):
        if len(operandList)==1:
            if(len(operandList[-1]) >1):
                mArgs = self.prepareFunctionArgs(operandList[-1])
                self.parseCallFunction(mArgs[0],mArgs[1],mNode)
        
        else:
            for idx, op in enumerate(operandList):
                if len(op)==1 and op[0].name=="COMPARISON_OPERATOR":
                    if(op[0].value in ["<=",">=","==","!=","<",">"]):
                        
                        right=[]
                        left =[]
                        operator = operandList[idx]
                        mOperationNode = Node(operator[0].name,mNode,value=operator[0].value)
                        mLeftNode=Node("left",mOperationNode)
                        mRightNode=Node("right",mOperationNode)
                        for i in range(0,idx):
                            left.append(operandList[i])
                        for i in range(idx+1,len(operandList)):
                            right.append(operandList[i]) 
                        if len(left)>1:
                            print(left)
                            print(right)
                            print('Syntax error at line: %s ' %(left[0][0].getsourcepos().lineno) )
                            exit()
                        if len(left[0])==1:
                            Node("VALUE",mLeftNode,value=left[0][0].value,token=left[0][0]) 
                        else:
                            mArgs = self.prepareFunctionArgs(left[0])
                            self.parseCallFunction(mArgs[0],mArgs[1],mLeftNode)
                            pass      
                        if len(right)==1:
                            if len(right[0])==1:
                                Node("VALUE",mRightNode,value=right[0][0].value,token=right[0][0])
                            else:
                                mArgs = self.prepareFunctionArgs(left[0])
                                self.parseCallFunction(mArgs[0],mArgs[1],mRightNode)
                                pass
                        else:
                            self.evaluateExpressionList(right,mRightNode)
                        break                    
    def parseWhileBody(self,param_list,mBody):
        lexStream = naivilLexerSubStream(param_list)
        while not lexStream.isEnd():
            currentToken = lexStream.useToken()
            
            if (currentToken.name == "}") and (lexStream.getCurrent().value == ";"):
                    break     
            else:
                if ((currentToken.name == "NAME") and lexStream.getCurrent().value =="="):
                    lexStream.useExpectedToken("ASSIGN")
                    expected_list=['ARITHMETIC_OPERATOR','NAME','NUMBER','STRING','(',')']
                    param_list = self.readUntillToken(lexStream,";",expected_list)
                    if len(param_list)==0:
                        print("Unexpected token near {%s} at Line: %s, Column: %s"%(currentToken.value,currentToken.getsourcepos().lineno,currentToken.getsourcepos().colno))
                        exit()
                    mAssignNode = Node("ASSIGN",mBody)
                    mLeftNode=Node("left",mAssignNode)
                    mRightNode=Node("right",mAssignNode)
                    Node("VALUE",mLeftNode,value=currentToken.value,token=currentToken)
                    if(len(param_list)==1):
                        Node('VALUE',mRightNode,value=param_list[0].value,token=param_list[0])
                    elif(len(param_list)>1):
                        
                        self.parseExpression(param_list,mRightNode)
                                        
                elif ((currentToken.name == "NAME") and lexStream.getCurrent().value =="("):
                    expected_list=['ARITHMETIC_OPERATOR','NAME','NUMBER','STRING','(',')']
                    param_list = self.readBetweenBrackets(lexStream,"(",")",expected_list)
                    self.parseCallFunction(currentToken,param_list,mBody)
                elif((currentToken.name == 'IF')and lexStream.getCurrent().value =='('):
                    condition = self.readBetweenBrackets(lexStream,"(",")",None)
                    ifBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    elseBody = None
                    if(lexStream.getCurrent().name=="ELSE"):
                        lexStream.useExpectedToken("ELSE")
                        elseBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    self.parseIfStatement(condition,ifBody,elseBody,mBody)   
    
    # IF STATEMET METHODS

    def parseIfStatement(self,condition,ifBody,elseBody,mNode):
        mIfNode = Node("IF STATEMENT",mNode)
        mIfCondition = Node("Condition",mIfNode)
        mIfConditionBody = Node('Body',mIfNode)
        if(elseBody!=None):
            mIfConditionElse = Node('Else',mIfNode)
            self.parseIfBody(elseBody,mIfConditionElse)
        self.parseIfCondition(condition,mIfCondition)
        self.parseIfBody(ifBody,mIfConditionBody)
        pass
    def parseIfCondition(self,param_list,mNode):
        subStream=naivilLexerSubStream(param_list)
        operand_list=[]
        
        while not subStream.isEnd():
            currentToken = subStream.useToken()
            if(subStream.isEnd()):
                temp_list =[]
                temp_list.append(currentToken)
                operand_list.append(temp_list)
            else:
                if currentToken.name=="NAME" and subStream.getCurrent().name=='(':
                    temp_list = []
                    temp_list.append(currentToken)
                    while True:
                        currentToken = subStream.useToken()
                        temp_list.append(currentToken)
                        if currentToken.name==')':
                            operand_list.append(temp_list)
                            break
                else: # to do brackets
                    temp_list =[]
                    temp_list.append(currentToken)
                    operand_list.append(temp_list)
        self.evaluateIfCondition(operand_list,mNode)
        pass   
    def evaluateIfCondition(self,operandList,mNode):
        if len(operandList)==1:
            if(len(operandList[-1]) >1):
                mArgs = self.prepareFunctionArgs(operandList[-1])
                self.parseCallFunction(mArgs[0],mArgs[1],mNode)
        
        else:
            for idx, op in enumerate(operandList):
                if len(op)==1 and op[0].name=="COMPARISON_OPERATOR":
                    if(op[0].value in ["<=",">=","==","!=","<",">"]):
                        
                        right=[]
                        left =[]
                        operator = operandList[idx]
                        mOperationNode = Node(operator[0].name,mNode,value=operator[0].value)
                        mLeftNode=Node("left",mOperationNode)
                        mRightNode=Node("right",mOperationNode)
                        for i in range(0,idx):
                            left.append(operandList[i])
                        for i in range(idx+1,len(operandList)):
                            right.append(operandList[i]) 
                        if len(left)>1:
                            print(left)
                            print(right)
                            print('Syntax error at line: %s ' %(left[0][0].getsourcepos().lineno) )
                            exit()
                        if len(left[0])==1:
                            Node("VALUE",mLeftNode,value=left[0][0].value,token=left[0][0]) 
                        else:
                            mArgs = self.prepareFunctionArgs(left[0])
                            
                            self.parseCallFunction(mArgs[0],mArgs[1],mLeftNode)
                        
                            pass      
                        
                        if len(right)==1:
                            
                            if len(right[0])==1:
                                Node("VALUE",mRightNode,value=right[0][0].value,token=right[0][0])
                            else:
                                
                                mArgs = self.prepareFunctionArgs(right[0])
                                
                                self.parseCallFunction(mArgs[0],mArgs[1],mRightNode)
                                pass
                        else:
                            self.evaluateExpressionList(right,mRightNode)
                        break                              
    def parseIfBody(self,param_list,mBody):
        lexStream = naivilLexerSubStream(param_list)
        while not lexStream.isEnd():
            currentToken = lexStream.useToken()
            
            if (currentToken.name == "}") and (lexStream.getCurrent().value == ";"):
                    break     
            else:
                if ((currentToken.name == "NAME") and lexStream.getCurrent().value =="="):
                    lexStream.useExpectedToken("ASSIGN")
                    expected_list=['ARITHMETIC_OPERATOR','NAME','NUMBER','STRING','(',')']
                    param_list = self.readUntillToken(lexStream,";",expected_list)
                    if len(param_list)==0:
                        print("Unexpected token near {%s} at Line: %s, Column: %s"%(currentToken.value,currentToken.getsourcepos().lineno,currentToken.getsourcepos().colno))
                        exit()
                    mAssignNode = Node("ASSIGN",mBody)
                    mLeftNode=Node("left",mAssignNode)
                    mRightNode=Node("right",mAssignNode)
                    Node("VALUE",mLeftNode,value=currentToken.value,token=currentToken)
                    if(len(param_list)==1):
                        Node('VALUE',mRightNode,value=param_list[0].value,token=param_list[0])
                    elif(len(param_list)>1):
                        
                        self.parseExpression(param_list,mRightNode)
                                        
                elif ((currentToken.name == "NAME") and lexStream.getCurrent().value =="("):
                    expected_list=['ARITHMETIC_OPERATOR','NAME','NUMBER','STRING','(',')']
                    param_list = self.readBetweenBrackets(lexStream,"(",")",expected_list)
                    self.parseCallFunction(currentToken,param_list,mBody)
                elif((currentToken.name == 'IF')and lexStream.getCurrent().value =='('):
                    condition = self.readBetweenBrackets(lexStream,"(",")",None)
                    ifBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    elseBody = None
                    if(lexStream.getCurrent().name=="ELSE"):
                        lexStream.useExpectedToken("ELSE")
                        elseBody = self.readBetweenBrackets(lexStream,"{","}",None)
                    self.parseIfStatement(condition,ifBody,elseBody,mBody)                                 
    
    # PARSE EXPRESSION METHODS
    
    def parseExpression(self,param_list,mNode):
        subStream=naivilLexerSubStream(param_list)
        operand_list=[]
        
        while not subStream.isEnd():
            currentToken = subStream.useToken()
            if(subStream.isEnd()):
                temp_list =[]
                temp_list.append(currentToken)
                operand_list.append(temp_list)
            else:
                
                if currentToken.name=="NAME" and subStream.getCurrent().name=='(':
                    
                    temp_list = []
                    temp_list.append(currentToken)
                    while True:
                        currentToken = subStream.useToken()
                        temp_list.append(currentToken)
                        if currentToken.name==')':
                            
                            operand_list.append(temp_list)
                            break
                else: # to do brackets
                    temp_list =[]
                    temp_list.append(currentToken)
                    operand_list.append(temp_list)
                    

        self.evaluateExpressionList(operand_list,mNode)           
    def evaluateExpressionList(self,operandList,mNode):
        
        if len(operandList)==1:
            if(len(operandList[-1]) >1):
                mArgs = self.prepareFunctionArgs(operandList[-1])
                self.parseCallFunction(mArgs[0],mArgs[1],mNode)
                
        else:
            for idx, op in enumerate(operandList):
                if len(op)==1 and op[0].name=="ARITHMETIC_OPERATOR":
                    if(op[0].value in ["+","-","*","/"]):
                        
                        right=[]
                        left =[]
                        operator = operandList[idx]
                        mOperationNode = Node(operator[0].name,mNode,value=operator[0].value,token=operator)
                        mLeftNode=Node("left",mOperationNode)
                        mRightNode=Node("right",mOperationNode)
                        for i in range(0,idx):
                            left.append(operandList[i])
                        for i in range(idx+1,len(operandList)):
                            right.append(operandList[i]) 
                        
                        if len(left)>1:
                            print(left)
                            print(right)
                            print('Syntax error at line: %s ' %(left[0][0].getsourcepos().lineno) )
                            exit()
                        if len(left[0])==1:
                            Node("VALUE",mLeftNode,value=left[0][0].value,token=left[0][0]) 
                        else:
                            mArgs = self.prepareFunctionArgs(left[0])
                            self.parseCallFunction(mArgs[0],mArgs[1],mLeftNode)
                            pass      
                        if len(right)==1:
                            if len(right[0])==1:
                                Node("VALUE",mRightNode,value=right[0][0].value,token=right[0][0])
                            else:
                                
                                mArgs = self.prepareFunctionArgs(right[0])
                                self.parseCallFunction(mArgs[0],mArgs[1],mRightNode)
                                pass
                        else:
                            self.evaluateExpressionList(right,mRightNode)
                        break                              
                       
    # FUNCTION CALL METHODS
    
    def parseCallFunction(self,f_name,param_list,mNode):
        
        mParamMultipleIdx = []
        
        mFunctionCall=Node("FUNCTION CALL",mNode)
        Node("Function Name ",mFunctionCall,value=f_name.value,token=f_name)
        mArguments = Node("Arguments",mFunctionCall)
        
        if len(param_list)==1:
            Node("VALUE",mArguments,value=param_list[-1].value,token=param_list[-1])
            
        elif len(param_list)>1:
            
            for idx in range(len(param_list)):
                
                if  param_list[idx].name == "COMMA":     
                    mParamMultipleIdx.append(idx)
               
            if len(mParamMultipleIdx)==0:
                
                self.parseExpression(param_list,mArguments)  
                
            else:
                self.parseMultipleArgs(param_list,mArguments,mParamMultipleIdx)      
    def parseMultipleArgs(self,param_list,mNode,mParamMultipleIdx):
        
        mParams =[None]
        
        for i in range(len(mParamMultipleIdx)):
            if i == 0:
                mParams.append(param_list[0:mParamMultipleIdx[i]])
            if i == len(mParamMultipleIdx)-1:
                mParams.append(param_list[mParamMultipleIdx[i]+1:len(param_list)])    
            else:
                mParams.append(param_list[mParamMultipleIdx[i]+1:mParamMultipleIdx[i+1]])
        
        for p in mParams:
            if p!=None:
                if len(p)>1:
                    self.parseExpression(p,mNode)   
                else:
                     Node("VALUE",mNode,value=p[-1].value,token=p[-1])    
    def prepareFunctionArgs(self,list):
        f_name = None
        p_list = []
        for i in range(len(list)):
            if i == 0:
                f_name=list[i]
            elif list[i].name=='(':
                i+=1
                while True:
                    if not list[i].name==')':
                        p_list.append(list[i])  
                    else:
                        break 
                    i+=1
        ret_array=[]
        ret_array.append(f_name)
        ret_array.append(p_list)                    
        return ret_array
    
    # HELPER METHODS
    
    def readBetweenBrackets(self,lexStream,bracketType,bracketTypeInvert,expected_list):
        
        bracket_count=1;
        lexStream.useExpectedToken(bracketType)
        contents_list=[]
        flag = True
        while flag:
            currentToken = lexStream.useToken()
            
            if ((currentToken.value==bracketType)):
                bracket_count+=1
            elif ((currentToken.value==bracketTypeInvert)):
                bracket_count-=1
                
            if not ((currentToken.value==bracketTypeInvert) and (bracket_count==0)):
                if expected_list == None:
                    contents_list.append(currentToken)
                else:    
                    if currentToken.name in expected_list: 
                        contents_list.append(currentToken)
                    else:
                        print("Unexpected token {%s} at Line: %s, Column: %s"%(currentToken.value,currentToken.getsourcepos().lineno,currentToken.getsourcepos().colno))
                        exit()
                       
            else:
                return contents_list  
    def readUntillToken(self,lexStream,untillToken,expected_list):

        flag=True
        read_list=[]
        while flag:
            currentToken = lexStream.useToken()
            if currentToken.value!=untillToken:
                if currentToken.name in expected_list: 
                    read_list.append(currentToken)
                else:
                    print("Unexpected token {%s} at Line: %s, Column: %s"%(currentToken.value,currentToken.getsourcepos().lineno,currentToken.getsourcepos().colno))
                    exit()
            else:
                flag = False    
        
        return read_list
    
