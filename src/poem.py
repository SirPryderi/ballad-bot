class Poem:
  def __init__(self, verses, form=None, form_repetition=1, author=None, syllables_count=None, syllables_total=None):
    self.verses = verses
    self.form = form
    self.form_repetition = form_repetition

    self.rhyme_scheme = None
    self.rhyme_count = None
    self.score = None
    self.verses_count = len([*filter(lambda v: v != "", verses)])

    if author == None:
      self.author = "anonymous"
    else:
      self.author = author

    if syllables_count == None:
      # normally passed in for performance
      # TODO: add a new method to analyze the syllables in a poem
      pass
    else:
      self.syllables_count = syllables_count
      self.syllables_total = syllables_total

  def __str__(self):
    output = []

    for verse in self.verses:
      output.append(" ".join(verse).capitalize())

    # TODO: support things like "two tercets by"

    output.append(f"\n — a {self.form.name} by {self.author}")

    return "\n".join(output)
