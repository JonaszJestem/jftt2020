import logging




class Variable:
    def __init__(self, name, cell, memory_localisation, is_iterator=False):
        self.name = name
        self.cell = cell
        self.memory_localisation = memory_localisation
        self.is_iterator = is_iterator

    def store_in_memory(self, program, cell):
        Number(self.memory_localisation).generate_code(program, 5)
        copy_value(program, cell, 0)
        program.code.append(f'STOREI {5} #store into memory {self.name}')
        program.line_no += 1

    def load_from_memory(self, program, cell):
        Number(self.memory_localisation).generate_code(program, cell)
        program.code.append(f'LOADI {cell} #load from memory {self.name}')
        copy_value(program, 0, cell)
        program.line_no += 1


class ArrayVariable:
    def __init__(self, array_name, start_index, end_index, memory_localisation):
        self.arrName = array_name
        self.memory_localisation = memory_localisation
        self.start_index = start_index
        self.end_index = end_index
        self.cells = dict()


class Number:
    def __init__(self, value, memory_localisation=-1):
        self.value = int(value)
        self.memory_localisation = memory_localisation

    def generate_code(self, program, cell=0):
        code = []
        value_to_generate = self.value

        # while self.value != 0:

        if value_to_generate > 0:
            while self.value != 0:
                if self.value % 2 == 0:
                    code.append(f'ADD {0}')
                    self.value //= 2
                else:
                    code.append(f'INC')
                    self.value -= 1
        else:
            while self.value != 0:
                if self.value % 2 == 0:
                    code.append(f'ADD {0}')
                    self.value //= 2
                else:
                    code.append(f'DEC')
                    self.value += 1
        code = list(reversed(code))
        code.insert(0, f'SUB 0 #generate number {value_to_generate}')
        [program.code.append(command) for command in code]
        program.line_no += len(code)
        copy_value(program, from_cell=0, to_cell=cell)

        self.value = value_to_generate
        return Variable("accumulator_tmp", cell, memory_localisation=-1)


class Value:
    def __init__(self, value):
        self.value = value
        self.memory_localisation = -1

    def generate_code(self, program, cell=0):
        variable = self.value.generate_code(program, cell)
        return variable

    def get_variable_names(self):
        if type(self.value) is not Number:
            return self.value.get_variable_names()
        return ()


class ArrayCell:
    def __init__(self, name, memory_localisation, parent, cell=None):
        self.name = name
        self.memory_localisation = memory_localisation  # index
        self.index = memory_localisation  # index
        self.cell = cell
        self.parent = parent

    def store_in_memory(self, program, cell):
        """
        Stores `array cell` into memory.
        """
        if type(self.memory_localisation) is str:
            variable = program.get_variable(self.memory_localisation)
            variable.load_from_memory(program, 2)

            Number(self.parent.memory_localisation + abs(self.parent.start_index)).generate_code(program,3)

            copy_value(program, from_cell=2,to_cell=0)
            program.code.append('ADD 3')
            program.code.append(f'STORE {3}')
            program.code.append(f'LOAD {cell}')

            program.code.append(f'STOREI {3} # end store into memory {self.parent.arrName}({self.index})')

            self.cell = cell
            program.line_no += 4
        else:
            Number(abs(self.parent.start_index) + self.memory_localisation + self.parent.memory_localisation).generate_code(program, 1)
            copy_value(program, cell, 0)
            program.code.append(f'STOREI 1 # store into memory {self.parent.arrName}({self.index})')
            program.line_no += 1

    def load_from_memory(self, program, cell):
        """
        Loads `array cell` to given cell.
        """
        if type(self.memory_localisation) is str:
            variable = program.get_variable(self.memory_localisation)
            variable.load_from_memory(program, 2)

            Number(self.parent.memory_localisation + abs(self.parent.start_index)).generate_code(program, 3)

            copy_value(program, from_cell=2,to_cell=0)
            program.code.append('ADD 3')
            program.code.append(f'STORE {3}')

            program.code.append(f'LOADI {3} # load from memory {self.parent.arrName}({self.index})')
            copy_value(program,from_cell=0,to_cell=cell)
            program.line_no += 3

        else:
            Number(abs(self.parent.start_index) + self.memory_localisation + self.parent.memory_localisation).generate_code(program, 1)
            program.code.append(f'LOADI {1} # load from memory {self.parent.arrName}({self.index})')
            copy_value(program,from_cell=0, to_cell=cell)
            program.line_no += 1


def copy_value(program, from_cell, to_cell=0):
    if from_cell != 0:
        program.code.append(f'SUB 0')
        program.code.append(f'ADD {from_cell}')
        program.line_no += 2
    if to_cell != 0:
        program.code.append(f'STORE {to_cell} # copied from {from_cell} to {to_cell}')
        program.line_no += 1
