import pytest
from sentence2pronunciation.core import (Pronunciation,
                                         add_pronunciation_for_splitted_word,
                                         add_pronunciation_for_word,
                                         annotation2pronunciation,
                                         get_annotation_content, is_annotation,
                                         not_annotation_word2pronunciation,
                                         pronunciation_list_to_pronunciation,
                                         remove_trim_symbols_at_beginning,
                                         remove_trim_symbols_at_end,
                                         sentence2pronunciation,
                                         split_pronunciation_on_symbol,
                                         symbols_join, trim_word,
                                         word2pronunciation)

HYPHEN = "-"


def get_pronunciation(x: Pronunciation):
  assert isinstance(x, tuple)
  return x


HELLO_DICT = {("hel", HYPHEN, "lo"): ("hel", "hyphen", "lo"), ("hel",): ("hel",),
              ("lo",): ("lo",), ("hel", "lo",): ("hel", "lo"), ("hello", ): ("hello", )}


def get_pronunciation_with_dict(word, dictionary=HELLO_DICT):
  assert word in dictionary.keys()
  return dictionary[word]


def get_pronunciation_with_dict_or_replace(word, dictionary=HELLO_DICT):
  if word in dictionary.keys():
    return dictionary[word]
  return ("*",)

# region get_annotation_content


def test_get_annotation_content__one_symbols__is_taken():
  result = get_annotation_content(
    annotation=("/", "h", "/"),
    annotation_split_symbol="/",
  )

  assert result == ("h",)


def test_get_annotation_content__two_symbols__were_merged():
  result = get_annotation_content(
    annotation=("/", "h", "a", "/"),
    annotation_split_symbol="/",
  )

  assert result == ("ha",)


def test_get_annotation_content__two_symbols_in_one_symbol__were_merged():
  result = get_annotation_content(
    annotation=("/", "ha", "/"),
    annotation_split_symbol="/",
  )

  assert result == ("ha",)


def test_get_annotation_content__two_symbols_separated_by_split__were_not_merged():
  result = get_annotation_content(
    annotation=("/", "h", "/", "a", "/"),
    annotation_split_symbol="/",
  )

  assert result == ("h", "a",)


def test_get_annotation_content__empty_inner_annotation_is_ignored():
  result = get_annotation_content(
    annotation=("/", "/", "a", "/"),
    annotation_split_symbol="/",
  )

  assert result == ("a",)


def test_get_annotation_content__empty_annotation_is_ignored():
  result = get_annotation_content(
    annotation=("/", "/"),
    annotation_split_symbol="/",
  )

  assert result == ()

# endregion

# region symbols_join


def test_symbols_join():
  list_of_pronunciations = [("abc",), ("de",), ("f",)]
  join_symbol = HYPHEN
  res = symbols_join(list_of_pronunciations, join_symbol)

  assert res == ("abc", HYPHEN, "de", HYPHEN, "f")

# endregion

# region pronunciation_list_to_pronunciation


def test_pronunciation_list_to_pronunciation():
  p = [("a",), ("bc", "d"), ("efg",), ("",), ("hi", "")]
  res = pronunciation_list_to_pronunciation(p)

  assert res == ("a", "bc", "d", "efg", "hi")


def test_pronunciation_list_to_pronunciation__empty_list():
  p = []
  res = pronunciation_list_to_pronunciation(p)

  assert isinstance(res, tuple)
  assert res == ()

# endregion

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


def test_trim_word__split_symbol_consists_of_two_symbols():
  word = ("!(", "hel", "lo", "(", "!")
  trim_symbols = {"!("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ("!(",)
  assert res_2 == ("hel", "lo", "(", "!")
  assert res_3 == ()


def test_trim_word__first_element_is_combination_of_two_split_symbols_but_not_split_symbol_itself():
  word = ("!(", "hel", "lo", "(", "!")
  trim_symbols = {"!", "("}
  res_1, res_2, res_3 = trim_word(word, trim_symbols)

  assert res_1 == ()
  assert res_2 == ("!(", "hel", "lo")
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

# region split_pronunciation_on_symbol


def test_split_pronunciation_on_symbol__hyphen_only_in_middle_and_not_double():
  word = ("ab", "c", HYPHEN, "d", "e")
  res = split_pronunciation_on_symbol(word, HYPHEN)

  assert res == [("ab", "c"), ("d", "e")]


def test_split_pronunciation_on_symbol__double_hyphen_in_middle():
  word = ("ab", "c", HYPHEN, HYPHEN, "d", "e")
  res = split_pronunciation_on_symbol(word, HYPHEN)

  assert res == [("ab", "c"), (), ("d", "e")]


def test_split_pronunciation_on_symbol__hyphen_at_beginning():
  word = (HYPHEN, "ab", "c")
  res = split_pronunciation_on_symbol(word, HYPHEN)

  assert res == [(), ("ab", "c")]


def test_split_pronunciation_on_symbol__double_hyphen_at_beginning():
  word = (HYPHEN, HYPHEN, "ab", "c")
  res = split_pronunciation_on_symbol(word, HYPHEN)

  assert res == [(), (), ("ab", "c")]


def test_split_pronunciation_on_symbol__hyphen_at_end():
  word = ("f", HYPHEN,)
  res = split_pronunciation_on_symbol(word, HYPHEN)

  assert res == [("f",), ()]


def test_split_pronunciation_on_symbol__double_hyphen_at_end():
  word = ("f", HYPHEN, HYPHEN,)
  res = split_pronunciation_on_symbol(word, HYPHEN)

  assert res == [("f",), (), ()]

# endregion

# region add_pronunciation_for_splitted_word


def test_add_pronunciation_for_splitted_word__hyphen_only_in_middle_and_not_double():
  word = ("ab", "c", HYPHEN, "d", "e")
  res = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert res == word


def test_add_pronunciation_for_splitted_word__double_hyphen_in_middle():
  word = ("ab", "c", HYPHEN, HYPHEN, "d", "e")
  res = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert res == word


def test_add_pronunciation_for_splitted_word__hyphen_at_beginning():
  word = (HYPHEN, "ab", "c")
  res = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert res == word


def test_add_pronunciation_for_splitted_word__double_hyphen_at_beginning():
  word = (HYPHEN, HYPHEN, "ab", "c")
  res = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert res == word


def test_add_pronunciation_for_splitted_word__hyphen_at_end():
  word = ("f", HYPHEN,)
  res = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert res == word


def test_add_pronunciation_for_splitted_word__double_hyphen_at_end():
  word = ("f", HYPHEN, HYPHEN,)
  res = add_pronunciation_for_splitted_word(word, get_pronunciation)

  assert res == word

# endregion


# region add_pronunciation_for_word

def test_add_pronunciation_for_word__one_hyphen__split_on_hyphen_false():
  word = ("hel", HYPHEN, "lo")
  split_on_hyphen = False
  res = add_pronunciation_for_word(word, split_on_hyphen, get_pronunciation_with_dict)

  assert res == ("hel", "hyphen", "lo")


def test_add_pronunciation_for_word__one_hyphen__split_on_hyphen_true():
  word = ("hel", HYPHEN, "lo")
  split_on_hyphen = True
  res = add_pronunciation_for_word(word, split_on_hyphen, get_pronunciation_with_dict)

  assert res == ("hel", HYPHEN, "lo")

# endregion


# region not_annotation_word2pronunciation


def test_not_annotation_word2pronunciation():
  word = ("!", "(", "hel", "lo", "(", "!")
  trim_symbols = {"!", "("}
  split_on_hyphen = True
  res = not_annotation_word2pronunciation(
    word, trim_symbols, split_on_hyphen, get_pronunciation_with_dict)

  assert res == ("!", "(", "hel", "lo", "(", "!")


# endregion

# region word2pronunciation

def test_word2pronunciation__consider_annotation_is_true__annotation_split_symbol_has_len_2():
  consider_annotation = True
  word = ("/", "hello", "/")
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "//"

  with pytest.raises(ValueError):
    word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation_with_dict,
                       consider_annotation, annotation_split_symbol)


def test_word2pronunciation__consider_annotation_is_true__annotation_split_symbol_has_len_0():
  consider_annotation = True
  word = ("/", "hello", "/")
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = ""

  with pytest.raises(ValueError):
    word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation_with_dict,
                       consider_annotation, annotation_split_symbol)


def test_word2pronunciation__consider_annotation_is_true__word_is_annotation():
  consider_annotation = True
  word = ("/", "h", "e", "/")
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"
  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation_with_dict,
                           consider_annotation, annotation_split_symbol)

  assert res == ("he",)


def test_word2pronunciation__consider_annotation_is_false__word_is_annotation():
  consider_annotation = False
  word = ("/", "hello", "/")
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "/"
  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation_with_dict_or_replace,
                           consider_annotation, annotation_split_symbol)

  assert res == ("*",)


def test_word2pronunciation__word_is_not_annotation():
  consider_annotation = True
  word = ("!", "hello", "!")
  trim_symbols = {"!"}
  split_on_hyphen = True
  annotation_split_symbol = "/"
  res = word2pronunciation(word, trim_symbols, split_on_hyphen, get_pronunciation_with_dict,
                           consider_annotation, annotation_split_symbol)

  assert res == word

# endregion

# region sentence2pronunciation


def test_sentence2pronunciation__consider_annotation_is_true__annotation_split_symbol_has_len_2():
  consider_annotation = True
  sentence = ("/", "hello", "/", " ", "world")
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = "//"

  with pytest.raises(ValueError):
    sentence2pronunciation(sentence, trim_symbols, split_on_hyphen, get_pronunciation_with_dict,
                           consider_annotation, annotation_split_symbol)


def test_sentence2pronunciation__consider_annotation_is_true__annotation_split_symbol_has_len_0():
  consider_annotation = True
  sentence = ("/", "hello", "/", " ", "world")
  trim_symbols = {"!"}
  split_on_hyphen = False
  annotation_split_symbol = ""

  with pytest.raises(ValueError):
    sentence2pronunciation(sentence, trim_symbols, split_on_hyphen, get_pronunciation_with_dict,
                           consider_annotation, annotation_split_symbol)


def test_sentence2pronunciation__single_word():
  sentence = ("hello",)
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciation(sentence, trim_symbols, split_on_hyphen,
                               get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_sentence2pronunciation__two_words():
  sentence = ("hello", " ", "world")
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciation(sentence, trim_symbols, split_on_hyphen,
                               get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello", " ", "world")


def test_sentence2pronunciation__single_annotation():
  sentence = ("/", "hello", "/")
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciation(sentence, trim_symbols, split_on_hyphen,
                               get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello",)


def test_sentence2pronunciation__one_word_and_one_annotation():
  sentence = ("hello", " ", "/", "world", "/")
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciation(sentence, trim_symbols, split_on_hyphen,
                               get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello", " ", "world")


def test_sentence2pronunciation__one_word_and_one_annotation_separate_symbols():
  sentence = ("hello", " ", "/", "w", "o", "r", "l", "d", "/")
  trim_symbols = {"!"}
  split_on_hyphen = True
  consider_annotation = True
  annotation_split_symbol = "/"

  res = sentence2pronunciation(sentence, trim_symbols, split_on_hyphen,
                               get_pronunciation, consider_annotation, annotation_split_symbol)

  assert res == ("hello", " ", "world")

# endregion
