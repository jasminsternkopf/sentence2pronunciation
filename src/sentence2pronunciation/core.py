import re
from typing import Callable, Dict, List, Optional, Set, Tuple

Symbol = str
Pronunciation = Tuple[Symbol, ...]
#Pronunciation_Dict = Dict[str, Pronunciation]
HYPHEN = "-"


def sentence2pronunciaton(sentence: str, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[str], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Pronunciation:
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


def word2pronunciation(word: str, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[str], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Pronunciation:
  if consider_annotation and len(annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  if consider_annotation and is_annotation(word, annotation_split_symbol):
    annotations = annotation2pronunciation(word, annotation_split_symbol)
    return annotations
  new_pronun = not_annotation_word2pronunciation(
    word, trim_symbols, split_on_hyphen, get_pronunciation)
  return new_pronun


def is_annotation(word: str, annotation_split_symbol: Symbol) -> bool:
  assert len(annotation_split_symbol) == 1
  annot = re.compile(rf"{annotation_split_symbol}[\S]*{annotation_split_symbol}\Z")
  poss_annot = annot.match(word)
  return poss_annot is not None


def annotation2pronunciation(annot: str, annotation_split_symbol: Symbol) -> Pronunciation:
  assert is_annotation(annot, annotation_split_symbol)
  single_annots = re.findall(rf"[^{annotation_split_symbol}]+", annot)
  single_annots = tuple(single_annots)
  return single_annots


def not_annotation_word2pronunciation(word: str, trim_symbols: Set[Symbol], split_on_hyphen: bool, get_pronunciation: Callable[[str], Pronunciation]) -> Pronunciation:
  trim_beginning, act_word, trim_end = trim_word(word, trim_symbols)
  pronunciations = [(trim_beginning,)]
  pronunciations.append(add_pronunciation_for_word(act_word, split_on_hyphen, get_pronunciation))
  pronunciations.append((trim_end,))
  complete_pronunciation = pronunciation_list_to_pronunciation(pronunciations)
  return complete_pronunciation


def add_pronunciation_for_word(word: str, split_on_hyphen: bool, get_pronunciation: Callable[[str], Pronunciation]) -> Pronunciation:
  if split_on_hyphen:
    return add_pronunciation_for_splitted_word(word, get_pronunciation)
  return get_pronunciation(word)


def add_pronunciation_for_splitted_word(word: str, get_pronunciation: Callable[[str], Pronunciation]) -> Pronunciation:
  splitted_words = word.split(HYPHEN)
  pronunciations = [get_pronunciation(single_word) for single_word in splitted_words]
  pronunciations_with_hyphens = symbols_join(pronunciations, HYPHEN)
  return pronunciations_with_hyphens


def trim_word(word: str, trim_symbols: Set[Symbol]) -> Tuple[str, str, str]:
  trim_symbols_single_str = "".join(str(symb) for symb in trim_symbols)
  if len(trim_symbols_single_str) == 0:
    return "", word, ""
  trim_symbols_single_str = re.escape(trim_symbols_single_str)
  trim = re.compile(rf"[{trim_symbols_single_str}]*")
  beginning = trim.match(word).group(0)
  reverse_word = word[::-1]
  end = trim.match(reverse_word).group(0)
  end = end[::-1]
  if len(end) > 0:
    act_word = word[len(beginning):-len(end)]
  else:
    act_word = word[len(beginning):]
  return beginning, act_word, end


def pronunciation_list_to_pronunciation(pronunciation_list: List[Pronunciation]) -> Pronunciation:
  for element in pronunciation_list:
    assert isinstance(element, tuple)
  flattened_pronunciation_list = tuple(
    pronunciation for pronunciation_tuple in pronunciation_list for pronunciation in pronunciation_tuple if pronunciation != "")
  return flattened_pronunciation_list
