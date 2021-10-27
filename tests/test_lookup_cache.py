import time
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from multiprocessing import Manager
from multiprocessing.managers import SyncManager
from typing import List, cast

from sentence2pronunciation.lookup_cache import (
    get_empty_cache, lookup_in_cache_and_add_if_missing,
    lookup_in_cache_and_add_if_missing_mp, pronunciation_upper)


def get_pron(x, l: List) -> str:
  l.append(x)
  time.sleep(0.5)
  return x


def test_lookup_with_cache_mp__is_thread_safe():
  unique_words = ["test1", "test2"]
  words = unique_words * 6

  with Manager() as manager:
    manager = cast(SyncManager, manager)

    cache = manager.dict()
    check_list = manager.list()
    lock = manager.RLock()

    get_pr = partial(get_pron, l=check_list)
    method = partial(lookup_in_cache_and_add_if_missing_mp,
                     ignore_case=False,
                     get_pronunciation=get_pr,
                     cache=cache,
                     lock=lock,
                     )

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=2) as ex:
      method = partial(
        method,
          cache=cache,
          lock=lock,
      )
      res = list(ex.map(method, words, chunksize=3))
    end = time.perf_counter()
    duration = end - start
    assert len(check_list) == 2
    assert duration < 1.1
    assert sorted(res) == sorted(words)


def test_pronunciation_upper():
  result = pronunciation_upper(tuple("abAB"))
  assert result == ("A", "B", "A", "B")


def test_lookup_with_cache():
  result = lookup_in_cache_and_add_if_missing(
    word=tuple("a"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=True,
    cache=get_empty_cache(),
  )

  assert result == ("aa",)


def test_lookup_with_cache__ignore_case():
  cache = get_empty_cache()
  result1 = lookup_in_cache_and_add_if_missing(
    word=tuple("a"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=True,
    cache=cache,
  )

  result2 = lookup_in_cache_and_add_if_missing(
    word=tuple("A"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=True,
    cache=cache,
  )

  assert result1 == ("aa",)
  assert result2 == ("aa",)


def test_lookup_with_cache__dont_ignore_case():
  cache = get_empty_cache()
  result1 = lookup_in_cache_and_add_if_missing(
    word=tuple("a"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=False,
    cache=cache,
  )

  result2 = lookup_in_cache_and_add_if_missing(
    word=tuple("A"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=False,
    cache=cache,
  )

  assert result1 == ("aa",)
  assert result2 == ("AA",)


def test_get_empty_cache__returns_empty_dictionary():
  cache = get_empty_cache()
  assert cache == dict()
