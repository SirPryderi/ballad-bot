import pronouncing as pr


class MeterAnalyer:

  METRES_STYLES = {
      'pyrrhic': '00',
      'iambic': '01',
      'trochaic': '10',
      'spondaic': '11',
      'anapestic': '001',
      'dactyl': '100',
      'amphibrachic': '010',
  }

  METRES_NAMES = {
      1: "monometer",
      2: "dimeter",
      3: "trimeter",
      4: "tetrameter",
      5: "pentameter",
      6: "hexameter",
      7: "heptameter",
      8: "octameter"
  }

  @staticmethod
  def get_stresses(word):
    stresses = set()

    for syllables in pr.stresses_for_word(word):
      # Identify type 2 stresses with type 1
      syllables = syllables.translate({ord('2'): u'1'})
      # Number of syllables of the word
      syllables_length = len(syllables)
      # Trick from (Ghazvininejad et al., 2016)
      if syllables_length > 2 and syllables[-3:] == '100':
        syllables = '%s%s' % (syllables[:-1], '1')
      stresses.add(syllables)

    return stresses

  @classmethod
  def get_meter(cls, tokenized_text):
    for meter_style in cls.METRES_STYLES.keys():
      meter = cls.follows_meter_style(tokenized_text, meter_style)
      if meter != False:
        return meter
    return None

  @classmethod
  def get_pattern(cls, tokenized_text):
    # TODO: this is buggy, it doesn't return the right meter at all.
    # Maybe calculate all the permutations, then compute the string distance with one of the meters?
    text_pattern = {}

    for word in tokenized_text:
      word_pattern = []
      for stress_pattern in cls.get_stresses(word):
        word_pattern.append(stress_pattern)

      text_pattern[word] = word_pattern

    return text_pattern

  @classmethod
  def follows_meter_style(cls, tokenized_text, meter_style, allow_feminine_rhyme=True):
    pattern = ""
    foot = cls.METRES_STYLES[meter_style]

    if len(tokenized_text) == 0:
      return False

    # Iterate over words
    for word in tokenized_text:
      # Start looping over possible stress patterns of current word
      found_pattern = False
      for stress_pattern in cls.get_stresses(word):
        new_pattern = cls.repeat_pattern_to_length(foot, len(pattern) + len(stress_pattern))
        # check whether the stress patterns match
        if pattern + stress_pattern == new_pattern:
          pattern = new_pattern
          found_pattern = True
          break
      if not found_pattern:
        return False

    if len(pattern) % len(foot):
      # not enough syllables to complete the foot pattern
      # TODO: support feminine rhymes (at least for iambic pentameter)
      return False

    return cls.get_pattern_name(meter_style, pattern)

  @classmethod
  def get_pattern_name(cls, meter_style, pattern):
    foot = cls.METRES_STYLES[meter_style]
    # retrieves the foot length (tetrameter, pentameter, etc.)
    feet_count = len(pattern) // len(foot)
    # foot style + foot length (e.g. ['iambic', 'pentameter')
    return (meter_style, cls.METRES_NAMES[feet_count])

  @staticmethod
  def repeat_pattern_to_length(s, wanted):
    a, b = divmod(wanted, len(s))
    return s * a + s[:b]
