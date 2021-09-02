from sentence2pronunciation.sentence2pronunciation import (
    pronunlist_to_pronun, trim_word, word2pronunciation)

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
  word = "!(hallo!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hallo", "!")


def test_word2pronunciation__no_hyphen__split_on_hyphen_true():
  word = "!(hallo!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hallo", "!")


def test_word2pronunciation__one_hyphen__split_on_hyphen_false():
  word = "!(hal-lo!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hal-lo", "!")


def test_word2pronunciation__one_hyphen__split_on_hyphen_true():
  word = "!(hal-lo!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "hal", HYPHEN, "lo", "!")

##


def test_word2pronunciation__no_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = "hallo!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hallo", "!")


def test_word2pronunciation__no_hyphen__split_on_hyphen_true__no_trim_at_beginning():
  word = "hallo!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hallo", "!")


def test_word2pronunciation__one_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = "hal-lo!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hal-lo", "!")


def test_word2pronunciation__one_hyphen__split_on_hyphen_true__no_trim_at_beginning():
  word = "hal-lo!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("hal", HYPHEN, "lo", "!")

##


def test_word2pronunciation__two_hyphen__split_on_hyphen_false__no_trim_at_beginning():
  word = "ha-ll-o!"
  trim_symb = {"!", "("}
  split_on_hyphen = False
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "ha-ll-o", "!")


def test_word2pronunciation__two_hyphen__split_on_hyphen_true():
  word = "ha-ll-o!"
  trim_symb = {"!", "("}
  split_on_hyphen = True

  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!(", "ha", HYPHEN, "ll", HYPHEN, "o", "!")


def test_word2pronunciation_no_trim_in_beginning():
  word = "ha-ll-o!"
  trim_symb = {"!", "("}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("h", "a", HYPHEN, "l", "l", HYPHEN, "o", ")#")


def test_word2pronunciation_no_trim_in_end():
  word = "!?%(ha-ll-o"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = True
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("h", "a", HYPHEN, "l", "l", HYPHEN, "o", ")#")