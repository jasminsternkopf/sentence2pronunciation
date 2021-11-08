import random
import string
from logging import getLogger
from multiprocessing import Pool
from typing import Tuple

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


def random_string_generator(str_size: int, allowed_chars: str):
  return ''.join(random.choice(allowed_chars) for x in range(str_size))


chars = string.ascii_letters + string.punctuation


def get_random_sentence(words_count: int) -> Pronunciation:
  words = []
  for _ in range(words_count):
    words.append(random_string_generator(random.randint(3, 10), chars))
  return tuple(' '.join(words))


def mp_get_random_sentence(i: int) -> Pronunciation:
  return get_random_sentence(random.randint(3, 20))


def test_prepare_cache_mp__stress_test():
  n_jobs = 16
  maxtasksperchild = None
  chunksize = 10000
  utterances_count = 1000000
  # utterances_count = 1000
  random.seed(1234)

  logger = getLogger(__name__)
  logger.info("Generating test sentences...")
  with Pool(processes=n_jobs, maxtasksperchild=maxtasksperchild) as pool:
    sentences = set(pool.map(mp_get_random_sentence,
                             range(utterances_count), chunksize=chunksize))
  logger.info("Done generating")

  cache = prepare_cache_mp(
    sentences=sentences,
    annotation_split_symbol="/",
    consider_annotation=True,
    get_pronunciation=get_pronunciation_added_X,
    ignore_case=True,
    split_on_hyphen=True,
    trim_symbols=set(string.punctuation),
    chunksize=chunksize,
    maxtasksperchild=maxtasksperchild,
    n_jobs=n_jobs,
  )

  assert len(cache) > 0


def get_random_word(i: int) -> Pronunciation:
  return tuple(random_string_generator(random.randint(3, 10), chars))


def test_sentences2pronunciations_from_cache_mp__stress_test():
  n_jobs = 16
  maxtasksperchild = None
  chunksize = 10000
  utterances_count = 1000000
  # utterances_count = 1000
  random.seed(1234)

  logger = getLogger(__name__)
  logger.info("Generating test words...")
  with Pool(processes=n_jobs, maxtasksperchild=maxtasksperchild) as pool:
    words = set(pool.map(get_random_word,
                         range(utterances_count), chunksize=chunksize))
  logger.info("Done generating")

  cache = {word: word for word in words}
  sentences = set(words)

  result = sentences2pronunciations_from_cache_mp(
    sentences=sentences,
    annotation_split_symbol="/",
    consider_annotation=True,
    ignore_case=False,
    cache=cache,
    n_jobs=n_jobs,
    chunksize=chunksize,
    maxtasksperchild=maxtasksperchild,
  )

  assert len(result) > 0
