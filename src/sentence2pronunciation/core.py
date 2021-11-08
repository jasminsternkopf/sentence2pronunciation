from functools import partial
from typing import Callable, Iterable, List, Optional, Set, Tuple

from sentence2pronunciation.lookup_cache import (
    LookupCache, lookup_in_cache, lookup_in_cache_and_add_if_missing,
    pronunciation_upper)
from sentence2pronunciation.types import Pronunciation, Symbol

HYPHEN = "-"


def add_to_words_method(x: Pronunciation, words: Set[Pronunciation], ignore_case: bool):
  word = x
  if ignore_case:
    word = pronunciation_upper(word)
  words.add(word)
  return word


def get_non_annotated_words(sentence: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, consider_annotation: bool, annotation_split_symbol: Optional[Symbol], ignore_case: bool) -> Set[Pronunciation]:
  words: Set[Pronunciation] = set()
  get_pronunciation_proxy = partial(add_to_words_method, words=words, ignore_case=ignore_case)
  sentence2pronunciation(
    sentence=sentence,
    trim_symbols=trim_symbols,
    split_on_hyphen=split_on_hyphen,
    consider_annotation=consider_annotation,
    annotation_split_symbol=annotation_split_symbol,
    get_pronunciation=get_pronunciation_proxy,
  )
  return words


def sentence2pronunciation_from_cache(sentence: Pronunciation, consider_annotation: bool, annotation_split_symbol: Optional[Symbol], ignore_case: bool, cache: LookupCache) -> Pronunciation:
  words = split_pronunciation_on_symbol(sentence, " ")
  pronunciations = []
  for word in words:
    if ignore_case:
      if consider_annotation and is_annotation(word, annotation_split_symbol):
        pass
      else:
        word = pronunciation_upper(word)
    word_pron = lookup_in_cache(word, cache)
    pronunciations.append(word_pron)
  complete_pronunciation = symbols_join(pronunciations, " ")
  return complete_pronunciation


def sentence2pronunciation_cached(sentence: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol], ignore_case_in_cache: bool, cache: LookupCache) -> Pronunciation:
  method = partial(lookup_in_cache_and_add_if_missing, get_pronunciation=get_pronunciation,
                   ignore_case=ignore_case_in_cache, cache=cache)
  result = sentence2pronunciation(
    sentence=sentence,
    annotation_split_symbol=annotation_split_symbol,
    consider_annotation=consider_annotation,
    get_pronunciation=method,
    split_on_hyphen=split_on_hyphen,
    trim_symbols=trim_symbols,
  )
  return result


def sentence2pronunciation(sentence: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Pronunciation:
  assert isinstance(sentence, tuple)
  if consider_annotation and len(annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  words = split_pronunciation_on_symbol(sentence, " ")
  pronunciations = [word2pronunciation(
      word, trim_symbols, split_on_hyphen, get_pronunciation, consider_annotation, annotation_split_symbol) for word in words]
  complete_pronunciation = symbols_join(pronunciations, " ")
  return complete_pronunciation


def symbols_join(list_of_pronunciations: List[Pronunciation], join_symbol: Symbol) -> None:
  res = []
  for i, word in enumerate(list_of_pronunciations):
    res.extend(word)
    is_last_word = i == len(list_of_pronunciations) - 1
    if not is_last_word:
      res.append(join_symbol)
  return tuple(res)


def word2pronunciation_cached(word: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol], ignore_case_in_cache: bool, cache: LookupCache) -> Pronunciation:
  method = partial(lookup_in_cache_and_add_if_missing, get_pronunciation=get_pronunciation,
                   ignore_case=ignore_case_in_cache, cache=cache)
  result = word2pronunciation(
    word=word,
    annotation_split_symbol=annotation_split_symbol,
    consider_annotation=consider_annotation,
    get_pronunciation=method,
    split_on_hyphen=split_on_hyphen,
    trim_symbols=trim_symbols,
  )
  return result


def word2pronunciation(word: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Pronunciation:
  if consider_annotation and len(annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  if consider_annotation and is_annotation(word, annotation_split_symbol):
    annotations = annotation2pronunciation(word, annotation_split_symbol)
    return annotations
  new_pronun = not_annotation_word2pronunciation(
    word, trim_symbols, split_on_hyphen, get_pronunciation)
  return new_pronun


def is_annotation(word: Pronunciation, annotation_split_symbol: Symbol) -> bool:
  return word[0] == annotation_split_symbol and word[-1] == annotation_split_symbol


def annotation2pronunciation(annotation: Pronunciation, annotation_split_symbol: Symbol) -> Pronunciation:
  return get_annotation_content(annotation, annotation_split_symbol)
  # assert is_annotation(annotation, annotation_split_symbol)
  # single_annotations = tuple(
  #   [element for element in annotation if element != annotation_split_symbol])
  # return single_annotations


def get_annotation_content(annotation: Pronunciation, annotation_split_symbol: Symbol) -> Pronunciation:
  assert is_annotation(annotation, annotation_split_symbol)
  resulting_parts = []
  current_merge = ""
  for symbol in annotation[1:-1]:
    if symbol == annotation_split_symbol:
      if current_merge != "":
        resulting_parts.append(current_merge)
        current_merge = ""
    else:
      current_merge += symbol
  if current_merge != "":
    resulting_parts.append(current_merge)
  return tuple(resulting_parts)


def not_annotation_word2pronunciation(word: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation]) -> Pronunciation:
  trim_beginning, actual_word, trim_end = trim_word(word, trim_symbols)
  pronunciations = []
  if len(trim_beginning) > 0:
    pronunciations.append(trim_beginning)
  if len(actual_word) > 0:
    actual_pronunciation = add_pronunciation_for_word(
      actual_word, split_on_hyphen, get_pronunciation)
    pronunciations.append(actual_pronunciation)
  if len(trim_end) > 0:
    pronunciations.append(trim_end)
  complete_pronunciation = pronunciation_list_to_pronunciation(pronunciations)
  return complete_pronunciation


def add_pronunciation_for_word(word: Pronunciation, split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation]) -> Pronunciation:
  if split_on_hyphen:
    return add_pronunciation_for_splitted_word(word, get_pronunciation)
  return get_pronunciation(word)


def add_pronunciation_for_splitted_word(word: Pronunciation, get_pronunciation: Callable[[Pronunciation], Pronunciation]) -> Pronunciation:
  splitted_words = split_pronunciation_on_symbol(word, HYPHEN)
  pronunciations = [get_pronunciation(single_word) if single_word != () else ()
                    for single_word in splitted_words]
  pronunciations_with_hyphens = symbols_join(pronunciations, HYPHEN)
  return pronunciations_with_hyphens


def split_pronunciation_on_symbol(word: Pronunciation, split_symbol: Symbol):
  single_word = []
  all_single_words = []
  for element in word:
    if element != split_symbol:
      single_word.append(element)
    else:
      all_single_words.append(tuple(single_word))
      single_word = []
  all_single_words.append(tuple(single_word))
  return all_single_words


def trim_word(word: Pronunciation, trim_symbols: Set[Symbol]) -> Tuple[Pronunciation, Pronunciation, Pronunciation]:
  beginning, remaining_word = remove_trim_symbols_at_beginning(word, trim_symbols)
  actual_word, end = remove_trim_symbols_at_end(remaining_word, trim_symbols)
  return beginning, actual_word, end


def remove_trim_symbols_at_end(word: Pronunciation, trim_symbols: Set[Symbol]) -> Tuple[Pronunciation, Pronunciation]:
  word_reversed = word[::-1]
  end_reversed, remaining_word_reversed = remove_trim_symbols_at_beginning(
    word_reversed, trim_symbols)
  end = end_reversed[::-1]
  remaining_word = remaining_word_reversed[::-1]
  return remaining_word, end


def remove_trim_symbols_at_beginning(word: Pronunciation, trim_symbols: Set[Symbol]) -> Tuple[Pronunciation, Pronunciation]:
  beginning = []
  for element in word:
    if element in trim_symbols:
      beginning.append(element)
    else:
      break
  beginning = tuple(beginning)
  remaining_word = word[len(beginning):]
  return beginning, remaining_word


def pronunciation_list_to_pronunciation(pronunciation_list: List[Pronunciation]) -> Pronunciation:
  for element in pronunciation_list:
    assert isinstance(element, tuple)
  flattened_pronunciation_list = tuple(
    pronunciation for pronunciation_tuple in pronunciation_list for pronunciation in pronunciation_tuple)
  return flattened_pronunciation_list
