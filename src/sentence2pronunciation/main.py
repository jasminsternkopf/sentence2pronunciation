from functools import partial
from typing import Callable, Dict, Optional, Set, Tuple, Union

from sentence2pronunciation.core import Pronunciation, sentence2pronunciaton


def sentence2pronunciaton_dict(sentence: Pronunciation, dictionary: Dict[str, Tuple[str, ...]], trim_symbols: Set[str], split_on_hyphen: bool, lookup_oov: Union[str, Tuple[str, ...]], consider_annotation: bool, annotation_split_symbol: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Pronunciation:
  get_pronunciation = partial(lookup_dict, dictionary=dictionary, replace_unknown_with=lookup_oov)
  pronunciation = sentence2pronunciaton(
    sentence, trim_symbols, split_on_hyphen, get_pronunciation, consider_annotation, annotation_split_symbol)
  return pronunciation


def lookup_dict(word: Pronunciation, dictionary: Dict[str, Tuple[str, ...]], replace_unknown_with: Callable[[str], Tuple[str, ...]]) -> Tuple[str, ...]:
  word_upper = word.upper()
  if word_upper in dictionary:
    return dictionary[word_upper][0]
  return replace_unknown_with(word)


def sentence2pronunciaton_lookup(sentence: Pronunciation, trim_symbols: Set[str], split_on_hyphen: bool, lookup: Union[str, Tuple[str, ...]], consider_annotation: bool, annotation_split_symbol: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Pronunciation:
  pronunciation = sentence2pronunciaton(
    sentence, trim_symbols, split_on_hyphen, lookup, consider_annotation, annotation_split_symbol)
  return pronunciation
