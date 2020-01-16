import logging

from .variables import Number, copy_value




class Write:
    def __init__(self, value):
        self.value = value

    def generate_code(self, program):

        variable = self.value.generate_code(program)
        if variable.memory_localisation != -1:
            variable.load_from_memory(program, 0)
        program.code.append(f'PUT')
        program.line_no += 1

    def get_variable_names(self):
        if type(self.value) is not Number:
            return self.value.get_variable_names()
        return ()


class Read:
    def __init__(self, identifier):
        self.identifier = identifier

    def generate_code(self, program):

        variable = self.identifier.get_variable(program)
        program.code.append(f'GET')
        copy_value(program, from_cell=0, to_cell=2)
        variable.store_in_memory(program, 2)
        program.line_no += 1

    def get_variable_names(self):
        return self.identifier.get_variable_names()
