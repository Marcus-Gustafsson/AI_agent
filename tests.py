import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file
from functions.run_python import run_python_file


class TestFunctions(unittest.TestCase):

    # def test_calculator_current_dir(self):
    #     result = get_files_info("calculator", ".")
    #     print(f"Result for current directory:\n{result}")

    # def test_calculator_pkg_dir(self):
    #     result = get_files_info("calculator", "pkg")
    #     print(f"Result for 'pkg' directory:\n{result}")

    # def test_calculator_bin_dir(self):
    #     result = get_files_info("calculator", "/bin")
    #     print(f"Result for '/bin' directory:\n{result}")

    # def test_calculator_root_dir(self):
    #     result = get_files_info("calculator", "../")
    #     print(f"Result for '../' directory:\n{result}")

    # def test_calculator_root_dir(self):
    #     result = get_file_content("calculator", "lorem.txt")
    #     print(f"Result for '../' directory:\n{result}")



    # def test_get_main_content(self):
    #     result = get_file_content("calculator", "main.py")
    #     print(f"Result for reading main.py in 'calculator' dir:\n{result}")

    # def test_get_pkg_calc_file(self):
    #     result = get_file_content("calculator", "pkg/calculator.py")
    #     print(f"Result for 'pkg/calculator.py' file:\n{result}")

    # def test_calculator_bin_dir(self):
    #     result = get_file_content("calculator", "/bin/cat")
    #     print(f"Result for '/bin/cat' file (should be error string):\n{result}")

    # def test_calculator_root_dir(self):
    #     result = get_file_content("calculator", "pkg/does_not_exist.py")
    #     print(f"Result for 'pkg/does_not_exist.py' file (should be error string):\n{result}")


    # def test_write_file_1(self):
    #     result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    #     print(f"Result of writing 'wait, this isn't lorem ipsum' to 'lorem.txt' :\n{result}")

    # def test_write_file_2(self):
    #     result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    #     print(f"Result of writing 'lorem ipsum dolor sit amet' to 'pkg/morelorem.txt' (this should create the 'morelorem.txt' file and write):\n{result}")

    # def test_write_file_3(self):
    #     result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    #     print(f"Result of writing 'this should not be allowed' to '/tmp/temp.txt' (this should be an error):\n{result}")



    def test_write_file_1(self):
        result = run_python_file("calculator", "main.py")
        print(f"Test 1 -> should print the calculator's usage instructions):\n{result}")

    def test_write_file_2(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(f"Test 2 -> (should run the calculator... which gives a kinda nasty rendered result):\n{result}")
    
    def test_write_file_3(self):
        result = run_python_file("calculator", "tests.py")
        print(f"Test 3 -> (should print the calculator's unittests):\n{result}")

    def test_write_file_4(self):
        result = run_python_file("calculator", "../main.py")
        print(f"Test 4 -> (this should return an error, 'outside dir' error):\n{result}")
    
    def test_write_file_5(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(f"Test 5 -> (this should return an error, 'file not found' error):\n{result}")

    

if __name__ == "__main__":
    unittest.main()

