import re
from typing import Dict, List, Set, Tuple

Pronun = Tuple[str, ...]
Pronun_Dict = Dict[str, Pronun]


def sentence2pronunciaton(sentence: str, dict: Pronun_Dict, trim_symb: Set[str], split_on_hyphen: bool) -> Pronun:
  pass


def word2pronunciation(word: str, dict: Pronun_Dict, trim_symb: Set[str], split_on_hyphen: bool) -> Pronun:
  trim_beginning, act_word, trim_end = trim_word(word, trim_symb)
  pronuns = [(trim_beginning,)]
  if split_on_hyphen:
    splitted_words = act_word.split("-")
    for index, single_word in enumerate(splitted_words):
      pronuns.append(get_pronun(single_word, dict, "-"))
      if index != len(splitted_words) - 1:
        pronuns.append(("-"))
  else:
    pronuns.append(get_pronun(act_word, dict, "-"))
  pronuns.append((trim_end,))
  complete_pronun = pronunlist_to_pronun(pronuns)
  return complete_pronun  # - einfügen


def trim_word(word: str, trim_symb: Set[str]) -> Tuple[str, str, str]:
  trim_symb_single_str = "".join(str(symb) for symb in trim_symb)
  trim = re.compile(rf"[{trim_symb_single_str}]*")
  beginning = trim.match(word).group(0)
  reverse_word = word[::-1]
  end = trim.match(reverse_word).group(0)
  end = end[::-1]
  if end != "":
    act_word = word[len(beginning):-len(end)]
  else:
    act_word = word[len(beginning):]
  return beginning, act_word, end


def get_pronun(word: str, dict: Pronun_Dict, replace_unknown_with) -> Pronun:
  if word in dict.keys():
    return dict[word]
  return replace_unknown_with * len(word)


def pronunlist_to_pronun(pronunlist: List[Pronun]) -> Pronun:
  for ele in pronunlist:
    assert isinstance(ele, tuple)
  flattened_pronunlist = [pronun for pronuntuple in pronunlist for pronun in pronuntuple]
  return tuple(flattened_pronunlist)
