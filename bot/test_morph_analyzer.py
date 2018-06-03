import re
import math
import pymorphy2
from collections import Counter
from difflib import SequenceMatcher
import unittest
from unittest.mock import MagicMock
from morph_analyzer import (get_normal_form,
                            text_to_vector,
                            get_normalized_similarity_by_cosine,
                            get_similarity_by_sequence_matcher,
                            get_max_similarity)


class TestMorphAnalysis(unittest.TestCase):
    def setUp(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.text1 = "Тестовые примеры"
        self.text2 = "Тестовые пирожки"
        self.string = "пирожок"

    def test_get_normal_form(self):
        word = 'Примеры'
        normal_form = self.morph.parse(word)[0].normal_form
        self.assertEqual(normal_form, 'пример')

    def test_text_to_vector(self):
        text = "Тестовые примеры"
        re_word = re.compile(r'\w+')
        words = [get_normal_form(x) for x in re_word.findall(text)]
        self.assertEqual(dict(Counter(words)), {'тестовый': 1, 'пример': 1})

    def test_get_cosine(self):
        vec1 = text_to_vector(self.text1)
        vec2 = text_to_vector(self.text2)
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        self.assertAlmostEqual(float(numerator) / denominator, 0.5, 3)

    def test_get_similarity_by_sequence_matcher(self):
        rate = SequenceMatcher(None, self.text1, self.text2).ratio()
        self.assertAlmostEqual(rate, 0.75, 3)

    def test_get_max_similarity(self):
        best_score = max(get_normalized_similarity_by_cosine(self.text1, self.text2),
                         get_similarity_by_sequence_matcher(self.text1, self.text2))
        self.assertAlmostEqual(best_score, 0.75, 3)

    def test_string_detection(self):
        max_rate = get_max_similarity(self.text2, self.string)
        for word in self.text2.split():
            similarity = get_similarity_by_sequence_matcher(word, self.string)
            if similarity > max_rate:
                max_rate = similarity
        self.assertAlmostEqual(max_rate, 0.857, 3)

if __name__ == '__main__':
    unittest.main()