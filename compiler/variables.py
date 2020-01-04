import logging

logging.basicConfig(level=logging.ERROR)


class Variable:
    def __init__(self, name, memory_localisation, is_iterator=False):
        self.name = name
        self.memory_localisation = memory_localisation
        self.is_iterator = is_iterator

    def store_in_memory(self, program, cell):
        Number(self.memory_localisation).generate_code(program)
        program.code.append(f'STORE {cell} #store into memory {self.name}')
        program.line_no += 1

    def load_from_memory(self, program, cell):
        Number(self.memory_localisation).generate_code(program)
        program.code.append(f'LOAD {cell} #load from memory {self.name}')
        program.line_no += 1


class ArrayVariable:
    def __init__(self, arrName, start_index, end_index, memory_localisation):
        self.arrName = arrName
        self.memory_localisation = memory_localisation
        self.start_index = start_index
        self.end_index = end_index
        self.cells = dict()


class Number:
    def __init__(self, value):
        self.value = int(value)

    def generate_code(self, program, cell=0):
        code = []

        while self.value != 0:
            if self.value % 2 == 0:
                code.append(f'ADD {cell}')
            else:
                code.append(f'ADD {cell}')
                code.append(f'INC {cell}')

            self.value //= 2
            code = code[:0:-1]
        code.insert(0, f'SUB {cell}')
        [program.code.append(command) for command in code]
        program.line_no += len(code)
        logging.info(f"Generating number {self.value}")
        return Variable('accumulator_tmp', cell)


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
    def __init__(self, name, memory_localisation, parent, register=None):
        self.name = name
        self.memory_localisation = memory_localisation  # index
        self.register = register
        self.parent = parent

    def store_in_memory(self, program, register):
        """
        Stores `array cell` into memory.
        """
        if type(self.memory_localisation) is str:
            variable = program.get_variable(self.memory_localisation)
            variable.load_from_memory(program, 'A')

            Number(self.parent.memory_localisation).generate_code(program)

            program.code.append('ADD A H')

            program.code.append(f'STORE {register} # end store into memory ')

            self.register = register
            program.line_no += 2
        else:
            Number(self.memory_localisation + self.parent.memory_localisation).generate_code(program, 'A')
            program.code.append(f'STORE {register} # store into memory {self.parent.arrName}({self.name})')
            program.line_no += 1

    def load_from_memory(self, program, register):
        """
        Loads `array cell` to given register.
        """
        if type(self.memory_localisation) is str:
            variable = program.get_variable(self.memory_localisation)
            variable.load_from_memory(program, 'A')

            Number(self.parent.memory_localisation).generate_code(program)

            program.code.append('ADD A H')
            program.code.append(f'LOAD {register} # load from memory {self.parent.arrName}({self.memory_localisation})')
            program.line_no += 2

        else:
            Number(self.memory_localisation + self.parent.memory_localisation).generate_code(program, 'A')
            program.code.append(f'LOAD {register} # load from memory {self.parent.arrName}({self.memory_localisation})')
            program.line_no += 1
