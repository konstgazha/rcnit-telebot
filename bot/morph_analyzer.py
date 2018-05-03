import re
import math
import pymorphy2
from collections import Counter
from difflib import SequenceMatcher

morph = pymorphy2.MorphAnalyzer()

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def get_normal_form(word):
    return morph.parse(word)[0].normal_form

def text_to_vector(text):
    word = re.compile(r'\w+')
    words = [get_normal_form(x) for x in word.findall(text)]
    return Counter(words)

def get_normalized_similarity_by_cosine(text1, text2):
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    return get_cosine(vector1, vector2)

def get_similarity_by_sequence_matcher(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

def get_max_similarity(text1, text2):
    return (max(get_normalized_similarity_by_cosine(text1, text2),
                get_similarity_by_sequence_matcher(text1, text2)
                ))

def string_detection(text, string):
    max_rate = get_max_similarity(text, string)
    for word in text.split():
        similarity = get_similarity_by_sequence_matcher(word, string)
        if similarity > max_rate:
            max_rate = similarity
    return max_rate
