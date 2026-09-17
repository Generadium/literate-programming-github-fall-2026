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
# Write a Python function named "truncate" that truncates a string to a maximum of 100 characters 
# and adds a Unicode ellipsis, adhering to the following rules. Use the third-party 
# Python package regex and its \X pattern to identify Unicode grapheme clusters.
#
# 1. Characters are measured as Unicode grapheme clusters. 
# 2. The 100-character limit is an inclusive maximum.
# 3. The appended ellipsis must be a Unicode ellipsis and counts as one grapheme 
#    cluster towards the 100-grapheme-cluster budget.
# 4. Truncation can occur mid-word.
# 5. Strip trailing whitespace from the input before appending the ellipsis. 
# 6. If the stripped input contains 100 or more grapheme clusters, retain the first 
#    99 grapheme clusters of the input and then append the ellipsis.
# 7. If the stripped input contains fewer than 100 grapheme clusters, return the entire stripped input
#    followed by the ellipsis, even if the resulting string is shorter than 100 grapheme clusters.
# 8. An empty input is treated like any other input containing fewer than 
#    100 grapheme clusters and therefore returns the ellipsis alone.

import regex

# text: the input string to truncate
# return: the input string with trailing whitespace removed and a Unicode ellipsis appended,
#         truncated so the total result is no more than 100 grapheme clusters. 
def truncate(text: str) -> str:
    """
    Strip trailing whitespace, then return at most 100 Unicode grapheme clusters,
    including a final Unicode ellipsis (…).
    """
    stripped = text.rstrip()

    # \X matches one Unicode grapheme cluster.
    clusters = regex.findall(r"\X", stripped)

    if len(clusters) >= 100:
        return "".join(clusters[:99]) + "…"

    return stripped + "…"

# Tests a string shorter than 100 characters.
def test_1():
    assert truncate("one") == "one…"

# Tests a string exactly 100 characters long.
def test_2():
    text = "a" * 100
    assert truncate(text) == ("a" * 99) + "…"

# Tests a string longer than 100 characters.
def test_3():
    text = "a" * 120
    assert truncate(text) == ("a" * 99) + "…"

# Tests an empty string.
def test_4():
    assert truncate("") == "…"


