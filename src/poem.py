import inflect

p = inflect.engine()


class Poem:
  def __init__(self, verses, form=None, form_repetition=1, author=None, syllables_count=None, syllables_total=None):
    self.verses = verses
    self.form = form
    self.form_repetition = form_repetition

    self.rhyme_scheme = None
    self.rhyme_count = None
    self.score = None
    self.verses_count = len([*filter(lambda v: v != "", verses)])
    self.verses_meter = None

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

    self.title = ' '.join(self.verses[0]).capitalize()

  def formatted_lines(self):
    output = []
    for verse in self.verses:
      output.append(" ".join(verse).capitalize())
    if self.form_repetition == 1:
      number = "a"
      form = self.form.name
    else:
      number = p.number_to_words(self.form_repetition)
      form = p.plural_noun(self.form.name)
    output.append("")
    output.append(f" — {number} {form} by {self.author}")
    return output

  def to_markdown(self):
    return "&#010;  \n".join(self.formatted_lines())

  def __str__(self):
    return "\n".join(self.formatted_lines())
