import os
from src.poetry_processor import PoetryProcessor
from src.poem import Poem


class PoeticForm:
  def __init__(self, name, verses):
    self.name = name
    self.verses = verses

    self.verses_count = len(verses)
    self.syllables_count = 0

    for verse in verses:
      self.syllables_count = self.syllables_count + len(verse)

  @classmethod
  def load_forms(cls, path):
    forms = []
    entries = os.listdir(path)

    for entry in entries:
      verses = []
      with open(os.path.join(path, entry), 'r') as f:
        lines = f.readlines()
        for line in lines:
          line = line.strip()
          if line == "":
            continue
          verses.append(line)

      form = cls(entry, verses)
      forms.append(form)
      print(f"Learnt {form.name}\t| {form.verses_count} verses\t| {form.syllables_count} syllables")

    return forms

  def construct(self, tokenized_text, syllables_count=None, syllables_total=None):
    if syllables_count == None:
      # normally passed in for performance
      syllables_count = PoetryProcessor.get_syllables_count(tokenized_text)
      syllables_total = sum(syllables_count)

    if syllables_total % self.syllables_count != 0:
      return False

    failed = False
    verses = []
    verses_syllables = []

    word_index = 0
    repetitions = syllables_total // self.syllables_count
    verses_count = repetitions * self.verses_count

    for verse_index in range(verses_count):
      if verse_index != 0 and verse_index % self.verses_count == 0 and self.verses_count != 1:
        verses.append("")
      verse_index = (verse_index % self.verses_count)

      expected_syllables_count = len(self.verses[verse_index])

      verse = []
      verse_syllables = []

      verse_syllables_count = 0

      while verse_syllables_count < expected_syllables_count:
        verse.append(tokenized_text[word_index])
        verse_syllables.append(syllables_count[word_index])
        verse_syllables_count = verse_syllables_count + syllables_count[word_index]
        word_index = word_index + 1

      if verse_syllables_count != expected_syllables_count:
        failed = True
        break

      verses.append(verse)

    if failed:
      return False

    return Poem(verses, form=self, form_repetition=repetitions, syllables_count=syllables_count, syllables_total=syllables_total)
