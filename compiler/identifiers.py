import logging

from variables import Variable




class ArrayIdentifier:
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index

    def generate_code(self, program, cell):

        array_cell = program.get_array_cell(self.identifier, self.index)
        array_cell.cell = cell
        return array_cell

    def get_variable(self, program):
        return program.get_array_cell(self.identifier, self.index)

    def get_variable_names(self):
        if type(self.index) == Identifier:
            index_name = self.index.get_variable_names()
            return (index_name[0], )
        return ()

class Pidentifier:
    def __init__(self, value):
        self.value = value

    def generate_code(self, program):

        program.variables[self.value] = Variable(self.value, None,  program.used_memory)
        program.used_memory += 1
        variable = program.get_variable(self.value)

        return variable

class Identifier:
    def __init__(self, value):
        self.value = value

    def generate_code(self, program, cell):

        variable = program.get_variable(self.value)
        variable.cell = cell
        return variable

    def get_variable(self, program):
        return program.get_variable(self.value)
    
    def get_variable_names(self):
        return (self.value, )
