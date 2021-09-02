from sentence2pronunciation.sentence2pronunciation import (
    annotation2pronunciation, is_annotation, pronunlist_to_pronun, trim_word, word2pronunciation)

# region pronunlist_to_pronun


def test_pronunlist_to_pronun():
  p = [("a",), ("bc", "d"), ("efg",)]
  res = pronunlist_to_pronun(p)

  assert isinstance(res, tuple)
  assert res == ("a", "bc", "d", "efg")


# endregion


# region trim_word

def test_trim_word_trimsymbs_before_and_after():
  word = "!?%(hallo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == "!?%("
  assert res_2 == "hallo"
  assert res_3 == ")#"


def test_trim_word_trimsymbs_only_before():
  word = "!?%(hallo"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == "!?%("
  assert res_2 == "hallo"
  assert res_3 == ""


def test_trim_word_trimsymbs_only_after():
  word = "hallo!?%("
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == "hallo"
  assert res_3 == "!?%("


def test_trim_word_trimsymbs_before_in_between_and_after():
  word = "!?%(hal=?!lo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == "!?%("
  assert res_2 == "hal=?!lo"
  assert res_3 == ")#"


def test_trim_word_trimsymbs_only_in_between():
  word = "hal=?!lo"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == "hal=?!lo"
  assert res_3 == ""


def test_trim_word_trimsymbs_in_between_and_before():
  word = "!?%(hal=?!lo"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == "!?%("
  assert res_2 == "hal=?!lo"
  assert res_3 == ""


def test_trim_word_trimsymbs_in_between_and_after():
  word = "hal=?!lo!?%("
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  res_1, res_2, res_3 = trim_word(word, trim_symb)

  assert res_1 == ""
  assert res_2 == "hal=?!lo"
  assert res_3 == "!?%("

# endregion

# region word2pronunciation


HYPHEN = "-"


def get_pronun(x):
  return (x,)


def test_word2pronunciation__no_hyphen__split_on_hyphen_false():
  word = "!(hello!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hello", "!")


def test_word2pronunciation__no_hyphen__split_on_hyphen_true():
  word = "!(hello!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hello", "!")


def test_word2pronunciation__one_hyphen__split_on_hyphen_false():
  word = "!(hel-lo!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hel-lo", "!")


def test_word2pronunciation__one_hyphen__split_on_hyphen_true():
  word = "!(hel-lo!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hel", HYPHEN, "lo", "!")


def test_word2pronunciation__two_hyphen__split_on_hyphen_false_():
  word = "!(he-ll-o!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "he-ll-o", "!")


def test_word2pronunciation__two_hyphen__split_on_hyphen_true():
  word = "!(he-ll-o!"
  trim_symb = {"!", "("}
  split_on_hyphen = True

  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "he", HYPHEN, "ll", HYPHEN, "o", "!")


def test_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = "hello!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hello", "!")


def test_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_beginning():
  word = "hello!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hello", "!")


def test_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = "hel-lo!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hel-lo", "!")


def test_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_beginning():
  word = "hel-lo!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hel", HYPHEN, "lo", "!")


def test_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_end():
  word = "!hello"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!", "hello")


def test_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_end():
  word = "!hello"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!", "hello")


def test_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_end():
  word = "!hel-lo"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!", "hel-lo")


def test_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_end():
  word = "!hel-lo"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!", "hel", HYPHEN, "lo")


def test_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_beginning_and_end():
  word = "hello"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hello",)


def test_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_beginning_and_end():
  word = "hello"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hello",)


def test_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_beginning_and_end():
  word = "hel-lo"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hel-lo",)


def test_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_beginning_and_end():
  word = "hel-lo"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hel", HYPHEN, "lo")

# endregion

# region add_pronun_for_word

# def test_add_pronun_for_word__

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

# endregion

# region