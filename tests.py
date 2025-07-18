import unittest
from functions.get_files_info import get_files_info


class TestFunctions(unittest.TestCase):

    def test_calculator_current_dir(self):
        result = get_files_info("calculator", ".")
        print(f"Result for current directory:\n{result}")

    def test_calculator_pkg_dir(self):
        result = get_files_info("calculator", "pkg")
        print(f"Result for 'pkg' directory:\n{result}")

    def test_calculator_bin_dir(self):
        result = get_files_info("calculator", "/bin")
        print(f"Result for '/bin' directory:\n{result}")

    def test_calculator_root_dir(self):
        result = get_files_info("calculator", "../")
        print(f"Result for '../' directory:\n{result}")

if __name__ == "__main__":
    unittest.main()

