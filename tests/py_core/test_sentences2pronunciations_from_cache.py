from ordered_set import OrderedSet
from sentence2pronunciation.core import sentences2pronunciations_from_cache


def test_component():
  cache = {
    ('/', 'a', 'n', 'o', 't', 'h', 'e', 'r', '/'): ('another',),
    ('I', 'S'): ('I', 'S', 'X'),
    ('I', 'S', '-', 'A', ','): ('I', 'S', 'X', '-', 'A', 'X', ','),
    ('T', 'E', 'S', 'T', '.'): ('T', 'E', 'S', 'T', 'X', '.'),
    ('T', 'H', 'I', 'S'): ('T', 'H', 'I', 'S', 'X')
  }

  sentences = [
    tuple("This is-a, test."),
    tuple("This is /another/ Test."),
  ]

  result = list(sentences2pronunciations_from_cache(
    sentences=OrderedSet(sentences),
    annotation_split_symbol="/",
    consider_annotation=True,
    ignore_case=True,
    cache=cache,
  ))

  assert len(result) == 2
  assert result[0] == ('T', 'H', 'I', 'S', 'X', ' ', 'I', 'S', 'X', '-',
                       'A', 'X', ',', ' ', 'T', 'E', 'S', 'T', 'X', '.')
  assert result[1] == ('T', 'H', 'I', 'S', 'X', ' ', 'I', 'S', 'X', ' ',
                       'another', ' ', 'T', 'E', 'S', 'T', 'X', '.')
