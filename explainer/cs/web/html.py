"""A small HTML parser in the shape of the WHATWG algorithm (Part 42): a tokenizer that is a state machine with error
recovery, and a tree builder that closes elements implicitly, so that every input produces some tree."""

from __future__ import annotations

from dataclasses import dataclass, field

INLINE_CONTEXT = {"pre", "p", "li", "b", "i", "a", "code", "h1", "h2", "h3", "span", "em", "strong"}
VOID = {"br", "img", "hr", "meta", "link", "input"}
BLOCK_CLOSES_P = {"p", "div", "h1", "h2", "h3", "ul", "ol", "li", "pre", "table", "blockquote", "hr"}


@dataclass
class Node:
    tag: str                      # "#text" for text, "#document" for the root
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    text: str = ""
    parent: "Node | None" = None

    def append(self, n):
        n.parent = self
        self.children.append(n)
        return n

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


def tokenize(src: str, trace: list | None = None):
    """States: data, tag open, end tag open, tag name, before attribute name, attribute name, before attribute value,
    attribute value (quoted or not), self-closing, comment.  Errors are recovered from, never raised: a stray "<"
    becomes text, an unterminated tag ends at end of input.  Yields tokens; optionally records (state, char)."""
    i, n = 0, len(src)
    state = "data"
    buf = ""
    tag = None
    attr = None
    tokens, errors = [], []

    def emit_text():
        nonlocal buf
        if buf:
            tokens.append(("text", buf))
            buf = ""
    while i <= n:
        c = src[i] if i < n else ""
        if trace is not None:
            trace.append((state, c))
        if state == "data":
            if c == "<":
                emit_text()
                state = "tag open"
            elif c == "":
                emit_text()
                break
            else:
                buf += c
        elif state == "tag open":
            if c == "/":
                state = "end tag open"
            elif c == "!" and src.startswith("!--", i):
                state = "comment"
                i += 2
            elif c.isalpha():
                tag = {"kind": "start", "name": c.lower(), "attrs": {}, "self": False}
                state = "tag name"
            else:
                errors.append(("invalid-first-character-of-tag-name", i))
                buf = "<" + c if c else "<"
                state = "data"
        elif state == "end tag open":
            if c.isalpha():
                tag = {"kind": "end", "name": c.lower(), "attrs": {}, "self": False}
                state = "tag name"
            else:
                errors.append(("invalid-end-tag", i))
                state = "data"
        elif state == "tag name":
            if c in " \t\n":
                state = "before attribute name"
            elif c == "/":
                state = "self-closing"
            elif c == ">":
                tokens.append((tag["kind"], tag))
                state = "data"
            elif c == "":
                errors.append(("eof-in-tag", i))
                break
            else:
                tag["name"] += c.lower()
        elif state == "before attribute name":
            if c in " \t\n":
                pass
            elif c == ">":
                tokens.append((tag["kind"], tag))
                state = "data"
            elif c == "/":
                state = "self-closing"
            elif c == "":
                errors.append(("eof-in-tag", i))
                break
            else:
                attr = [c.lower(), ""]
                state = "attribute name"
        elif state == "attribute name":
            if c == "=":
                state = "before attribute value"
            elif c in " \t\n/>" or c == "":
                tag["attrs"][attr[0]] = ""
                state = "before attribute name"
                continue
            else:
                attr[0] += c.lower()
        elif state == "before attribute value":
            if c in "\"'":
                q = c
                j = src.find(q, i + 1)
                if j < 0:
                    errors.append(("eof-in-attribute-value", i))
                    j = n
                tag["attrs"][attr[0]] = src[i + 1:j]
                i = j
                state = "before attribute name"
            else:
                j = i
                while j < n and src[j] not in " \t\n>":
                    j += 1
                tag["attrs"][attr[0]] = src[i:j]
                i = j - 1
                state = "before attribute name"
        elif state == "self-closing":
            if c == ">":
                tag["self"] = True
                tokens.append((tag["kind"], tag))
                state = "data"
            else:
                errors.append(("unexpected-solidus-in-tag", i))
                state = "before attribute name"
                continue
        elif state == "comment":
            j = src.find("-->", i)
            if j < 0:
                errors.append(("eof-in-comment", i))
                j = n
            tokens.append(("comment", src[i + 1:j]))
            i = j + 2
            state = "data"
        i += 1
    return tokens, errors


def build(tokens):
    """The tree builder: an open-element stack.  A block start tag implicitly closes an open <p>; a <li> closes an
    open <li>; an end tag closes up to the matching open element, or is ignored if none is open."""
    doc = Node("#document")
    stack = [doc]
    fixes = []
    for kind, t in tokens:
        top = stack[-1]
        if kind == "text":
            if t.strip() or top.tag in INLINE_CONTEXT:     # whitespace between inline elements is a space
                top.append(Node("#text", text=t))
        elif kind == "start":
            name = t["name"]
            if name in BLOCK_CLOSES_P and any(s.tag == "p" for s in stack):
                while stack[-1].tag != "p":
                    stack.pop()
                stack.pop()
                fixes.append(f"<{name}> closed an open <p>")
            if name == "li" and stack[-1].tag == "li":
                stack.pop()
                fixes.append("<li> closed the previous <li>")
            el = stack[-1].append(Node(name, attrs=t["attrs"]))
            if name not in VOID and not t["self"]:
                stack.append(el)
        elif kind == "end":
            name = t["name"]
            if any(s.tag == name for s in stack[1:]):
                while stack[-1].tag != name:
                    fixes.append(f"</{name}> also closed <{stack[-1].tag}>")
                    stack.pop()
                stack.pop()
            else:
                fixes.append(f"stray </{name}> ignored")
    return doc, fixes


def parse(src: str):
    toks, errs = tokenize(src)
    doc, fixes = build(toks)
    return doc, errs, fixes


def outline(node, depth=0, out=None):
    out = [] if out is None else out
    if node.tag == "#text":
        out.append("  " * depth + repr(node.text.strip()[:30]))
    elif node.tag != "#document":
        a = "".join(f' {k}="{v}"' for k, v in node.attrs.items())
        out.append("  " * depth + f"<{node.tag}{a}>")
    for c in node.children:
        outline(c, depth + (node.tag != "#document"), out)
    return out


def markdown_to_html(md: str, limit: int | None = None) -> str:
    """Enough Markdown for this repository's READMEs: headings, paragraphs, bullet lists, code spans, bold, links."""
    import html as H
    import re
    out, para, lst, raw = [], [], False, []

    def inline(s):
        s = H.escape(s, quote=False)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    def flush():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
    lines = md.splitlines()
    for ln in lines[:limit] if limit else lines:
        if ln.startswith("```"):
            continue
        m = re.match(r"(#+) (.*)", ln)
        if m:
            flush()
            if lst:
                out.append("</ul>")
                lst = False
            k = min(3, len(m.group(1)))
            out.append(f"<h{k}>{inline(m.group(2))}</h{k}>")
        elif re.match(r"\s*[*-] ", ln):
            flush()
            if not lst:
                out.append("<ul>")
                lst = True
            raw.append(re.sub(r"^\s*[*-] ", "", ln))
            out.append("<li>" + inline(raw[-1]) + "</li>")
        elif not ln.strip():
            flush()
            if lst:
                out.append("</ul>")
                lst = False
        elif lst and ln.startswith("  "):
            raw[-1] += " " + ln.strip()
            out[-1] = "<li>" + inline(raw[-1]) + "</li>"
        else:
            para.append(ln.strip())
    flush()
    if lst:
        out.append("</ul>")
    return "\n".join(out)
