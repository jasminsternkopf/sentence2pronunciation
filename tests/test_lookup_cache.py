from sentence2pronunciation.lookup_cache import (clear_cache, get_cache,
                                                 lookup_with_cache,
                                                 pronunciation_upper)


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
