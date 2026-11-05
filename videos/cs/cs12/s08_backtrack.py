from __future__ import annotations

import itertools
import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)


def compositions(n):
    for cuts in itertools.product([0, 1], repeat=n - 1):
        parts, cur = [], 1
        for c in cuts:
            if c:
                parts.append(cur)
                cur = 1
            else:
                cur += 1
        parts.append(cur)
        yield parts


class Backtrack(VoiceoverScene):
    def construct(self):
        self.card()
        self.how()
        self.measured()
        self.outages()
        self.backrefs()

    def card(self):
        card = chapter_card(7, r"Backtracking engines", r"Why is \texttt{(a+)+b} slow in Python and instant in grep?",
                            lit=(2007, 2019), extra=((2007, r"Cox: \ ``simple and fast''"),
                                                     (2019, r"the Cloudflare outage")), part=PART)
        with self.voiceover("Chapter seven. Backtracking engines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def how(self):
        head = label(r"A backtracker tries one possibility at a time", font_size=34).to_edge(UP, buff=0.3)
        pat = Text("(a+)+b   against   aaaa", font="DejaVu Sans Mono", font_size=26, color=CODE).next_to(
            head, DOWN, buff=0.35)
        n = 4
        rows = VGroup()
        for parts in compositions(n):
            g = VGroup()
            for p in parts:
                r = RoundedRectangle(width=0.42 * p + 0.04 * (p - 1), height=0.42, corner_radius=0.08,
                                     stroke_color=HEAD, stroke_width=1.6, fill_color=HEAD, fill_opacity=0.12)
                t = Text("a" * p, font="DejaVu Sans Mono", font_size=18, color=CODE).move_to(r)
                g.add(VGroup(r, t))
            g.arrange(RIGHT, buff=0.06)
            fail = label(r"then \texttt{b}? \ no", font_size=17, color=NO).next_to(g, RIGHT, buff=0.3)
            rows.add(VGroup(g, fail))
        rows.arrange_in_grid(4, 2, buff=(1.4, 0.25), col_alignments="ll").next_to(pat, DOWN, buff=0.45)
        expl = VGroup(
            label(r"the outer \texttt{+} may cut the $a$'s into groups in $2^{n-1}$ ways, \ and each one fails at the "
                  r"end", font_size=21, color=GREY_A),
            label(r"a backtracker cannot know they all fail the same way: \ it tries every one", font_size=21,
                  color=NO),
            label(r"an NFA simulation tries them all \textit{at once}: \ they are the same few states", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Python, Perl, Java, JavaScript and PCRE do not simulate an automaton. They backtrack. <bookmark "
            "mark='a'/> To match a plus, plus, then b, against four a's, the engine has to decide how the outer "
            "plus groups the a's. It tries one grouping, all four a's in one group, and then looks for a b. There "
            "is none, so it backs up and tries another grouping. <bookmark mark='b'/> There are two to the n minus "
            "one ways to cut n a's into groups, and every one of them fails in exactly the same place. <bookmark "
            "mark='c'/> The backtracker has no way to know that: it tries them all, one by one. <bookmark "
            "mark='d'/> Thompson's simulation follows every grouping at once, and they collapse into the same "
            "handful of states."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pat))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), FadeIn(expl[0]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(expl[1]))
            vo.wait_until("d")
            self.play(FadeIn(expl[2]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        b = load("blowup")
        head = label(r"Measured: \ steps and seconds", font_size=34).to_edge(UP, buff=0.3)
        rows = [r for r in b["ours"] if r["steps"]]
        ax = Axes(x_range=[0, 24, 4], y_range=[0, 8, 2], x_length=6.2, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.4)
        yl = VGroup(*[label(rf"$10^{v}$", font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in range(0, 9, 2)])
        xt = VGroup(*[label(str(n), font_size=14, color=GREY_B).next_to(ax.c2p(n, 0), DOWN, buff=0.08)
                      for n in range(4, 25, 4)])
        xl = label(r"$n$ \ (\texttt{a}'s)", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.35)
        bt = VMobject(color=NO, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], math.log10(r["steps"])) for r in rows])
        th = VMobject(color=YES, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], math.log10(r["thompson"])) for r in b["ours"]])
        btl = label(r"our backtracker: \ steps double per \texttt{a}", font_size=18, color=NO).next_to(
            ax.c2p(13, 6.6), UP, buff=0.0)
        thl = label(r"our NFA simulation: \ linear", font_size=18, color=YES).next_to(ax.c2p(14, 2.5), UP, buff=0.0)
        last = rows[-1]
        side = VGroup(
            label(rf"backtracker, \ $n = {last['n']}$: \ {last['steps']:,} steps", font_size=19, color=NO),
            label(r"Python \texttt{re}, \ $n = 28$: \ " + f"{[r for r in b['python'] if r['n'] == 28][0]['s']:.1f}"
                  r" s", font_size=19, color=NO),
            label(r"Perl, \ $n = 30$: \ instant: \ it caches positions \\ it has already tried, \ a patch for "
                  r"exactly this", font_size=19, color=CTRL),
            label(rf"GNU grep, \ $n = 10^6$: \ {b['grep'][-1]['s'] * 1000:.1f} ms \ (a DFA)", font_size=19,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, RIGHT, buff=0.6).shift(UP * 0.4)
        with self.voiceover(
            "We measured it. <bookmark mark='a'/> Our own backtracker, counting steps: they double with every a, "
            "past twenty-nine million at n equals twenty-two. Thompson's simulation on the same inputs grows in a "
            "straight line. <bookmark mark='b'/> Python's engine behaves like ours: eight seconds at twenty-eight. "
            "<bookmark mark='c'/> Perl answers instantly, because its engine remembers positions it has already "
            "tried in situations like this one: a patch added for exactly this problem, not a different algorithm. "
            "<bookmark mark='d'/> And GNU grep, which compiles the pattern to an automaton, handles a million a's "
            "in a millisecond and a half."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(xt), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(bt), FadeIn(btl), run_time=2)
            self.play(Create(th), FadeIn(thl))
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def outages(self):
        cf = load("cloudflare")
        head = label(r"Not exponential, \ and still fatal", font_size=34).to_edge(UP, buff=0.3)
        pat = VGroup(label(r"the heart of Cloudflare's rule:", font_size=21, color=GREY_A),
                     Text(".*.*=.*", font="DejaVu Sans Mono", font_size=30, color=HEAD)).arrange(RIGHT, buff=0.3)
        pat.next_to(head, DOWN, buff=0.35)
        why = label(r"on a line with no \texttt{=}: \ every start, \ every split between the two \texttt{.*}: \ "
                    r"$\sim n^3$ tries", font_size=21, color=GREY_A).next_to(pat, DOWN, buff=0.2)
        rows = [[f"{r['n']:,}", f"{r['python']:.2f} s" if r["python"] is not None else "—",
                 f"{1000 * r['grep']:.2f} ms"] for r in cf["rows"]]
        t = grid_table([r"characters", r"Python \texttt{re}", r"GNU grep"], rows, [2.6, 2.8, 2.8], row_h=0.5,
                       font_size=21, colors=[[GREY_A, NO, YES]] * len(rows), mono_cols=()).next_to(why, DOWN,
                                                                                                    buff=0.4)
        x8 = label(r"double the line, \ $\times 8$ the time", font_size=20, color=NO).next_to(t, DOWN, buff=0.2)
        more = VGroup(
            label(r"20 July 2016: \ Stack Overflow down for 34 minutes: \ trimming spaces from a post with 20,000 "
                  r"of them \ (quadratic)", font_size=19, color=GREY_A),
            label(r"Russ Cox, \ 2007: \ ``Regular expression matching can be simple and fast'' \ $\to$ \ RE2, \ "
                  r"Go's and Rust's engines: \ automata, \ guaranteed linear", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Cloudflare rule was not even exponential. <bookmark mark='a'/> At its heart was dot star, dot "
            "star, equals, dot star. On a line with no equals sign, a backtracker tries every starting point and "
            "every way of dividing the line between the two dot stars: about n cubed attempts. <bookmark mark='b'/> "
            "On this computer, Python takes a tenth of a second on a thousand characters, and nearly a minute on "
            "eight thousand: double the line, eight times the time. grep does not notice. <bookmark mark='c'/> "
            "Three years earlier, Stack Overflow went down for thirty-four minutes because a regular expression "
            "that trimmed white space met a post containing twenty thousand spaces. <bookmark mark='d'/> In 2007 "
            "Russ Cox wrote the article that brought Thompson's method back into fashion, and his RE2 library, "
            "like the regular expression engines of Go and Rust, uses automata and guarantees linear time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pat), FadeIn(why))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.4),
                      run_time=3)
            self.play(FadeIn(x8))
            vo.wait_until("c")
            self.play(FadeIn(more[0]))
            vo.wait_until("d")
            self.play(FadeIn(more[1]))
        self.wait(0.3)
        self.clear_scene()

    def backrefs(self):
        pr = load("primes")
        head = label(r"Why backtrackers survive: \ back-references", font_size=34).to_edge(UP, buff=0.3)
        pat = VGroup(Text(r"(11+)\1+", font="DejaVu Sans Mono", font_size=32, color=HEAD),
                     label(r"a group of two or more 1's, \ then the \textit{same} group, \ again and again",
                           font_size=21, color=GREY_A)).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.4)
        cells = VGroup()
        for r in pr["rows"][:38]:
            k = r["k"]
            c = NO if r["composite"] else YES
            sq = Square(side_length=0.5, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.25)
            cells.add(VGroup(sq, label(str(k), font_size=16, color=WHITE).move_to(sq)))
        cells.arrange_in_grid(3, 13, buff=0.1).next_to(pat, DOWN, buff=0.45)
        leg = label(r"matches $1^k$ exactly when $k$ is composite: \ red matched, \ green did not --- \ the primes",
                    font_size=20, color=GREY_A).next_to(cells, DOWN, buff=0.25)
        pts = VGroup(
            label(r"\texttt{\textbackslash 1} must repeat what the group matched: \ no finite automaton can "
                  r"remember that", font_size=20, color=GREY_A),
            label(r"matching with back-references is NP-complete \ (Aho, \ 1990): \ no fast algorithm is known for "
                  r"any engine", font_size=20, color=NO),
            label(r"so: \ automata when you can, \ backtracking only when the pattern needs it", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why does anyone backtrack, then? <bookmark mark='a'/> Because practical regular expressions can do "
            "things regular expressions cannot. This one says: a group of two or more ones, then the same group, "
            "repeated. <bookmark mark='b'/> Run on k ones, it matches exactly when k can be split into equal groups "
            "of two or more, that is, when k is composite. It is a primality test. <bookmark mark='c'/> A back "
            "reference must repeat exactly what an earlier group matched, which no finite automaton can remember, "
            "so this is not a regular language at all. <bookmark mark='d'/> And matching with back-references is "
            "NP-complete, as Alfred Aho showed: no engine of any kind is known to do it fast. <bookmark mark='e'/> "
            "The modern answer is to use an automaton whenever the pattern allows it, and to backtrack only when "
            "it must."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pat))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.04), FadeIn(leg), run_time=3)
            for mk, p in zip("cde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
