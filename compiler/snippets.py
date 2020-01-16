import logging

from variables import Variable, copy_value


def less_or_equal(variable_x, variable_y, program, swap=False):
    x, y = variable_x.cell, variable_y.cell

    label_false = "<replace_here>"
    line_to_fill = program.line_no + 4
    if swap:
        x, y = y, x

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
    result = 11
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
    helper_1 = 8
    helper_2 = 9

    if x == y:
        x = 5
        copy_value_code(program, from_cell=6, to_cell=5)

    clear = ['SUB 0', 'STORE 3', 'STORE 4', 'STORE 7', 'STORE 8', 'STORE 9', 'STORE 17']
    [program.code.append(command) for command in clear]
    program.line_no += len(clear)

    div = [
        f'LOAD {y}',
        f'JZERO {program.line_no + 134} # dzielenie przez 0',
        f'LOAD {x}',
        f'JPOS {program.line_no + 7}',
        f'LOAD {sign_helper}',
        f'INC',
        f'STORE {sign_helper}',
        f'LOAD {y}',#7
        f'JPOS {program.line_no + 12}',
        f'LOAD {sign_helper}',
        f'INC',
        f'STORE {sign_helper}',
        f'LOAD {sign_helper}', #12
        f'JZERO {program.line_no + 69} #jump to normal',
        f'DEC',  # 14
        f'JZERO {program.line_no + 28} #jump to handling mixed',
        f'SUB 0',  # handle all negative, set flag
        f'INC',
        f'STORE 17',
        f'LOAD {x}',
        f'SUB {x}',
        f'SUB {x}',
        f'STORE {x}',
        f'LOAD {y}',
        f'SUB {y}',
        f'SUB {y}',
        f'STORE {y}',
        f'JUMP {program.line_no + 69} #JUMP TO NORMAL DIV', # 27 -
        # mixed
        f'LOAD {x} # mixed start', #28
        f'STORE {reszta}',
        f'JPOS {program.line_no + 50} # 30 to second negative',
        f'LOAD {x}', # 31
        f'ADD {y}',
        f'STORE {x}',
        f'LOAD {iloraz}',
        f'INC',
        f'STORE {iloraz}',
        f'LOAD {x}',
        f'SUB {x}',
        f'SUB {x}',
        f'STORE {reszta}', #40
        f'STORE 17',
        f'LOAD {x}',
        f'JPOS {program.line_no + 45} #to flip',
        f'JUMP {program.line_no + 31}',#44
        f'LOAD {iloraz}',
        f'SUB {iloraz}',
        f'SUB {iloraz}',
        f'STORE {iloraz}',
        f'JUMP {program.line_no + 42 + 73 + 19} # 49 mixed end',  # to end

        f'LOAD {x} #50 second negative',
        f'ADD {y}',
        f'STORE {x}',
        f'LOAD {iloraz}',
        f'INC',
        f'STORE {iloraz}',
        f'LOAD {x}',
        f'SUB {x}',
        f'SUB {x}',
        f'STORE {reszta}',
        f'STORE 17', #60
        f'LOAD {x}',
        f'JNEG {program.line_no + 44 + 20} #to flip',
        f'JUMP {program.line_no + 30 + 21}',
        f'LOAD {iloraz} #flip',
        f'SUB {iloraz}',
        f'SUB {iloraz}',
        f'STORE {iloraz}',
        f'JUMP {program.line_no + 134} # 68 mixed end',  # to end
    ]#69
    [program.code.append(command) for command in div]
    program.line_no += len(div)
    #
    # # mixed
    # f'LOAD {x}',  # 35
    # f'JNEG {program.line_no + 46}',  # 36 do poczatekdzielenia
    # f'LOAD {x}',  # 37
    # f'STORE {reszta}',
    # f'ADD {y}',
    # f'STORE {x}',
    # f'JNEG {program.line_no + 60} # jump to end',
    # f'LOAD {iloraz}',
    # f'DEC',
    # f'STORE {iloraz}',
    # f'JUMP {program.line_no + 37} # koniec dzeielenia',  # 45 do poczatek dzielenia
    #
    # f'LOAD {x}',  # 46 poczatek dzielenia
    # f'STORE {reszta}',
    # f'ADD {y}',
    # f'STORE {x}',
    # f'JPOS {program.line_no + 55} # jump to end',
    # f'LOAD {iloraz}',
    # f'DEC',
    # f'STORE {iloraz}',
    # f'JUMP {program.line_no + 46} #54 koniec dzeielenia',  # do poczatek dzielenia
    # f'LOAD {iloraz}',
    # f'DEC',
    # f'STORE {iloraz}',
    # f'LOAD {x}',
    # f'STORE {reszta}',  # 59

    out_code = [
        # f'COPY {reszta} {x} #division',
        f'LOAD {x} #normal div',
        f'STORE {reszta}',

        # f'JZERO {y} {program.line_no + 24} #zero_divison',
        f'LOAD {y}',  # 2
        f'JZERO {program.line_no + 63} # dzielenie przez 0',  # jump to zeroying

        # f'COPY {helper_1} {y}',
        f'LOAD {y}',  # 4
        f'STORE {helper_1}',

        # f'COPY {iloraz} {helper_1}',
        f'LOAD {helper_1}',  # 6
        f'STORE {iloraz}',

        # f'SUB {iloraz} {reszta}',
        f'LOAD {iloraz}',  # 8
        f'SUB {reszta}',
        f'STORE {iloraz}',

        # f'JZERO {iloraz} {program.line_no + 7}',
        f'LOAD {iloraz}',  # 11
        f'JNEG {program.line_no + 15}',
        f'JZERO {program.line_no + 15}',


        # f'JUMP {program.line_no + 9}',
        f'JUMP {program.line_no + 19}',  # 14

        # f'ADD {helper_1} {helper_1}', #7
        f'LOAD {helper_1}',  # 15
        f'ADD {helper_1}',
        f'STORE {helper_1}',

        # f'JUMP {program.line_no + 3}',
        f'JUMP {program.line_no + 6}',  # 18

        # f'SUB {iloraz} {iloraz}',
        f'SUB 0',  # 19
        f'STORE {iloraz}',

        # f'COPY {helper_2} {helper_1}', #10
        f'LOAD {helper_1}',  # 21
        f'STORE {helper_2}',

        # f'SUB {helper_2} {reszta}',
        f'LOAD {helper_2}',  # 23
        f'SUB {reszta}',
        f'STORE {helper_2}',

        # f'JZERO {helper_2} {program.line_no + 16}',
        f'LOAD {helper_2}',  # 26
        f'JZERO {program.line_no + 39}',
        f'JNEG {program.line_no + 39}',

        # f'ADD {iloraz} {iloraz}',
        f'LOAD {iloraz}',  # 29
        f'ADD {iloraz}',
        f'STORE {iloraz}',

        # f'HALF {helper_1}',
        f'SUB 0',  # 32
        f'DEC',
        f'STORE 13',
        f'LOAD {helper_1}',
        f'SHIFT {13}',
        f'STORE {helper_1}',

        # f'JUMP {program.line_no + 20}',
        f'JUMP {program.line_no + 54}',  # 38

        # f'ADD {iloraz} {iloraz}', # 16
        f'LOAD {iloraz}',  # 39
        f'ADD {iloraz}',
        f'STORE {iloraz}',

        # f'INC {iloraz}',
        f'LOAD {iloraz}',  # 42
        f'INC',
        f'STORE {iloraz}',

        # f'SUB {reszta} {helper_1}',
        f'LOAD {reszta}',  # 45
        f'SUB {helper_1}',
        f'STORE {reszta}',

        # f'HALF {helper_1}',
        f'SUB 0',  # 48
        f'DEC',
        f'STORE 13',
        f'LOAD {helper_1}',
        f'SHIFT {13}',
        f'STORE {helper_1}',

        # f'COPY {helper_2} {y}',#20
        f'LOAD {y}',  # 54
        f'STORE {helper_2}',

        # f'SUB {helper_2} {helper_1}',
        f'LOAD {helper_2}',  # 56
        f'SUB {helper_1}',
        f'STORE {helper_2}',

        # f'JZERO {helper_2} {program.line_no + 10}',
        f'LOAD {helper_2}',  # 59
        f'JZERO {program.line_no + 21}',
        f'JNEG {program.line_no + 21}',

        # f'JUMP {program.line_no + 26}',
        f'JUMP {program.line_no + 66}',  # 62

        # f'SUB {reszta} {reszta}',#zeroying
        # f'SUB {iloraz} {iloraz} #division end',
        f'SUB 0',  # 63
        f'LOAD {reszta}',
        f'LOAD {iloraz} #division end',

        f'LOAD 17',
        f'JZERO {program.line_no + 72}',
        f'LOAD {reszta}',
        f'SUB {reszta}',
        f'SUB {reszta}',
        f'STORE {reszta}',
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
