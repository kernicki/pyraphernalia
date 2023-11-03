from unittest import TestCase

import lsequels

class TestSequel(TestCase):
    def test_module(self):
        try:
            s = lsequels.Sequel( "../__temp_tests/" )
            for  i in s.get():
                print (i)
        except Exception:
            print ("Please run generate_seqs.sh first.")
