import threading
from multiprocessing.synchronize import RLock
from typing import Callable, Dict, Tuple

from sentence2pronunciation.types import Pronunciation

LookupCache = Dict[Pronunciation, Pronunciation]

# CACHE: Dict[Pronunciation, Pronunciation] = None


# def get_cache() -> Dict[Pronunciation, Pronunciation]:
#   # pylint: disable=global-statement
#   global CACHE
#   if CACHE is None:
#     CACHE = {}
#   return CACHE


# def clear_cache():
#   # pylint: disable=global-statement
#   global CACHE
#   if CACHE is not None:
#     CACHE = None


def pronunciation_upper(pronunciation: Pronunciation) -> Pronunciation:
  result = tuple(symbol.upper() for symbol in pronunciation)
  return result


def pronunciation_lower(pronunciation: Pronunciation) -> Pronunciation:
  result = tuple(symbol.lower() for symbol in pronunciation)
  return result


def lookup_in_cache_and_add_if_missing(word: Pronunciation, get_pronunciation: Callable[[Pronunciation], Pronunciation], ignore_case: bool, cache: LookupCache) -> Pronunciation:
  cache_key = pronunciation_upper(word) if ignore_case else word
  if cache_key in cache:
    return lookup_in_cache(cache_key, cache)

  word_pronunciation = get_pronunciation(word)
  cache[cache_key] = word_pronunciation
  return word_pronunciation


def lookup_in_cache_and_add_if_missing_mp(word: Pronunciation, get_pronunciation: Callable[[Pronunciation], Pronunciation], ignore_case: bool, lock: RLock, cache: LookupCache) -> Pronunciation:
  cache_key = pronunciation_upper(word) if ignore_case else word
  pronunciation = None
  with lock:
    print([''.join(key) for key in cache.keys()])
    if cache_key not in cache:
      pronunciation = get_pronunciation(word)
      cache[cache_key] = pronunciation

  pronunciation_was_not_added = pronunciation is None
  if pronunciation_was_not_added:
    pronunciation = lookup_in_cache(cache_key, cache)
  return pronunciation


def get_pronunciation_to_word(word: Pronunciation, get_pronunciation: Callable[[Pronunciation], Pronunciation]) -> Tuple[Pronunciation, Pronunciation]:
  pronunciation = get_pronunciation(word)
  return word, pronunciation


def lookup_in_cache(word: Pronunciation, cache: LookupCache) -> Pronunciation:
  assert word in cache
  pronunciation = cache[word]
  return pronunciation


def get_empty_cache() -> LookupCache:
  return dict()
