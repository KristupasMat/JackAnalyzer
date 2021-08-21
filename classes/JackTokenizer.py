# Deals with lexical elements

class JackTokenizer:

  # Jack language tokens

  keywords = [
    'class', 'constructor', 'function', 'method', 'field', 'static', 
    'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 
    'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'
  ]

  symbols = [
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', 
    '-', '*', '/', '&', '|', '<', '>', '=', '~'
  ]

  # integerConstant: 0 - 32767

  # stringConstant: a sequence of Unicode characters

  # identifier: a sequence of letters, digits, and underscore not starting with a digit

  token_types = ['KEYWORD', 'SYMBOL', 'IDENTIFIER', 'INT_CONST', 'STRING_CONST']

  def __init__(self, input_file) -> None:
    '''Opens .jack input file and prepares to tokenize it. '''
    
    self.current_token = None

  def hasMoreTokens(self) -> bool:
    '''Does the input file has more tokens?'''
    pass

  def advance(self) -> None:
    '''Gets the next token from the input, and makes it a current token.'''
    pass
  
  def tokenType(self) -> str:
    '''Returns a token type of the current token.'''
    pass
  
  def keyword(self) -> str:
    '''Returns the keyword which is the current token, as a constant.'''
    pass

  def symbol(self) -> str:
    '''Returns the character which is the current token.'''
    pass

  def identifier(self) -> str:
    '''Returns the identifier which is the current token.'''
    pass

  def intVal(self) -> int:
    '''Returns the integer value which is the current token.'''
    pass

  def stringVal(self) -> str:
    '''Returns the string value which is the current token.'''
    pass

