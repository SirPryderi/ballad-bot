from src.poem import Poem
import pronouncing as pr


class PoemAnalyzer:
  def __init__(self, poem: Poem):
    self.poem = poem

  def analyze(self):
    self.rhyme_scheme()
    self.metre()
    self.score()

  def rhyme_scheme(self):
    self.poem.rhyme_count = 0
    rhyme_parts = []
    rhyme_scheme = [''] * len(self.poem.verses)

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

              if i_word == j_word:
                continue

              self.poem.rhyme_count += 1
              letter = self.cardinal_n_to_ordinal_letter(self.poem.rhyme_count)
              rhyme_scheme[i] = letter
              rhyme_scheme[j] = letter

      # fills empty cells in the rhyme scheme
      for i, letter in enumerate(rhyme_scheme):
        if letter == '':
          rhyme_scheme[i] = '–'

      self.poem.rhyme_scheme = rhyme_scheme

  def metre(self):
    pass

  def score(self):
    pass

  @staticmethod
  def cardinal_n_to_ordinal_letter(number: int):
    return chr(ord('@')+number)
