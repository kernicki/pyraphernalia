from unittest import TestCase

from lsequels.command_line import main


class TestCmd(TestCase):
    def test_basic(self):
        main()
