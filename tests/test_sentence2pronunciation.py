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


def test_word2pronunciation__no_hyphen__split_on_hyphen_false__get_pronun_identity_but_as_tuple():
  word = "!?%(hallo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = False
  def get_pronun(x): return (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "hallo", ")#")


def test_word2pronunciation__no_hyphen__split_on_hyphen_false__get_pronun_splits_in_half():
  word = "!?%(hallo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = False
  def get_pronun(x): return (x[:int(len(x) / 2)], x[int(len(x) / 2):]) if len(x) > 1 else (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "ha", "llo", ")#")


def test_word2pronunciation__no_hyphen__split_on_hyphen_true__get_pronun_identity_but_as_tuple():
  word = "!?%(hallo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = True
  def get_pronun(x): return (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "hallo", ")#")


def test_word2pronunciation__no_hyphen__split_on_hyphen_true__get_pronun_splits_in_half():
  word = "!?%(hallo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = True
  def get_pronun(x): return (x[:int(len(x) / 2)], x[int(len(x) / 2):]) if len(x) > 1 else (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "ha", "llo", ")#")


def test_word2pronunciation__one_hyphen__split_on_hyphen_false__get_pronun_identity_but_as_tuple():
  word = "!?%(hal-lo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = False
  def get_pronun(x): return (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "hal-lo", ")#")


def test_word2pronunciation__one_hyphen__split_on_hyphen_false__get_pronun_splits_in_half():
  word = "!?%(hal-lo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = False
  def get_pronun(x): return (x[:int(len(x) / 2)], x[int(len(x) / 2):]) if len(x) > 1 else (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "hal", "-lo", ")#")


def test_word2pronunciation__one_hyphen__split_on_hyphen_true__get_pronun_identity_but_as_tuple():
  word = "!?%(hal-lo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = True
  def get_pronun(x): return (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "hal", "-", "lo", ")#")


def test_word2pronunciation__one_hyphen__split_on_hyphen_true__get_pronun_splits_in_half():
  word = "!?%(hal-lo)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = True
  def get_pronun(x): return (x[:int(len(x) / 2)], x[int(len(x) / 2):]) if len(x) > 1 else (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "h", "al", "-", "l", "o", ")#")


def test_word2pronunciation__two_hyphen__split_on_hyphen_false__get_pronun_identity_but_as_tuple():
  word = "!?%(ha-ll-o)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = False
  def get_pronun(x): return (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "ha-ll-o", ")#")


def test_word2pronunciation__two_hyphen__split_on_hyphen_false__get_pronun_splits_in_half():
  word = "!?%(ha-ll-o)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = False
  def get_pronun(x): return (x[:int(len(x) / 2)], x[int(len(x) / 2):]) if len(x) > 1 else (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "ha-", "ll-o", ")#")


def test_word2pronunciation__two_hyphen__split_on_hyphen_true__get_pronun_identity_but_as_tuple():
  word = "!?%(ha-ll-o)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = True
  def get_pronun(x): return (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "ha", "-", "ll", "-", "o", ")#")


def test_word2pronunciation__two_hyphen__split_on_hyphen_true__get_pronun_splits_in_half():
  word = "!?%(ha-ll-o)#"
  trim_symb = {"!", "?", "(", ")", "#", "%"}
  split_on_hyphen = True
  def get_pronun(x): return (x[:int(len(x) / 2)], x[int(len(x) / 2):]) if len(x) > 1 else (x,)
  res = word2pronunciation(word, trim_symb, split_on_hyphen, get_pronun)

  assert res == ("!?%(", "h", "a", "-", "l", "l", "-", "o", ")#")
