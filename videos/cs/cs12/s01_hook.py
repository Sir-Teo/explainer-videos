from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, chips, code, load, region)


class Hook(VoiceoverScene):
    def construct(self):
        self.outage()
        self.reading()
        self.preview()
        self.plan()

    # ------------------------------------------------------------------
    def outage(self):
        b = load("blowup")
        cf = load("cloudflare")
        head = label(r"Six characters that stop a computer", font_size=36).to_edge(UP, buff=0.35)
        pat = Text("(a+)+b", font="DejaVu Sans Mono", font_size=40, color=HEAD).next_to(head, DOWN, buff=0.4)
        sub = label(r"matched against \texttt{aaa\dots a}, \ with no \texttt{b}: \ the answer is ``no''", font_size=22,
                    color=GREY_A).next_to(pat, DOWN, buff=0.2)
        rows = [r for r in b["python"] if r["s"] is not None]
        ax = Axes(x_range=[13, 29, 2], y_range=[0, 5.5, 1], x_length=6.0, y_length=3.4, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(LEFT, buff=1.0).shift(DOWN * 1.2)
        ylab = VGroup(*[label(t, font_size=14, color=GREY_B).next_to(ax.c2p(13, v + 4), LEFT, buff=0.12)
                        for v, t in ((-3, r"1 ms"), (-1, r"0.1 s"), (0, r"1 s"), (1, r"10 s"))])
        xl = label(r"number of \texttt{a}'s", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        xt = VGroup(*[label(str(n), font_size=14, color=GREY_B).next_to(ax.c2p(n, 0), DOWN, buff=0.1)
                      for n in range(14, 29, 4)])
        import math
        pts = [ax.c2p(r["n"], math.log10(r["s"]) + 4) for r in rows]
        py = VMobject(color=NO, stroke_width=4).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.05, color=NO) for p in pts])
        pyl = label(r"Python's \texttt{re}: \ ${\times}4$ per two \texttt{a}'s", font_size=19, color=NO).next_to(
            pts[-1], LEFT, buff=0.25).shift(UP * 0.2)
        g = b["grep"][-1]
        gl = label(rf"GNU grep, \ a million \texttt{{a}}'s: \ {g['s'] * 1000:.1f} ms", font_size=19, color=YES)
        gl.next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        last = rows[-1]
        big = label(rf"{last['n']} \texttt{{a}}'s: \ {last['s']:.1f} s; \ 30: \ over 30 s", font_size=19,
                    color=NO).next_to(gl, DOWN, buff=0.35).align_to(gl, LEFT)
        cfl = VGroup(label(r"2 July 2019: \ Cloudflare", font_size=22, color=HEAD),
                     label(r"one new firewall rule containing \texttt{.*(?:.*=.*)}", font_size=18, color=GREY_A),
                     label(r"every CPU serving its web traffic, \ worldwide, \\ at 100\% \ for 27 minutes",
                           font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(big, DOWN, buff=0.45)
        cfl.align_to(gl, LEFT)
        with self.voiceover(
            "Here are six characters: a pattern. One or more a's, repeated one or more times, then a b. <bookmark "
            "mark='a'/> Ask Python whether a string of a's, with no b, matches it. The answer is obviously no. "
            "<bookmark mark='b'/> But the time it takes to say no, measured on this computer, multiplies by four "
            "for every two more a's. Twenty-eight a's take eight seconds; thirty take longer than we were willing "
            "to wait. <bookmark mark='c'/> GNU grep answers the same question for a million a's in about a "
            "millisecond. <bookmark mark='d'/> This is not a curiosity. On the second of July 2019, Cloudflare "
            "deployed one new rule to its web firewall. It contained a regular expression of this kind, and for "
            "twenty-seven minutes every processor serving its traffic, around the world, was at full load, trying "
            "to match it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pat))
            vo.wait_until("a")
            self.play(FadeIn(sub), Create(ax), FadeIn(ylab), FadeIn(xl), FadeIn(xt))
            vo.wait_until("b")
            self.play(Create(py), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2), run_time=3)
            self.play(FadeIn(pyl), FadeIn(big))
            vo.wait_until("c")
            self.play(FadeIn(gl))
            vo.wait_until("d")
            self.play(FadeIn(cfl, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reading(self):
        lx = load("lexer")
        pb = load("pebble")
        head = label(r"Before a compiler can translate a program, \ it has to read it", font_size=32).to_edge(
            UP, buff=0.35)
        src = code(["fn lookup(w: *char, n: int) -> *Node {", "    var p: *Node = head;", "    while p != null {",
                    "        if p.length == n && same(p.letters, w, n) { return p; }", "        p = p.next;",
                    "    }", "    ..."], size=18).next_to(head, DOWN, buff=0.45)
        sl = label(r"the Job, \ in the Pebble language: \ 88 lines", font_size=18, color=GREY_B).next_to(src, UP,
                                                                                                  buff=0.1)
        sl.align_to(src, LEFT)
        toks = chips(lx["sample_tokens"], font_size=15, max_width=12.5).next_to(src, DOWN, buff=0.5)
        tl = label(rf"characters into tokens: \ {lx['chars']:,} characters, \ {lx['tokens']} tokens \ "
                   r"(regular expressions)", font_size=19, color=CTRL).next_to(toks, DOWN, buff=0.25)
        trl = label(rf"tokens into a tree: \ {pb['nodes']} nodes \ (a grammar)", font_size=19, color=YES).next_to(
            tl, DOWN, buff=0.15)
        with self.voiceover(
            "And this part has a job of its own to do. <bookmark mark='a'/> Here is the Job again, written this "
            "time in a programming language: the Pebble language, which we design in this part and compile in "
            "the next. Before any compiler can translate it, something has to read it. <bookmark mark='b'/> First "
            "its characters are grouped into words, called tokens, and the rules for tokens are regular "
            "expressions. <bookmark mark='c'/> Then the tokens are fitted to a grammar, which turns a flat list "
            "into a tree. Both steps rest on one of the most beautiful theories in computer science: languages, and "
            "the machines that recognize them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(sl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for row in toks for c in row], lag_ratio=0.04), FadeIn(tl), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(trl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"regular expressions, \ finite automata, \ and the constructions that join them", font_size=27,
                  color=DATA),
            label(r"why \texttt{(a+)+b} is slow in Python and instant in grep", font_size=27, color=NO),
            label(r"what no finite machine can recognize, \ and the stack that fixes it", font_size=27, color=CTRL),
            label(r"grammars, \ and four ways to parse them", font_size=27, color=YES),
            label(r"the Pebble language: \ its lexer, \ its grammar, \ its parser", font_size=27, color=FUNC),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where we are going. <bookmark mark='a'/> Regular expressions and finite automata, and the "
            "constructions that turn each into the other. <bookmark mark='b'/> Why one pattern is instant in grep "
            "and exponential in Python. <bookmark mark='c'/> What no finite machine can ever recognize, with a "
            "proof, and the single stack that fixes it. <bookmark mark='d'/> Grammars, and four ways to parse "
            "them, from top down and from bottom up. <bookmark mark='e'/> And the Pebble language itself: its "
            "lexer, its grammar, and its parser, run on the Job."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Languages and Automata", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"languages as sets of strings; \ recognition and parsing",
            r"regular expressions, \ NFAs, \ DFAs: \ Thompson, \ subsets, \ minimization, \ Kleene",
            r"the pumping lemma; \ backtracking engines and their blow-up",
            r"lexing; \ context-free grammars, \ ambiguity, \ pushdown automata",
            r"CYK, \ Earley, \ LL(1), \ Pratt, \ LR(0), \ SLR, \ LALR, \ LR(1)",
            r"the Pebble language parsed; \ how fast parsing can be",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 12 of Computer Science, Built, in Act Three, Speaking to the Machine. <bookmark "
            "mark='a'/> In this part: languages as sets of strings, and the difference between recognizing and "
            "parsing. Regular expressions and finite automata, with Thompson's construction, the subset "
            "construction, minimization and Kleene's theorem. The pumping lemma, and backtracking engines with their "
            "blow-up. Lexing, context-free grammars, ambiguity and pushdown automata. Seven parsing algorithms. "
            "And the Pebble language, parsed, with the open question of how fast parsing can ever be."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
