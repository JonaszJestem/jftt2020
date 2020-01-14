import re

from sly import Parser

from .analysis_help import VariableTrace
from .conditionals import IfThenConditional, IfThenElseConditional
from .exceptions import SyntaxError, ArrayWrongDeclaration, ArrrayOutOfBound, DoubledDeclarationVariable, \
    IteratorManipulation, UndeclaredVariable, VariableNotInitialized
from .identifiers import Identifier, ArrayIdentifier, Variable
from .io_operations import Read, Write
from .lexer import JFTTLexer
from .loops import DoWhileLoop, ForDownToLoop, ForLoop, WhileLoop
from .operations import AssignmentOperations, ConditionOperations, Number, ArithemticOperations
from .program import JFTTProgram
from .variables import ArrayVariable, Value


class JFTTParser(Parser):
    debugfile = 'parser.out'

    tokens = JFTTLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', MULTIPLY, DIVIDE, MODULO),
    )

    def __init__(self, analysis=True):
        self.variables = {}
        self.arrays = {}
        self.used_memory = 10
        self.analysis = analysis
        self.variables_tracker = {}
        self.ignored_variables = []
        self.iterators = []

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        return JFTTProgram(p.declarations, p.commands, self.variables, self.arrays, self.used_memory)

    @_('declarations PIDENTIFIER')
    def declarations(self, p):
        variable_name = p.PIDENTIFIER
        if self.analysis or variable_name not in self.ignored_variables:
            self.variables[variable_name] = Variable(variable_name, None, self.used_memory)
            self.used_memory += 1
            if self.variables_tracker.get(variable_name) is None:
                variable_trace = VariableTrace(variable_name)
                self.variables_tracker[variable_name] = variable_trace
            elif self.analysis:
                raise DoubledDeclarationVariable(variable_name, p.lineno)
        return None

    @_('declarations COMMA PIDENTIFIER')
    def declarations(self, p):
        variable_name = p.PIDENTIFIER
        if self.analysis or variable_name not in self.ignored_variables:
            self.variables[variable_name] = Variable(variable_name, None, self.used_memory)
            self.used_memory += 1
            if self.variables_tracker.get(variable_name) is None:
                variable_trace = VariableTrace(variable_name)
                self.variables_tracker[variable_name] = variable_trace
            elif self.analysis:
                raise DoubledDeclarationVariable(variable_name, p.lineno)
        return None

    @_('declarations PIDENTIFIER LPARENTHESIS NUMBER COLON NUMBER RPARENTHESIS')
    def declarations(self, p):
        if self.analysis or p.PIDENTIFIER not in self.ignored_variables:
            start_array = int(p.NUMBER0)
            end_array = int(p.NUMBER1)
            self.arrays[p.PIDENTIFIER] = ArrayVariable(p.PIDENTIFIER, start_array, end_array, self.used_memory)
            self.used_memory += abs(end_array) + abs(start_array) + 1

            if start_array > end_array:
                raise ArrayWrongDeclaration(p.PIDENTIFIER, p.lineno)

            array_name = p.PIDENTIFIER + p.LPARENTHESIS + str(p.NUMBER0) + p.COLON + str(p.NUMBER1) + p.RPARENTHESIS
            if self.variables_tracker.get(p.PIDENTIFIER) is None:
                variable_use = VariableTrace(array_name, is_array=1, start_index=p.NUMBER0, end_index=p.NUMBER1)
                self.variables_tracker[p.PIDENTIFIER] = variable_use
            elif self.analysis:
                raise DoubledDeclarationVariable(p.PIDENTIFIER, p.lineno)

        return None

    @_('declarations COMMA PIDENTIFIER LPARENTHESIS NUMBER COLON NUMBER RPARENTHESIS')
    def declarations(self, p):
        if self.analysis or p.PIDENTIFIER not in self.ignored_variables:
            start_array = int(p.NUMBER0)
            end_array = int(p.NUMBER1)
            self.arrays[p.PIDENTIFIER] = ArrayVariable(p.PIDENTIFIER, start_array, end_array, self.used_memory)
            self.used_memory += abs(end_array) + abs(start_array) + 1

            if start_array > end_array:
                raise ArrayWrongDeclaration(p.PIDENTIFIER, p.lineno)

            array_name = p.PIDENTIFIER + p.LPARENTHESIS + str(p.NUMBER0) + p.COLON + str(p.NUMBER1) + p.RPARENTHESIS
            if self.variables_tracker.get(p.PIDENTIFIER) is None:
                variable_use = VariableTrace(array_name, is_array=1, start_index=p.NUMBER0, end_index=p.NUMBER1)
                self.variables_tracker[p.PIDENTIFIER] = variable_use
            elif self.analysis:
                raise DoubledDeclarationVariable(p.PIDENTIFIER, p.lineno)

        return None

    @_('')
    def declarations(self, p):
        return None

    # grammar connected to commands in program

    @_('commands command')
    def commands(self, p):
        cmds = p.commands
        cmds.insert(0, p.command)
        return cmds

    @_('command')
    def commands(self, p):
        return [p.command]

    # assignment grammar
    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, p):
        if hasattr(p.identifier, 'value') and p.identifier.value in self.iterators:
            raise IteratorManipulation(p.identifier.value, p.lineno)
        if hasattr(p.expression, 'value') and type(p.expression) is Value:
            self.add_variable_use(p.expression.value, p.lineno)
        self.add_variable_assignment(Value(p.identifier))
        if not self.check_ignoring(p.identifier):
            return AssignmentOperations(p.identifier, p.expression)

    # if then else grammar
    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return IfThenElseConditional(p.condition, p.commands0, p.commands1)

    # if then grammar
    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return IfThenConditional(p.condition, p.commands)

    # while loop grammar
    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return WhileLoop(p.condition, p.commands)

    # do while loop grammar
    @_('DO commands WHILE condition ENDDO')
    def command(self, p):
        return DoWhileLoop(p.condition, p.commands)

    # for loop grammar
    @_('FOR PIDENTIFIER FROM value TO value DO commands ENDFOR')
    def command(self, p):
        if self.analysis and p.PIDENTIFIER not in self.iterators:
            self.iterators.append(p.PIDENTIFIER)
        self.add_variable_use(p.value0, p.lineno)
        self.add_variable_use(p.value1, p.lineno)
        return ForLoop(p.PIDENTIFIER, p.value0, p.value1, p.commands)

    # for down to loop grammar
    @_('FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        if self.analysis and p.PIDENTIFIER not in self.iterators:
            self.iterators.append(p.PIDENTIFIER)
        self.add_variable_use(p.value0, p.lineno)
        self.add_variable_use(p.value1, p.lineno)
        return ForDownToLoop(p.PIDENTIFIER, p.value0, p.value1, p.commands)

    # io grammar
    @_('WRITE value SEMICOLON')
    def command(self, p):
        self.add_variable_use(p.value, p.lineno)
        return Write(p.value)

    @_('READ identifier SEMICOLON')
    def command(self, p):
        self.add_variable_assignment(Value(p.identifier))
        self.add_variable_use(Value(p.identifier), p.lineno)
        return Read(p.identifier)

    @_('value')
    def expression(self, p):
        return Value(p.value)

    # arithmetic operations
    @_('value PLUS value')
    @_('value MINUS value')
    @_('value MULTIPLY value')
    @_('value DIVIDE value')
    @_('value MODULO value')
    def expression(self, p):
        self.add_variable_use(p.value0, p.lineno)
        self.add_variable_use(p.value1, p.lineno)
        if (p[1] == '+' or p[1] == '*') and type(p.value0) is Number:
            p.value0, p.value1 = p.value1, p.value0
        return ArithemticOperations(p[1], p.value0, p.value1)

    # relation operations
    @_('value GREATER_THAN value')
    @_('value LESS_THAN value')
    @_('value GREATER_OR_EQUAL value')
    @_('value LESS_OR_EQUAL value')
    @_('value EQUAL value')
    @_('value NOT_EQUAL value')
    def condition(self, p):
        self.add_variable_use(p.value0, p.lineno)
        self.add_variable_use(p.value1, p.lineno)
        return ConditionOperations(p[1], p.value0, p.value1)

    @_('identifier')
    def value(self, p):
        return Value(p.identifier)

    @_('NUMBER')
    def value(self, p):
        return Number(p.NUMBER)

    @_('PIDENTIFIER')
    def identifier(self, p):
        if not self.analysis:
            if p.PIDENTIFIER not in self.iterators and p.PIDENTIFIER not in list(self.variables_tracker.keys()):
                raise UndeclaredVariable(p.PIDENTIFIER, p.lineno)
        return Identifier(p.PIDENTIFIER)

    @_('PIDENTIFIER LPARENTHESIS PIDENTIFIER RPARENTHESIS')
    def identifier(self, p):
        if not self.analysis and p.PIDENTIFIER1 not in self.iterators and p.PIDENTIFIER1 not in list(
                self.variables_tracker.keys()):
            raise UndeclaredVariable(p.PIDENTIFIER1, p.lineno)
        variable = self.variables_tracker.get(p.PIDENTIFIER1)
        if variable is not None and variable.assignments == 0:
            raise VariableNotInitialized(variable.name, p.lineno)
        return ArrayIdentifier(p.PIDENTIFIER0, p.PIDENTIFIER1)

    @_('PIDENTIFIER LPARENTHESIS NUMBER RPARENTHESIS')
    def identifier(self, p):
        if not self.analysis and p.PIDENTIFIER not in self.iterators and p.PIDENTIFIER not in list(
                self.variables_tracker.keys()):
            raise UndeclaredVariable(p.PIDENTIFIER, p.lineno)
        variable = self.variables_tracker.get(p.PIDENTIFIER)
        start_index, end_index = re.findall(r'-?[\d]+', variable.name)
        if variable is not None and (p.NUMBER < int(start_index) or p.NUMBER > int(end_index)):
            raise ArrrayOutOfBound(p.lineno)
        return ArrayIdentifier(p.PIDENTIFIER, p.NUMBER)

    def add_variable_use(self, p, line_no):
        variable_name = None
        if type(p.value) is Identifier:
            variable_name = p.value.value
        elif type(p.value) is ArrayIdentifier:
            index = p.value.index
            variable_name = p.value.identifier
            variable_index = self.variables_tracker.get(index)
            if variable_index is not None:
                if variable_index.assignments == 0:
                    raise VariableNotInitialized(variable_index.name, line_no)
                variable_index.uses += 1

        variable = self.variables_tracker.get(variable_name)
        if variable is not None:
            if variable.assignments == 0:
                raise VariableNotInitialized(variable.name, line_no)
            variable.uses += 1

    def add_variable_assignment(self, p):
        variable_name = None
        if hasattr(p.value, 'value'):
            variable_name = p.value.value
        elif hasattr(p.value, 'identifier'):
            variable_name = p.value.identifier

        variable = self.variables_tracker.get(variable_name)
        if variable is not None:
            variable.assignments += 1

    def check_ignoring(self, p):
        if hasattr(p, 'value'):
            for variable_name in self.ignored_variables:
                if variable_name == p.value:
                    return True

        if hasattr(p, 'identifier'):
            for variable_name in self.ignored_variables:
                if variable_name == p.identifier:
                    return True

        return False

    def error(self, p):
        if p:
            raise SyntaxError(p.lineno)
        self.errok()
        raise SyntaxError(p.lineno)
