import pronouncing as pr
import math


class PoetryProcessor:
  @classmethod
  def identify_form_from_syllables(cls, tokenized_text, forms):
    syllables_count = cls.get_syllables_count(tokenized_text)
    syllables_total = sum(syllables_count)

    if syllables_total == 0:
      return

    for form in forms:
      result = form.construct(tokenized_text, syllables_count, syllables_total)
      if result:
        yield result

  @staticmethod
  def get_syllables_count(tokenized_text):
    """Returns an array of with the same order of tokenized_text with each element being the word count"""
    return [*map(get_syllables_count_in_word, tokenized_text)]


def get_syllables_count_in_word(word):
  phones = pr.phones_for_word(word)
  if len(phones) > 0:
    return pr.syllable_count(phones[0])
  else:
    return math.ceil(len(word) * 0.3)
