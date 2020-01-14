import os
import unittest
from subprocess import run, PIPE

from compiler import main

class CTestFile(unittest.TestCase):
    def setUp(self):
        self.parse = main.parse

    def test_div_mod(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/0-div-mod.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/0-div-mod.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/0-div-mod.mr", "1 0")

        self.assertEqual("1\n0\n0\n0", result)

    def test_div_mod2(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/00-div-mod.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/00-div-mod.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/00-div-mod.mr", "33 7")

        self.assertEqual("4\n5\n-4\n5\n5\n2\n-5\n2", result)

    def test_numbers(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/1-numbers.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/1-numbers.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/1-numbers.mr", "5")
        # print(result)
        self.assertEqual("0\n1\n-2\n10\n-100\n10000\n-1234567890\n20\n15\n-999\n-555555555\n7777\n-999\n11\n707\n7777",
                         result)


    def test_fib(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/2-fib.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/2-fib.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/2-fib.mr", "1")

        self.assertEqual("121393", result)

    def test_fib_factorial(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/3-fib-factorial.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/3-fib-factorial.mr", "w+") as file:
            file.write(code)
        result = get_output_from("na_zaliczenie/3-fib-factorial.mr", "20")

        self.assertEqual("2432902008176640000\n17711", result)

    def test_factorial(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/4-factorial.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/4-factorial.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/4-factorial.mr", "11")

        self.assertEqual("2432902008176640000", result)

    def test_tab(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/5-tab.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/5-tab.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/5-tab.mr", "")

        self.assertEqual("", result)

    @unittest.skip("Mulitply too slow")
    def test_mod_mult(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/6-mod-mult.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/6-mod-mult.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/6-mod-mult.mr", "1234567890 1234567890987654321 987654321")

        self.assertEqual("674106858", result)

    def test_loopiii1(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/7-loopiii.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/7-loopiii.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/7-loopiii.mr", "0 0 0")

        self.assertEqual("31000\n40900\n2222010", result)

    def test_loopiii2(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/7-loopiii.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/7-loopiii.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/7-loopiii.mr", "1 0 2")

        self.assertEqual("31001\n40900\n2222012", result)

    def test_for(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/8-for.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/8-for.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/8-for.mr", "12 23 34")

        self.assertEqual("507\n4379\n0", result)

    def test_sort(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/9-sort.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/9-sort.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/9-sort.mr", "12 23 34")

        self.assertEqual("", result)

    def test_program1(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/program0.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/program0.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/program0.mr", "8")

        self.assertEqual("0\n0\n0\n0", result)

    def test_program2(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/program1.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/program1.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/program1.mr", "12 23 34")

        self.assertEqual("", result)

    def test_program3(self):
        data = read_file_content(os.path.join(os.path.dirname(__file__), "na_zaliczenie/program2.imp"))
        code = self.parse(data)
        with open("na_zaliczenie/program2.mr", "w+") as file:
            file.write(code)

        result = get_output_from("na_zaliczenie/program2.mr", "12 23 34")

        self.assertEqual("", result)


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