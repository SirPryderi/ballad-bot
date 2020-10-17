import pronouncing as pr

two_to_one_stress = {ord('2'): u'1'}

class PoetryProcessor:
  @staticmethod
  def is_ballad(tokenized_text):
    return True

  @classmethod
  def identify_structure(cls, tokenized_text, syllables_count, syllables_total):
    viable_structures = []

    if syllables_total == 0: return []
    
    if syllables_total % 28 == 0:
      failed = False
      verses = []
      verses_syllables = []
      
      word_index = 0
      verses_count = syllables_total // 28 * 4

      for verse_count in range(verses_count):
        verse_count = (verse_count % 4) + 1
        if (verse_count == 1 or verse_count == 3):
          expected_syllables_count = 8
        if (verse_count == 2 or verse_count == 4):
          expected_syllables_count = 6
        
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

      if not failed:
        viable_structures.append(["ballad", verses])

    return viable_structures

  @staticmethod
  def get_syllables_count(tokenized_text):
    """Returns an array of with the same order of tokenized_text with each element being the word count"""
    return [*map(lambda word: pr.syllable_count(pr.phones_for_word(word)[0]), tokenized_text)]

  @staticmethod
  def get_stresses(word):
    stresses = set()

    for syllables in pr.stresses_for_word(word):
      # Identify type 2 stresses with type 1
      syllables = syllables.translate(two_to_one_stress)
      # Number of syllables of the word
      syllables_length = len(syllables)
      # Trick from (Ghazvininejad et al., 2016)
      if syllables_length > 2 and syllables[-3:] == '100':
          syllables = '%s%s' % (syllables[:-1], '1')
      stresses.add(syllables)

    return stresses

  @classmethod
  def get_pattern(cls, tokenized_text):
    text_pattern = {}

    for word in tokenized_text:
      word_pattern = []
      for stress_pattern in cls.get_stresses(word):
        word_pattern.append(stress_pattern)

      text_pattern[word] = word_pattern

    return text_pattern

  @classmethod
  def is_iambic_pentameter(cls, tokenized_text, pattern='01010101010', allow_feminine_rhyme=True):
    """Detects whether tokenized_text matches the iambic pentameter stress pattern"""

    # Iterate over words
    for word in tokenized_text:
        # Remaining syllables
        remaining_syllables = len(pattern)
        # Start looping over possible stress patterns of current word
        found_pattern = False
        for stress_pattern in cls.get_stresses(word):
          pattern_length = len(stress_pattern)
          # check whether the stress patterns match
          if pattern_length <= remaining_syllables and pattern[0:pattern_length] == stress_pattern:
            # if yes, reduce the target pattern and get to next word
            pattern = pattern[pattern_length:]
            found_pattern = True
            break
        # If no matching stress pattern was found for this word, return false
        if not found_pattern:
            return False
    # If there are more syllables remaining (not counting the feminine rhyme)
    if len(pattern) > 1 or (not allow_feminine_rhyme and len(pattern) == 1):
        return False
    # Return the iambic pentameter
    return tokenized_text