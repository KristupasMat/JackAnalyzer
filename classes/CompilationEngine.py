from classes.SymbolTable import SymbolTable
from classes.VMWriter import VMWriter
from classes.JackTokenizer import JackTokenizer

class CompilationEngine:
    '''Gets input from the JackAnalyzer, and writes its output using the VMWriter.'''

    operators = {
      '+': 'add', 
      '-': 'sub', 
      '*': 'Math.multiply', 
      '/': 'Math.divide', 
      '&': 'and', 
      '|': 'or', 
      '<': 'lt', 
      '>': 'gt', 
      '=': 'eq'
    }
    unary_operators = {'-': 'neg', '~': 'not'}

    def __init__(self, input_file, output_file) -> None:
      self.tokenizer = JackTokenizer(input_file)
      self.vm_writer = VMWriter(output_file)
      self.symbol_table = SymbolTable()
      self.advanceTokenizer()
      self.compileClass()

    def __consume_token(self, token: str) -> None:
      if self.tokenizer.current_token != token:
        print('Does not match')
      else:
        self.advanceTokenizer()

    def close_output_file(self) -> None:
      self.vm_writer.close()

    def advanceTokenizer(self) -> None:
      if self.tokenizer.hasMoreTokens():
        self.tokenizer.advance()

    def compileClass(self) -> None:
      '''Compile a complete class.'''
      self.__consume_token('class')
      self.class_name = self.tokenizer.current_token
      self.__consume_token(self.tokenizer.current_token)
      self.__consume_token('{')
      self.compileClassVarDec()
      self.compileSubroutineDec()
      self.__consume_token('}')

      self.close_output_file()

    def compileClassVarDec(self) -> None:
      '''Compiles a static variable declaration, or a field declaration.'''
      while True:
        if self.tokenizer.current_token in ['static', 'field']:

          identifier = {}
          identifier["kind"] = 'STATIC' if self.tokenizer.current_token == 'static' else 'FIELD'
          self.__consume_token(self.tokenizer.current_token) # static or field

          identifier["type"] = self.tokenizer.current_token
          self.__consume_token(self.tokenizer.current_token) # type

          identifier["name"] = self.tokenizer.current_token
          self.symbol_table.define(identifier["name"], identifier["type"], identifier["kind"]) # add to class level symbol table

          self.__consume_token(self.tokenizer.current_token) # varName
          
          while self.tokenizer.current_token == ',':
            self.__consume_token(self.tokenizer.current_token) # ,

            identifier["name"] = self.tokenizer.current_token
            self.symbol_table.define(identifier["name"], identifier["type"], identifier["kind"]) # add to class level symbol table
            self.__consume_token(self.tokenizer.current_token) # varName

          self.__consume_token(';')
          
        else:
          break

    def compileSubroutineDec(self) -> None:
      '''Compiles a complete method, function or constructor.'''
      while True:
        if self.tokenizer.current_token in ['constructor', 'function', 'method']:
          
          # Reset every time a new subroutine is started
          self.control_statement_labels = {
            'WHILE_EXP': -1,
            'WHILE_END': -1,
            'IF_TRUE': -1,
            'IF_FALSE': -1,
            'IF_END': -1,
          }
          self.symbol_table.startSubroutine()
          self.compiling_method = True if self.tokenizer.current_token == 'method' else False 
          self.compiling_constructor = True if self.tokenizer.current_token == 'constructor' else False 

          self.__consume_token(self.tokenizer.current_token) # constructor or function or method
          self.__consume_token(self.tokenizer.current_token) # type

          self.function_name = self.tokenizer.current_token
          self.__consume_token(self.tokenizer.current_token) # subroutineName
          self.__consume_token('(')
          if self.tokenizer.tokenType() in ['IDENTIFIER', 'SYMBOL', 'KEYWORD']: 
            self.compileParameterList()
          self.__consume_token(')')

          self.compileSubroutineBody()

        else:
          break

    def compileParameterList(self) -> None:
      '''Compiles a (possibly empty) parameter list. Does not handle "()". '''
      if self.compiling_method:
        self.symbol_table.define("this", self.class_name, 'ARG')

      if self.tokenizer.current_token != ')':
        identifier = {}
        identifier["type"] = self.tokenizer.current_token
        self.__consume_token(self.tokenizer.current_token) # type

        identifier["name"] = self.tokenizer.current_token
        self.symbol_table.define(identifier["name"], identifier["type"], 'ARG') # add argument to subroutine level symbol table
        self.__consume_token(self.tokenizer.current_token) # varName

        while self.tokenizer.current_token == ',':
          self.__consume_token(self.tokenizer.current_token) # ,
          identifier["type"] = self.tokenizer.current_token
          self.__consume_token(self.tokenizer.current_token) # type
          identifier["name"] = self.tokenizer.current_token
          self.symbol_table.define(identifier["name"], identifier["type"], 'ARG') # add argument to subroutine level symbol table
          self.__consume_token(self.tokenizer.current_token) # varName

    def compileSubroutineBody(self) -> None:
      '''Compiles a subroutine's body.'''
      self.__consume_token('{')
      self.compileVarDec()
      self.vm_writer.writeFunction(f'{self.class_name}.{self.function_name}', self.symbol_table.varCount('VAR')) # By now, we already added all the variables to the symbol table
      if self.compiling_method:
        self.vm_writer.writePush('argument', 0)
        self.vm_writer.writePop('pointer', 0) # Sets THIS to argument 0

      if self.compiling_constructor:
        self.vm_writer.writePush('constant', self.symbol_table.varCount('FIELD')) # the size of the object is determined by its field variables
        self.vm_writer.writeCall('Memory.alloc', 1) # OS function that allocates the actual memory and returns its base address
        self.vm_writer.writePop('pointer', 0) # anchors this to the base address
      self.compileStatements()
      self.__consume_token('}')

    def compileVarDec(self) -> None:
      '''Compiles a var declaration.'''
      while self.tokenizer.current_token == 'var':

        identifier = {}
        self.__consume_token('var')
        identifier["type"] = self.tokenizer.current_token
        self.__consume_token(self.tokenizer.current_token) # type
        identifier["name"] = self.tokenizer.current_token
        self.symbol_table.define(identifier["name"], identifier["type"], 'VAR') # add var (local) to subroutine level symbol table
        self.__consume_token(self.tokenizer.current_token) # varName

        while self.tokenizer.current_token == ',':
          self.__consume_token(self.tokenizer.current_token) # ,
          identifier["name"] = self.tokenizer.current_token
          self.symbol_table.define(identifier["name"], identifier["type"], 'VAR') # add var (local) to subroutine level symbol table
          self.__consume_token(self.tokenizer.current_token) # varName

        self.__consume_token(';')
      
    def compileStatements(self) -> None:
      '''Compiles a sequence of statements. Does not handle "{}". '''
      while self.tokenizer.current_token in ['let', 'if', 'while', 'do', 'return']:
        if self.tokenizer.current_token == 'let':
          self.compileLet()
        elif self.tokenizer.current_token == 'if':
          # increment used label counts, so it stays unique in case there are nested statements
          self.control_statement_labels["IF_TRUE"] += 1
          self.control_statement_labels["IF_FALSE"] += 1
          self.control_statement_labels["IF_END"] += 1
          self.compileIf()
        elif self.tokenizer.current_token == 'while':
          self.control_statement_labels["WHILE_EXP"] += 1
          self.control_statement_labels["WHILE_END"] += 1
          self.compileWhile()
        elif self.tokenizer.current_token == 'do':
          self.compileDo()
        elif self.tokenizer.current_token == 'return':
          self.compileReturn()

    def compileLet(self) -> None:
      # NOT YET IMPLEMENTED
      '''Compiles a let statement.'''
      self.__consume_token('let')
      var_name = self.tokenizer.current_token
      self.__consume_token(self.tokenizer.current_token)
      
      if self.tokenizer.current_token == '[':
        self.__consume_token('[')
        self.compileExpression()
        self.__consume_token(']')

      self.__consume_token('=')
      self.compileExpression()
      self.__consume_token(';')
      # pop to expression value to the selected variable
      # TEMP for field
      segment = 'this' if self.symbol_table.kindOf(var_name) == 'field' else self.symbol_table.kindOf(var_name)
      self.vm_writer.writePop(segment, self.symbol_table.indexOf(var_name))

    def compileIf(self) -> None:
      '''Compiles an if statement, possibly with a trailing else clause.'''
      self.__consume_token('if')
      self.__consume_token('(')
      self.compileExpression()
      
      # Compose label of its name and index, increment afterwards
      label_if_true = f'IF_TRUE{self.control_statement_labels["IF_TRUE"]}'
      label_if_false = f'IF_FALSE{self.control_statement_labels["IF_FALSE"]}'
      label_if_end = f'IF_END{self.control_statement_labels["IF_END"]}'
      self.vm_writer.writeIf(label_if_true)
      self.vm_writer.writeGoto(label_if_false)
      self.vm_writer.writeLabel(label_if_true)
      self.__consume_token(')')
      self.__consume_token('{')
      self.compileStatements()
      self.__consume_token('}')
      
      if self.tokenizer.current_token == 'else':
        self.vm_writer.writeGoto(label_if_end)
        self.vm_writer.writeLabel(label_if_false)
        self.__consume_token('else')
        self.__consume_token('{')
        self.compileStatements()
        self.__consume_token('}')
        self.vm_writer.writeLabel(label_if_end)
      else:
        self.vm_writer.writeLabel(label_if_false)

    def compileWhile(self) -> None:
      # NOT YET IMPLEMENTED
      '''Compiles a while statement.'''
      label_while_exp = f'WHILE_EXP{self.control_statement_labels["WHILE_EXP"]}'
      label_while_end = f'WHILE_END{self.control_statement_labels["WHILE_END"]}'
      self.vm_writer.writeLabel(label_while_exp)
      self.__consume_token('while')
      self.__consume_token('(')
      self.compileExpression()
      self.vm_writer.writeArithmetic('not')
      # go to end of the lopp if false
      self.vm_writer.writeIf(label_while_end)

      self.__consume_token(')')
      self.__consume_token('{')
      self.compileStatements()
      # go back to evaluate the loop expression and repeat if condition is satisfied
      self.vm_writer.writeGoto(label_while_exp)
      self.__consume_token('}')
      # end of the loop
      self.vm_writer.writeLabel(label_while_end)

    def compileDo(self) -> None:
      '''Compiles a do statement.'''
      self.__consume_token('do')
      #  Need to first push all expressions to the stack, compute them and only then call the function
      self.compileSubroutineCall()
      self.__consume_token(';')

      # Callers of void methods are responsible for removing the returned value from the stack
      self.vm_writer.writePop('temp', 0)

    def compileReturn(self) -> None:
      '''Compiles a return statement.'''

      self.__consume_token('return')
      if self.tokenizer.current_token != ';': 
        self.compileExpression()
        self.vm_writer.writeReturn('return')
      else:
        # compile void return
        self.vm_writer.writePush('constant', 0)
        self.vm_writer.writeReturn('return')

      self.__consume_token(';')

    def compileSubroutineCall(self) -> None:
      '''Compiles a subroutine call'''
      vm_subroutine_call_name = None
      # How many arguments does the function take. In case of a class method, it has at least 1 (the class itself)
      self.vm_subroutine_args = 0
      if self.tokenizer.next_token == "(":
        # Push base address of THIS before calling a method
        self.vm_writer.writePush('pointer', 0)
        vm_subroutine_call_name = f'{self.class_name}.{self.tokenizer.current_token}'
        self.__consume_token(self.tokenizer.current_token) # subroutineName
        self.vm_subroutine_args += 1
        self.__consume_token("(")
        self.compileExpressionList()
        self.__consume_token(")")
      else:
        # class method call.
        # vm_class_name can be either className or user defined variable name
        vm_class_name = self.tokenizer.current_token
        kind_of_token = self.symbol_table.kindOf(vm_class_name) # is it field or local?
        type_of_token = self.symbol_table.typeOf(vm_class_name)
        index_of_token = self.symbol_table.indexOf(vm_class_name)

        self.__consume_token(self.tokenizer.current_token) # className|varName
        self.__consume_token(".")
        
        vm_subroutine_name = self.tokenizer.current_token
        self.__consume_token(self.tokenizer.current_token) # subroutineName
        self.__consume_token("(")
        self.compileExpressionList()
        self.__consume_token(")")

        # Handle method calls.
        if kind_of_token is not None:
          # Change name to the type of variable which will be the actual class name
          vm_class_name = type_of_token
          self.vm_subroutine_args += 1
          segment = 'this' if kind_of_token == 'field' else kind_of_token
          self.vm_writer.writePush(segment, index_of_token)
          
        vm_subroutine_call_name = f'{vm_class_name}.{vm_subroutine_name}'
          
      self.vm_writer.writeCall(vm_subroutine_call_name, self.vm_subroutine_args)

    def compileExpression(self) -> None:
      '''Compiles an expression.'''
      self.compileTerm()

      expression_commands = []

      while self.tokenizer.current_token in self.operators:
        expression_commands.append(self.operators.get(self.tokenizer.current_token))
        self.__consume_token(self.tokenizer.current_token)
        self.compileTerm()

      if expression_commands:
        for command in expression_commands:
          if command.startswith('Math'):
            self.vm_writer.writeCall(command, 2)
          else:
            self.vm_writer.writeArithmetic(command)

    def compileTerm(self) -> None:
      '''Compiles a term.'''
      if self.tokenizer.tokenType() in ['INT_CONST', 'STRING_CONST', 'KEYWORD']:
        
        if self.tokenizer.tokenType() == 'INT_CONST':
          self.vm_writer.writePush('constant', self.tokenizer.current_token) # push constant i 
        elif self.tokenizer.current_token in ['false', 'null']:
          self.vm_writer.writePush('constant', 0)
        elif self.tokenizer.current_token == 'true':
          self.vm_writer.writePush('constant', 0)
          self.vm_writer.writeArithmetic('not')
        elif self.tokenizer.current_token == 'this':
          self.vm_writer.writePush('pointer', 0)

        self.__consume_token(self.tokenizer.current_token)
      elif self.tokenizer.current_token in self.unary_operators:
        command = self.unary_operators.get(self.tokenizer.current_token)
        self.__consume_token(self.tokenizer.current_token)
        self.compileTerm()
        self.vm_writer.writeArithmetic(command)

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
        # varName
        kind_of_token = self.symbol_table.kindOf(self.tokenizer.current_token) # is it field or local?
        segment = 'this' if kind_of_token == 'field' else kind_of_token
        self.vm_writer.writePush(segment, self.symbol_table.indexOf(self.tokenizer.current_token))
        self.__consume_token(self.tokenizer.current_token)

    def compileExpressionList(self) -> None:
      '''Compiles an expression list.'''
      if self.tokenizer.current_token != ")":
        self.compileExpression()
        self.vm_subroutine_args += 1
        while self.tokenizer.current_token == ',':
          self.__consume_token(",")
          self.compileExpression()
          self.vm_subroutine_args += 1
