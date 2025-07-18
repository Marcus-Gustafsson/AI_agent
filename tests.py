import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file


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


    def test_write_file_1(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(f"Result of writing 'wait, this isn't lorem ipsum' to 'lorem.txt' :\n{result}")

    def test_write_file_2(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(f"Result of writing 'lorem ipsum dolor sit amet' to 'pkg/morelorem.txt' (this should create the 'morelorem.txt' file and write):\n{result}")

    def test_write_file_3(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(f"Result of writing 'this should not be allowed' to '/tmp/temp.txt' (this should be an error):\n{result}")

    

if __name__ == "__main__":
    unittest.main()

