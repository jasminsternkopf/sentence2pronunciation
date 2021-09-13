import string

import pytest
from sentence2pronunciation.core import (Pronunciation,
                                         add_pronunciation_for_splitted_word,
                                         add_pronunciation_for_word,
                                         annotation2pronunciation,
                                         is_annotation,
                                         not_annotation_word2pronunciation,
                                         pronunciation_list_to_pronunciation,
                                         remove_trim_symbols_at_beginning,
                                         remove_trim_symbols_at_end,
                                         sentence2pronunciaton,
                                         split_word_on_hyphens, symbols_join,
                                         trim_word, word2pronunciation)

HYPHEN = "-"


# def get_pronunciation(x: Pronunciation):
#   y = []
#   for ele in x:
#     y.append(ele+ele)
#   return tuple(y)

def get_pronunciation(x: Pronunciation):
  return x

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


# region add_pronunciation_for_splitted_word


def test_add_pronunciation_for_splitted_word_no_hyphen():
  word = "hello"
  pronunciations = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert pronunciations == ("hello",)


def test_add_pronunciation_for_splitted_word_one_hyphen():
  word = f"hel{HYPHEN}lo"
  pronunciations = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert pronunciations == ("hel", HYPHEN, "lo")


def test_add_pronunciation_for_splitted_word_two_hyphens():
  word = f"he{HYPHEN}ll{HYPHEN}o"
  pronunciations = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert pronunciations == ("he", HYPHEN, "ll", HYPHEN, "o")

# endregion

# region add_pronunciation_for_word


def test_add_pronunciation_for_word_one_hyphen__split_on_hyphen_false():
  word = f"hel{HYPHEN}lo"
  split_on_hyphen = False
  pronunciations = add_pronunciation_for_word(word, split_on_hyphen, get_pronunciation)

  assert pronunciations == (f"hel{HYPHEN}lo",)


def test_add_pronunciation_for_word_one_hyphen__split_on_hyphen_true():
  word = f"hel{HYPHEN}lo"
  split_on_hyphen = True
  pronunciations = add_pronunciation_for_word(word, split_on_hyphen, get_pronunciation)

  assert pronunciations == ("hel", HYPHEN, "lo")

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

# new

# region remove_trim_symbols_at_beginning


def test_remove_trim_symbols_at_beginning():
  word = ("!", "(", "hel", "lo", "(", "!")
  trim_symbols = {"!", "("}
  res_1, res_2 = remove_trim_symbols_at_beginning(word, trim_symbols)

  assert res_1 == ("!", "(")
  assert res_2 == ("hel", "lo", "(", "!")


def test_remove_trim_symbols_at_beginning__first_element_consists_of_trim_symbol_and_not_trim_symbol():
  word = ("!?", "(", "hel", "lo", "(", "!")
  trim_symbols = {"!", "("}
  res_1, res_2 = remove_trim_symbols_at_beginning(word, trim_symbols)

  assert res_1 == ()
  assert res_2 == word


def test_remove_trim_symbols_at_beginning__trim_symbols_empty():
  word = ("!", "(", "hel", "lo", "(", "!")
  trim_symbols = {}
  res_1, res_2 = remove_trim_symbols_at_beginning(word, trim_symbols)

  assert res_1 == ()
  assert res_2 == word


def test_remove_trim_symbols_at_beginning__word_is_empty():
  word = ()
  trim_symbols = {"!", "("}
  res_1, res_2 = remove_trim_symbols_at_beginning(word, trim_symbols)

  assert res_1 == ()
  assert res_2 == ()


def test_remove_trim_symbols_at_beginning__word_and_trim_symbols_are_empty():
  word = ()
  trim_symbols = {}
  res_1, res_2 = remove_trim_symbols_at_beginning(word, trim_symbols)

  assert res_1 == ()
  assert res_2 == ()

# endregion

# region remove_trim_symbols_at_end


def test_remove_trim_symbols_at_end():
  word = ("!", "(", "hel", "lo", "(", "!")
  trim_symbols = {"!", "("}
  res_1, res_2 = remove_trim_symbols_at_end(word, trim_symbols)

  assert res_1 == ("!", "(", "hel", "lo")
  assert res_2 == ("(", "!")


def test_remove_trim_symbols_at_end__word_is_empty():
  word = ()
  trim_symbols = {"!", "("}
  res_1, res_2 = remove_trim_symbols_at_end(word, trim_symbols)

  assert res_1 == ()
  assert res_2 == ()

# endregion

# region trim_word


def test_trim_word():
  word = ("!", "(", "hel", "lo", "(", "!")
  trim_symbols = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ("!", "(")
  assert res_2 == ("hel", "lo")
  assert res_3 == ("(", "!")

# endregion

# region is_annotation


def test_is_annotation__is_annotation():
  word = ("/", "abc", "/", "d", "/")
  res = is_annotation(word, "/")

  assert res


def test_is_annotation__is_not_annotation__first_element_is_annotation_split_symbol_together_with_other_symbol():
  word = ("/a", "abc", "/", "d", "/")
  res = is_annotation(word, "/")

  assert not res


def test_is_annotation__annotation_split_symbol_only_at_beginning():
  word = ("/", "abc", "/", "d")
  res = is_annotation(word, "/")

  assert not res


def test_is_annotation__annotation_split_symbol_only_at_end():
  word = ("abc", "/", "d", "/")
  res = is_annotation(word, "/")

  assert not res

# endregion

# region annotation2pronunciation


def test_annotation2pronunciation():
  annotation = ("/", "abc", "/", "d", "/")
  res = annotation2pronunciation(annotation, "/")

  assert res == ("abc", "d")


def test_annotation2pronunciation__one_element_consists_of_annotation_split_symbol_and_other_symbol():
  annotation = ("/", "abc", "/", "/d", "/")
  res = annotation2pronunciation(annotation, "/")

  assert res == ("abc", "/d")

# endregion

# region split_word_on_hyphens


def test_split_word_on_hyphens():
  word = ("ab", "c", HYPHEN, "d", "e", HYPHEN, "f")
  res = split_word_on_hyphens(word)

  assert res == [("ab", "c"), ("d", "e"), ("f",)]


def test_split_word_on_hyphens_ends_with_hyphen():
  word = ("ab", "c", HYPHEN, "d", "e", HYPHEN, "f", HYPHEN)
  res = split_word_on_hyphens(word)

  assert res == [("ab", "c"), ("d", "e"), ("f",)]

# endregion

# region add_pronunciation_for_splitted_word


def test_add_pronunciation_for_splitted_word():
  word = ("ab", "c", HYPHEN, "d", "e", HYPHEN, "f")
  res = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert res == ("ab", "c", HYPHEN, "d", "e", HYPHEN, "f")

# endregion
