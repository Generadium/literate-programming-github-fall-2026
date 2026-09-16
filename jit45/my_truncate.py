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
# Specification
# -------------
#
# `truncate(s, max_length=100)` shortens a string only when its trailing-stripped
# form is longer than `max_length`.
#
# Ordered rules:
#
# 1. `s` must be a `str` or `None`.
# 2. If `s` is `None`, return `None`.
# 3. `max_length` must be an `int` greater than or equal to `1`.
# 4. Apply `rstrip()` to `s`. This removes all trailing whitespace, including an
#    all-whitespace input. Leading and internal whitespace are otherwise kept.
# 5. If the trailing-stripped string is empty, return `""`.
# 6. If `len(s) <= max_length`, return the trailing-stripped string unchanged.
#    Do not append an ellipsis because no content was removed.
# 7. If `len(s) > max_length`, begin with `s[:max_length]`.
# 8. The cut is in the middle of a word when `s[max_length - 1]` and
#    `s[max_length]` are both non-whitespace according to `str.isspace()`.
# 9. When the cut is in the middle of a word, search `s[:max_length]` backward
#    for the last whitespace character at index `i`. If one exists, use `s[:i]`.
#    There is no minimum backup distance; avoiding a split word takes priority.
# 10. If backing up would leave no non-whitespace text, fall back to the hard
#     cut `s[:max_length]` rather than returning a bare ellipsis.
# 11. Remove trailing whitespace from the shortened text with `rstrip()`.
# 12. Append exactly one Unicode ellipsis character, U+2026 (`"…"`).
# 13. A truncated result contains at most `max_length` characters of retained text
#     followed by the ellipsis.
# 14. Word boundaries are whitespace only. Hyphens, dashes, zero-width spaces,
#     URLs, and scripts without whitespace do not create additional boundaries.
# 15. Python `len()` defines character count. A hard cut may therefore split a
#     grapheme cluster; no Unicode normalization is performed.
#
# 
#
# Function
# --------


def truncate(s: str | None, max_length: int = 100) -> str | None:
    """Return *s* shortened to at most *max_length* characters plus an ellipsis.

    Trailing whitespace is removed before length checking. Text at or below the
    limit is returned unchanged after that cleanup. Longer text is cut at the
    limit and, when possible, backed up to whitespace so a word is not split.
    """

    if s is None:
        return None

    if not isinstance(s, str):
        raise TypeError("s must be a string or None")

    if isinstance(max_length, bool) or not isinstance(max_length, int):
        raise TypeError("max_length must be an integer")

    if max_length < 1:
        raise ValueError("max_length must be at least 1")

    stripped = s.rstrip()

    if stripped == "":
        return ""

    if len(stripped) <= max_length:
        return stripped

    shortened = stripped[:max_length]

    cut_is_mid_word = (
        not stripped[max_length - 1].isspace()
        and not stripped[max_length].isspace()
    )

    if cut_is_mid_word:
        last_whitespace = -1

        for index in range(max_length - 1, -1, -1):
            if shortened[index].isspace():
                last_whitespace = index
                break

        if last_whitespace != -1:
            backed_up = shortened[:last_whitespace].rstrip()

            # Do not collapse nonempty input to a bare ellipsis.
            if backed_up:
                shortened = backed_up

    shortened = shortened.rstrip()

    # If the hard cut itself contains only whitespace, do not return a bare
    # ellipsis. Return the empty string instead.
    if shortened == "":
        return ""

    return shortened + "…"


# Tests
# -----


def test_1():
    assert truncate("one") == "one"


def test_2():
    assert truncate("") == ""


def test_3():
    assert truncate(None) is None


def test_4():
    assert truncate("hello   ") == "hello"


def test_5():
    assert truncate("   hello") == "   hello"


def test_6():
    assert truncate("hello   world") == "hello   world"


def test_7():
    text = "x" * 99
    assert truncate(text) == text


def test_8():
    text = "x" * 100
    assert truncate(text) == text


def test_9():
    text = "x" * 101
    assert truncate(text) == ("x" * 100) + "…"


def test_10():
    result = truncate("x" * 150)
    assert len(result) <= 101


def test_11():
    text = ("a" * 90) + " " + ("b" * 20)
    assert truncate(text) == ("a" * 90) + "…"


def test_12():
    text = ("z" * 96) + "     " + "trailing content here"
    result = truncate(text)

    assert result.endswith("…")
    assert not result[:-1].endswith(" ")


def test_13():
    result = truncate("x" * 101)

    assert result.endswith("…")
    assert not result.endswith("...")


def test_14():
    assert truncate("abcdefghij", 5) == "abcde…"


def test_15():
    try:
        truncate(42)
    except TypeError:
        pass
    else:
        raise AssertionError("truncate(42) should raise TypeError")


def test_16():
    try:
        truncate("hello", 2.5)
    except TypeError:
        pass
    else:
        raise AssertionError("float max_length should raise TypeError")


def test_17():
    try:
        truncate("hello", 0)
    except ValueError:
        pass
    else:
        raise AssertionError("max_length=0 should raise ValueError")


def test_18():
    text = " " + ("b" * 200)
    result = truncate(text)

    assert result != "…"
    assert result.endswith("…")


def test_19():
    assert truncate(" " * 150) == ""