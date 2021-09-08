from typing import Dict, Optional, Set, Tuple, Union

from sentence2pronunciation.core import Pronunciation


def sentence2pronunciaton_dict(sentence: str, dictionary: Dict[str, Tuple[str, ...]], trim_symbols: Set[str], split_on_hyphen: bool, lookup_oov: Union[str, Tuple[str, ...]], consider_annotation: bool, annotation_split_symbol: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Pronunciation:
  if consider_annotation and len(annotation_split_symbol) != 1:
    raise ValueError("annotation_split_symbol has to be a string of length 1.")
  words = sentence.split(" ")
  for word in words:
    if word in dictionary.keys():
      pronuns


def sentence2pronunciaton_lookup(sentence: str, trim_symbols: Set[str], split_on_hyphen: bool, lookup: Union[str, Tuple[str, ...]], consider_annotations: bool, annotation_split_symbol: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Pronunciation:
  pass
