class Poem:
  def __init__(self, verses, form=None, form_repetition=1, author=None):
    self.verses = verses
    self.form = form
    self.form_repetition = form_repetition

    if author == None:
      self.author = "anonymous"
    else:
      self.author = author

  def __str__(self):
    output = []

    for verse in self.verses:
      output.append(" ".join(verse).capitalize())

    # TODO: support things like "two tercets by"

    output.append(f"\n — a {self.form.name} by {self.author}")

    return "\n".join(output)
