from typing import Set, Tuple, Optional, Union, Dict
from sentence2pronunciation.core import Pronunciation


def sentence2pronunciaton_dict(sentence: str, dictionary: Dict[str, Tuple[str, ...]], trim_symbols: Set[str], split_on_hyphen: bool, lookup_oov: Union[str, Tuple[str, ...]], consider_annotations: bool, annotation_indicator: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Pronunciation:
  pass


def sentence2pronunciaton_lookup(sentence: str, trim_symbols: Set[str], split_on_hyphen: bool, lookup: Union[str, Tuple[str, ...]], consider_annotations: bool, annotation_indicator: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Pronunciation:
  pass
