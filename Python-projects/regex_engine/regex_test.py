import unittest
import regex

class MyTestCase(unittest.TestCase):
    def test_single_char(self):
        self.assertEqual(regex.start_end("a", "a"), True)
        self.assertEqual(regex.start_end(".", "a"), True)
        self.assertEqual(regex.start_end("", "a"), True)
        self.assertEqual(regex.start_end("", ""), True)
        self.assertEqual(regex.start_end("a", ""), False)

    def test_word_and_regex_same_length(self):
        self.assertEqual(regex.start_end("apple", "apple"), True)
        self.assertEqual(regex.start_end(".pple", "apple"), True)
        self.assertEqual(regex.start_end("appl.", "apple"), True)
        self.assertEqual(regex.start_end(".....", "apple"), True)
        self.assertEqual(regex.start_end("peach", "apple"), False)

    def test_word_and_regex_different_length(self):
        self.assertEqual(regex.start_end("apple", "apple"), True)
        self.assertEqual(regex.start_end("ap", "apple"), True)
        self.assertEqual(regex.start_end("le", "apple"), True)
        self.assertEqual(regex.start_end("a", "apple"), True)
        self.assertEqual(regex.start_end(".", "apple"), True)
        self.assertEqual(regex.start_end("apwle", "apple"), False)
        self.assertEqual(regex.start_end("peach", "apple"), False)

    def test_starts_with(self):
        self.assertEqual(regex.start_end("^app", "apple"), True)
        self.assertEqual(regex.start_end("^a", "apple"), True)
        self.assertEqual(regex.start_end("^apple", "apple pie"), True)
        self.assertEqual(regex.start_end("^le", "apple"), False)

    def test_ends_with(self):
        self.assertEqual(regex.start_end("le$", "apple"), True)
        self.assertEqual(regex.start_end("apple$", "tasty apple"), True)
        self.assertEqual(regex.start_end(".$", "apple"), True)
        self.assertEqual(regex.start_end("app$", "apple"), False)

    def test_starts_and_ends_with(self):
        self.assertEqual(regex.start_end("^apple$", "apple pie"), False)
        self.assertEqual(regex.start_end("^apple$", "apple"), True)
        self.assertEqual(regex.start_end("^apple$", "tasty apple"), False)
        self.assertEqual(regex.start_end("^apple$", "apple pie"), False)

    def test_repetition_with_question_mark(self):
        self.assertEqual(regex.start_end("colou?r", "color"), True)
        self.assertEqual(regex.start_end("colou?r", "colour"), True)
        self.assertEqual(regex.start_end("colou?r", "colouur"), False)

    def test_repetition_with_asterisk(self):
        self.assertEqual(regex.start_end("colou*r", "color"), True)
        self.assertEqual(regex.start_end("colou*r", "colour"), True)
        self.assertEqual(regex.start_end("colou*r", "colouur"), True)
        self.assertEqual(regex.start_end("a*b", "aaaaaaaaaab"), True)

    def test_repetition_with_plus_operator(self):
        self.assertEqual(regex.start_end("colou+r", "colour"), True)
        self.assertEqual(regex.start_end("colou+r", "color"), False)
        self.assertEqual(regex.start_end("a+b", "aaaaaaaaaab"), True)

    def test_repetitions_and_dots(self):
        self.assertEqual(regex.start_end("col.*p", "coloooooooooooooeeeruto"), False)
        self.assertEqual(regex.start_end(".*", "aaa"), True)
        self.assertEqual(regex.start_end(".*b", "aaaaaaaaaab"), True)
        self.assertEqual(regex.start_end("col.*r", "coloooooooooooooeeer"), True)
        self.assertEqual(regex.start_end("col.*r", "color"), True)
        self.assertEqual(regex.start_end("col.*r", "colour"), True)
        self.assertEqual(regex.start_end("col.*r", "colr"), True)
        self.assertEqual(regex.start_end("col.*r", "collar"), True)
        self.assertEqual(regex.start_end("col.*r", "coloooooooooooooeeeruto"), True)
        self.assertEqual(regex.start_end("col.+r", "coloooooooooooooeeeruto"), True)
        self.assertEqual(regex.start_end("col.+r", "colour"), True)
        self.assertEqual(regex.start_end("col.+r", "colr"), False)
        self.assertEqual(regex.start_end(".+", "aaa"), True)
        self.assertEqual(regex.start_end(".+b", "aaaaaaaaaab"), True)

    def test_combination_of_different_rules(self):
        self.assertEqual(regex.start_end("^no+pe", "noooooooope"), True)
        self.assertEqual(regex.start_end("^no+pe$", "noooooooope"), True)
        self.assertEqual(regex.start_end("no+$", "noooooooope"), False)
        self.assertEqual(regex.start_end("^no+pe$", "noooooooope"), True)
        self.assertEqual(regex.start_end("col.*r$", "colors"), False)

if __name__ == '__main__':
    unittest.main()
