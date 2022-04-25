


from anytree import Node


class naivilRustPrototypes():
        def __init__(self):
            print("PROTOTYPES INIT")
        
        def functionPrototype(self,functionName,funtionParamList,functionReturnType,functionBody):
            prototype='fn {name} ({variableList}) {returnType}{{\n'\
                    '{body}'\
                    '\n}}\n'.format(name=functionName,variableList=funtionParamList,returnType=functionReturnType,body=functionBody)
            return prototype
        def functionCallPrototype(self,functionName,functionArgs):
            prototype='{name}({args})'.format(name=functionName,args=functionArgs)
            return prototype
        def ifStatementPrototype(self,condition,body,hasElse,elsebody):
            prototype='if {condition} {{\n {body} \n}}\n'.format(condition=condition,body=body)
            if hasElse:
                prototypeElse='else {{\n {elseBody} \n}}\n'.format(elseBody=elsebody)
                prototype+=prototypeElse
            return prototype    
        def variableDeclarationPrototype(self,variableName):
            prototype='let mut {name};'.format(name=variableName)
            return prototype
        def whileStatementPrototype(self,condition,body):
            prototype='while {condition} {{\n {body} \n}}\n'.format(condition=condition,body=body)
            return prototype
        def forStatementPrototype(self,index,range,body):
            prototype = 'for {index} in {r1}..{r2} {{\n {body} \n}}\n'.format(index=index,r1=range[0],r2=range[1],body=body)
            return prototype

        def printFunctionPrototype(self,functionArgs):
            prototype='println!("{{}}",{args})'.format(args=functionArgs)
            return prototype

class naivilRustTranspiler():
        def __init__(self,env):
            self.env = env
            self.mPrototypes = naivilRustPrototypes()
            self.mCode = ""
            self.variablePairs = dict([("int32","i32"),("int64","i64"),("int128","i128"),("float","f64"),("str","&str"),("bigint","BigUint")]) 
            
            for n in env.children:
                for  f in n.children:
                   self.mCode += self.generateFunction(f)
            
            with open("./mainTemplate/src/main.rs","wb") as f:
                f.flush()
                
                f.write(self.mCode.encode())
                f.close()
        
        def getReturnType(self,mNode):
            if mNode =="void":
                return ""
            else:
                return self.variablePairs[mNode]

        def generateFunction(self,mNode):
            f_name = mNode.name
            if len(self.getReturnType(mNode.returnType.value))>0:
                f_return = " -> "+self.getReturnType(mNode.returnType.value)
            else:
                f_return = ""    
            f_params = ""
            f_body = ""
            for n in mNode.children:
                if n.name =="Params":
                    f_params = self.getFunctionParams(n)
                if n.name =="Body":
                    f_body = self.getFunctionBody(n)
            return(self.mPrototypes.functionPrototype(f_name,f_params,f_return,f_body))
        
        def getFunctionParams(self,mNode):
            param_list = []
            for n in mNode.children:
                param_list.append(" "+n.name+" : "+ self.getReturnType(n.type.value))
            ret = ""
            for i in range(len(param_list)):
                ret+=param_list[i]
                if i+1<len(param_list):
                    ret+=" ,"
            return ret
    
        def getFunctionBody(self,mNode):
            mBody = ""
            for n in mNode.children:
                if n.name == "FUNCTION CALL":
                    mBody += self.getFunctionCall(n)+";\n"
                if n.name == "ASSIGN":
                    mBody += self.getAssign(n)+";\n"
                if n.name == "VARIABLE":
                    mBody += self.mPrototypes.variableDeclarationPrototype(n.value+":"+self.variablePairs[n.type.value])+"\n"    
                if n.name == "IF STATEMENT":
                    mBody += self.getIfStatement(n)+"\n"
                if n.name == "RUST_NATIVE":
                    mBody +=n.tk.value[1:-1]+"\n"
                if n.name == "WHILE STATEMENT":
                    mBody += self.getWhileStatement(n)+"\n"
                if n.name == "FOR STATEMENT":
                    mBody += self.getForStatement(n)+"\n"
            return mBody
        
        def getFunctionCall(self,mNode):
            f_name = ""
            f_args = ""
            for n in mNode.children:
                if n.name == "Function Name ":
                    f_name=n.value
                if n.name == "Arguments":
                    f_args=self.getFunctionArgs(n)
            if f_name =="print":
                return self.mPrototypes.printFunctionPrototype(f_args)
            return self.mPrototypes.functionCallPrototype(f_name,f_args)    
        
        def getFunctionArgs(self,mNode):
            for arg in mNode.children:
                if arg.name == "VALUE":
                    return arg.value
                if arg.name == "FUNCTION CALL":
                    return self.getFunctionCall(arg)
                if arg.name == "ARITHMETIC_OPERATOR":
                    return self.getArithmeticOperator(arg)
            return""
        
        def getArithmeticOperator(self,mNode):
            mOperator = mNode.value
            mLeft = ""
            mRight = ""
            
            for n in mNode.children:
                if n.name == "right":
                    mRight=self.getArithmeticOperatorLR(n)
                if n.name == "left":
                    mLeft=self.getArithmeticOperatorLR(n)
            return mLeft+mOperator+mRight
        def getArithmeticOperatorLR(self,mNode):
            for n in mNode.children:
                if n.name == "VALUE":
                    return n.value
                if n.name == "ARITHMETIC_OPERATOR":
                    return self.getArithmeticOperator(n)
                if n.name ==  "FUNCTION CALL":
                    return self.getFunctionCall(n)
            return""            
        def getAssign(self,mNode):
            mLeft=""
            mRight=""
            for n in mNode.children:
                if n.name == "right":
                    mRight=self.getArithmeticOperatorLR(n)
                if n.name == "left":
                    mLeft=self.getArithmeticOperatorLR(n)
            return mLeft+"="+mRight
        def getIfStatement(self,mNode):
            mCondition=""
            mBody =""
            mHasElse=False
            mElseBody=""
            for n in mNode.children:
                if n.name=="Condition":
                    mCondition=self.getifCondition(n)
                if n.name=="Body":
                    mBody=self.getFunctionBody(n)   
                if n.name=="Else":
                    mHasElse=True
                    mElseBody=self.getFunctionBody(n)                                          
            
            return self.mPrototypes.ifStatementPrototype(mCondition,mBody,mHasElse,mElseBody)
        
        def getifCondition(self,mNode):
        
            mOperator ="" 
            mLeft = ""
            mRight = ""
            
            for n in mNode.children:
                mOperator=n.value
                for s in n.children:
                    if s.name == "right":
                        mRight=self.getArithmeticOperatorLR(s)
                    if s.name == "left":
                        mLeft=self.getArithmeticOperatorLR(s)
            return mLeft+mOperator+mRight
        def getWhileStatement(self,mNode):
            mCondition=""
            mBody =""
            for n in mNode.children:
                if n.name=="Condition":
                    mCondition=self.getifCondition(n)
                if n.name=="Body":
                    mBody=self.getFunctionBody(n)   
                
            return self.mPrototypes.whileStatementPrototype(mCondition,mBody)
        def getForStatement(self,mNode):
            mCondition=[None,[None,None]]
            
            mBody=""
            for n in mNode.children:
                if n.name=="Condition":
                    mCondition=self.getForStatementCondition(n)
                    pass
                if n.name=="Body":
                    mBody=self.getFunctionBody(n)   
            
            return self.mPrototypes.forStatementPrototype(mCondition[0],mCondition[1],mBody)   
        
        def getForStatementCondition(self,mNode):
            mReturn=[None,[None,None]]
            for n in mNode.children:
                mReturn=[n.value,[n.range_low,n.range_high]]
            
            return mReturn
        