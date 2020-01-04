import os
import unittest
from subprocess import run, PIPE

from compiler import main

class CTestFile(unittest.TestCase):
    def setUp(self):
        self.parse = main.parse

    def test_printing(self):
        data = "DECLARE IN WRITE 5; END"
        code = self.parse(data)
        print(code)
        # with open("test_cases/print.mr", "w") as file:
        #     file.write(code)
        # print(code)
        # result = get_output_from("test_cases/print.mr")
        #
        # self.assertEqual("5", result)
    #
    # def test_printing_var(self):
    #     data = "DECLARE a; IN a := 5; WRITE a; END"
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/print_var.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("test_cases/print_var.mr")
    #
    #     self.assertEqual("5", result)
    #
    # def test_example(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "test_cases/example_1"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/example_1.mr", "w+") as file:
    #         file.write(code)
    #     # result = get_output_from("test_cases/example_1.mr", "2")
    #     #
    #     # self.assertEqual("5", result)
    #
    # def test_array(self):
    #     data = "DECLARE a(5:10); IN " \
    #            "a(5) := 5;" \
    #            "a(7) := 2;" \
    #            "WRITE a(5);" \
    #            "WRITE a(7);" \
    #            "END"
    #
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/array.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #
    #     result = get_output_from("test_cases/array.mr")
    #
    #     self.assertEqual("5\n2", result)
    #
    # def test_array_with_var(self):
    #     data = "DECLARE a(5:10); b; IN " \
    #            "b := 5;" \
    #            "a(b) := 10;" \
    #            "WRITE a(5);" \
    #            "END"
    #
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/array_var.mr", "w+") as file:
    #         file.write(code)
    #     # print(code)
    #     result = get_output_from("test_cases/array_var.mr")
    #
    #     self.assertEqual("10", result)
    #
    # def test_array_with_var_right_side(self):
    #     data = "DECLARE a(5:10); b; IN " \
    #            "b := 5;" \
    #            "a(b) := 7;" \
    #            "b := a(5);" \
    #            "WRITE b;" \
    #            "END"
    #
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/array_var.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("test_cases/array_var.mr")
    #
    #     self.assertEqual("7", result)
    #     # self.assertEqual(54, self.parser.code_generator.get_lines())
    #
    # def test_array_with_var_right_side_and_left_side(self):
    #     data = "DECLARE a(5:10); b; c; d; IN " \
    #            "b := 5;" \
    #            "c := 6;" \
    #            "d := 7;" \
    #            "a(6) := 6;" \
    #            "a(7) := 7;" \
    #            "a(b) := a(6) + a(7);" \
    #            "WRITE a(b);" \
    #            "END"
    #
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/array_var.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("test_cases/array_var.mr")
    #
    #     self.assertEqual("13", result)
    #     # self.assertEqual(109, self.parser.code_generator.get_lines())
    #
    # def test_substracting_array_with_var_right_side_and_left_side(self):
    #     data = "DECLARE a(5:10); b; c; d; IN " \
    #            "b := 5;" \
    #            "c := 6;" \
    #            "d := 7;" \
    #            "a(6) := 6;" \
    #            "a(7) := 7;" \
    #            "a(b) := a(7) - a(6);" \
    #            "WRITE a(b);" \
    #            "END"
    #
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/array_var.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("test_cases/array_var.mr")
    #
    #     self.assertEqual("1", result)
    #     # self.assertEqual(109, self.parser.code_generator.get_lines())
    #
    # def test_adding(self):
    #     data = "DECLARE a; b; c; IN " \
    #            "READ a;" \
    #            "a := a + 5;" \
    #            "WRITE a;" \
    #            "b := 10 - a;" \
    #            "WRITE b;" \
    #            "c := a + b;" \
    #            "WRITE c;" \
    #            "c := a - b;" \
    #            "WRITE c;" \
    #            "END"
    #
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/array_var.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("test_cases/array_var.mr", "3")
    #
    #     self.assertEqual("8\n2\n10\n6", result)
    #     # self.assertEqual(54, self.parser.code_generator.get_lines())
    #
    # def test_adding_no_vars(self):
    #     data = "DECLARE a; b; c; IN " \
    #            "a := 3 + 5;" \
    #            "WRITE a;" \
    #            "c := 3 + 3;" \
    #            "WRITE c;" \
    #            "END"
    #
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("test_cases/array_var.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("test_cases/array_var.mr", "")
    #
    #     self.assertEqual("8\n6", result)
    #
    # def test_div_mod(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/0-div-mod.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/0-div-mod.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("na_zaliczenie/0-div-mod.mr", "1 0")
    #
    #     self.assertEqual("1\n0\n0\n0", result)
    #
    # def test_numbers(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/1-numbers.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/1-numbers.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("na_zaliczenie/1-numbers.mr", "5")
    #     print(result)
    #     self.assertEqual("0\n1\n2\n10\n100\n10000\n1234567890\n20\n15\n999\n555555555\n7777\n999\n11\n707\n7777",
    #                      result)
    #
    # def test_numbers_mine(self):
    #     data = "DECLARE	c; h; j;IN " \
    #            "c := 15;" \
    #            "READ h;	" \
    #            "j := h + c;	" \
    #            "WRITE j;" \
    #            "END"
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/1-numbers.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("na_zaliczenie/1-numbers.mr", "5")
    #     print(result)
    #     self.assertEqual("20", result)
    #
    # def test_fib(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/2-fib.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/2-fib.mr", "w+") as file:
    #         file.write(code)
    #
    #     result = get_output_from("na_zaliczenie/2-fib.mr", "1")
    #
    #     self.assertEqual("121393", result)
    #
    # def test_fib_factorial(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/3-fib-factorial.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/3-fib-factorial.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     # result = get_output_from("na_zaliczenie/3-fib-factorial.mr", "20")
    #
    #     self.assertEqual("2432902008176640000\n17711", result)
    #
    # def test_factorial(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/4-factorial.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/4-factorial.mr", "w+") as file:
    #         file.write(code)
    #
    #     result = get_output_from("na_zaliczenie/4-factorial.mr", "20")
    #
    #     self.assertEqual("2432902008176640000", result)
    #
    # def test_tab(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/5-tab.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/5-tab.mr", "w+") as file:
    #         file.write(code)
    #
    #     # result = get_output_from("na_zaliczenie/5-tab.mr", "")
    #
    #     self.assertEqual("", result)
    #
    # def test_mod_mult(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/6-mod-mult.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/6-mod-mult.mr", "w+") as file:
    #         file.write(code)
    #
    #     result = get_output_from("na_zaliczenie/6-mod-mult.mr", "1234567890 1234567890987654321 987654321")
    #
    #     self.assertEqual("674106858", result)
    #
    # def test_loopiii1(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/7-loopiii.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/7-loopiii.mr", "w+") as file:
    #         file.write(code)
    #
    #     result = get_output_from("na_zaliczenie/7-loopiii.mr", "0 0 0")
    #
    #     self.assertEqual("31000\n40900\n2222010", result)
    #
    # def test_loopiii2(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/7-loopiii.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/7-loopiii.mr", "w+") as file:
    #         file.write(code)
    #
    #     result = get_output_from("na_zaliczenie/7-loopiii.mr", "1 0 2")
    #
    #     self.assertEqual("31001\n40900\n2222012", result)
    #
    # def test_for(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/8-for.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/8-for.mr", "w+") as file:
    #         file.write(code)
    #
    #     result = get_output_from("na_zaliczenie/8-for.mr", "12 23 34")
    #
    #     self.assertEqual("507\n4379\n0", result)
    #
    # def test_sort(self):
    #     data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/9-sort.imp"))
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/9-sort.mr", "w+") as file:
    #         file.write(code)
    #
    #     # result = get_output_from("na_zaliczenie/9-sort.mr", "12 23 34")
    #
    #     self.assertEqual("", result)
    #
    # def test_divide(self):
    #     data = "DECLARE	tab(0:5);IN	" \
    #            "tab(4) := 11;	" \
    #            "tab(0) := 7777;	" \
    #            "tab(5) := tab(0) / tab(4);	" \
    #            "WRITE tab(5);" \
    #            "END"
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/1-numbers.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("na_zaliczenie/1-numbers.mr", "5")
    #     # print(result)
    #     self.assertEqual("707", result)
    #
    # def test_multiply(self):
    #     data = "DECLARE a; b; c; tab(0:5); IN	" \
    #            "a := 1;" \
    #            "b := 2;" \
    #            "tab(a) := 10;" \
    #            "tab(b) := 3;" \
    #            "c := tab(a) * tab(b);" \
    #            "WRITE c;" \
    #            "END"
    #     tree = self.parse(data, debug=False)
    #     code = tree.get_string_representation()
    #     with open("na_zaliczenie/multiply.mr", "w+") as file:
    #         file.write(code)
    #     print(code)
    #     result = get_output_from("na_zaliczenie/multiply.mr", "30")
    #     print(result)
    #     self.assertEqual("3", result)



def get_output_from(mr_code, input_string=""):
    input_bytes = str(input_string).encode()
    mr = os.path.join(os.path.dirname(__file__), "maszyna_rejestrowa/maszyna-rejestrowa")
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