from sentence2pronunciation.sentence2pronunciation import (
    pronunlist_to_pronun, trim_word)

# region pronunlist_to_pronun


def test_pronunlist_to_pronun():
  p = [("a",), ("bc", "d"), ("efg",)]
  res = pronunlist_to_pronun(p)

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
