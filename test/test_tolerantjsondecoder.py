import unittest
from tolerantjsondecoder import _py_scanstring_singlequote, JSONDecoder

class TestSingleQuoteScanString(unittest.TestCase):

    def testCase1(self):
        string = r""" 'abc' """.strip()
        (s, _) = _py_scanstring_singlequote(string, 1)
        self.assertEqual(s, 'abc')

    def testCase2(self):
        string = r""" 'a"bc' """.strip()
        (s, _) = _py_scanstring_singlequote(string, 1)
        self.assertEqual(s, 'a"bc')

    def testCase3(self):
        string = r""" 'a\'bc' """.strip()
        (s, _) = _py_scanstring_singlequote(string, 1)
        self.assertEqual(s, "a'bc")


class TestJSONDecoder(unittest.TestCase):

    def testDoubleQuotedString(self):
        string = r""" "asdf"  """.strip()
        data = JSONDecoder().decode(string)
        self.assertEqual(data, "asdf")

    def testSingleQuotedString(self):
        string = r""" 'asdf' """.strip()
        data = JSONDecoder().decode(string)
        self.assertEqual(data, "asdf")

    def testListWithMixedStrings(self):
        string = r"""['abc', "abc", 34]""".strip()
        data = JSONDecoder().decode(string)
        self.assertEqual(data, ['abc', 'abc', 34])

    def testEmptyObject(self):
        string = r"""{}""".strip()
        data = JSONDecoder().decode(string)
        self.assertEqual(data, {})

    def testObjectWithDoubleQuotedStrings(self):
        string = r""" {"key":"value"} """.strip()
        data = JSONDecoder().decode(string)
        self.assertEqual(data, {"key":"value"})

    def testObjectWithDoubleAndSingleQuotedStrings(self):
        string = r""" {"c":'d', '4':5} """.strip()
        data = JSONDecoder().decode(string)
        self.assertEqual(data, {"c":'d', '4':5})
