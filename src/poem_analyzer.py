from src.meter_analyzer import MeterAnalyer
from src.poem import Poem
import pronouncing as pr


class PoemAnalyzer:
  def __init__(self, poem: Poem):
    self.poem = poem

  def analyze(self):
    self.rhyme_scheme()
    self.meter()
    self.score()

  def rhyme_scheme(self):
    self.poem.rhyme_count = 0
    rhyme_parts = []
    rhyme_scheme = [''] * len(self.poem.verses)
    rhyme_ordinal = 0

    for i, verse in enumerate(self.poem.verses):
      if verse == "":
        rhyme_parts.append("")
        rhyme_scheme[i] = " "
        continue

      phones = pr.phones_for_word(verse[-1])

      if len(phones) == 0:
        rhyme_parts.append("")
        continue

      rhyming_parts = [*map(lambda phone: pr.rhyming_part(phone), phones)]

      rhyme_parts.append(rhyming_parts)

    # god of complexity forgive me
    for i, i_part_variants in enumerate(rhyme_parts):
      for i_part in i_part_variants:
        for j, j_part_variants in enumerate(rhyme_parts[i+1:]):
          j = j+i+1
          for j_part in j_part_variants:
            if i_part == j_part:
              # the rhyming part maches, now let's check if it's the same word
              i_word = self.poem.verses[i][-1]
              j_word = self.poem.verses[j][-1]

              if len(rhyme_scheme[i]) != 0:
                letter = rhyme_scheme[i]
              else:
                rhyme_ordinal += 1
                letter = self.cardinal_n_to_ordinal_letter(rhyme_ordinal)
              rhyme_scheme[i] = letter
              rhyme_scheme[j] = letter

              if i_word == j_word:
                continue

              self.poem.rhyme_count += 1

    # fills empty cells in the rhyme scheme
    for i, letter in enumerate(rhyme_scheme):
      if letter == '':
        rhyme_ordinal += 1
        rhyme_scheme[i] = self.cardinal_n_to_ordinal_letter(rhyme_ordinal).lower()

      self.poem.rhyme_scheme = rhyme_scheme

  def meter(self):
    self.poem.verses_meter = [*map(lambda v: MeterAnalyer.get_meter(v), self.poem.verses)]

  def score(self):
    unique_words_count = len(self.unique_words())
    length_score = unique_words_count * 2
    if unique_words_count > 60:  # demote poems that are too long
      length_score = length_score - ((unique_words_count - 60) * 3)
    rhymes_score = self.poem.rhyme_count / self.poem.verses_count * 200
    repetition_score = -self.poem.form_repetition  # demote excessively repeated forms in favour of longer forms
    total = length_score + rhymes_score + repetition_score
    self.poem.score = round(total)

  def unique_words(self):
    unique_words = set()
    for verse in self.poem.verses:
      for word in verse:
        unique_words.add(word)
    return unique_words

  @ staticmethod
  def cardinal_n_to_ordinal_letter(number: int):
    return chr(ord('@')+number)
