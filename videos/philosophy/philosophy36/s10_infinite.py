from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


def cells_row(bits, x0, y, size=0.3, gap=0.06, color=INF, fade=True, highlight=()):
    g = VGroup()
    n = len(bits)
    for i, v in enumerate(bits):
        op = (1 - 0.85 * i / n) if fade else 1.0
        sq = Square(side_length=size, stroke_width=1.2, stroke_color=GREY_B, stroke_opacity=op,
                    fill_color=color if v else BLACK, fill_opacity=(0.85 * op if v else 0.0))
        if i in highlight:
            sq.set_stroke(WHITE, width=2.5, opacity=1)
        sq.move_to([x0 + i * (size + gap), y, 0])
        g.add(sq)
    return g


class Infinite(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Infinite ethics", r"Can we rank worlds with infinitely many lives?", lit=(1965, 2003),
                            part=PART)
        with self.voiceover("Chapter nine. Infinite ethics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.streams()
        self.theorem()
        self.responses()

    def streams(self):
        d = load("infinite")
        head = label(r"Infinite streams", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert (d["liminf_ab"], d["liminf_ba"]) == (0, -1)
        assert d["partial_diff"][:6] == [1, 0, 1, 0, 1, 0]
        n = 24
        ra = cells_row(d["a"][:n], -4.2, 1.5)
        rb = cells_row(d["b"][:n], -4.2, 0.7)
        la = label(r"$a$", font_size=24, color=INF).next_to(ra, LEFT, buff=0.3)
        lb = label(r"$b$", font_size=24, color=INF).next_to(rb, LEFT, buff=0.3)
        sums = VGroup(*[label(f"{v}", font_size=16, color=GOAL).move_to([-4.2 + i * 0.36, -0.1, 0])
                        for i, v in enumerate(d["partial_diff"][:n])])
        ls = MathTex(r"\textstyle\sum_{t \le T}(a_t - b_t)", font_size=24, color=GOAL).next_to(sums, LEFT, buff=0.3)
        rows = stack([(r"generation $t$ has welfare $a_t$ or $b_t$; \ the streams go on for ever", GREY_A),
                      (r"catching up \ (von Weizsäcker; \ Atsumi, \ 1965): \ $a \succeq b$ if the partial sums of "
                       r"$a - b$ end up $\ge 0$: \ here $a \succ b$", INF),
                      (r"yet $b$ is $a$ with its generations relabelled: \ an infinite permutation", BAD),
                      (r"anonymity for infinite permutations would make them equal: \ it must be weakened to finite "
                       r"ones", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=11.0, buff=0.22).move_to([0, -1.9, 0])
        with self.voiceover(
            "If the universe is infinite, or humanity's future has no end, our rankings must compare infinite "
            "streams of welfare. <bookmark mark='a'/>Here are two: a alternates one, zero, one, zero, for ever; b "
            "alternates zero, one. <bookmark mark='b'/>The catching-up criterion, from 1965, ranks a above b if the "
            "partial sums of their difference end up non-negative. They run one, zero, one, zero: a is never "
            "behind, and b is behind infinitely often, so a is better. <bookmark mark='c'/>But b is just a with its "
            "generations relabelled, each pair swapped: an infinite permutation. <bookmark mark='d'/>If everyone "
            "counts equally whatever their position, the two should be equal. So impartiality across generations "
            "must be weakened to finite permutations, and even that, it turns out, is too much to ask of a "
            "numerical measure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(ra), FadeIn(la))
            self.play(FadeIn(rb), FadeIn(lb))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in sums], lag_ratio=0.04), FadeIn(ls), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def theorem(self):
        d = load("infinite")
        head = label(r"Pareto against anonymity \ (Basu and Mitra, \ 2003)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert (d["r"], d["s"], d["m"], d["j"]) == (0.3, 0.45, 0, 1) and d["dominated_after_swap"]
        assert d["rationals"][:4] == ["1/2", "1/3", "2/3", "1/4"]
        assert [i for i in range(16) if d["x_s"][i] - d["swapped"][i] == 1] == [6, 13]
        assert (d["rationals"][6], d["rationals"][13]) == ("2/5", "3/7")
        n = 16
        x0 = -3.9
        qs = VGroup(*[MathTex(rf"\frac{{{q.split('/')[0]}}}{{{q.split('/')[1]}}}", font_size=26, color=GREY_A)
                      .move_to([x0 + i * 0.56, 2.3, 0]) for i, q in enumerate(d["rationals"][:n])])
        lq = MathTex(r"q_n", font_size=28, color=GREY_A).next_to(qs, LEFT, buff=0.35)
        rows = [("x(r)", d["x_r"], INF, ()), ("y(r)", d["y_r"], RISK, (d["m"],)),
                (r"y'(r)", d["swapped"], RISK, (d["m"], d["j"])), ("x(s)", d["x_s"], WELL, ())]
        grids, labs = VGroup(), VGroup()
        for k, (nm, bits, col, hl) in enumerate(rows):
            g = cells_row(bits[:n], x0, 1.55 - 0.62 * k, size=0.46, gap=0.1, color=col, fade=False, highlight=hl)
            grids.add(g)
            labs.add(MathTex(nm, font_size=28, color=col).next_to(g, LEFT, buff=0.35))
        steps = stack([(r"suppose $W$ assigns every infinite stream a real number, \ with strong Pareto and finite "
                        r"anonymity", GREY_A),
                       (r"enumerate the rationals in $(0, 1)$; \ for each real $r$: \ $x(r)_n = 1$ if $q_n < r$", INF),
                       (r"$y(r)$: \ $x(r)$ with one more 1: \ Pareto gives $W(x(r)) < W(y(r))$", RISK),
                       (r"for $r < s$: \ move that 1 into a place with $r \le q_n < s$ \ (finite anonymity): \ now "
                        r"below $x(s)$, \ so $W(y(r)) < W(x(s))$", RISK),
                       (r"so the intervals $(W(x(r)), W(y(r)))$ are disjoint, \ one for every real $r$: \ uncountably "
                        r"many, \ each holding its own rational: \ impossible", GOAL)],
                      font_size=18, aligned_edge=LEFT, width=12.0, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Kaushik Basu and Tapan Mitra proved in 2003 that two mild principles cannot both hold of any numerical "
            "measure of infinite streams. <bookmark mark='a'/>Suppose W gives every stream a real number, respects "
            "strong Pareto, so that a stream at least as good everywhere and better somewhere scores higher, and "
            "respects finite anonymity, so that swapping finitely many generations changes nothing. "
            "<bookmark mark='b'/>List the rational numbers between zero and one: a half, a third, two thirds, a "
            "quarter, and so on. For each real number r, let the stream x of r have a one at place n exactly when the "
            "n-th rational is below r. Here r is point three. <bookmark mark='c'/>Let y of r be x of r with one more "
            "one, at the first place whose rational is at least r. By Pareto, y of r scores more than x of r. "
            "<bookmark mark='d'/>Now take a larger s, here point four five. Move y's extra one into a place whose "
            "rational lies between r and s: a finite swap, so the score is unchanged. The swapped stream is below x "
            "of s everywhere, and strictly below where the rationals two fifths and three sevenths sit; so y of r "
            "scores less than x of s. <bookmark mark='e'/>So each real r owns an interval of scores, from x of r to y "
            "of r, and no two intervals overlap. Each contains a rational number of its own; but there are "
            "uncountably many reals and only countably many rationals. No such W exists."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(qs), FadeIn(lq), FadeIn(steps[1]))
            self.play(FadeIn(grids[0]), FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(FadeIn(grids[1]), FadeIn(labs[1]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(grids[3]), FadeIn(labs[3]))
            self.play(FadeIn(grids[2]), FadeIn(labs[2]), FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.clear_scene()

    def responses(self):
        head = label(r"After the theorem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"orderings, \ not numbers", r"Svensson \ (1980): \ complete orderings with both principles exist, \ "
                                             r"but only by the axiom of choice; \ Zame \ (2007): \ none can be written "
                                             r"down", INF),
                (r"weaker rankings", r"accept incompleteness: \ catching up and overtaking leave many pairs unranked",
                 GREY_A),
                (r"infinitarian paralysis", r"Bostrom \ (2011): \ if the world holds infinitely much good, \ no act "
                                            r"changes the total, \ and aggregative ethics seems to say nothing matters",
                 BAD),
                (r"new principles", r"Askell \ (2018); \ Wilkinson: \ rank by what each act changes, \ region by "
                                    r"region", WELL)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.2, x_text=-2.0, label_size=20, text_size=19)
        with self.voiceover(
            "What survives? <bookmark mark='a'/>Lars-Gunnar Svensson showed in 1980 that complete orderings with both "
            "principles exist, but only through the axiom of choice; William Zame showed in 2007 that none can be "
            "explicitly written down. <bookmark mark='b'/>So practical rankings, like catching up, accept "
            "incompleteness: many pairs of streams are simply not ranked. <bookmark mark='c'/>Nick Bostrom described "
            "infinitarian paralysis in 2011: if the world already contains infinitely much good and bad, no act "
            "changes the total, and an aggregative ethics seems to say that nothing we do matters. "
            "<bookmark mark='d'/>Amanda Askell and others have proposed principles that rank acts by the changes they "
            "make, region by region, rather than by totals. This is the part's second impossibility, beside "
            "Arrhenius's: impartiality, aggregation and infinity cannot all be kept."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
