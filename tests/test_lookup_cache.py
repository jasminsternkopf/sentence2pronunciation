import time
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from multiprocessing import Manager
from multiprocessing.managers import SyncManager
from typing import List, cast

from sentence2pronunciation.lookup_cache import (clear_cache, get_cache,
                                                 lookup_with_cache,
                                                 lookup_with_cache_mp,
                                                 pronunciation_upper)


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
    method = partial(lookup_with_cache_mp,
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
    assert res == words


def test_pronunciation_upper():
  result = pronunciation_upper(tuple("abAB"))
  assert result == ("A", "B", "A", "B")


def test_lookup_with_cache():
  result = lookup_with_cache(
    word=tuple("a"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=True,
  )

  clear_cache()
  assert result == ("aa",)


def test_lookup_with_cache__ignore_case():
  result1 = lookup_with_cache(
    word=tuple("a"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=True,
  )

  result2 = lookup_with_cache(
    word=tuple("A"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=True,
  )

  clear_cache()
  assert result1 == ("aa",)
  assert result2 == ("aa",)


def test_lookup_with_cache__dont_ignore_case():
  result1 = lookup_with_cache(
    word=tuple("a"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=False,
  )

  result2 = lookup_with_cache(
    word=tuple("A"),
    get_pronunciation=lambda pronunciation: tuple([pronunciation[0] + pronunciation[0]]),
    ignore_case=False,
  )

  clear_cache()
  assert result1 == ("aa",)
  assert result2 == ("AA",)


def test_clear_cache__clears_cache():
  cache1 = get_cache()
  cache1[("a",)] = ("b")

  clear_cache()
  cache2 = get_cache()

  clear_cache()
  assert cache2 == {}


def test_clear_cache__clears_cache__with_lookup():
  result1 = lookup_with_cache(
    word=tuple("a"),
    get_pronunciation=lambda _: ("1",),
    ignore_case=False,
  )
  clear_cache()
  result2 = lookup_with_cache(
    word=tuple("a"),
    get_pronunciation=lambda _: ("2",),
    ignore_case=False,
  )

  clear_cache()
  assert result1 == ("1",)
  assert result2 == ("2",)


def test_get_cache__is_not_None():
  cache = get_cache()
  assert cache == {}
