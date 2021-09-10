class VMWriter:
  '''Emits VM code to the output .vm file'''
  
  def __init__(self, output_file: str) -> None:
    '''Creates a new .vm file and prepars it for writing'''
    self.output_file = open(output_file, 'w')

  def __write_statement_to_output(self, statement):
    self.output_file.write(statement + '\n')

  # segment: ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
  def writePush(self, segment: str, index: int) -> None:
    '''Writes a VM push command'''
    self.__write_statement_to_output(f'push {segment} {index}')

  def writePop(self, segment: str, index: int) -> None:
    '''Writes a VM pop command'''
    self.__write_statement_to_output(f'pop {segment} {index}')
  
  # command: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT 
  def writeArithmetic(self, command: str) -> None:
    '''Writes a VM arithmetic-logical command'''
    self.__write_statement_to_output(command)

  def writeLabel(self, label: str) -> None:
    '''Writes a VM label command'''
    self.__write_statement_to_output(f'label {label}')

  def writeGoto(self, label: str) -> None:
    '''Writes a VM goto command'''
    self.__write_statement_to_output(f'goto {label}')

  def writeIf(self, label: str) -> None:
    '''Writes a VM if-goto command'''
    self.__write_statement_to_output(f'if-goto {label}')

  def writeCall(self, name: str, nArgs: int) -> None:
    '''Writes a VM call command'''
    self.__write_statement_to_output(f'call {name} {nArgs}')

  def writeFunction(self, name: str, nLocals: int) -> None:
    '''Writes a VM function command'''
    self.__write_statement_to_output(f'function {name} {nLocals}')

  def writeReturn(self, label: str) -> None:
    '''Writes a VM return command'''
    self.__write_statement_to_output(label)

  def close(self) -> None:
    '''Closes the output file'''
    self.output_file.close()