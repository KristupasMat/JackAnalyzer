class CompilationEngine:
    '''Gets input from the JackAnalyzer, and emits its output to an output file.'''

    operators = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    unary_operators = ['-', '~']

    def __init__(self, tokenizer, output_file: str) -> None:
      self.tokenizer = tokenizer
      self.tab_size = 0
      self.output_file = open(output_file, 'w')
      self.advanceTokenizer()
      self.compileClass()

    def __consume_token(self, token: str) -> None:
      if self.tokenizer.current_token != token:
        print('Does not match')
      else:
        if self.tokenizer.tokenType() == 'KEYWORD':
          self.__write_statement_to_output(self.tokenizer.keyword())
        elif self.tokenizer.tokenType() == 'SYMBOL':
          self.__write_statement_to_output(self.tokenizer.symbol())
        elif self.tokenizer.tokenType() == 'IDENTIFIER':
          self.__write_statement_to_output(self.tokenizer.identifier())
        elif self.tokenizer.tokenType() == 'INT_CONST':
          self.__write_statement_to_output(self.tokenizer.intVal())
        elif self.tokenizer.tokenType() == 'STRING_CONST':
          self.__write_statement_to_output(self.tokenizer.stringVal())

        self.advanceTokenizer()

    def __write_statement_to_output(self, statement):
      self.output_file.write('\t'.expandtabs(self.tab_size) + statement + '\n')

    def close_output_file(self) -> None:
      self.output_file.close()

    def advanceTokenizer(self) -> None:
      if self.tokenizer.hasMoreTokens():
        self.tokenizer.advance()

    def compileClass(self) -> None:
      '''Compile a complete class.'''
      self.__write_statement_to_output('<class>')
      self.tab_size += 2
      self.__consume_token('class')
      self.__consume_token(self.tokenizer.current_token)
      self.__consume_token('{')
      self.compileClassVarDec()
      self.compileSubroutineDec()
      self.__consume_token('}')
      self.tab_size -= 2
      self.__write_statement_to_output('</class>')
      self.close_output_file()

    def compileClassVarDec(self) -> None:
      '''Compiles a static variable declaration, or a field declaration.'''
      while True:
        if self.tokenizer.current_token in ['static', 'field']:
          self.__write_statement_to_output('<classVarDec>')
          self.tab_size += 2

          self.__consume_token(self.tokenizer.current_token) # static or field
          self.__consume_token(self.tokenizer.current_token) # type
          self.__consume_token(self.tokenizer.current_token) # varName
          while self.tokenizer.current_token == ',':
            self.__consume_token(self.tokenizer.current_token) # ,
            self.__consume_token(self.tokenizer.current_token) # varName

          self.__consume_token(';')
          
          self.tab_size -= 2
          self.__write_statement_to_output('</classVarDec>')
        else:
          break

    def compileSubroutineDec(self) -> None:
      '''Compiles a complete method, function or constructor.'''
      while True:
        if self.tokenizer.current_token in ['constructor', 'function', 'method']:
          self.__write_statement_to_output('<subroutineDec>')          
          self.tab_size += 2

          self.__consume_token(self.tokenizer.current_token) # constructor or function or method
          self.__consume_token(self.tokenizer.current_token) # type
          self.__consume_token(self.tokenizer.current_token) # subroutineName
          self.__consume_token('(')
          if self.tokenizer.tokenType() in ['IDENTIFIER', 'SYMBOL', 'KEYWORD']: 
            self.compileParameterList()
          self.__consume_token(')')
          self.compileSubroutineBody()

          self.tab_size -= 2
          self.__write_statement_to_output('</subroutineDec>')
        else:
          break

    def compileParameterList(self) -> None:
      '''Compiles a (possibly empty) parameter list. Does not handle "()". '''
      self.__write_statement_to_output('<parameterList>')
      self.tab_size += 2

      if self.tokenizer.current_token != ')':
        self.__consume_token(self.tokenizer.current_token) # type
        self.__consume_token(self.tokenizer.current_token) # varName

        while self.tokenizer.current_token == ',':
          self.__consume_token(self.tokenizer.current_token) # ,
          self.__consume_token(self.tokenizer.current_token) # type
          self.__consume_token(self.tokenizer.current_token) # varName
      
      self.tab_size -= 2
      self.__write_statement_to_output('</parameterList>')

    def compileSubroutineBody(self) -> None:
      '''Compiles a subroutine's body.'''
      self.__write_statement_to_output('<subroutineBody>')
      self.tab_size += 2

      self.__consume_token('{')
      self.compileVarDec()
      self.compileStatements()
      self.__consume_token('}')

      self.tab_size -= 2
      self.__write_statement_to_output('</subroutineBody>')

    def compileVarDec(self) -> None:
      '''Compiles a var declaration.'''
      while self.tokenizer.current_token == 'var':
        self.__write_statement_to_output('<varDec>')
        self.tab_size += 2

        self.__consume_token('var')
        self.__consume_token(self.tokenizer.current_token) # type
        self.__consume_token(self.tokenizer.current_token) # varName

        while self.tokenizer.current_token == ',':
          self.__consume_token(self.tokenizer.current_token) # ,
          self.__consume_token(self.tokenizer.current_token) # varName

        self.__consume_token(';')

        self.tab_size -= 2
        self.__write_statement_to_output('</varDec>')
      

    def compileStatements(self) -> None:
      '''Compiles a sequence of statements. Does not handle "{}". '''
      self.__write_statement_to_output('<statements>')
      self.tab_size += 2

      while self.tokenizer.current_token in ['let', 'if', 'while', 'do', 'return']:
        if self.tokenizer.current_token == 'let':
          self.compileLet()
        elif self.tokenizer.current_token == 'if':
          self.compileIf()
        elif self.tokenizer.current_token == 'while':
          self.compileWhile()
        elif self.tokenizer.current_token == 'do':
          self.compileDo()
        elif self.tokenizer.current_token == 'return':
          self.compileReturn()
        
      self.tab_size -= 2
      self.__write_statement_to_output('</statements>')

    def compileLet(self) -> None:
      '''Compiles a let statement.'''
      self.__write_statement_to_output('<letStatement>')
      self.tab_size += 2

      self.__consume_token('let')
      self.__consume_token(self.tokenizer.current_token)
      
      if self.tokenizer.current_token == '[':
        self.__consume_token('[')
        self.compileExpression()
        self.__consume_token(']')

      self.__consume_token('=')
      self.compileExpression()
      self.__consume_token(';')

      self.tab_size -= 2
      self.__write_statement_to_output('</letStatement>')

    def compileIf(self) -> None:
      '''Compiles an if statement, possibly with a trailing else clause.'''
      self.__write_statement_to_output('<ifStatement>')
      self.tab_size += 2

      self.__consume_token('if')
      self.__consume_token('(')
      self.compileExpression()
      self.__consume_token(')')
      self.__consume_token('{')
      self.compileStatements()
      self.__consume_token('}')

      if self.tokenizer.current_token == 'else':
        self.__consume_token('else')
        self.__consume_token('{')
        self.compileStatements()
        self.__consume_token('}')

      self.tab_size -= 2
      self.__write_statement_to_output('</ifStatement>')

    def compileWhile(self) -> None:
      '''Compiles a while statement.'''
      self.__write_statement_to_output('<whileStatement>')
      self.tab_size += 2

      self.__consume_token('while')
      self.__consume_token('(')
      self.compileExpression()
      self.__consume_token(')')
      self.__consume_token('{')
      self.compileStatements()
      self.__consume_token('}')

      self.tab_size -= 2
      self.__write_statement_to_output('</whileStatement>')

    def compileDo(self) -> None:
      '''Compiles a do statement.'''
      self.__write_statement_to_output('<doStatement>')
      self.tab_size += 2

      self.__consume_token('do')
      self.compileSubroutineCall()
      self.__consume_token(';')

      self.tab_size -= 2
      self.__write_statement_to_output('</doStatement>')

    def compileReturn(self) -> None:
      '''Compiles a return statement.'''
      self.__write_statement_to_output('<returnStatement>')
      self.tab_size += 2

      self.__consume_token('return')
      if self.tokenizer.current_token != ';': 
        self.compileExpression()
      self.__consume_token(';')

      self.tab_size -= 2
      self.__write_statement_to_output('</returnStatement>')

    def compileSubroutineCall(self) -> None:
      '''Compiles a subroutine call'''
      if self.tokenizer.next_token == "(":
        # subroutineName
        self.__consume_token(self.tokenizer.current_token)
        self.__consume_token("(")
        self.compileExpressionList()
        self.__consume_token(")")
      else:
        # class method call
        self.__consume_token(self.tokenizer.current_token)
        self.__consume_token(".")
        self.__consume_token(self.tokenizer.current_token)
        self.__consume_token("(")
        self.compileExpressionList()
        self.__consume_token(")")

    def compileExpression(self) -> None:
      '''Compiles an expression.'''
      self.__write_statement_to_output('<expression>')
      self.tab_size += 2

      self.compileTerm()

      while self.tokenizer.current_token in self.operators:
        self.__consume_token(self.tokenizer.current_token)
        self.compileTerm()

      self.tab_size -= 2
      self.__write_statement_to_output('</expression>')

    def compileTerm(self) -> None:
      '''Compiles a term.'''
      self.__write_statement_to_output('<term>')
      self.tab_size += 2

      if self.tokenizer.tokenType() in ['INT_CONST', 'STRING_CONST', 'KEYWORD']:
        self.__consume_token(self.tokenizer.current_token)
      elif self.tokenizer.current_token in self.unary_operators:
        self.__consume_token(self.tokenizer.current_token)
        self.compileTerm()
      elif self.tokenizer.current_token == "(":
        self.__consume_token("(")
        self.compileExpression()
        self.__consume_token(")")
      elif self.tokenizer.next_token == "[":
        # array
        self.__consume_token(self.tokenizer.current_token)
        self.__consume_token("[")
        self.compileExpression()
        self.__consume_token("]")
      elif self.tokenizer.next_token in ["(", "."]:
        self.compileSubroutineCall()
      else:
        self.__consume_token(self.tokenizer.current_token)

      self.tab_size -= 2
      self.__write_statement_to_output('</term>')

    def compileExpressionList(self) -> None:
      '''Compiles an expression list.'''
      self.__write_statement_to_output('<expressionList>')
      self.tab_size += 2

      if self.tokenizer.current_token != ")":
        self.compileExpression()
        while self.tokenizer.current_token == ',':
          self.__consume_token(",")
          self.compileExpression()

      self.tab_size -= 2
      self.__write_statement_to_output('</expressionList>')
