import threading
from multiprocessing.synchronize import RLock
from typing import Callable, Dict

from sentence2pronunciation.types import Pronunciation

CACHE: Dict[Pronunciation, Pronunciation] = None


def get_cache() -> Dict[Pronunciation, Pronunciation]:
  # pylint: disable=global-statement
  global CACHE
  if CACHE is None:
    CACHE = {}
  return CACHE


def clear_cache():
  # pylint: disable=global-statement
  global CACHE
  if CACHE is not None:
    CACHE = None


def pronunciation_upper(pronunciation: Pronunciation) -> Pronunciation:
  result = tuple(symbol.upper() for symbol in pronunciation)
  return result


def pronunciation_lower(pronunciation: Pronunciation) -> Pronunciation:
  result = tuple(symbol.lower() for symbol in pronunciation)
  return result


def lookup_with_cache(word: Pronunciation, get_pronunciation: Callable[[Pronunciation], Pronunciation], ignore_case: bool) -> Pronunciation:
  cache = get_cache()
  cache_key = pronunciation_upper(word) if ignore_case else word
  if cache_key in cache:
    return cache[cache_key]

  word_pronunciation = get_pronunciation(word)
  cache[cache_key] = word_pronunciation
  return word_pronunciation


def lookup_with_cache_mp(word: Pronunciation, get_pronunciation: Callable[[Pronunciation], Pronunciation], ignore_case: bool, lock: RLock, cache: Dict[Pronunciation, Pronunciation]) -> Pronunciation:
  cache_key = pronunciation_upper(word) if ignore_case else word
  pronunciation = None
  with lock:
    print([''.join(key) for key in cache.keys()])
    if cache_key not in cache:
      pronunciation = get_pronunciation(word)
      cache[cache_key] = pronunciation

  pronunciation_was_not_added = pronunciation is None
  if pronunciation_was_not_added:
    pronunciation = cache[cache_key]
  return pronunciation
