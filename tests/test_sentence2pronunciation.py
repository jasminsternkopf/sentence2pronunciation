import pytest
from sentence2pronunciation.sentence2pronunciation import (
    add_pronun_for_word, annotation2pronunciation, is_annotation,
    not_annot_word2pronunciation, pronunlist_to_pronun, trim_word,
    word2pronunciation)

HYPHEN = "-"


def get_pronun(x):
  return (x,)

# region pronunlist_to_pronun


def test_pronunlist_to_pronun():
  p = [("a",), ("bc", "d"), ("efg",), ("",), ("hi", "")]
  res = pronunlist_to_pronun(p)

  assert isinstance(res, tuple)
  assert res == ("a", "bc", "d", "efg", "hi")


def test_pronunlist_to_pronun_empty_list():
  p = []
  res = pronunlist_to_pronun(p)

  assert isinstance(res, tuple)
  assert res == ()

# endregion


# region trim_word

def test_trim_word_trimsymbs_before_and_after():
  word = "!(hello(!"
  trim_symb = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == "!("
  assert res_2 == "hello"
  assert res_3 == "(!"


def test_trim_word_trimsymbs_only_before():
  word = "!(hello"
  trim_symb = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == "!("
  assert res_2 == "hello"
  assert res_3 == ""


def test_trim_word_trimsymbs_only_after():
  word = "hello!"
  trim_symb = {"!"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == "hello"
  assert res_3 == "!"


def test_trim_word_trimsymbs_before_in_between_and_after():
  word = "!(hel!(!lo(!"
  trim_symb = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == "!("
  assert res_2 == "hel!(!lo"
  assert res_3 == "(!"


def test_trim_word_trimsymbs_only_in_between():
  word = "hel!(!lo"
  trim_symb = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == "hel!(!lo"
  assert res_3 == ""


def test_trim_word_trimsymbs_in_between_and_before():
  word = "!(hel!(!lo"
  trim_symb = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == "!("
  assert res_2 == "hel!(!lo"
  assert res_3 == ""


def test_trim_word_trimsymbs_in_between_and_after():
  word = "hel!(!lo!"
  trim_symb = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == "hel!(!lo"
  assert res_3 == "!"


def test_trim_word__trim_symb_is_empty():
  word = "!(hello(!"
  trim_symb = {}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == word
  assert res_3 == ""


def test_trim_word__word_is_empty():
  word = ""
  trim_symb = {"!"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == ""
  assert res_3 == ""


def test_trim_word__trim_symb_and_word_are_empty():
  word = ""
  trim_symb = {}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == ""
  assert res_3 == ""

# endregion

# region add_pronun_for_word


def test_add_pronun_for_word_no_hyphen__split_on_hyphen_false():
  word = "hello"
  split_on_hyphen = False
  pronuns = add_pronun_for_word(word, split_on_hyphen, get_pronun)

  assert pronuns == ("hello",)


def xtest_add_pronun_for_word_no_hyphen__split_on_hyphen_true():
  word = "hello"
  split_on_hyphen = True
  pronuns = add_pronun_for_word(word, split_on_hyphen, get_pronun)

  assert pronuns == [("hello",)]


def xtest_add_pronun_for_word_one_hyphen__split_on_hyphen_false():
  word = f"hel{HYPHEN}lo"
  split_on_hyphen = False
  pronuns = add_pronun_for_word(word, split_on_hyphen, get_pronun)

  assert pronuns == [(f"hel{HYPHEN}lo",)]


def xtest_add_pronun_for_word_one_hyphen__split_on_hyphen_true():
  word = f"hel{HYPHEN}lo"
  split_on_hyphen = True
  pronuns = add_pronun_for_word(word, split_on_hyphen, get_pronun)

  assert pronuns == [("hel",), (HYPHEN,), ("lo",)]


def xtest_add_pronun_for_word_two_hyphens__split_on_hyphen_true():
  word = f"he{HYPHEN}ll{HYPHEN}o"
  split_on_hyphen = True
  pronuns = add_pronun_for_word(word, split_on_hyphen, get_pronun)

  assert pronuns == [("he",), (HYPHEN,), ("ll",), (HYPHEN,), ("o",)]

  # endregion

# region not_annot_word2pronunciation


def test_not_annot_word2pronunciation__no_hyphen__split_on_hyphen_false():
  word = "!(hello(!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hello", "(!")


def test_not_annot_word2pronunciation__no_hyphen__split_on_hyphen_true():
  word = "!(hello(!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hello", "(!")


def test_not_annot_word2pronunciation__one_hyphen__split_on_hyphen_false():
  word = f"!(hel{HYPHEN}lo(!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", f"hel{HYPHEN}lo", "(!")


def test_not_annot_word2pronunciation__one_hyphen__split_on_hyphen_true():
  word = f"!(hel{HYPHEN}lo(!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hel", HYPHEN, "lo", "(!")


def test_not_annot_word2pronunciation__two_hyphen__split_on_hyphen_false_():
  word = f"!(he{HYPHEN}ll{HYPHEN}o(!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", f"he{HYPHEN}ll{HYPHEN}o", "(!")


def test_not_annot_word2pronunciation__two_hyphen__split_on_hyphen_true():
  word = f"!(he{HYPHEN}ll{HYPHEN}o(!"
  trim_symb = {"!", "("}
  split_on_hyphen = True

  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "he", HYPHEN, "ll", HYPHEN, "o", "(!")


def test_not_annot_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = "hello!"
  trim_symb = {"!"}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hello", "!")


def test_not_annot_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_beginning():
  word = "hello!"
  trim_symb = {"!"}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hello", "!")


def test_not_annot_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = f"hel{HYPHEN}lo!"
  trim_symb = {"!"}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == (f"hel{HYPHEN}lo", "!")


def test_not_annot_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_beginning():
  word = f"hel{HYPHEN}lo!"
  trim_symb = {"!"}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hel", HYPHEN, "lo", "!")


def test_not_annot_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_end():
  word = "!hello"
  trim_symb = {"!"}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!", "hello")


def test_not_annot_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_end():
  word = "!hello"
  trim_symb = {"!"}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!", "hello")


def test_not_annot_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_end():
  word = f"!hel{HYPHEN}lo"
  trim_symb = {"!"}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!", f"hel{HYPHEN}lo")


def test_not_annot_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_end():
  word = f"!hel{HYPHEN}lo"
  trim_symb = {"!"}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!", "hel", HYPHEN, "lo")


def test_not_annot_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_beginning_and_end():
  word = "hello"
  trim_symb = {"!"}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hello",)


def test_not_annot_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_beginning_and_end():
  word = "hello"
  trim_symb = {"!"}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hello",)


def test_not_annot_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_beginning_and_end():
  word = f"hel{HYPHEN}lo"
  trim_symb = {"!"}
  split_on_hyphen = False
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == (f"hel{HYPHEN}lo",)


def test_not_annot_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_beginning_and_end():
  word = f"hel{HYPHEN}lo"
  trim_symb = {"!"}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hel", HYPHEN, "lo")


def test_not_annot_word2pronunciation__empty_word():
  word = ""
  trim_symb = {"!"}
  split_on_hyphen = True
  res = not_annot_word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ()

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

# region word2pronunciation


def test_word2pronunciaton__cons_annotation_is_false__word_is_not_annot():
  cons_annotation = False
  word = "hello"
  trim_symb = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun,
                           cons_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_word2pronunciaton__cons_annotation_is_false__word_is_annot():
  cons_annotation = False
  word = "/hello/"
  trim_symb = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun,
                           cons_annotation, annotation_split_symbol)

  assert res == ("/hello/",)


def test_word2pronunciaton__cons_annotation_is_true__word_is_annot():
  cons_annotation = True
  word = "/hello/"
  trim_symb = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun,
                           cons_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_word2pronunciaton__cons_annotation_is_true__word_is_not_annot():
  cons_annotation = True
  word = "hello"
  trim_symb = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun,
                           cons_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_word2pronunciaton__cons_annotation_is_true__annotation_split_symbol_has_len_2():
  cons_annotation = True
  word = "/hello/"
  trim_symb = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "//"

  with pytest.raises(ValueError):
    word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun,
                       cons_annotation, annotation_split_symbol)


def test_word2pronunciaton__cons_annotation_is_true__annotation_split_symbol_has_len_0():
  cons_annotation = True
  word = "/hello/"
  trim_symb = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = ""

  with pytest.raises(ValueError):
    word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun,
                       cons_annotation, annotation_split_symbol)


def test_word2pronunciaton__cons_annotation_is_true__word_is_annot__annotation_split_symbol_is_also_trim_symbol():
  cons_annotation = True
  word = "/hello/"
  trim_symb = {"/"}
  split_on_hyphen = False
  annotation_split_symbol = "/"

  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun,
                           cons_annotation, annotation_split_symbol)

  assert res == ("hello",)

# endregion

# region sentence2pronunciation


def test_sentence2pronunciation():
