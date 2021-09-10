from typing import Union

class SymbolTable:
  ''' Creates class-level and subroutine-level symbol tables '''
  
  class_kinds = ['STATIC', 'FIELD']
  subroutine_kinds = ['ARG', 'VAR']

  def __init__(self) -> None:
    self.class_sym_table = {}
    self.subroutine_sym_table = {}
    self.static_count = 0
    self.field_count = 0
    self.argument_count = 0
    self.variable_count = 0

  def startSubroutine(self) -> None:
    '''Starts a new subroutine scope (i.e., resets the subroutine's symbol table)'''
    self.subroutine_sym_table.clear()
    self.argument_count = 0
    self.variable_count = 0

  def define(self, name: str, type: str, kind: str) -> None:
    '''Defines a new identifier of the given name, type and kind and assigns it a running index'''
    
    if kind in self.class_kinds:
      self.class_sym_table[name] = {
        "name": name,
        "type": type,
        "kind": 'static' if kind == 'STATIC' else 'field',
        "index": self.static_count if kind == 'STATIC' else self.field_count
      }

      if kind == 'STATIC':
        self.static_count += 1 
      else:
        self.field_count += 1

    else:
      self.subroutine_sym_table[name] = {
        "name": name,
        "type": type,
        "kind": 'argument' if kind == 'ARG' else 'local',
        "index": self.argument_count if kind == 'ARG' else self.variable_count
      }

      if kind == 'ARG':
        self.argument_count += 1 
      else:
        self.variable_count += 1

  def varCount(self, kind: str) -> int:
    '''Returns the number of variables of the given kind already defined in the current scope'''
    if kind == 'STATIC':
      return self.static_count
    elif kind == 'FIELD':
      return self.field_count
    elif kind == 'ARG':
      return self.argument_count
    elif kind == 'VAR':
      return self.variable_count
    else:
      return 0

  def kindOf(self, name: str) -> Union[str, None]:
    '''Returns the kind of the named identifier in the current scope. Returns None if the identifier is unknown'''
    get_match = self.subroutine_sym_table.get(name) or self.class_sym_table.get(name)

    if get_match:
      return get_match['kind'] 

    return None

  def typeOf(self, name: str) -> str:
    '''Returns the type of the named identifier'''
    get_match = self.subroutine_sym_table.get(name) or self.class_sym_table.get(name)

    if get_match:
      return get_match['type'] 

    return None

  def indexOf(self, name: str) -> int:
    '''Returns the index assigned to the named identifier'''
    get_match = self.subroutine_sym_table.get(name) or self.class_sym_table.get(name)

    if get_match:
      return get_match['index'] 

    return None