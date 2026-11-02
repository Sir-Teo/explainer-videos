"""Small punctuation-aware prose wrapping; independent of scenes and data."""

import re

_TOKENS = re.compile(r"[A-Za-z0-9]+(?:[-'’][A-Za-z0-9]+)*|[ \t]+|.")
_CLOSE = set("，。！？：；、）》】」』”…,.;:!?%％)")
_OPEN = set("（《【「『“(")


def prose_lines(text, width, measure, *, atoms=()):
    """Wrap prose without stranding closing punctuation or splitting Latin words.

    ``measure`` supplies actual font widths. Explicit newlines remain breaks;
    only whitespace at line boundaries is discarded.
    """
    tokens = _TOKENS
    if atoms:
        protected = "|".join(re.escape(s) for s in sorted(set(atoms), key=len, reverse=True) if s)
        if protected:
            tokens = re.compile(protected + "|" + _TOKENS.pattern)
    lines = []
    for paragraph in text.split("\n"):
        line = []
        for token in tokens.findall(paragraph):
            trial = "".join(line) + token
            if not line or measure(trial) <= width:
                line.append(token)
                continue
            carry = []
            if token in _CLOSE:
                # Keep punctuation with the preceding word/character.
                while line and line[-1].isspace():
                    line.pop()
                while line and line[-1] in _CLOSE:
                    carry.insert(0, line.pop())
                if line:
                    carry.insert(0, line.pop())
            while line and line[-1] in _OPEN:
                carry.insert(0, line.pop())
            if "".join(line).strip():
                lines.append("".join(line).strip())
            line = carry + [token]
        if "".join(line).strip():
            lines.append("".join(line).strip())
    return lines
