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
            label("a naive backtracker revisits these partitions; real engines may optimize them away", font_size=21,
                  color=NO),
            label(r"an NFA simulation tries them all \textit{at once}: \ they are the same few states", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Many familiar regex engines use backtracking, with optimizations that vary by engine and pattern. "
            "<bookmark mark='a'/> Our deliberately simple matcher tries ways of partitioning four a's among the "
            "repeated groups of parenthesized a-plus, followed by b. With no b, each completed partition fails. "
            "<bookmark mark='b'/> For n positive a's there are two to the n minus one partitions into nonempty "
            "consecutive groups: choose a cut or no cut at each gap. <bookmark mark='c'/> A naive backtracker can "
            "revisit these possibilities one by one. This explains an exponential failure mode; it does not say "
            "every real engine explores every partition for every expression. <bookmark mark='d'/> Thompson's "
            "simulation instead merges paths that reach the same state at the same input position. Many possible "
            "histories collapse into a bounded set of active states."
        )
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
        thl = label("NFA active-set proxy", font_size=18, color=YES).next_to(ax, DOWN, buff=.8).align_to(ax, LEFT)
        last = rows[-1]
        side = VGroup(
            label(rf"backtracker, \ $n = {last['n']}$: \ {last['steps']:,} steps", font_size=19, color=NO),
            label(r"Python \texttt{re}, \ $n = 28$: \ " + f"{[r for r in b['python'] if r['n'] == 28][0]['s']:.1f}"
                  r" s", font_size=19, color=NO),
            label(rf"Perl, $n={b['perl'][-1]['n']}$: {1e6*b['perl'][-1]['s']:.0f} microseconds"
                  r" \\ optimization on this case; not a universal bound", font_size=19, color=CTRL),
            label(rf"GNU grep adjusted, \ $n = 10^6$: \ {b['grep'][-1]['s'] * 1000:.1f} ms \ (a DFA)", font_size=19,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, RIGHT, buff=0.6).shift(UP * 0.4)
        with self.voiceover(
            (
            "The counters and timings show different aspects of the same failing pattern. <bookmark mark='a'/> "
            "Our deliberately naive backtracker counts more than twenty-nine million steps at length twenty-two, "
            "while the NFA active-set counter grows linearly. That counter is a work proxy, not an instruction "
            "count. <bookmark mark='b'/> The displayed Python measurements also show rapid growth; their seconds "
            "belong to this host and engine version. <bookmark mark='c'/> Perl is fast on this case because its "
            "optimizations avoid much of the naive search. This observation gives no linear guarantee for every "
            "Perl pattern. <bookmark mark='d'/> GNU grep handles the million-character input efficiently here. "
            "Its baseline-subtracted estimate is noisy, especially near zero. Compare the trend and the execution "
            "strategy, rather than treating any one duration as a universal constant."
        )
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
        pat = VGroup(label("simplified overlapping-repetition experiment:", font_size=21, color=GREY_A),
                     Text(".*.*=.*", font="DejaVu Sans Mono", font_size=30, color=HEAD)).arrange(RIGHT, buff=0.3)
        pat.next_to(head, DOWN, buff=0.35)
        why = label("unanchored naive search, no equals sign: starting positions and overlapping splits give cubic work", font_size=21, color=GREY_A).next_to(pat, DOWN, buff=0.2)
        rows = [[f"{r['n']:,}", f"{r['python']:.2f} s" if r["python"] is not None else "timeout at 60 s",
                 f"{1000 * r['grep']:.2f} ms"] for r in cf["rows"]]
        t = grid_table([r"characters", r"Python \texttt{re}", r"grep adjusted"], rows, [2.6, 2.8, 2.8], row_h=0.5,
                       font_size=21, colors=[[GREY_A, NO, YES]] * len(rows), mono_cols=()).next_to(why, DOWN,
                                                                                                    buff=0.4)
        x8 = label("cubic trend on uncensored samples; timeout denotes a waiting limit", font_size=20, color=NO).next_to(t, DOWN, buff=0.2)
        more = VGroup(
            label(r"20 July 2016: \ Stack Overflow down for 34 minutes: \ trimming spaces from a post with 20,000 "
                  r"of them \ (quadratic)", font_size=19, color=GREY_A),
            label("Cox (2007), RE2: automata and linear input time for fixed supported patterns", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover("Polynomial search can also exhaust a service. <bookmark mark='a'/> Our simplified pattern is dot-star, dot-star, equals, dot-star, searched without anchoring in text lacking equals. A naive search explores starting positions and overlapping splits, giving cubic growth for this experiment. This is an illustration of the outage mechanism, not a claim that every engine executes the original rule identically. <bookmark mark='b'/> Read the measured Python durations and any timeout limits in the table. The GNU grep column is a noisy baseline-subtracted comparison. <bookmark mark='c'/> Stack Overflow's 2016 whitespace-regex outage supplies another example of a small rule interacting badly with long input. <bookmark mark='d'/> Automata engines such as RE2 offer linear input-time guarantees for fixed supported patterns. Pattern size, compilation, memory limits and supported features still matter; backreferences are outside RE2's supported language.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pat), FadeIn(why), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.4), run_time=3)
            self.play(FadeIn(x8))
            vo.wait_until('c')
            self.play(FadeIn(more[0]))
            vo.wait_until('d')
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
            label("general backreferences can compare unbounded substrings and describe nonregular languages", font_size=20, color=GREY_A),
            label("backreference matching: NP-complete with both pattern and text as inputs (combined complexity)", font_size=20, color=NO),
            label("choose features, semantics and resource bounds; backtracking is one execution strategy", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover("Why retain backtracking engines? Their features and matching semantics can be useful, but some features go beyond regular languages. <bookmark mark='a'/> This whole-string matcher captures at least two ones and then repeats exactly that captured group. <bookmark mark='b'/> For unary strings of length k at least two, it matches precisely the composite lengths: k has at least two equal groups, each of size at least two. Handle zero and one separately before calling its negation a primality test. <bookmark mark='c'/> A backreference can require an arbitrarily long earlier substring to recur. General backreference patterns can therefore describe nonregular languages; this does not mean every pattern containing one is nonregular. <bookmark mark='d'/> With both the pattern and text supplied as inputs, matching standard backreference expressions is NP-complete. This combined-complexity statement is not a lower bound for every fixed pattern. <bookmark mark='e'/> Choose an engine by its supported features, semantics and resource guarantees. Backtracking is one implementation choice, not the definition of every extended regex language.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pat), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.04), FadeIn(leg), run_time=3)
            for mk, p in zip('cde', pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
