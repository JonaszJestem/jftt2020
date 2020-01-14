import os
import unittest
from subprocess import run, PIPE

from compiler import main

class CTestFile(unittest.TestCase):
    def setUp(self):
        self.parse = main.parse

    def test_printing(self):
        data = "DECLARE BEGIN\n WRITE 5;\n END"
        code = self.parse(data)

        with open("test_cases/print.mr", "w") as file:
            file.write(code)

        result = get_output_from("test_cases/print.mr")

        self.assertEqual("5", result)

    def test_printing_var(self):
        data = "DECLARE\n a\n BEGIN\n a ASSIGN 5;\n WRITE a;\n END"
        code = self.parse(data)

        with open("test_cases/print_var.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/print_var.mr")

        self.assertEqual("5", result)

    def test_array(self):
        data = "DECLARE a(5:10) BEGIN " \
               "a(5) ASSIGN 5;" \
               "a(7) ASSIGN 2;" \
               "WRITE a(5);" \
               "WRITE a(7);" \
               "END"

        code = self.parse(data)
        with open("test_cases/array.mr", "w+") as file:
            file.write(code)


        result = get_output_from("test_cases/array.mr")

        self.assertEqual("5\n2", result)

    def test_array1(self):
        data = "DECLARE a(-5:10) BEGIN " \
               "a(-5) ASSIGN 3;" \
               "a(10) ASSIGN 5;" \
               "WRITE a(-5);" \
               "WRITE a(10);" \
               "END"

        code = self.parse(data)
        with open("test_cases/array.mr", "w+") as file:
            file.write(code)


        result = get_output_from("test_cases/array.mr")

        self.assertEqual("3\n5", result)

    def test_array_with_var(self):
        data = "DECLARE a(5:10), b BEGIN " \
               "b ASSIGN 5;" \
               "a(b) ASSIGN 10;" \
               "WRITE a(5);" \
               "END"

        code = self.parse(data)
        with open("test_cases/array_var.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/array_var.mr")

        self.assertEqual("10", result)

    def test_array_with_var_right_side(self):
        data = "DECLARE a(5:10), b BEGIN " \
               "b ASSIGN 5;" \
               "a(b) ASSIGN 7;" \
               "b ASSIGN a(5);" \
               "WRITE b;" \
               "END"

        code = self.parse(data)
        with open("test_cases/array_var.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/array_var.mr")

        self.assertEqual("7", result)

    def test_array_with_var_right_side_and_left_side(self):
        data = "DECLARE a(5:10), b, c, d BEGIN " \
               "b ASSIGN 5;" \
               "c ASSIGN 6;" \
               "d ASSIGN 7;" \
               "a(6) ASSIGN 6;" \
               "a(7) ASSIGN 7;" \
               "a(b) ASSIGN a(6) PLUS a(7);" \
               "WRITE a(b);" \
               "END"

        code = self.parse(data)
        with open("test_cases/array_var.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/array_var.mr")

        self.assertEqual("13", result)

    def test_substracting_array_with_var_right_side_and_left_side(self):
        data = "DECLARE a(5:10), b, c, d BEGIN " \
               "b ASSIGN 5;" \
               "c ASSIGN 6;" \
               "d ASSIGN 7;" \
               "a(6) ASSIGN 6;" \
               "a(7) ASSIGN 7;" \
               "a(b) ASSIGN a(7) MINUS a(6);" \
               "WRITE a(b);" \
               "END"

        code = self.parse(data)
        with open("test_cases/array_var.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/array_var.mr")

        self.assertEqual("1", result)
        # self.assertEqual(109, self.parser.code_generator.get_lines())

    def test_adding(self):
        data = "DECLARE a, b, c  \n" \
               "BEGIN  \n" \
               "READ a; \n" \
               "a ASSIGN a PLUS 5; \n" \
               "WRITE a; \n" \
               "b ASSIGN 10 MINUS a; \n" \
               "WRITE b; \n" \
               "c ASSIGN a PLUS b; \n" \
               "WRITE c; \n" \
               "c ASSIGN a MINUS b; \n" \
               "WRITE c; \n" \
               "c ASSIGN 10000 PLUS 1; \n" \
               "WRITE c; \n" \
               "END"

        code = self.parse(data)
        with open("test_cases/array_var.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/array_var.mr", "3")

        self.assertEqual("8\n2\n10\n6\n10001", result)

    def test_adding_no_vars(self):
        data = "DECLARE a, b, c BEGIN " \
               "a ASSIGN 3 PLUS 5;" \
               "WRITE a;" \
               "c ASSIGN 3 PLUS 3;" \
               "WRITE c;" \
               "END"

        code = self.parse(data)
        with open("test_cases/array_var.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/array_var.mr", "")

        self.assertEqual("8\n6", result)

    def test_div_minus(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "test_cases/div-minus.imp"))
        code = self.parse(data)
        with open("test_cases/div-minus.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/div-minus.mr", "33 7")

        self.assertEqual("-4\n5", result)

    def test_multiply(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "test_cases/multiply.imp"))
        code = self.parse(data)
        with open("test_cases/multiply.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/multiply.mr", "33 7")

        self.assertEqual("6\n9", result)

    def test_numbers_mine(self):
        data = "DECLARE	c, h, j BEGIN " \
               "c ASSIGN 15;" \
               "READ h;	" \
               "j ASSIGN h PLUS c;	" \
               "WRITE j;" \
               "END"
        code = self.parse(data)
        with open("test_cases/1-numbers.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/1-numbers.mr", "5")

        self.assertEqual("20", result)


    def test_for_1(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "test_cases/test_for_1.in"))
        code = self.parse(data)
        with open("test_cases/test_for_1.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/test_for_1.mr", "20")

        self.assertEqual("1\n1\n1\n2\n2\n3", result)

    def test_for_2(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "test_cases/test_for_2.in"))
        code = self.parse(data)
        with open("test_cases/test_for_2.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/test_for_2.mr", "20")

        self.assertEqual("1\n1\n2", result)

    def test_for_3(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "test_cases/test_for_3.in"))
        code = self.parse(data)
        with open("test_cases/test_for_3.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/test_for_3.mr", "20")

        self.assertEqual("4\n3\n2\n1\n0\n4\n3\n2\n1\n4\n3\n2", result)

    def test_divide(self):
        data = "DECLARE	tab(0:5) BEGIN	" \
               "tab(4) ASSIGN 11;	" \
               "tab(0) ASSIGN 7777;	" \
               "tab(5) ASSIGN tab(0) DIV tab(4);	" \
               "WRITE tab(5);" \
               "END"
        code = self.parse(data)
        with open("test_cases/1-numbers.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/1-numbers.mr", "5")

        self.assertEqual("707", result)

    def test_multiply_1(self):
        data = "DECLARE a, b, c, tab(0:5) BEGIN	" \
               "a ASSIGN 1;" \
               "b ASSIGN 2;" \
               "tab(a) ASSIGN 10;" \
               "tab(b) ASSIGN 3;" \
               "c ASSIGN tab(a) TIMES tab(b);" \
               "WRITE c;" \
               "END"
        code = self.parse(data)
        with open("test_cases/multiply.mr", "w+") as file:
            file.write(code)

        result = get_output_from("test_cases/multiply.mr", "30")

        self.assertEqual("30", result)



def get_output_from(mr_code, input_string=""):
    input_bytes = str(input_string).encode()
    mr = os.path.join(os.path.dirname(__file__), "../maszyna-wirtualna/maszyna-wirtualna-cln")
    test_output = run([mr, mr_code], stdout=PIPE, input=input_bytes)
    lines = test_output.stdout.decode().split("\n")[3:-2]
    print(test_output.stdout.decode())
    lines = [x.split("> ")[1] for x in lines]
    result = "\n".join(lines)
    return result


def read_file_content(file_name):
    with open(file_name) as file:
        data = file.read()
    return data

if __name__ == '__main__':
    unittest.main()