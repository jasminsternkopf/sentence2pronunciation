from sentence2pronunciation.multiprocessing import (
    prepare_cache_mp, sentences2pronunciations_from_cache_mp)
from sentence2pronunciation.types import Pronunciation


def get_pronunciation_added_X(x: Pronunciation):
  assert isinstance(x, tuple)
  return tuple(list(x) + ["X"])


def test_prepare_cache_mp():
  cache = prepare_cache_mp(
    sentences={
      tuple("This is-a, test."),
      tuple("This is /another/ Test."),
    },
    annotation_split_symbol="/",
    consider_annotation=True,
    get_pronunciation=get_pronunciation_added_X,
    ignore_case=True,
    split_on_hyphen=True,
    trim_symbols={".", ","},
    n_jobs=1,
    chunksize=1,
    maxtasksperchild=1,
  )

  assert len(cache) == 5
  assert cache[tuple("THIS")] == tuple("THISX")
  assert cache[tuple("IS")] == tuple("ISX")
  assert cache[tuple("IS-A,")] == tuple("ISX-AX,")
  assert cache[tuple("TEST.")] == tuple("TESTX.")
  assert cache[tuple("/another/")] == ("another",)


def test_sentences2pronunciations_from_cache_mp():
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

  result = sentences2pronunciations_from_cache_mp(
    sentences=set(sentences),
    annotation_split_symbol="/",
    consider_annotation=True,
    ignore_case=True,
    cache=cache,
    n_jobs=1,
    chunksize=1,
    maxtasksperchild=1,
  )

  assert len(result) == 2
  assert result[sentences[0]] == ('T', 'H', 'I', 'S', 'X', ' ', 'I', 'S', 'X', '-',
                                  'A', 'X', ',', ' ', 'T', 'E', 'S', 'T', 'X', '.')
  assert result[sentences[1]] == ('T', 'H', 'I', 'S', 'X', ' ', 'I', 'S', 'X', ' ',
                                  'another', ' ', 'T', 'E', 'S', 'T', 'X', '.')
