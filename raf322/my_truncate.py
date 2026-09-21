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

# Write a truncator function (named "truncate") that takes a string as an input and
# adheres to the following guidelines. Note that the maximum length specified in this case is
# 100 characters.

# 1. A character is defined as one Unicode code point. Letters, numbers, spaces, tabs, newline characters, and other whitespace each count as characters.

# 2. Whitespace includes spaces, tabs, and newline characters, and any of these may serve as a word boundary. 
# Leading and internal whitespace are preserved and count toward the character limit. Trailing whitespace is omitted, even if the string is within the maximum length.

# 3.An ellipsis is a single Unicode character ("…").

# 4. An ellipsis should not be added to the middle of a word. If a word is caught in the middle of the character limit,
# then the entire word should be omitted with the ellipsis trailing the previous complete word.

# 5. Strings shorter than or equal to 100 characters should not have an ellipsis.

# 6. When truncation occurs, the resulting length is the length of the retained portion of the string plus one character for the ellipsis. 
# The complete result, including the ellipsis, must not exceed 100 characters.

# 7. If a string is empty, there is no ellipsis placed and the string remains empty.

# 8. The ellipsis backs up to a word boundary and does not cut the string off mid-word. The only situation in which an ellipsis can
# cut a word is if the word itself exceeds the maximum length. In this case, the word is cut at the 99th character and the ellipsis is 
# appended at the 100th character position

# 9. If the input is not a string, including None, the function raises a TypeError.


# Fingerprint: 3cef2b4f


# Parameters:
#   text - The input string itself.

# Return - The input string. If the string's length is greater than the max_length specified then the 
#   string will be truncated.

def truncate(text):
    """
    Truncate a string to a maximum of 100 Unicode code points.

    Parameters:
        text - The input string itself.

    Returns:
        The input string with trailing whitespace removed.
        If the string exceeds 100 characters, it is truncated
        and a Unicode ellipsis is appended.

    Raises:
        TypeError - If text is not a string.
    """

    MAX_LENGTH = 100
    ELLIPSIS = "…"

    # Rule 9: Input must be a string.
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    # Rule 2: Remove trailing whitespace.
    text = text.rstrip()

    # Rule 7: An empty string remains empty.
    if text == "":
        return ""

    # Rule 5: Strings of 100 characters or fewer
    # do not receive an ellipsis.
    if len(text) <= MAX_LENGTH:
        return text

    # Rule 6: Reserve one code point for the ellipsis.
    cutoff = MAX_LENGTH - 1

    # Initially retain the first 99 code points.
    truncated = text[:cutoff]

    # Rules 4 and 8:
    # If the cutoff occurs in the middle of a word,
    # search backward for the closest whitespace boundary.
    if not text[cutoff].isspace() and not truncated[-1].isspace():
        boundary = -1

        for i in range(len(truncated) - 1, -1, -1):
            if truncated[i].isspace():
                boundary = i
                break

        # If a word boundary exists, remove the incomplete word.
        if boundary != -1:
            truncated = truncated[:boundary]

        # If no boundary exists, the word itself exceeds the
        # available length, so keep the cutoff at 99 characters.

    # Remove whitespace directly before the ellipsis.
    truncated = truncated.rstrip()

    return truncated + ELLIPSIS

# Your tests here.

def test_1():
    assert truncate("forty five") == "forty five"

def test_2():
    assert truncate("This string is to have more than 100 characters total. It needs to be this way so that I can test the truncating function.") == "This string is to have more than 100 characters total. It needs to be this way so that I can test…"

def test_3():
    assert truncate("This string is to have trailing whitespace to demonstrate how it handles it.                        ") == "This string is to have trailing whitespace to demonstrate how it handles it."

def test_4():
    assert truncate("A" * 101) == "A" * 99 + "…"

def test_5():
    raised = False

    try:
        truncate(67)
    except TypeError:
        raised = True

    assert raised

def test_6():
    assert truncate("") == ""

def test_7():
    assert truncate("A" * 100) == "A" * 100

def test_8():
    assert truncate("   Hello") == "   Hello"

def test_9():
    assert truncate("Hello    world") == "Hello    world"

def test_10():
    raised = False

    try:
        truncate(None)
    except TypeError:
        raised = True

    assert raised

def test_11():
    assert truncate("Hello\t\n") == "Hello"

def test_12():
    text = ("word " * 30).rstrip()
    result = truncate(text)

    assert len(result) <= 100
    assert result.endswith("…")


def test_13():
    text = "A" * 90 + "\n" + "B" * 20
    result = truncate(text)

    assert result == "A" * 90 + "…"


def test_14():
    text = "A" * 90 + "\t" + "B" * 20
    result = truncate(text)

    assert result == "A" * 90 + "…"





