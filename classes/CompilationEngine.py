class CompilationEngine:
  '''Gets input from the JackAnalyzer, and emits its output to an output file.'''

  def __init__(self, input_file, output_file) -> None:
    pass

  def compileClass(self) -> None:
    '''Compile a complete class.'''
    pass

  def compileClassVarDec(self) -> None:
    '''Compiles a static variable declaration, or a field declaration.'''
    pass

  def compileSubroutineDec(self) -> None:
    '''Compiles a complete method, function or constructor.'''
  
  def compileParameterList(self) -> None:
    '''Compiles a (possibly empty) parameter list. Does not handle "()". '''
    pass

  def compileSubroutineBody(self) -> None:
    '''Compiles a subroutine's body.'''
    pass

  def compileVarDec(self) -> None:
    '''Compiles a var declaration.'''
    pass

  def compileStatements(self) -> None:
    '''Compiles a sequence of statements. Does not handle "{}". '''
    pass

  def compileLet(self) -> None:
    '''Compiles a let statement.'''
    pass

  def compileIf(self) -> None:
    '''Compiles an if statement, possibly with a trailing else clause.'''
    pass

  def compileWhile(self) -> None:
    '''Compiles a while statement.'''
    pass

  def compileDo(self) -> None:
    '''Compiles a do statement.'''
    pass

  def compileReturn(self) -> None:
    '''Compiles a return statement.'''
    pass

  def compileExpression(self) -> None:
    '''Compiles an expression.'''
    pass

  def compileTerm(self) -> None:
    pass

  def compileExpressionList(self) -> None:
    pass