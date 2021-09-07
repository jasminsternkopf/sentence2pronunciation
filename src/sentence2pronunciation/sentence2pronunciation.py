import re
from typing import Callable, Dict, List, Optional, Set, Tuple

Symbol = str
Pronunciation = Tuple[Symbol, ...]
#Pronunciation_Dict = Dict[str, Pronunciation]
HYPHEN = "-"


def sentence2pronunciaton(sentence: str, trim_symb: Set[Symbol], split_on_hyphen: bool, get_pronun: Callable[[str], Pronunciation], cons_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Pronunciation:
  if cons_annotation and len(annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  words = sentence.split(" ")
  pronuns = [word2pronunciation(
      word, trim_symb, split_on_hyphen, get_pronun, cons_annotation, annotation_split_symbol) for word in words]
  complete_pronun = symbols_join(pronuns, " ")
  return complete_pronun


def symbols_join(list_of_symbols: List[Pronunciation], join_symbol: Symbol) -> None:
  res = []
  for i, word in enumerate(list_of_symbols):
    res.extend(word)
    is_last_word = i == len(list_of_symbols) - 1
    if not is_last_word:
      res.append(join_symbol)
  return tuple(res)


def word2pronunciation(word: str, trim_symb: Set[Symbol], split_on_hyphen: bool, get_pronun: Callable[[str], Pronunciation], cons_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Pronunciation:
  if cons_annotation and len(annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  if cons_annotation and is_annotation(word, annotation_split_symbol):
    annotations = annotation2pronunciation(word, annotation_split_symbol)
    return annotations
  new_pronun = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)
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


def not_annot_word2pronunciation(word: str, trim_symb: Set[Symbol], split_on_hyphen: bool, get_pronun: Callable[[str], Pronunciation]) -> Pronunciation:
  trim_beginning, act_word, trim_end = trim_word(word, trim_symb)
  pronuns = [(trim_beginning,)]
  pronuns.append(add_pronun_for_word(act_word, split_on_hyphen, get_pronun))
  pronuns.append((trim_end,))
  complete_pronun = pronunlist_to_pronun(pronuns)
  return complete_pronun


def add_pronun_for_word(word: str, split_on_hyphen: bool, get_pronun: Callable[[str], Pronunciation]) -> Pronunciation:
  if split_on_hyphen:
    return add_pronun_for_splitted_word(word, get_pronun)
  return get_pronun(word)


def add_pronun_for_splitted_word(word: str, get_pronun: Callable[[str], Pronunciation]) -> Pronunciation:
  splitted_words = word.split(HYPHEN)
  pronuns = [get_pronun(single_word) for single_word in splitted_words]
  pronuns_with_hyphens = symbols_join(pronuns, HYPHEN)
  return pronuns_with_hyphens


def trim_word(word: str, trim_symb: Set[Symbol]) -> Tuple[str, str, str]:
  trim_symb_single_str = "".join(str(symb) for symb in trim_symb)
  if len(trim_symb_single_str) == 0:
    return "", word, ""
  trim = re.compile(rf"[{trim_symb_single_str}]*")
  beginning = trim.match(word).group(0)
  reverse_word = word[::-1]
  end = trim.match(reverse_word).group(0)
  end = end[::-1]
  if len(end) > 0:
    act_word = word[len(beginning):-len(end)]
  else:
    act_word = word[len(beginning):]
  return beginning, act_word, end


# def get_pronun(word: str, dict: Pronun_Dict, replace_unknown_with) -> Pronun:
#  if word in dict.keys():
#    return dict[word]
#  return replace_unknown_with * len(word)


def pronunlist_to_pronun(pronunlist: List[Pronunciation]) -> Pronunciation:
  for ele in pronunlist:
    assert isinstance(ele, tuple)
  flattened_pronunlist = tuple(
    pronun for pronuntuple in pronunlist for pronun in pronuntuple if pronun != "")
  return flattened_pronunlist
