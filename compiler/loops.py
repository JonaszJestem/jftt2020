import logging

from variables import Value, Number
from identifiers import Identifier, Pidentifier
from jump_fillers import JumpFiller, ForDownToLoopJumpFiller, ForLoopJumpFiller, LoopJumpFiller
from operations import AssignmentOperations, ConditionOperations




class WhileLoop:
    def __init__(self, condition, do_commands):
        self.condition = condition
        self.do_commands = do_commands

    def generate_code(self, program):
        loop_end = LoopJumpFiller(program.line_no)
        line_to_fill = self.condition.generate_code(program)

        # while is endless or while has condition we cannot predict
        if line_to_fill is not False:
            if type(line_to_fill) is list:
                condition_end = JumpFiller(line_to_fill)
                program.stack.append(condition_end)
            program.stack.append(loop_end)
            [program.stack.append(do_command) for do_command in self.do_commands]

    def get_variable_names(self):
        return self.condition.get_variable_names()


class DoWhileLoop(WhileLoop):

    def generate_code(self, program):
        while_loop = WhileLoop(self.condition, self.do_commands)
        program.stack.append(while_loop)
        [program.stack.append(do_command) for do_command in self.do_commands]


class ForLoop:
    def __init__(self, i, startValue, endValue, commands):
        self.i = i
        self.startValue = startValue
        self.endValue = endValue
        self.commands = commands

    def generate_code(self, program):

        if type(self.startValue) is not Value:
            self.startValue = Value(self.startValue)
        if type(self.endValue) is not Value:
            self.endValue = Value(self.endValue)

        Pidentifier(self.i).generate_code(program)
        iterator_assignment = AssignmentOperations(Identifier(self.i), self.startValue)
        iterator_variable = program.get_variable(self.i)
        iterator_assignment.generate_code(program)
        iterator_variable.is_iterator = True

        Pidentifier(self.i + '_end0').generate_code(program)
        end_iterator_variable = program.get_variable(self.i + '_end0')
        end_iterator_assignment = AssignmentOperations(Identifier(self.i + '_end0'), self.endValue)
        end_iterator_assignment.generate_code(program)
        end_iterator_variable.is_iterator = True

        # create loop end to know where we should return
        loop_end = ForLoopJumpFiller(program.line_no, iterator=self.i)

        # generate condition
        condition = ConditionOperations("LEQ", Identifier(self.i), Identifier(self.i + '_end0'))
        line_to_fill = condition.generate_code(program)

        # add command end to fill jumps in condition
        if line_to_fill is not False:
            if type(line_to_fill) is list:
                condition_end = JumpFiller(line_to_fill)
                program.stack.append(condition_end)

        # add commands
        program.stack.append(loop_end)
        [program.stack.append(command) for command in self.commands]

    def get_variable_names(self):
        result = []
        if type(self.i) is not Number:
            result.extend(self.i)
        if type(self.startValue) is not Number:
            result.extend(self.startValue.get_variable_names())
        if type(self.endValue) is not Number:
            result.extend(self.endValue.get_variable_names())
        return tuple(result)


class ForDownToLoop(ForLoop):

    def generate_code(self, program):
        # assignment of iterator
        Pidentifier(self.i).generate_code(program)
        iterator_variable = program.get_variable(self.i)
        iterator_assignment = AssignmentOperations(Identifier(self.i),
                                                   Value(self.startValue))
        iterator_assignment.generate_code(program)
        iterator_variable.is_iterator = True

        Pidentifier(self.i + '_end0').generate_code(program)
        end_iterator_variable = program.get_variable(self.i + '_end0')
        end_iterator_assignment = AssignmentOperations(Identifier(self.i + '_end0'),
                                                       Value(self.endValue))
        end_iterator_assignment.generate_code(program)
        end_iterator_variable.is_iterator = True

        # create loop end to know where we should return
        loop_end = ForDownToLoopJumpFiller(program.line_no, iterator=self.i)

        # generate condition
        condition = ConditionOperations("GEQ",
                                        Identifier(self.i),
                                        Identifier(self.i + '_end0'))
        line_to_fill = condition.generate_code(program)

        # add command end to fill jumps in condition
        if line_to_fill is not False:
            if type(line_to_fill) is list:
                condition_end = JumpFiller(line_to_fill)
                program.stack.append(condition_end)

        # add commands
        program.stack.append(loop_end)
        [program.stack.append(command) for command in self.commands]
