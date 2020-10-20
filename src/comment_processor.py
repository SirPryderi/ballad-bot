# -*- coding: utf-8 -*-

import re
from src.poetry_processor import PoetryProcessor
from src.poetic_form import PoeticForm
from src.poem_analyzer import PoemAnalyzer


class CommentProcessor:
  def __init__(self):
    self.forms = PoeticForm.load_forms('./forms')

  def tokenize_text(self, text):
    # TODO: we need need better tokenization here, this is way to makeshift.
    # remove new lines
    preprocessed = text.replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
    # lowercase
    preprocessed = preprocessed.strip().lower()
    # filter just alphanumeric and space characters
    preprocess_text = re.sub('[^a-z \'\d]+', '', preprocessed)
    # split word
    tokenized_text = preprocess_text.split()
    return tokenized_text

  @staticmethod
  def print_poem_info(poem):
    print("\n")
    print(poem)
    print(f"Score: {poem.score}")
    print(f"Meter: {poem.verses_meter}")
    if poem.rhyme_count:
      print(f"Rhymes: {poem.rhyme_count} | {''.join(poem.rhyme_scheme)}")

  def process_text(self, text, author=None):
    tokenized_text = self.tokenize_text(text)
    generated_poems = PoetryProcessor.identify_form_from_syllables(tokenized_text, self.forms)
    # Let's face it: I don't know how to use generators
    candidates = []
    for poem in generated_poems:
      poem.author = author
      PoemAnalyzer(poem).analyze()
      if (poem.score) > 100:
        self.print_poem_info(poem)
      candidates.append(poem)
    return candidates
