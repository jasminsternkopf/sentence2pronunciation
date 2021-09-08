import string
import pytest
from sentence2pronunciation.core import (add_pronunciation_for_splitted_word,
                                         add_pronunciation_for_word,
                                         annotation2pronunciation,
                                         is_annotation,
                                         not_annotation_word2pronunciation,
                                         pronunciation_list_to_pronunciation,
                                         sentence2pronunciaton, symbols_join,
                                         trim_word, word2pronunciation)

HYPHEN = "-"


def get_pronunciation(x):
  return (x,)

# region pronunciation_list_to_pronunciation


def test_pronunciation_list_to_pronunciation():
  p = [("a",), ("bc", "d"), ("efg",), ("",), ("hi", "")]
  res = pronunciation_list_to_pronunciation(p)

  assert isinstance(res, tuple)
  assert res == ("a", "bc", "d", "efg", "hi")


def test_pronunciation_list_to_pronunciation_empty_list():
  p = []
  res = pronunciation_list_to_pronunciation(p)

  assert isinstance(res, tuple)
  assert res == ()

# endregion


# region trim_word

def test_trim_word_trimsymbs_before_and_after():
  word = "!(hello(!"
  trim_symbols = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == "!("
  assert res_2 == "hello"
  assert res_3 == "(!"


def test_trim_word_trimsymbs_only_before():
  word = "!(hello"
  trim_symbols = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == "!("
  assert res_2 == "hello"
  assert res_3 == ""


def test_trim_word_trimsymbs_only_after():
  word = "hello!"
  trim_symbols = {"!"}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ""
  assert res_2 == "hello"
  assert res_3 == "!"


def test_trim_word_trimsymbs_before_in_between_and_after():
  word = "!(hel!(!lo(!"
  trim_symbols = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == "!("
  assert res_2 == "hel!(!lo"
  assert res_3 == "(!"


def test_trim_word_trimsymbs_only_in_between():
  word = "hel!(!lo"
  trim_symbols = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ""
  assert res_2 == "hel!(!lo"
  assert res_3 == ""


def test_trim_word_trimsymbs_in_between_and_before():
  word = "!(hel!(!lo"
  trim_symbols = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == "!("
  assert res_2 == "hel!(!lo"
  assert res_3 == ""


def test_trim_word_trimsymbs_in_between_and_after():
  word = "hel!(!lo!"
  trim_symbols = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ""
  assert res_2 == "hel!(!lo"
  assert res_3 == "!"


def test_trim_word__trim_symbols_is_empty():
  word = "!(hello(!"
  trim_symbols = {}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ""
  assert res_2 == word
  assert res_3 == ""


def test_trim_word__word_is_empty():
  word = ""
  trim_symbols = {"!"}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ""
  assert res_2 == ""
  assert res_3 == ""


def test_trim_word__trim_symbols_and_word_are_empty():
  word = ""
  trim_symbols = {}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ""
  assert res_2 == ""
  assert res_3 == ""


def test_trim_word__use_stringpunctuation_as_trim_symbols():
  word = "!hello!"
  trim_symbols = set(string.punctuation)
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == "!"
  assert res_2 == "hello"
  assert res_3 == "!"


# endregion

# region add_pronunciation_for_splitted_word


def test_add_pronunciation_for_splitted_word_no_hyphen():
  word = "hello"
  pronuns = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert pronuns == ("hello",)


def test_add_pronunciation_for_splitted_word_one_hyphen():
  word = f"hel{HYPHEN}lo"
  pronuns = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert pronuns == ("hel", HYPHEN, "lo")


def test_aadd_pronunciation_for_splitted_word_two_hyphens():
  word = f"he{HYPHEN}ll{HYPHEN}o"
  pronuns = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert pronuns == ("he", HYPHEN, "ll", HYPHEN, "o")

# endregion

# region add_pronunciation_for_word


def test_add_pronunciation_for_word_one_hyphen__split_on_hyphen_false():
  word = f"hel{HYPHEN}lo"
  split_on_hyphen = False
  pronuns = add_pronunciation_for_word(word, split_on_hyphen, get_pronunciation)

  assert pronuns == (f"hel{HYPHEN}lo",)


def test_add_pronunciation_for_word_one_hyphen__split_on_hyphen_true():
  word = f"hel{HYPHEN}lo"
  split_on_hyphen = True
  pronuns = add_pronunciation_for_word(word, split_on_hyphen, get_pronunciation)

  assert pronuns == ("hel", HYPHEN, "lo")

# endregion

# region not_annotation_word2pronunciation


def test_not_annotation_word2pronunciation__no_hyphen__split_on_hyphen_false():
  word = "!(hello(!"
  trim_symbols = {"!", "("}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!(", "hello", "(!")


def test_not_annotation_word2pronunciation__no_hyphen__split_on_hyphen_true():
  word = "!(hello(!"
  trim_symbols = {"!", "("}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!(", "hello", "(!")


def test_not_annotation_word2pronunciation__one_hyphen__split_on_hyphen_false():
  word = f"!(hel{HYPHEN}lo(!"
  trim_symbols = {"!", "("}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!(", f"hel{HYPHEN}lo", "(!")


def test_not_annotation_word2pronunciation__one_hyphen__split_on_hyphen_true():
  word = f"!(hel{HYPHEN}lo(!"
  trim_symbols = {"!", "("}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!(", "hel", HYPHEN, "lo", "(!")


def test_not_annotation_word2pronunciation__two_hyphen__split_on_hyphen_false_():
  word = f"!(he{HYPHEN}ll{HYPHEN}o(!"
  trim_symbols = {"!", "("}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!(", f"he{HYPHEN}ll{HYPHEN}o", "(!")


def test_not_annotation_word2pronunciation__two_hyphen__split_on_hyphen_true():
  word = f"!(he{HYPHEN}ll{HYPHEN}o(!"
  trim_symbols = {"!", "("}
  split_on_hyphen = True

  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!(", "he", HYPHEN, "ll", HYPHEN, "o", "(!")


def test_not_annotation_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = "hello!"
  trim_symbols = {"!"}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("hello", "!")


def test_not_annotation_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_beginning():
  word = "hello!"
  trim_symbols = {"!"}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("hello", "!")


def test_not_annotation_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = f"hel{HYPHEN}lo!"
  trim_symbols = {"!"}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == (f"hel{HYPHEN}lo", "!")


def test_not_annotation_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_beginning():
  word = f"hel{HYPHEN}lo!"
  trim_symbols = {"!"}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("hel", HYPHEN, "lo", "!")


def test_not_annotation_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_end():
  word = "!hello"
  trim_symbols = {"!"}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!", "hello")


def test_not_annotation_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_end():
  word = "!hello"
  trim_symbols = {"!"}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!", "hello")


def test_not_annotation_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_end():
  word = f"!hel{HYPHEN}lo"
  trim_symbols = {"!"}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!", f"hel{HYPHEN}lo")


def test_not_annotation_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_end():
  word = f"!hel{HYPHEN}lo"
  trim_symbols = {"!"}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("!", "hel", HYPHEN, "lo")


def test_not_annotation_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_beginning_and_end():
  word = "hello"
  trim_symbols = {"!"}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("hello",)


def test_not_annotation_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_beginning_and_end():
  word = "hello"
  trim_symbols = {"!"}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("hello",)


def test_not_annotation_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_beginning_and_end():
  word = f"hel{HYPHEN}lo"
  trim_symbols = {"!"}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == (f"hel{HYPHEN}lo",)


def test_not_annotation_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_beginning_and_end():
  word = f"hel{HYPHEN}lo"
  trim_symbols = {"!"}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ("hel", HYPHEN, "lo")


def test_not_annotation_word2pronunciation__empty_word():
  word = ""
  trim_symbols = {"!"}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == ()


def test_not_annotation_word2pronunciation__hyphen_in_trim_symbolsols_and_split_on_hyphen_true():
  word = f"{HYPHEN}hel{HYPHEN}lo{HYPHEN}"
  trim_symbols = {HYPHEN}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == (HYPHEN, "hel", HYPHEN, "lo", HYPHEN,)


def test_not_annotation_word2pronunciation__hyphen_in_trim_symbolsols_and_split_on_hyphen_false():
  word = f"{HYPHEN}hel{HYPHEN}lo{HYPHEN}"
  trim_symbols = {HYPHEN}
  split_on_hyphen = False
  res = not_annotation_word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation)

  assert res == (HYPHEN, f"hel{HYPHEN}lo", HYPHEN,)

# endregion

# region is_annotation


def test_is_annotation_split_symbol_just_at_beginning_and_end():
  word = "/hello/"
  assert is_annotation(word, "/")


def test_is_annotation_two_split_symbols_at_beginning_and_end():
  word = "//hello//"
  assert is_annotation(word, "/")


def test_is_annotation_split_symbol_also_in_between():
  word = "/hel/lo/"
  assert is_annotation(word, "/")


def test_is_annotation_no_split_symbol_at_end():
  word = "/hello"
  assert not is_annotation(word, "/")


def test_is_annotation_no_split_symbol_at_end_but_in_between():
  word = "/hel/lo"
  assert not is_annotation(word, "/")


def test_is_annotation_no_split_symbol_at_beginning():
  word = "hello/"
  assert not is_annotation(word, "/")


def test_is_annotation_no_split_symbol_at_beginning_but_in_between():
  word = "hel/lo/"
  assert not is_annotation(word, "/")


def test_is_annotation_word_is_only_two_split_symbols():
  word = "//"
  assert is_annotation(word, "/")


def test_is_annotation_two_split_symbols_in_middle_of_word():
  word = "/hel//lo/"
  assert is_annotation(word, "/")


def test_is_annotation_word_is_empty():
  word = ""
  assert not is_annotation(word, "/")

# endregion

# region annotation2pronunciation


def test_annotation2pronunciation():
  annot = "/hello/world/!/"
  res = annotation2pronunciation(annot, "/")

  assert res == ("hello", "world", "!")


def test_annotation2pronunciation_double_annotation_split_symbol_between_annotations():
  annot = "/hello//world/!/"
  res = annotation2pronunciation(annot, "/")

  assert res == ("hello", "world", "!")


def test_annotation2pronunciation_double_annotation_split_symbol_at_beginning():
  annot = "//hello/world/!/"
  res = annotation2pronunciation(annot, "/")

  assert res == ("hello", "world", "!")


def test_annotation2pronunciation_double_annotation_split_symbol_at_end():
  annot = "/hello//world/!//"
  res = annotation2pronunciation(annot, "/")

  assert res == ("hello", "world", "!")


def test_annotation2pronunciation_word_is_only_two_split_symbols():
  annot = "//"
  res = annotation2pronunciation(annot, "/")

  assert res == ()


def test_annotation2pronunciation_two_split_symbols_in_middle_of_word():
  annot = "/hel//lo/"
  res = annotation2pronunciation(annot, "/")

  assert res == ("hel", "lo")

# endregion

# region symbols_join


def test_symbols_join():
  list_of_pronunciations = [("abc",), ("de",), ("f",)]
  join_symbol = HYPHEN
  res = symbols_join(list_of_pronunciations, join_symbol)

  assert res == ("abc", HYPHEN, "de", HYPHEN, "f")

# endregion

# region word2pronunciation


def test_word2pronunciaton__consider_annotation_is_false__word_is_not_annot():
  consider_annotation = False
  word = "hello"
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation,
                           consider_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_word2pronunciaton__consider_annotation_is_false__word_is_annot():
  consider_annotation = False
  word = "/hello/"
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation,
                           consider_annotation, annotation_split_symbol)

  assert res == ("/hello/",)


def test_word2pronunciaton__consider_annotation_is_true__word_is_annot():
  consider_annotation = True
  word = "/hello/"
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation,
                           consider_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_word2pronunciaton__consider_annotation_is_true__word_is_not_annot():
  consider_annotation = True
  word = "hello"
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation,
                           consider_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_word2pronunciaton__consider_annotation_is_true__annotation_split_symbol_has_len_2():
  consider_annotation = True
  word = "/hello/"
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "//"

  with pytest.raises(ValueError):
    word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation,
                       consider_annotation, annotation_split_symbol)


def test_word2pronunciaton__consider_annotation_is_true__annotation_split_symbol_has_len_0():
  consider_annotation = True
  word = "/hello/"
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = ""

  with pytest.raises(ValueError):
    word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation,
                       consider_annotation, annotation_split_symbol)


def test_word2pronunciaton__consider_annotation_is_true__word_is_annot__annotation_split_symbol_is_also_trim_symbolsol():
  consider_annotation = True
  word = "/hello/"
  trim_symbols = {"/"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation,
                           consider_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_word2pronunciaton__consider_annotation_is_true__word_is_annot_and_contains_several_trim_symbolsols__annotation_split_symbol_is_also_trim_symbolsol():
  consider_annotation = True
  word = "/!hello!/"
  trim_symbols = {"/", "!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation,
                           consider_annotation, annotation_split_symbol)

  assert res == ("!hello!",)

# endregion

# region sentence2pronunciation


def test_sentence2pronunciation_single_word():
  sentence = "hello"
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciaton(sentence, trim_symbols, split_on_hyphen,
                              get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_sentence2pronunciation_two_words():
  sentence = "hello world"
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciaton(sentence, trim_symbols, split_on_hyphen,
                              get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello", " ", "world")


def test_sentence2pronunciation_single_annotation():
  sentence = "/hello/"
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciaton(sentence, trim_symbols, split_on_hyphen,
                              get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_sentence2pronunciation_one_word_and_one_annotation():
  sentence = "hello /world/"
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciaton(sentence, trim_symbols, split_on_hyphen,
                              get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello", " ", "world")


def test_sentence2pronunciation__consider_annotation_is_true__annotation_split_symbol_has_len_2():
  sentence = "/hello/"
  consider_annotation = True
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "//"

  with pytest.raises(ValueError):
    sentence2pronunciaton(sentence, trim_symbols, split_on_hyphen,
                          get_pronunciation, consider_annotation, annotation_split_symbol)


def test_sentence2pronunciation__consider_annotation_is_true__annotation_split_symbol_has_len_0():
  sentence = "/hello/"
  consider_annotation = True
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = ""

  with pytest.raises(ValueError):
    sentence2pronunciaton(sentence, trim_symbols, split_on_hyphen,
                          get_pronunciation, consider_annotation, annotation_split_symbol)

# endregion
