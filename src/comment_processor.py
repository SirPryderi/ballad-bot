import re
import logging
from src.poetry_processor import PoetryProcessor


class CommentProcessor:
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

  def write_poem(self, poem, author="Anonymous"):
    print("\n")
    for verse in poem:
      print(" ".join(verse))

    print("\n —", author)

  def process_text(self, text, author=None):
    try:
      tokenized_text = self.tokenize_text(text)

      syllables_count = PoetryProcessor.get_syllables_count(tokenized_text)
      syllables_total = sum(syllables_count)

      formats = PoetryProcessor.identify_structure(
          tokenized_text, syllables_count, syllables_total)

      if len(formats) != 0:
        for format in formats:
          self.write_poem(format[1], author)

    except Exception as ex:
      pass
      # logging.error(logging.traceback.format_exc())

  def process_comment(self, comment):
    self.process_text(comment.body, f"u/{comment.author}")
