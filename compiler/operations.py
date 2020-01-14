import logging

from .variables import Number
from .snippets import add, bin_pow, decrement, divide, equals, greater_than, increment, less_or_equal, \
    multiply, sub

logging.basicConfig(level=logging.ERROR)


class AssignmentOperations:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def generate_code(self, program):
        logging.info("AssignmentOperations generating code")
        variable = self.identifier.get_variable(program)

        if isinstance(self.expression, ArithemticOperations):
            result_variable = self.expression.generate_code(program)
            variable.cell = result_variable.cell
            variable.store_in_memory(program, result_variable.cell)
        elif isinstance(self.expression.value, Number):
            result_variable = self.expression.generate_code(program, 4)
            variable.store_in_memory(program, result_variable.cell)
        else:
            result_variable = self.expression.generate_code(program, 4)
            result_variable.load_from_memory(program, 4)
            variable.store_in_memory(program, result_variable.cell)

    def get_variable_names(self):
        """
        Gets names of variables used in command
        """
        result = []
        result.extend(self.identifier.get_variable_names())
        result.extend(self.expression.get_variable_names())
        return tuple(result)


# DONE
class ConditionOperations:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.relations = {
            'GE': lambda x, y, p: greater_than(x, y, p),
            'LEQ': lambda x, y, p: less_or_equal(x, y, p),
            'LE': lambda x, y, p: greater_than(x, y, p, swap=True),
            'GEQ': lambda x, y, p: less_or_equal(x, y, p, swap=True),
            'EQ': lambda x, y, p: equals(x, y, p),
            'NEQ': lambda x, y, p: equals(x, y, p, negate=True)
        }

        self.lambdas = {
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y,
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y,
            '=': lambda x, y: x == y,
            '!=': lambda x, y: x != y
        }

    def generate_code(self, program):
        """
        Generates line to fill for condition
        """
        logging.info("ConditionOperations generating code")
        if type(self.left) is type(self.right) and type(self.left) is Number:
            return self.lambdas[self.op](self.left.value, self.right.value)

        left_value = self.left.generate_code(program, 3)
        right_value = self.right.generate_code(program, 4)

        if left_value.memory_localisation != -1:
            left_value.load_from_memory(program, 3)
        if right_value.memory_localisation != -1:
            right_value.load_from_memory(program, 4)

        line_to_fill = self.relations[self.op](left_value, right_value, program)

        return line_to_fill

    def get_variable_names(self):
        """
        Gets names of variables used in command
        """
        result = []
        if type(self.left) is not Number:
            result.extend(self.left.get_variable_names())
        if type(self.right) is not Number:
            result.extend(self.right.get_variable_names())
        return tuple(result)


# DONE
class ArithemticOperations(ConditionOperations):

    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.op = op
        self.snippets = {
            '+': lambda x, y, p: add(x, y, p),
            '-': lambda x, y, p: sub(x, y, p),
            '*': lambda x, y, p: multiply(x, y, p),
            '/': lambda x, y, p: divide(x, y, p),
            '%': lambda x, y, p: divide(x, y, p, modulo=True),
            '++': lambda x, y, p: increment(x, y, p),
            '--': lambda x, y, p: decrement(x, y, p),
            'bin_pow': lambda x, y, p: bin_pow(x, y, p)
        }

        self.lambdas = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: max(0, x - y),
            '*': lambda x, y: x * y,
            '/': lambda x, y: x // y,
            '%': lambda x, y: x % y,
        }

    def generate_code(self, program):
        logging.info("Arithmetic snippets generating code")
        operation = self.op

        if self.op == 'MINUS':
            operation = '-'
        elif self.op == 'PLUS':
            operation = '+'
        elif self.op == 'MOD':
            operation = '%'
        elif self.op == 'DIV':
            operation = '/'
        elif self.op == 'TIMES':
            operation = '*'

        variable_left = self.left.generate_code(program, 5)
        variable_right = self.right.generate_code(program, 6)

        if variable_left.memory_localisation != -1:
            variable_left.load_from_memory(program, 5)
        if variable_right.memory_localisation != -1:
            variable_right.load_from_memory(program, 6)

        result_variable = self.snippets[operation](variable_left, variable_right, program)

        return result_variable
