from typing import Dict, Set, Tuple

Pronun = Tuple[str, ...]
Pronun_Dict = Dict[str, Pronun]


def sentence2pronunciaton(sentence: str, dict: Pronun_Dict, trim_symb: Set[str], split_on_hyphen: bool) -> Pronun:
  pass


def word2pronunciation(word: str, dict: Pronun_Dict, trim_symb: Set[str], split_on_hyphen: bool) -> Pronun:
  pass
