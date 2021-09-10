from re import compile, findall
class JackTokenizer:
  '''Handles the compiler's input.'''

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

  token_compiler = compile("\"\s*.+\s*\"|[\w]+|[\.,;\+\-\*/&\|<>=~\(\)\{\}\[\]]")

  # integerConstant: 0 - 32767
  # stringConstant: a sequence of Unicode characters
  # identifier: a sequence of letters, digits, and underscore not starting with a digit
  # keyword, symbol, identifier, integerConstant, stringConstant

  token_types = {
    'KEYWORD': 'KEYWORD', 
    'SYMBOL': 'SYMBOL', 
    'IDENTIFIER': 'IDENTIFIER', 
    'INT_CONST': 'INT_CONST', 
    'STRING_CONST': 'STRING_CONST'
  }

  def __init__(self, input_file) -> None:
    '''Opens .jack input file and prepares to tokenize it. '''
    
    self.input_file = open(input_file, 'r')
    # Whether we have processed a single line of input file, initially it is true since no line was read yet.
    self.current_line_tokens = None
    self.amount_of_tokens = 0
    self.current_token_index = 0
    self.current_token = None
    self.next_token = None
    self.is_final_token = True

  def __close_input_file(self):
    self.input_file.close()

  def __read_line(self): 
    return self.input_file.readline().strip(" ")

  def hasMoreTokens(self) -> bool:
    '''Does the input file has more tokens?'''
    if self.is_final_token is True:
      # End of the file will return empty space
      current_line = self.__read_line()
      # Handle single and multi line comments and new lines
      while True:
        if current_line.isspace():
          current_line = self.__read_line()
        elif current_line.startswith("/**"):
          while True:
            if current_line.endswith("*/\n"):
              current_line = self.__read_line()
              break
            else:  
              current_line = self.__read_line()
        elif current_line.startswith("//"):
          current_line = self.__read_line()
        elif current_line.find('//') != -1:
          current_line = current_line.split('//')[0]
        else:
          break
      # returning a list of all the different tokens in the currently read line
      self.current_line_tokens = findall(self.token_compiler, current_line)
      self.amount_of_tokens = len(self.current_line_tokens)
    
    if self.amount_of_tokens == 0:
      self.__close_input_file()
      return False

    # If the index is out of list range we have exhausted the list of tokens
    if self.current_token_index + 1 == self.amount_of_tokens:
      self.is_final_token = True
    else: 
      self.is_final_token = False
      self.next_token = self.current_line_tokens[self.current_token_index + 1]

    return True

  def advance(self) -> None:
    '''Gets the next token from the input, and makes it a current token.'''
    self.current_token = self.current_line_tokens[self.current_token_index]
    
    if self.is_final_token:
      self.current_token_index = 0
    else: 
      self.current_token_index += 1
  
  def tokenType(self) -> str:
    '''Returns a token type of the current token.'''
    if self.current_token in self.keywords:
      return self.token_types['KEYWORD']
    elif self.current_token in self.symbols:
      return self.token_types['SYMBOL']
    elif self.current_token.isidentifier(): 
      return self.token_types['IDENTIFIER']
    elif self.current_token.isdigit():
      return self.token_types['INT_CONST']
    elif self.current_token.startswith("\""):
      return self.token_types['STRING_CONST']
    else:
      # Questionable choice...
      raise ValueError('Did not find the correct token type for the token', self.current_token)
  
  def keyword(self) -> str:
    '''Returns the keyword which is the current token, as a constant.'''
    return "<keyword> " + self.current_token + " </keyword>"

  def symbol(self) -> str:
    '''Returns the character which is the current token.'''
    if self.current_token == '<':
      return "<symbol> " + '&lt;' + " </symbol>"
    elif self.current_token == '>':
      return "<symbol> " + '&gt;' + " </symbol>"
    elif self.current_token == '"':
      return "<symbol> " + '&quot;' + " </symbol>"
    elif self.current_token == '&':
      return "<symbol> " + '&amp;' + " </symbol>"
    else:
      return "<symbol> " + self.current_token + " </symbol>"

  def identifier(self) -> str:
    '''Returns the identifier which is the current token.'''
    return self.current_token

  def intVal(self) -> str:
    '''Returns the integer value which is the current token.'''
    return self.current_token

  def stringVal(self) -> str:
    '''Returns the string value which is the current token.'''
    return self.current_token.strip("\"")

