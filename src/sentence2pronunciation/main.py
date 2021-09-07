from typing import Set, Tuple, Optional, Union, Dict
from sentence2pronunciation.core import Pronunciation

def get_sentence2pronunciaton(sentence: str, dictionary: Dict[str, Tuple[str, ...]], trim_symb: Set[str], split_on_hyphen: bool, lookup_oov: Union[str, Tuple[str, ...]], consider_annotations: bool, annotation_indicator: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Pronunciation:
  pass


def get_sentence2pronunciaton2(sentence: str, trim_symb: Set[str], split_on_hyphen: bool, lookup: Union[str, Tuple[str, ...]], consider_annotations: bool, annotation_indicator: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Pronunciation:
  pass