from functools import partial
from logging import getLogger
from multiprocessing import Pool
from typing import Any, Callable, Dict, Optional, Set, Tuple

from ordered_set import OrderedSet
from tqdm import tqdm

from sentence2pronunciation.core import (is_annotation,
                                         sentence2pronunciation_from_cache,
                                         split_pronunciation_on_symbol,
                                         word2pronunciation)
from sentence2pronunciation.lookup_cache import (LookupCache,
                                                 pronunciation_upper)
from sentence2pronunciation.types import Pronunciation, Symbol


def return_input_too(inp: Any, method: Callable[[Any], Any]) -> Tuple[Any, Any]:
  return inp, method(inp)


process_unique_words: Set[Pronunciation] = None


def __init_pool_prepare_cache_mp(words: OrderedSet[Pronunciation]) -> None:
  global process_unique_words
  process_unique_words = words


def __main_prepare_cache_mp(word_index: int, trim_symbols: Set[Symbol], split_on_hyphen: bool, consider_annotation: bool, annotation_split_symbol: Optional[Symbol], get_pronunciation: Callable[[Pronunciation], Pronunciation]) -> None:
  # pylint: disable=global-variable-not-assigned
  global process_unique_words
  word = process_unique_words[word_index]
  pronunciation = word2pronunciation(
    word=word,
    get_pronunciation=get_pronunciation,
    trim_symbols=trim_symbols,
    split_on_hyphen=split_on_hyphen,
    consider_annotation=consider_annotation,
    annotation_split_symbol=annotation_split_symbol,
  )
  return word, pronunciation


def prepare_cache_mp(sentences: Set[Pronunciation], trim_symbols: Set[Symbol], split_on_hyphen: bool, consider_annotation: bool, annotation_split_symbol: Optional[Symbol], get_pronunciation: Callable[[Pronunciation], Pronunciation], ignore_case: bool, n_jobs: int, chunksize: int, maxtasksperchild: Optional[int] = None) -> LookupCache:
  logger = getLogger(__name__)

  logger.info("Getting all words...")
  unique_words = OrderedSet({
    word for sentence in tqdm(sentences)
    for word in split_pronunciation_on_symbol(sentence, " ")
  })
  logger.info("Done.")

  if ignore_case:
    logger.info("Ignoring case...")
    if consider_annotation:
      # Note: annotations will be taken as they are, i.e. no upper case since it is not clear which of the annotation will be taken as value later in the cache (if multiple keys merge to one due to upper case).
      unique_words = OrderedSet({
          word if is_annotation(
              word, annotation_split_symbol) else pronunciation_upper(word)
          for word in tqdm(unique_words)
      })
    else:
      unique_words = OrderedSet({pronunciation_upper(word) for word in tqdm(unique_words)})
    logger.info("Done.")

  logger.info("Getting pronunciations...")
  method_proxy = partial(
    __main_prepare_cache_mp,
    get_pronunciation=get_pronunciation,
    trim_symbols=trim_symbols,
    split_on_hyphen=split_on_hyphen,
    consider_annotation=consider_annotation,
    annotation_split_symbol=annotation_split_symbol,
  )

  with Pool(
    processes=n_jobs,
    initializer=__init_pool_prepare_cache_mp,
    initargs=(unique_words,),
    maxtasksperchild=maxtasksperchild,
  ) as pool:
    pronunciations_to_words: LookupCache = dict(tqdm(
      pool.imap_unordered(method_proxy, range(len(unique_words)), chunksize=chunksize),
      total=len(unique_words),
    ))

  logger.info("Done.")

  return pronunciations_to_words


process_lookup_cache: LookupCache = None
process_sentences: OrderedSet[Pronunciation] = None


def __main_sentences2pronunciations_from_cache_mp(sentence_index: int, ignore_case: bool, consider_annotation: bool, annotation_split_symbol: Optional[Symbol]) -> Tuple[Pronunciation, Pronunciation]:
  # pylint: disable=global-variable-not-assigned
  global process_lookup_cache
  # pylint: disable=global-variable-not-assigned
  global process_sentences

  sentence = process_sentences[sentence_index]
  pronunciation = sentence2pronunciation_from_cache(
    sentence=sentence,
    ignore_case=ignore_case,
    cache=process_lookup_cache,
    consider_annotation=consider_annotation,
    annotation_split_symbol=annotation_split_symbol
  )
  return sentence, pronunciation


def __init_pool_sentences2pronunciations_from_cache_mp(cache: LookupCache, sentences: OrderedSet[Pronunciation]) -> None:
  # pylint: disable=global-variable-not-assigned
  global process_lookup_cache
  # pylint: disable=global-variable-not-assigned
  global process_sentences

  process_lookup_cache = cache
  process_sentences = sentences


def sentences2pronunciations_from_cache_mp(sentences: Set[Pronunciation], ignore_case: bool, consider_annotation: bool, annotation_split_symbol: Optional[Symbol], cache: LookupCache, n_jobs: int, chunksize: int, maxtasksperchild: Optional[int] = None) -> Dict[Pronunciation, Pronunciation]:
  logger = getLogger(__name__)
  method_proxy = partial(
    __main_sentences2pronunciations_from_cache_mp,
    ignore_case=ignore_case,
    consider_annotation=consider_annotation,
    annotation_split_symbol=annotation_split_symbol
  )

  logger.info("Preparing sentences...")
  sentences_with_order = OrderedSet(sentences)
  logger.info("Done.")

  logger.info("Getting pronunciations from preparation...")
  with Pool(
    processes=n_jobs,
    initializer=__init_pool_sentences2pronunciations_from_cache_mp,
    initargs=(cache, sentences_with_order,),
    maxtasksperchild=maxtasksperchild,
  ) as pool:
    pronunciations_to_sentences: Dict[Pronunciation, Pronunciation] = dict(tqdm(
      pool.imap_unordered(method_proxy, range(len(sentences_with_order)), chunksize=chunksize),
      total=len(sentences_with_order),
    ))
  logger.info("Done.")

  return pronunciations_to_sentences
