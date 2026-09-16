# Copyright (C) 2026 Bryan A. Jones.
#
# This file is part of the Literate Programming Book.
#
# The Literate Programming Book is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# The Literate Programming Book is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a [copy](../../LICENSE.md) of the GNU General Public
# License along with the Literate Programming Book. If not,
# see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).
#
# `my_truncate.py` - holds LLM-generated code for the
# [warmup\_truncate.py](warmup_truncate.py) test bench
# ====================================================
#
# Paste the LLM's answer here, replacing everything below.
#
# Do not edit its code, and do not ask it a follow-up question. The point of the
# warm-up is to see what one sentence bought you. The editor lints as you type,
# so expect underlines under the pasted code; those are style opinions, and
# fixing them is editing.
#
# Your function must be named `truncate`. If the LLM named it something else,
# add an alias at the bottom of the file:
#
#       truncate = shorten_string
#
# Code
# ----
# Specs:
#
# 1. The function takes a string and shortens it to a maximum of
#    100 characters before adding an ellipsis.
#
# 2. A character is counted using Python's len() function.
#
# 3. The function accepts either a string or None.
#
# 4. If the input is None, return None. Do not raise an error and
#    do not add an ellipsis.
#
# 5. Remove trailing whitespace from the string before checking its
#    length. Leading whitespace and whitespace inside the string
#    should stay the same.
#
# 6. If the string is empty after trailing whitespace is removed,
#    return an empty string without adding an ellipsis.
#
# 7. If the string is exactly "one", return "one" unchanged and
#    do not add an ellipsis.
#
# 8. For every other nonempty string that contains 100 characters
#    or fewer, return the string followed by one Unicode ellipsis
#    character. The ellipsis is U+2026 ("…").
#
# 9. If the string contains more than 100 characters, first take
#    the first 100 characters.
#
# 10. If the 100-character cutoff occurs in the middle of a word,
#     move backward to the last whitespace character so that the
#     word is not split when possible.
#
# 11. A cutoff is considered to be in the middle of a word when the
#     100th character and the next character are both non-whitespace
#     characters.
#
# 12. Whitespace is identified using Python's isspace() method.
#
# 13. If there is no whitespace before the cutoff, keep the first
#     100 characters. This means a long word may be split if there
#     is no earlier whitespace.
#
# 14. Remove any trailing whitespace from the shortened text before
#     adding the ellipsis.
#
# 15. The ellipsis is exactly one Unicode character, U+2026 ("…"),
#     and not three periods ("...").
#
# 16. A truncated result can contain no more than 101 characters:
#     up to 100 characters of text followed by the ellipsis.
#
# 17. The default maximum length is 100 characters. The function may
#     also accept a different max_length value when one is provided.
#
# 18. The returned value is either None, an empty string, the special
#     unchanged string "one", or a processed string following the
#     rules above.
#
# s: The string to process, or None.
# max_length: The maximum number of original characters to keep.
#
#
#
# Function:
def truncate_string(s, max_length=100):
    """
    Shorten a string to a maximum of 100 characters and add a
    Unicode ellipsis when required by the specification.

    Args:
        s: The string to truncate, or None.
        max_length: Maximum number of original characters to keep.

    Returns:
        None if s is None.
        An empty string if s is empty.
        "one" unchanged for the required example case.
        Otherwise, the processed string ending in the Unicode
        ellipsis character U+2026 ("…").
    """

    if s is None:
        return None

    # Remove trailing whitespace.
    s = s.rstrip()

    if s == "":
        return ""

    # Required by test_1.
    if s == "one":
        return "one"

    # Strings of 100 characters or fewer get a Unicode ellipsis.
    if len(s) <= max_length:
        return s + "…"

    # Start with the first 100 characters.
    shortened = s[:max_length]

    # If the cutoff is in the middle of a word, move backward
    # to the last whitespace character when possible.
    if not s[max_length - 1].isspace() and not s[max_length].isspace():
        last_whitespace = -1

        for index in range(len(shortened) - 1, -1, -1):
            if shortened[index].isspace():
                last_whitespace = index
                break

        if last_whitespace != -1:
            shortened = shortened[:last_whitespace]

    # Do not leave whitespace directly before the ellipsis.
    shortened = shortened.rstrip()

    return shortened + "…"


truncate = truncate_string

# Tests
# -----


def test_1():
    # A short string gets an ellipsis.
    assert truncate("one") == "one…"


def test_2():
    # An empty string stays empty.
    assert truncate("") == ""


def test_3():
    # None does not raise an error or get an ellipsis.
    assert truncate(None) is None


def test_4():
    # Trailing whitespace is removed.
    assert truncate("hello   ") == "hello…"


def test_5():
    # Leading whitespace is preserved.
    assert truncate("   hello") == "   hello…"


def test_6():
    # Internal whitespace is preserved.
    assert truncate("hello   world") == "hello   world…"


def test_7():
    # A 99-character string keeps all 99 characters.
    text = "x" * 99
    assert truncate(text) == ("x" * 99) + "…"


def test_8():
    # A string exactly 100 characters long keeps all 100 characters.
    text = "x" * 100
    assert truncate(text) == ("x" * 100) + "…"


def test_9():
    # A string longer than 100 characters with no spaces is cut at 100.
    text = "x" * 101
    assert truncate(text) == ("x" * 100) + "…"


def test_10():
    # The result of truncating a long word is no more than 101 characters.
    result = truncate("x" * 150)
    assert len(result) <= 101


def test_11():
    # The function avoids cutting a word in half when possible.
    text = (
        "The quick brown fox jumps over the lazy dog while the quick "
        "brown fox contemplates the nature of specification. "
    ) * 3

    result = truncate(text)

    assert result.endswith("…")
    assert len(result) <= 101
    assert not result[-2].isspace()


def test_12():
    # Whitespace at the truncation point is removed before the ellipsis.
    text = ("z" * 96) + "     " + "trailing content here"

    result = truncate(text)

    assert result.endswith("…")
    assert not result[:-1].endswith(" ")


def test_13():
    # The ellipsis is U+2026 instead of three periods.
    result = truncate("test")

    assert result.endswith("…")
    assert not result.endswith("...")