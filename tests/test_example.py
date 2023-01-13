import unittest


class TestExample(unittest.TestCase):

    def test_example(self):
        expected = True
        actual = True
        self.assertEqual(expected, actual, "Change this test!")


if __name__ == '__main__':
    unittest.main()
