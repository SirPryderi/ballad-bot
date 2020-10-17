import re
import logging
from src.poetry_processor import PoetryProcessor
from src.poetic_form import PoeticForm


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

  def write_poem(self, poem, author=None, form=None):
    if author == None:
      author = "anonymous"
    
    print("\n")

    for verse in poem:
      print(" ".join(verse))

    # TODO: support things like "two tercets by"

    print(f"\n — a {form} by {author}")

  def process_text(self, text, author=None):
    try:
      tokenized_text = self.tokenize_text(text)
      generated_forms = PoetryProcessor.identify_form_from_syllables(tokenized_text, self.forms)

      if len(generated_forms) != 0:
        for form, poem in generated_forms.items():
          self.write_poem(poem, author, form)

    except Exception as ex:
      pass
      # logging.error(logging.traceback.format_exc())

  def process_comment(self, comment):
    self.process_text(comment.body, f"u/{comment.author}")
