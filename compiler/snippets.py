import logging

from .variables import Variable, copy_value


def less_or_equal(variable_x, variable_y, program, swap=False):
    x, y = variable_x.cell, variable_y.cell

    logging.info('Less or equal generating code')
    label_false = "<replace_here>"
    line_to_fill = program.line_no + 4
    if swap:
        x, y = y, x

    # NOTE x and y should become busy but here we
    # don't ask for registers so they are safe

    out_code = [
        f'LOAD {x} #condition begining ',
        f'SUB {y}',
        f'JNEG {program.line_no + 5}',
        f'JZERO {program.line_no + 5}',
        f'JUMP {label_false} #condtion end',
    ]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)

    return [line_to_fill]


def greater_than(variable_x, variable_y, program, swap=False):
    x_cell, y_cell = variable_x.cell, variable_y.cell

    logging.info('Greater than generating code')
    label_false = "<replace_here>"
    line_to_fill = program.line_no + 3
    if swap:
        x_cell, y_cell = y_cell, x_cell

    out_code = [
        f'LOAD {y_cell} #condition begining ',
        f'SUB {x_cell}',
        f'JNEG {program.line_no + 4}',
        f'JUMP {label_false} #condtion end',
    ]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)

    return [line_to_fill]


def equals(variable_x, variable_y, program, negate=False):
    logging.info('Equals generating code')

    x, y = variable_x.cell, variable_y.cell

    label_false = "<replace_here>"
    label_true = program.line_no + 8

    if negate:
        label_false, label_true = program.line_no + 7, label_false
        lines_to_fill = [program.line_no + 6]
    else:
        lines_to_fill = [program.line_no + 3, program.line_no + 7]

    out_code = [
        f'LOAD {y} # equals',
        f'SUB {x}',
        f'JZERO {program.line_no + 4}',
        f'JUMP {label_false}',
        f'LOAD {x}',
        f'SUB {y}',
        f'JZERO {label_true} # end for not equals',
        f'JUMP {label_false} # end equals',
    ]

    # delete last jump from notequal (so hard optimazition)
    if negate:
        out_code = out_code[:-1]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    # return number of line where jump label should be replaced
    return lines_to_fill


def add(variable_x, variable_y, program):
    x = variable_x.cell
    y = variable_y.cell

    program.code[-1] += "# started adding"
    copy_value(program, from_cell=x, to_cell=0)
    out_code = [
        f'ADD {y}',
    ]

    [program.code.append(command) for command in out_code]
    copy_value(program, from_cell=0, to_cell=9)
    program.line_no += len(out_code)
    return Variable('helper', 9, -1)


def sub(variable_x, variable_y, program):
    x = variable_x.cell
    y = variable_y.cell

    program.code[-1] += "# started substracting"
    copy_value(program, from_cell=x, to_cell=0)
    out_code = [
        f'SUB {y}',
    ]

    [program.code.append(command) for command in out_code]
    copy_value(program, from_cell=0, to_cell=9)
    program.line_no += len(out_code)

    return Variable('helper', 9, -1)


def multiply(variable_x, variable_y, program):
    x = variable_x.cell
    y = variable_y.cell
    result =11
    counter = 12

    shifts = ['SUB 0', f'STORE {result}', f'STORE {counter}', 'DEC', 'STORE 2', 'INC', 'INC', 'STORE 3']
    [program.code.append(command) for command in shifts]
    program.line_no += len(shifts)


    if x == y:
        x = 5
        copy_value_code(program, from_cell=6, to_cell=5)

    # def multiply(x, y):
    #     result = 0
    #     counter = 0
    #     while x:
    #         if x % 2 == 1:
    #             result += y << counter
    #         counter += 1
    #         x //= 2
    #
    #     return result

    out_code = [
        f'LOAD {x} #multiplication start',
        f'JZERO {program.line_no + 17}',  # jump to end
        f'SHIFT 2',
        f'SHIFT 3',
        f'SUB {x}',
        f'JZERO {program.line_no + 10}',  # to counter increase
        f'LOAD {y}',
        f'SHIFT {counter}',
        f'ADD {result}',
        f'STORE {result}',
        f'LOAD {counter}',  # counter increase
        f'INC',
        f'STORE {counter}',
        f'LOAD {x}',
        f'SHIFT 2',
        f'STORE {x}',
        f'JUMP {program.line_no}',  # 15
    ]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)

    return Variable('helper', result, -1)


def divide(variable_x, variable_y, program, modulo=False):
    x = variable_x.cell
    y = variable_y.cell
    # results
    iloraz = 3
    reszta = 4

    sign_helper = 7

    if x == y:
        x = 5
        copy_value_code(program, from_cell=6, to_cell=5)

    clear = ['SUB 0', 'STORE 3', 'STORE 4', 'STORE 7', 'STORE 8']
    [program.code.append(command) for command in clear]
    program.line_no += 5

    out_code = [
        f'LOAD {y}',
        f'JZERO {program.line_no + 60} # dzielenie przez 0',
        f'LOAD {x}',
        f'JPOS {program.line_no + 7}',
        f'LOAD {sign_helper}',
        f'INC',
        f'STORE {sign_helper}',
        f'LOAD {y}',
        f'JPOS {program.line_no + 12}',
        f'LOAD {sign_helper}',
        f'INC',
        f'STORE {sign_helper}',
        f'LOAD {sign_helper}',
        f'DEC',  # 13
        f'JZERO {program.line_no + 35} #jump to handling mixed',

        f'LOAD {x}',
        f'JPOS {program.line_no + 26}',  # do poczatekdzielenia
        f'LOAD {iloraz}',
        f'INC',
        f'STORE {iloraz}',
        f'LOAD {x}',  # poczatek dzielenia 26
        f'SUB {y}',
        f'STORE {x}',
        f'STORE {reszta}',
        f'JPOS {program.line_no + 60} # jump to end',
        f'JUMP {program.line_no + 17} #koniec dzeielenia',  # do poczatek dzielenia

        f'LOAD {x}',  # poczatek dzielenia 26
        f'STORE {reszta}',
        f'SUB {y}',
        f'STORE {x}',
        f'JNEG {program.line_no + 60} # jump to end',
        f'LOAD {iloraz}',
        f'INC',
        f'STORE {iloraz}',
        f'JUMP {program.line_no + 26} #koniec dzeielenia',  # do poczatek dzielenia

        # mixed
        f'LOAD {x}',  # 35
        f'JNEG {program.line_no + 46}',  # 36 do poczatekdzielenia
        f'LOAD {x}',  # 37
        f'STORE {reszta}',
        f'ADD {y}',
        f'STORE {x}',
        f'JNEG {program.line_no + 60} # jump to end',
        f'LOAD {iloraz}',
        f'DEC',
        f'STORE {iloraz}',
        f'JUMP {program.line_no + 37} # koniec dzeielenia',  # 45 do poczatek dzielenia

        f'LOAD {x}',  # 46 poczatek dzielenia
        f'STORE {reszta}',
        f'ADD {y}',
        f'STORE {x}',
        f'JPOS {program.line_no + 55} # jump to end',
        f'LOAD {iloraz}',
        f'DEC',
        f'STORE {iloraz}',
        f'JUMP {program.line_no + 46} #54 koniec dzeielenia',  # do poczatek dzielenia
        f'LOAD {iloraz}',
        f'DEC',
        f'STORE {iloraz}',
        f'LOAD {x}',
        f'STORE {reszta}',  # 59
    ]
    [program.code.append(command) for command in out_code]
    # [print(f'{i}: {program.code[i]}') for i in range(len(program.code))]
    program.line_no += len(out_code)
    # print(program.line_no)

    # return proper result based on modulo flag
    if modulo:
        return Variable('helper', reszta, -1)
    else:
        return Variable('helper', iloraz, -1)


def divide_by_2(variable_x, variable_y, program):
    x = variable_x.cell
    y = variable_y.cell
    # results
    iloraz = 3

    if x == y:
        x = 5
        copy_value_code(program, from_cell=6, to_cell=5)

    clear = ['SUB 0', 'STORE 3', 'STORE 4', 'STORE 7', 'STORE 8']
    [program.code.append(command) for command in clear]
    program.line_no += 5

    out_code = [
        f'SUB 0',
        f'DEC',
        f'STORE {y}',
        f'LOAD {x}',
        f'SHIFT {y}',
        f'STORE {iloraz}',
    ]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)

    return Variable('helper', iloraz, -1)


def mod_by_2(variable_x, variable_y, program):
    x = variable_x.cell
    y = variable_y.cell
    # results
    shift_left = 3
    shift_right = 4
    result = 8

    if x == y:
        x = 5
        copy_value_code(program, from_cell=6, to_cell=5)

    clear = ['SUB 0', 'DEC', 'STORE 3', 'INC', 'INC', 'STORE 4']
    [program.code.append(command) for command in clear]
    program.line_no += len(clear)

    out_code = [
        f'LOAD {x}',
        f'SHIFT {shift_left}',
        f'SHIFT {shift_right}',
        f'SUB {x}',
        f'JZERO {program.line_no + 6}',  # omit jump below
        f'JUMP {program.line_no + 9}',  # jump to is not odd
        f'SUB 0',
        f'STORE {result}',
        f'JUMP {program.line_no + 13}',  # jump to end
        f'SUB 0',  # is not odd
        f'INC',
        f'STORE {result}',
    ]

    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)

    return Variable('helper', result, -1)


def decrement(variable_x, variable_y, program):
    x = variable_x.register

    out_code = [f'DEC {x}' for _ in range(variable_y)]
    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return Variable('helper', 'G', -1)


def increment(variable_x, variable_y, program):
    x = variable_x.cell
    out_code = [f'INC {x}' for _ in range(variable_y)]
    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return Variable('helper', 'G', -1)


def bin_pow(variable_x, variable_y, program, ):
    x = variable_x.register
    out_code = []
    while variable_y != 1:
        out_code.append(f'ADD {x} {x}')
        variable_y //= 2
    [program.code.append(command) for command in out_code]
    program.line_no += len(out_code)
    return Variable('helper', 'G', -1)


def copy_value_code(program, from_cell, to_cell=0):
    if from_cell != 0:
        program.code.append(f'SUB 0')
        program.code.append(f'ADD {from_cell}')
        program.line_no += 2
    if to_cell != 0:
        program.code.append(f'STORE {to_cell} # copied from {from_cell} to {to_cell}')
        program.line_no += 1
