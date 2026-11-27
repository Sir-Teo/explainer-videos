"""Narration strings that hold a placeholder must be f-strings, or the film reads the braces aloud.

A plain literal next to an f-string is merged into it by the parser, so the check reads the tokens, not the tree."""

import glob
import io
import re
import tokenize

PLACEHOLDER = re.compile(r"\{[A-Za-z_0-9(][^{}]*(\[[^{}]*\]|\.[A-Za-z_]|\(|:[.,]?[0-9]*[a-z%,])[^{}]*\}")


def plain_strings(src):
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.STRING:
            prefix = re.match(r"[A-Za-z]*", tok.string).group(0).lower()
            if "f" not in prefix and "r" not in prefix:
                yield tok.start[0], tok.string


def test_no_placeholder_in_plain_strings():
    bad = []
    for fn in sorted(glob.glob("videos/industry/industry*/s*.py")):
        for line, s in plain_strings(open(fn, encoding="utf-8").read()):
            if "\\" not in s and PLACEHOLDER.search(s):
                bad.append(f"{fn}:{line}: {s[:70]}")
    assert not bad, "\n".join(bad)
