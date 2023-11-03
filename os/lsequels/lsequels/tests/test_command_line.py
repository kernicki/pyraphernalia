import unittest
from lsequels.command_line import main


class TestCmd(unittest.TestCase):
    def __init__(self, testname, path):
        super(TestHelpSpot, self).__init__(testname)
        self.seq = lsequels.Sequel(path)

    # def test_basic(self):
    #     main()

if __name__ == '__main__':
    import sys
    path = sys.argv[1]

    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(TestCmd)

    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(TestHelpSpot(test_name, path))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
