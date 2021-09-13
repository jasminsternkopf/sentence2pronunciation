import re
from typing import Callable, Dict, List, Optional, Set, Tuple

Symbol = str
Pronunciation = Tuple[Symbol, ...]
#Pronunciation_Dict = Dict[str, Pronunciation]
HYPHEN = "-"


def sentence2pronunciaton(sentence: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Pronunciation:
  if consider_annotation and len(annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  words = sentence.split(" ")
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


def word2pronunciation(word: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Pronunciation:
  if consider_annotation and len(annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  if consider_annotation and is_annotation(word, annotation_split_symbol):
    annotations = annotation2pronunciation(word, annotation_split_symbol)
    return annotations
  new_pronun = not_annotation_word2pronunciation(
    word, trim_symbols, split_on_hyphen, get_pronunciation)
  return new_pronun  # should work, not tested yet


def is_annotation(word: Pronunciation, annotation_split_symbol: Symbol) -> bool:
  assert len(annotation_split_symbol) == 1
  return word[0] == annotation_split_symbol and word[-1] == annotation_split_symbol  # works


def annotation2pronunciation(annotation: Pronunciation, annotation_split_symbol: Symbol) -> Pronunciation:
  assert is_annotation(annotation, annotation_split_symbol)
  single_annotations = tuple(
    [element for element in annotation if element != annotation_split_symbol])
  return single_annotations  # works


def not_annotation_word2pronunciation(word: Pronunciation, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation]) -> Pronunciation:
  trim_beginning, act_word, trim_end = trim_word(word, trim_symbols)
  pronunciations = [trim_beginning]
  pronunciations.append(add_pronunciation_for_word(act_word, split_on_hyphen, get_pronunciation))
  pronunciations.append(trim_end)
  complete_pronunciation = pronunciation_list_to_pronunciation(pronunciations)
  return complete_pronunciation  # should work, not tested yet

# below is done

def add_pronunciation_for_word(word: Pronunciation, split_on_hyphen: bool, get_pronunciation: Callable[[Pronunciation], Pronunciation]) -> Pronunciation:
  if split_on_hyphen:
    return add_pronunciation_for_splitted_word(word, get_pronunciation)
  return get_pronunciation(word)


def add_pronunciation_for_splitted_word(word: Pronunciation, get_pronunciation: Callable[[Pronunciation], Pronunciation]) -> Pronunciation:
  splitted_words = split_word_on_hyphens(word)
  pronunciations = [get_pronunciation(single_word) for single_word in splitted_words]
  pronunciations_with_hyphens = symbols_join(pronunciations, HYPHEN)
  return pronunciations_with_hyphens


def split_word_on_hyphens(word: Pronunciation):
  single_word = []
  all_single_words = []
  for element in word:
    if element != HYPHEN:
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
    pronunciation for pronunciation_tuple in pronunciation_list for pronunciation in pronunciation_tuple if pronunciation != "")
  return flattened_pronunciation_list
