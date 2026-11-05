"""The Pebble language: a small C-like language with structs, pointers, arrays and functions (Parts 12 and 13).

    struct Node { next: *Node; letters: *char; length: int; count: int; }

    fn lookup(w: *char, n: int) -> *Node {
        var p: *Node = head;
        while p != null {
            if p.length == n && same(p.letters, w, n) { return p; }
            p = p.next;
        }
        return null;
    }

Declarations are name-first (``x: int``), so the grammar never has to ask whether a name is a type, and every
statement starts with a keyword or an expression: the language is LL(1) apart from expressions, which a Pratt parser
handles, and the whole grammar (:data:`BNF`) is LALR(1) with no conflicts.

* :data:`TOKENS` and :class:`Lexer`: each token is a regular expression run through :mod:`regex`'s Thompson NFAs,
  all at once, taking the longest match (maximal munch) and the earliest rule on ties; keywords are identifiers
  looked up in a table.
* :class:`Parser`: recursive descent for declarations and statements, Pratt's (1973) top-down operator precedence
  for expressions, producing the dataclass AST below.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from explainer.cs.lang import regex as R

# ---------------------------------------------------------------------------
# tokens
# ---------------------------------------------------------------------------
TOKENS = [
    ("space", r"[ \t\n\r]+"),
    ("comment", r"//[^\n]*"),
    ("num", r"[0-9]+"),
    ("charlit", r"'([^'\\]|\\.)'"),
    ("string", r'"([^"\\]|\\.)*"'),
    ("ident", r"[a-zA-Z_][a-zA-Z_0-9]*"),
    ("op", r"->|==|!=|<=|>=|&&|\|\||[-+*/%<>=!&(){}\[\];,:.]"),
]
KEYWORDS = {"fn", "var", "struct", "if", "else", "while", "return", "break", "continue", "null", "int", "char",
            "sizeof"}


@dataclass
class Token:
    kind: str           # num, charlit, string, ident, a keyword, or the operator text itself
    text: str
    line: int
    col: int

    def __repr__(self):
        return f"{self.kind}:{self.text!r}" if self.kind != self.text else repr(self.text)


class LexError(ValueError):
    pass


class Lexer:
    """Maximal munch over all token NFAs at once."""

    def __init__(self, spec=TOKENS):
        self.spec = spec
        self.nfas = [(name, R.compile(rx)) for name, rx in spec]

    def longest(self, text: str, i: int):
        """(length, rule) of the longest token starting at i, earliest rule on ties; also the work done."""
        cur = [(name, m, m.closure({m.start})) for name, m in self.nfas]
        best = (0, None)
        j = i
        work = 0
        while cur and j < len(text):
            c = text[j]
            nxt = []
            for name, m, S in cur:
                T = m.step(S, c)
                work += len(T)
                if T:
                    nxt.append((name, m, T))
            j += 1
            cur = nxt
            for name, m, S in cur:            # spec order: the first accepting rule wins
                if m.accept in S:
                    best = (j - i, name)
                    break
        return best, work

    def tokens(self, text: str, keep_space: bool = False):
        out = []
        i, line, col = 0, 1, 1
        while i < len(text):
            (n, rule), _ = self.longest(text, i)
            if n == 0:
                raise LexError(f"unexpected {text[i]!r} at line {line}, column {col}")
            s = text[i:i + n]
            if rule == "ident" and s in KEYWORDS:
                kind = s
            elif rule == "op":
                kind = s
            else:
                kind = rule
            if keep_space or rule not in ("space", "comment"):
                out.append(Token(kind, s, line, col))
            for ch in s:
                if ch == "\n":
                    line, col = line + 1, 1
                else:
                    col += 1
            i += n
        out.append(Token("$", "", line, col))
        return out


def lex(text: str):
    return Lexer().tokens(text)


# ---------------------------------------------------------------------------
# the AST
# ---------------------------------------------------------------------------
@dataclass
class Type:
    kind: str                   # int, char, ptr, array, struct
    of: "Type | None" = None
    n: int = 0
    name: str = ""

    def __str__(self):
        if self.kind == "ptr":
            return "*" + str(self.of)
        if self.kind == "array":
            return f"[{self.n}]{self.of}"
        if self.kind == "struct":
            return self.name
        return self.kind


@dataclass
class Expr:
    pass


@dataclass
class Num(Expr):
    value: int


@dataclass
class CharLit(Expr):
    value: int


@dataclass
class Str(Expr):
    value: str


@dataclass
class Name(Expr):
    id: str


@dataclass
class Null(Expr):
    pass


@dataclass
class SizeOf(Expr):
    type: Type


@dataclass
class Unary(Expr):
    op: str
    e: Expr


@dataclass
class Binary(Expr):
    op: str
    l: Expr
    r: Expr


@dataclass
class Call(Expr):
    f: Expr
    args: list


@dataclass
class Index(Expr):
    a: Expr
    i: Expr


@dataclass
class Field(Expr):
    e: Expr
    name: str


@dataclass
class Stmt:
    pass


@dataclass
class Var(Stmt):
    name: str
    type: Type
    init: Expr | None = None


@dataclass
class Assign(Stmt):
    target: Expr
    value: Expr


@dataclass
class ExprStmt(Stmt):
    e: Expr


@dataclass
class Block(Stmt):
    stmts: list


@dataclass
class If(Stmt):
    cond: Expr
    then: Block
    els: Stmt | None = None


@dataclass
class While(Stmt):
    cond: Expr
    body: Block


@dataclass
class Return(Stmt):
    e: Expr | None = None


@dataclass
class Break(Stmt):
    pass


@dataclass
class Continue(Stmt):
    pass


@dataclass
class Struct:
    name: str
    fields: list                # [(name, Type)]


@dataclass
class Func:
    name: str
    params: list                # [(name, Type)]
    ret: Type | None
    body: Block


@dataclass
class Program:
    structs: list = field(default_factory=list)
    globals: list = field(default_factory=list)     # [Var]
    funcs: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# the parser
# ---------------------------------------------------------------------------
class ParseError(ValueError):
    pass


# binding powers for Pratt parsing: higher binds tighter
INFIX = {"||": 1, "&&": 2, "==": 3, "!=": 3, "<": 4, "<=": 4, ">": 4, ">=": 4, "+": 5, "-": 5, "*": 6, "/": 6,
         "%": 6}
PREFIX = 7          # - ! * &
POSTFIX = 8         # calls, indexing, fields


class Parser:
    def __init__(self, tokens, trace: bool = False):
        self.t = tokens
        self.i = 0
        self.trace = [] if trace else None
        self.depth = 0

    # --- token helpers ---------------------------------------------------
    @property
    def tok(self) -> Token:
        return self.t[self.i]

    def at(self, *kinds) -> bool:
        return self.tok.kind in kinds

    def eat(self, kind: str) -> Token:
        if self.tok.kind != kind:
            tk = self.tok
            raise ParseError(f"line {tk.line}, column {tk.col}: expected {kind!r}, found {tk.text or 'end'!r}")
        tk = self.tok
        self.i += 1
        return tk

    def note(self, what):
        if self.trace is not None:
            self.trace.append((self.depth, what, self.i))

    # --- declarations ----------------------------------------------------
    def program(self) -> Program:
        p = Program()
        while not self.at("$"):
            if self.at("struct"):
                p.structs.append(self.struct())
            elif self.at("fn"):
                p.funcs.append(self.func())
            elif self.at("var"):
                p.globals.append(self.var())
            else:
                raise ParseError(f"line {self.tok.line}: expected a declaration, found {self.tok.text!r}")
        return p

    def struct(self) -> Struct:
        self.note("struct")
        self.eat("struct")
        name = self.eat("ident").text
        self.eat("{")
        fields = []
        while not self.at("}"):
            f = self.eat("ident").text
            self.eat(":")
            fields.append((f, self.type()))
            self.eat(";")
        self.eat("}")
        return Struct(name, fields)

    def func(self) -> Func:
        self.note("fn")
        self.eat("fn")
        name = self.eat("ident").text
        self.eat("(")
        params = []
        if not self.at(")"):
            while True:
                p = self.eat("ident").text
                self.eat(":")
                params.append((p, self.type()))
                if not self.at(","):
                    break
                self.eat(",")
        self.eat(")")
        ret = None
        if self.at("->"):
            self.eat("->")
            ret = self.type()
        return Func(name, params, ret, self.block())

    def type(self) -> Type:
        if self.at("int", "char"):
            return Type(self.eat(self.tok.kind).kind)
        if self.at("*"):
            self.eat("*")
            return Type("ptr", self.type())
        if self.at("["):
            self.eat("[")
            n = int(self.eat("num").text)
            self.eat("]")
            return Type("array", self.type(), n)
        return Type("struct", name=self.eat("ident").text)

    # --- statements --------------------------------------------------------
    def block(self) -> Block:
        self.note("block")
        self.eat("{")
        self.depth += 1
        out = []
        while not self.at("}"):
            out.append(self.stmt())
        self.depth -= 1
        self.eat("}")
        return Block(out)

    def var(self) -> Var:
        self.note("var")
        self.eat("var")
        name = self.eat("ident").text
        self.eat(":")
        ty = self.type()
        init = None
        if self.at("="):
            self.eat("=")
            init = self.expr()
        self.eat(";")
        return Var(name, ty, init)

    def stmt(self) -> Stmt:
        k = self.tok.kind
        if k == "var":
            return self.var()
        if k == "if":
            self.note("if")
            self.eat("if")
            c = self.expr()
            th = self.block()
            els = None
            if self.at("else"):
                self.eat("else")
                els = self.stmt() if self.at("if") else self.block()
            return If(c, th, els)
        if k == "while":
            self.note("while")
            self.eat("while")
            c = self.expr()
            return While(c, self.block())
        if k == "return":
            self.note("return")
            self.eat("return")
            e = None if self.at(";") else self.expr()
            self.eat(";")
            return Return(e)
        if k == "break":
            self.eat("break")
            self.eat(";")
            return Break()
        if k == "continue":
            self.eat("continue")
            self.eat(";")
            return Continue()
        if k == "{":
            return self.block()
        self.note("expression statement")
        e = self.expr()
        if self.at("="):
            self.eat("=")
            v = self.expr()
            self.eat(";")
            return Assign(e, v)
        self.eat(";")
        return ExprStmt(e)

    # --- expressions: Pratt ----------------------------------------------
    def expr(self, rbp: int = 0) -> Expr:
        left = self.prefix()
        while True:
            op = self.tok.kind
            if op in INFIX and INFIX[op] > rbp:
                self.eat(op)
                right = self.expr(INFIX[op])        # left-associative: the right side binds tighter only
                left = Binary(op, left, right)
            else:
                return left

    def prefix(self) -> Expr:
        k = self.tok.kind
        if k in ("-", "!", "*", "&"):
            self.eat(k)
            return Unary(k, self.expr(PREFIX))
        return self.postfix(self.primary())

    def primary(self) -> Expr:
        tk = self.tok
        if tk.kind == "num":
            self.eat("num")
            return Num(int(tk.text))
        if tk.kind == "charlit":
            self.eat("charlit")
            body = tk.text[1:-1]
            return CharLit(ord(_unescape(body)))
        if tk.kind == "string":
            self.eat("string")
            return Str(_unescape(tk.text[1:-1]))
        if tk.kind == "ident":
            self.eat("ident")
            return Name(tk.text)
        if tk.kind == "null":
            self.eat("null")
            return Null()
        if tk.kind == "sizeof":
            self.eat("sizeof")
            self.eat("(")
            ty = self.type()
            self.eat(")")
            return SizeOf(ty)
        if tk.kind == "(":
            self.eat("(")
            e = self.expr()
            self.eat(")")
            return e
        raise ParseError(f"line {tk.line}, column {tk.col}: expected an expression, found {tk.text or 'end'!r}")

    def postfix(self, e: Expr) -> Expr:
        while True:
            if self.at("("):
                self.eat("(")
                args = []
                if not self.at(")"):
                    while True:
                        args.append(self.expr())
                        if not self.at(","):
                            break
                        self.eat(",")
                self.eat(")")
                e = Call(e, args)
            elif self.at("["):
                self.eat("[")
                i = self.expr()
                self.eat("]")
                e = Index(e, i)
            elif self.at("."):
                self.eat(".")
                e = Field(e, self.eat("ident").text)
            else:
                return e


def _unescape(s: str) -> str:
    out = []
    k = 0
    while k < len(s):
        if s[k] == "\\" and k + 1 < len(s):
            out.append({"n": "\n", "t": "\t", "0": "\0", "\\": "\\", "'": "'", '"': '"'}.get(s[k + 1], s[k + 1]))
            k += 2
        else:
            out.append(s[k])
            k += 1
    return "".join(out)


def parse(text: str) -> Program:
    return Parser(lex(text)).program()


def parse_expr(text: str) -> Expr:
    p = Parser(lex(text))
    e = p.expr()
    p.eat("$")
    return e


def show(e) -> str:
    """Fully parenthesized, to make the parser's grouping visible."""
    if isinstance(e, Num):
        return str(e.value)
    if isinstance(e, CharLit):
        return repr(chr(e.value))
    if isinstance(e, Str):
        return '"' + e.value.encode("unicode_escape").decode() + '"'
    if isinstance(e, Name):
        return e.id
    if isinstance(e, Null):
        return "null"
    if isinstance(e, SizeOf):
        return f"sizeof({e.type})"
    if isinstance(e, Unary):
        return f"({e.op}{show(e.e)})"
    if isinstance(e, Binary):
        return f"({show(e.l)} {e.op} {show(e.r)})"
    if isinstance(e, Call):
        return f"{show(e.f)}({', '.join(show(a) for a in e.args)})"
    if isinstance(e, Index):
        return f"{show(e.a)}[{show(e.i)}]"
    if isinstance(e, Field):
        return f"{show(e.e)}.{e.name}"
    raise TypeError(e)


def count_nodes(x) -> int:
    if isinstance(x, list):
        return sum(count_nodes(y) for y in x)
    if not hasattr(x, "__dataclass_fields__") or isinstance(x, Type):
        return 0
    n = 1
    for f in x.__dataclass_fields__:
        n += count_nodes(getattr(x, f))
    return n


# ---------------------------------------------------------------------------
# the same language as a plain context-free grammar, for the LR tables
# ---------------------------------------------------------------------------
BNF = r"""
Program -> Decls
Decls -> Decl Decls | ε
Decl -> StructDecl | FnDecl | VarDecl
StructDecl -> struct ident { Fields }
Fields -> ident : Type ; Fields | ε
FnDecl -> fn ident ( Params ) RetType Block
Params -> ParamList | ε
ParamList -> ident : Type | ident : Type , ParamList
RetType -> -> Type | ε
Type -> int | char | * Type | [ num ] Type | ident
VarDecl -> var ident : Type Init ;
Init -> = Expr | ε
Block -> { Stmts }
Stmts -> Stmt Stmts | ε
Stmt -> VarDecl | IfStmt | while Expr Block | return Expr ; | return ; | break ; | continue ; | Block | Expr ; | Expr = Expr ;
IfStmt -> if Expr Block | if Expr Block else Block | if Expr Block else IfStmt
Expr -> Expr || And | And
And -> And && Eq | Eq
Eq -> Eq == Rel | Eq != Rel | Rel
Rel -> Rel < Add | Rel <= Add | Rel > Add | Rel >= Add | Add
Add -> Add + Mul | Add - Mul | Mul
Mul -> Mul * Un | Mul / Un | Mul % Un | Un
Un -> - Un | ! Un | * Un | & Un | Post
Post -> Post ( Args ) | Post [ Expr ] | Post . ident | Prim
Args -> ArgList | ε
ArgList -> Expr | Expr , ArgList
Prim -> num | charlit | string | ident | null | sizeof ( Type ) | ( Expr )
"""


# ---------------------------------------------------------------------------
# the Job, in the Pebble language
# ---------------------------------------------------------------------------
JOB = r"""
// The Job: count the words of a text and print the twenty most frequent.
// Built-ins: getc() -> int (-1 at the end), putc(c: int), alloc(n: int) -> *char.

struct Node {
    next: *Node;        // the next word, in first-seen order
    letters: *char;     // the word, lower case
    length: int;
    count: int;
}

var head: *Node = null;
var tail: *Node = null;

fn same(a: *char, b: *char, n: int) -> int {
    var i: int = 0;
    while i < n {
        if a[i] != b[i] { return 0; }
        i = i + 1;
    }
    return 1;
}

fn lookup(w: *char, n: int) -> *Node {
    var p: *Node = head;
    while p != null {
        if p.length == n && same(p.letters, w, n) { return p; }
        p = p.next;
    }
    var q: *Node = alloc(sizeof(Node));
    q.letters = alloc(n);
    var i: int = 0;
    while i < n { q.letters[i] = w[i]; i = i + 1; }
    q.length = n;
    q.count = 0;
    q.next = null;
    if tail == null { head = q; } else { tail.next = q; }
    tail = q;
    return q;
}

fn printnum(n: int) {
    var digits: [12]char;
    var k: int = 0;
    if n == 0 { putc('0'); return; }
    while n > 0 { digits[k] = '0' + n % 10; n = n / 10; k = k + 1; }
    while k > 0 { k = k - 1; putc(digits[k]); }
}

fn report() {
    var shown: int = 0;
    while shown < 20 {
        var best: *Node = null;
        var p: *Node = head;
        while p != null {
            if p.count > 0 && (best == null || p.count > best.count) { best = p; }
            p = p.next;
        }
        if best == null { return; }
        var i: int = 0;
        while i < best.length { putc(best.letters[i]); i = i + 1; }
        putc(' ');
        printnum(best.count);
        putc('\n');
        best.count = -best.count;          // mark it printed
        shown = shown + 1;
    }
}

fn main() -> int {
    var word: [256]char;
    var n: int = 0;
    var c: int = getc();
    while c != -1 {
        if c >= 'A' && c <= 'Z' { c = c + 32; }
        if c >= 'a' && c <= 'z' {
            if n < 256 { word[n] = c; n = n + 1; }
        } else if n > 0 {
            var e: *Node = lookup(&word[0], n);
            e.count = e.count + 1;
            n = 0;
        }
        c = getc();
    }
    if n > 0 { var e: *Node = lookup(&word[0], n); e.count = e.count + 1; }
    report();
    return 0;
}
"""
