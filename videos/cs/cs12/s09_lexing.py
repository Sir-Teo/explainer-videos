from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, KIND_COLORS, NO, PART, YES, chips, code,
                                   grid_table, load, region)


class Lexing(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.munch()
        self.job()
        self.indent()

    def card(self):
        card = chapter_card(8, r"Lexing the Pebble language", r"How do characters become words?", lit=(1975,),
                            extra=((1975, r"Lesk: \ \texttt{lex}"),), part=PART)
        with self.voiceover("Chapter eight. Lexing the Pebble language."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rules(self):
        lx = load("lexer")
        head = label(r"Every kind of token is a regular expression", font_size=34).to_edge(UP, buff=0.3)
        what = {"space": (r"skipped", GREY_C), "comment": (r"skipped", GREY_C), "num": (r"numbers", HEAD),
                "charlit": (r"character literals", HEAD), "string": (r"strings", HEAD),
                "ident": (r"names \ (and keywords)", CODE), "op": (r"operators and punctuation", CTRL)}
        rows = VGroup()
        for name, rx in lx["rules"]:
            d, c = what[name]
            r = VGroup(Text(name, font="DejaVu Sans Mono", font_size=18, color=c),
                       Text(rx if len(rx) < 52 else rx[:49] + "...", font="DejaVu Sans Mono", font_size=17,
                            color=GREY_A), label(d, font_size=18, color=c))
            r[0].move_to([-6.4, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-4.4, 0, 0], aligned_edge=LEFT)
            r[2].move_to([3.6, 0, 0], aligned_edge=LEFT)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.45)
        for r in rows:
            r[0].align_to([-6.4, 0, 0], LEFT)
            r[1].align_to([-4.4, 0, 0], LEFT)
            r[2].align_to([3.6, 0, 0], LEFT)
        kw = label(r"keywords \ (" + r", \ ".join(rf"\texttt{{{k}}}" for k in lx["keywords"][:8]) +
                   r", \dots): \ lexed as names, \ then looked up in a table", font_size=19,
                   color=FUNC).next_to(rows, DOWN, buff=0.4)
        with self.voiceover(
            "The first stage of reading a program is lexing: grouping its characters into tokens, the words of the "
            "language. <bookmark mark='a'/> In the Pebble language there are seven kinds, and each is a regular "
            "expression. White space and comments, which are read and thrown away. Numbers, character literals and "
            "strings. Names. And operators and punctuation, from single characters up to the two-character "
            "operators like arrow and double equals. <bookmark mark='b'/> Keywords like while and return are read "
            "as names and then looked up in a table, which keeps the automaton small."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.3), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(kw))
        self.wait(0.3)
        self.clear_scene()

    def munch(self):
        lx = load("lexer")
        head = label(r"Maximal munch: \ always take the longest token", font_size=34).to_edge(UP, buff=0.3)
        ex = VGroup()
        for m in lx["munch"]:
            src = Text(m["text"], font="DejaVu Sans Mono", font_size=24, color=GREY_A)
            arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, color=GREY_B, stroke_width=2)
            toks = VGroup()
            for t in m["tokens"]:
                c = FUNC if t in lx["keywords"] else (CODE if t[0].isalpha() else CTRL)
                r = RoundedRectangle(width=0.3 + 0.2 * len(t), height=0.5, corner_radius=0.06, stroke_color=c,
                                     stroke_width=1.5, fill_color=c, fill_opacity=0.12)
                toks.add(VGroup(r, Text(t, font="DejaVu Sans Mono", font_size=20, color=c).move_to(r)))
            toks.arrange(RIGHT, buff=0.1)
            ex.add(VGroup(src, arrow, toks).arrange(RIGHT, buff=0.3))
        ex.arrange_in_grid(3, 2, buff=(1.2, 0.45), col_alignments="ll").next_to(head, DOWN, buff=0.6)
        notes = VGroup(
            label(r"run all seven automata together; \ keep reading while any can still match; \ back up to the "
                  r"last place one accepted", font_size=20, color=GREY_A),
            label(r"ties go to the earlier rule: \ \texttt{while} is a keyword, \ \texttt{whiles} a name", font_size=20,
                  color=FUNC),
            label(rf"combined: \ {lx['nfa_states']} NFA states, \ a {lx['dfa_states']}-state DFA over the characters "
                  r"the Job uses", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where does one token end and the next begin? <bookmark mark='a'/> The rule every lexer uses is "
            "maximal munch: always take the longest token that matches. Greater-than followed by equals is one "
            "token, not two. Arrow is one token. <bookmark mark='b'/> And x minus minus greater-than y? The "
            "lexer takes x, then a minus, because no token starts minus minus; then the arrow, then y. Maximal munch "
            "is greedy, and sometimes surprising. <bookmark mark='c'/> When two rules match the same longest text, "
            "the earlier rule wins, so while is a keyword and whiles is a name. <bookmark mark='d'/> All seven "
            "rules can be run as one automaton: ninety-six NFA states, which the subset construction turns into a "
            "deterministic machine of thirty states over the characters the Job uses. That is what lex, from 1975, "
            "and its descendants generate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ex[0]), FadeIn(ex[1]))
            vo.wait_until("b")
            self.play(FadeIn(ex[4]), FadeIn(ex[5]))
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(ex[2]), FadeIn(ex[3]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def job(self):
        lx = load("lexer")
        head = label(r"The Job, \ lexed", font_size=36).to_edge(UP, buff=0.3)
        row = chips(lx["sample_tokens"], font_size=17, max_width=13).next_to(head, DOWN, buff=0.95)
        src = Text(lx["sample"], font="DejaVu Sans Mono", font_size=18, color=GREY_B).next_to(row, UP, buff=0.15)
        kinds = lx["kinds"]
        order = [("operator", r"operators", CTRL), ("ident", r"names", CODE), ("keyword", r"keywords", FUNC),
                 ("num", r"numbers and characters", HEAD)]
        mx = max(kinds.values())
        bars = VGroup()
        for k, name, c in order:
            v = kinds.get(k, 0) + (kinds.get("charlit", 0) if k == "num" else 0)
            bar = Rectangle(width=6.0 * v / mx, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.75)
            bars.add(VGroup(label(name, font_size=19, color=c), bar, label(str(v), font_size=19, color=GREY_A)))
        for b in bars:
            b[1].move_to([-1.6, 0, 0], aligned_edge=LEFT)
            b[0].next_to(b[1], LEFT, buff=0.3)
            b[2].next_to(b[1], RIGHT, buff=0.2)
        bars.arrange(DOWN, buff=0.22).next_to(row, DOWN, buff=0.7)
        for b in bars:
            b[1].align_to([-1.6, 0, 0], LEFT)
            b[0].next_to(b[1], LEFT, buff=0.3)
            b[2].next_to(b[1], RIGHT, buff=0.2)
        tot = label(rf"{lx['chars']:,} characters, \ {lx['lines']} lines \ $\to$ \ {lx['tokens']} tokens; \ about "
                    rf"{lx['chars_per_s'] / 1000:.0f},000 characters a second, \ in plain Python", font_size=21,
                    color=YES).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is the lexer on the Job. <bookmark mark='a'/> One line of the lookup function becomes a row of "
            "tokens, each with its kind: keywords, names, operators, punctuation. <bookmark mark='b'/> The whole "
            "program, two thousand two hundred and eighty-five characters on eighty-eight lines, becomes six "
            "hundred and fifty-one tokens, more than half of them operators and punctuation. <bookmark mark='c'/> "
            "From here on, the parser never sees a character, only tokens."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src), LaggedStart(*[FadeIn(c) for r in row for c in r], lag_ratio=0.05), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b[1], LEFT) for b in bars], lag_ratio=0.3),
                      *[FadeIn(b[0]) for b in bars], *[FadeIn(b[2]) for b in bars], run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(tot))
        self.wait(0.3)
        self.clear_scene()

    def indent(self):
        ind = load("indent")
        head = label(r"When a lexer needs a stack: \ Python's indentation", font_size=34).to_edge(UP, buff=0.3)
        src = code(ind["source"], size=18).to_edge(LEFT, buff=0.6).shift(UP * 0.9)
        sl = label(r"Python's own \texttt{tokenize} module, \ run here:", font_size=18, color=GREY_B).next_to(
            src, UP, buff=0.15).align_to(src, LEFT)
        lines = {}
        for t in ind["tokens"]:
            lines.setdefault(t["line"], []).append(t)
        rows = VGroup()
        for ln in sorted(lines):
            chipsrow = VGroup()
            for t in lines[ln]:
                special = t["kind"] in ("INDENT", "DEDENT", "NEWLINE")
                txt = t["kind"] if special else t["text"]
                c = {"INDENT": YES, "DEDENT": NO, "NEWLINE": GREY_C}.get(t["kind"], CODE if t["kind"] == "NAME"
                                                                          else CTRL)
                tx = Text(txt, font="DejaVu Sans Mono", font_size=13, color=c)
                r = RoundedRectangle(width=tx.width + 0.14, height=0.32, corner_radius=0.05, stroke_color=c,
                                     stroke_width=1.1, fill_color=c, fill_opacity=0.12)
                chipsrow.add(VGroup(r, tx.move_to(r)))
            chipsrow.arrange(RIGHT, buff=0.05)
            stk = lines[ln][-1]["stack"]
            rows.add(VGroup(chipsrow, Text("[" + ", ".join(map(str, stk)) + "]", font="DejaVu Sans Mono",
                                           font_size=13, color=HEAD)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(src, DOWN, buff=0.45).align_to(src, LEFT)
        if rows.width > 12.8:
            rows.scale_to_fit_width(12.8)
        side = VGroup(
            label(r"the lexer keeps a stack of indentation levels", font_size=19, color=HEAD),
            label(r"deeper: \ push, \ emit \texttt{INDENT}", font_size=19, color=YES),
            label(r"shallower: \ pop, \ emit one \texttt{DEDENT} per level", font_size=19, color=NO),
            label(r"the grammar then sees braces in disguise", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(src, RIGHT, buff=1.0).align_to(src, UP)
        with self.voiceover(
            "One famous language breaks the clean division of labour. <bookmark mark='a'/> In Python, blocks are "
            "marked by indentation, and indentation is nesting, which, as we saw, no finite automaton can track. "
            "<bookmark mark='b'/> So Python's lexer keeps a stack of indentation levels. When a line is indented "
            "further, it pushes the new level and emits an INDENT token; when a line is indented less, it pops, "
            "emitting one DEDENT for each level it leaves. <bookmark mark='c'/> Here is Python's own tokenizer, "
            "run on a small function: three INDENTs going in, three DEDENTs coming out. To the parser, INDENT and "
            "DEDENT are simply opening and closing braces."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(sl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in side], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=3)
        self.wait(0.3)
        self.clear_scene()
