import re
import logging
from src.poetry_processor import PoetryProcessor
from src.poetic_form import PoeticForm
from src.poem import Poem


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

  def process_text(self, text, author=None):
    try:
      tokenized_text = self.tokenize_text(text)
      generated_poems = PoetryProcessor.identify_form_from_syllables(tokenized_text, self.forms)

      for poem in generated_poems:
        poem.author = author
        print("\n")
        print(poem)

    except Exception as ex:
      pass
      # logging.error(logging.traceback.format_exc())

  def process_comment(self, comment):
    self.process_text(comment.body, f"u/{comment.author}")
