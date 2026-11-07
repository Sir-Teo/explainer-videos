from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.ai.ai1.compute import BOOKS
from videos.cs.cs60.compute import load as load60
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'thirty-three')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))


def say1(x: float) -> str:
    """A number with one decimal, spoken: 'six point seven'."""
    whole, tenth = divmod(int(round(10 * x)), 10)
    return say(whole) + ("" if tenth == 0 else " point " + _ONES[tenth])


# ---------------------------------------------------------------------------
# Three towers, one floor per part
# ---------------------------------------------------------------------------
YB, H = -2.5, 4.85                     # bottom of every tower, and its height
TOWERS = {  # key: (parts, x, width, colour, name, acts as (first, last) part ranges)
    "ai": (31, -5.4, 1.0, LAM, r"\textit{AI, Built}",
           ((1, 5), (6, 12), (13, 19), (20, 25), (26, 29), (30, 31))),
    "cs": (61, 0.0, 1.1, DATA, r"\textit{Computer Science, Built}",
           ((1, 6), (7, 10), (11, 15), (16, 24), (25, 30), (31, 35), (36, 39), (40, 44), (45, 50), (51, 55),
            (56, 61))),
    "an": (10, 5.4, 1.0, YES, r"\textit{Analysis, Built}", tuple((k, k) for k in range(1, 11))),
}
# (this series' part, the other series' part, which tower, topic, where the topic sits along the bridge, caption)
AI_BRIDGES = [
    (23, 11, "ai", r"gradient descent", 0.5,
     r"Part 23: \ gradient descent against Newton's method \quad$\longleftrightarrow$\quad \textit{AI, Built} Part 11: "
     r"\ momentum, \ Adam and the schedules that train every network"),
    (57, 8, "ai", r"generalization", 0.3,
     r"Part 57: \ PAC learning and the VC dimension \quad$\longleftrightarrow$\quad \textit{AI, Built} Part 8: \ VC, "
     r"\ Rademacher complexity, \ double descent"),
    (60, 17, "ai", r"silicon", 0.66,
     r"Part 60: \ a systolic array on the roofline \quad$\longleftrightarrow$\quad \textit{AI, Built} Part 17: \ GPUs, "
     r"\ tiling and arithmetic intensity on the same roofline"),
    (28, 1, "ai", r"information", 0.5,
     r"Part 28: \ Shannon's channel theorem \ (1948), \ proved with typical sets \quad$\longleftrightarrow$\quad "
     r"\textit{AI, Built} Part 1: \ entropy, \ typical sets, \ cross-entropy"),
]
AN_BRIDGES = [
    (1, 1, "an", r"the real numbers", 0.5,
     r"Part 1: \ Turing's \textit{computable numbers} \ (1936) \quad$\longleftrightarrow$\quad \textit{Analysis, "
     r"Built} Part 1: \ the reals, \ and Cantor's diagonal: \ machines are countable, \ the reals are not"),
    (19, 9, "an", r"Fourier", 0.75,
     r"Part 19: \ the FFT \ (Cooley and Tukey, \ 1965) \quad$\longleftrightarrow$\quad \textit{Analysis, Built} "
     r"Part 9: \ the Fourier transform; \ the FFT computes it on a finite cycle of points"),
    (52, 2, "an", r"convergence", 0.25,
     r"Part 52: \ Newton's method and error bounds \quad$\longleftrightarrow$\quad \textit{Analysis, Built} Part 2: "
     r"\ Cauchy sequences, \ Taylor's remainder, \ how fast a limit is reached"),
]
SETTLED = interpolate_color(ManimColor(HEAD), ManimColor(GREY_B), 0.45)  # a bridge once it is no longer the current one
EXTRA = [(18, 5), (20, 3), (54, 25)]   # more crossings to AI, Built, drawn dashed in the last section


def floor_y(n: int, k: int) -> float:
    return YB + (k - 0.5) * H / n


def series_tower(key: str) -> VGroup:
    """One tower: a floor for each part, acts in alternating shades; ``.floors[k - 1]`` is part k."""
    n, x, w, col, name, acts = TOWERS[key]
    h = H / n
    floors = VGroup()
    for k in range(1, n + 1):
        act = next(i for i, (a, b) in enumerate(acts) if a <= k <= b)
        op = 0.22 if act % 2 == 0 else 0.42
        floors.add(Rectangle(width=w, height=h * 0.8, stroke_width=0.6, stroke_color=col, fill_color=col,
                             fill_opacity=op).move_to([x, floor_y(n, k), 0]))
    title = label(name, font_size=21, color=col).next_to(floors, UP, buff=0.15)
    count = label(rf"{n} parts", font_size=17, color=GREY_B).next_to(floors, DOWN, buff=0.12)
    g = VGroup(floors, title, count)
    g.floors, g.key = floors, key
    return g


def bridge(spec) -> VGroup:
    """A bridge from this series' floor to the other's: a part number at each end, a line, and the topic."""
    cs_part, other, key, topic, frac, _ = spec
    n_cs, _, w_cs, _, _, _ = TOWERS["cs"]
    n_o, x_o, w_o, col_o, _, _ = TOWERS[key]
    side = -1 if x_o < 0 else 1
    y1, y2 = floor_y(n_cs, cs_part), floor_y(n_o, other)
    t1 = label(rf"{cs_part}", font_size=17, color=DATA).move_to([side * (w_cs / 2 + 0.24), y1, 0])
    t2 = label(rf"{other}", font_size=17, color=col_o).move_to([x_o - side * (w_o / 2 + 0.24), y2, 0])
    a = t1.get_left() if side < 0 else t1.get_right()
    b = t2.get_right() if side < 0 else t2.get_left()
    line = Line(a + side * RIGHT * 0.08, b - side * RIGHT * 0.08, color=HEAD, stroke_width=3)
    tp = label(topic, font_size=17, color=HEAD)
    tp.add_background_rectangle(color=BG, opacity=1, buff=0.05)
    tp.move_to(line.point_from_proportion(frac))
    g = VGroup(line, t1, t2, tp)
    g.line, g.tags, g.topic, g.spec = line, VGroup(t1, t2), tp, spec
    return g


def towers_with(bridges, towers, settled=True):
    """Bridges drawn in their settled (not current) colours, with their floors lit."""
    out = VGroup()
    for spec in bridges:
        b = bridge(spec)
        if settled:
            settle(b)
        towers["cs"].floors[spec[0] - 1].set_fill(DATA, opacity=0.95)
        towers[spec[2]].floors[spec[1] - 1].set_fill(TOWERS[spec[2]][3], opacity=0.95)
        out.add(b)
    return out


def settle(b: VGroup) -> VGroup:
    b.line.set_stroke(color=SETTLED, width=2.2)
    b.topic[1].set_color(GREY_A)
    return b


def card_box(title: str, body: str, color, w=4.0, h=2.15) -> VGroup:
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=1.8,
                         fill_color=color, fill_opacity=0.08)
    t = label(title, font_size=21, color=color)
    bd = wrapped_label(body, w - 0.35, font_size=18, color=WHITE)
    VGroup(t, bd).arrange(DOWN, buff=0.18).move_to(r)
    return VGroup(r, t, bd)


JOB = load60("job")["job"]
NBYTES = JOB["bytes"]
NWORDS = JOB["lanes"][0]["words"]
TITLES = list(BOOKS.values())


class Bridges(VoiceoverScene):
    def construct(self):
        self.card()
        self.shelf()
        self.towers()
        self.descent()
        self.web()

    def card(self):
        card = chapter_card(10, r"Where the series meet",
                            r"What does computer science share with learning, \ and with analysis?",
                            lit=(1936, 1948), part=PART)
        with self.voiceover("Chapter ten. Where the series meet."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def shelf(self):
        head = label(r"Three series, \ one shelf", font_size=36).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(61)
        tints = [DATA, LAM, YES, HEAD, KERN, GREY_B]
        spines = VGroup()
        for i in range(len(TITLES)):
            hgt = rng.uniform(1.0, 1.45)
            c = tints[i % len(tints)]
            spines.add(Rectangle(width=0.3, height=hgt, stroke_width=1, stroke_color=c, fill_color=c,
                                 fill_opacity=rng.uniform(0.25, 0.5)))
        spines.arrange(RIGHT, buff=0.05, aligned_edge=DOWN).move_to([0, 1.75, 0])
        board = Line(spines.get_corner(DL) + LEFT * 0.2, spines.get_corner(DR) + RIGHT * 0.2, color=GREY_C,
                     stroke_width=3)
        cap = label(rf"the {len(TITLES)} novels of \textit{{AI, Built}} Part 1: \ \textit{{{TITLES[0]}}} \ldots\ "
                    rf"\textit{{{TITLES[-1]}}}", font_size=19, color=GREY_A).next_to(board, DOWN, buff=0.15)
        ai = card_box(r"\textit{AI, Built} \ (31 parts)",
                      r"trains its models on them, \ and scores each on a passage they never saw: \ "
                      r"\textit{The Maltese Falcon}, \ chapter 2", LAM)
        cs = card_box(r"\textit{Computer Science, Built} \ (61 parts)",
                      rf"the Job counts their {NBYTES:,} bytes: \ {NWORDS:,} words, \ and lists the twenty most "
                      r"common", DATA)
        an = card_box(r"\textit{Analysis, Built} \ (10 parts)",
                      r"reads no novels; \ it proves the theorems the other two lean on, \ from the real numbers to "
                      r"the spectral theorem", YES)
        VGroup(ai, cs, an).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.45)
        a1 = Arrow(cap.get_bottom() + LEFT * 2.0, ai[0].get_top(), buff=0.1, color=LAM, stroke_width=2.5)
        a2 = Arrow(cap.get_bottom(), cs[0].get_top(), buff=0.1, color=DATA, stroke_width=2.5)
        with self.voiceover(
            "This series has two older siblings: AI, Built, thirty-one parts on how machines learn, and Analysis, "
            "Built, ten parts on the mathematics of limits, from the real numbers to the spectral theorem. "
            "<bookmark mark='a'/> They share more than a style. These are the thirty novels that AI, Built's first "
            "part chose, from Pride and Prejudice to Ulysses. <bookmark mark='b'/> AI, Built trains its models on "
            "them, and scores every model on a passage none of them was trained on. <bookmark mark='c'/> This "
            f"series' Job counts their words: about {say(round(NBYTES / 1e6))} million bytes, about "
            f"{say1(NWORDS / 1e6)} million words, from Part 6's Pebble to Part 60's circuit. "
            "<bookmark mark='d'/> Analysis, Built reads no novels at all, but it proves the theorems that the other "
            "two keep leaning on."
        ) as vo:
            self.play(FadeIn(head), Create(board),
                      LaggedStart(*[GrowFromEdge(s, DOWN) for s in spines], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cap), Indicate(spines, color=HEAD, scale_factor=1.02))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(ai, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(GrowArrow(a2), FadeIn(cs, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(an, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def light(self, towers, spec, caption, old=None):
        """Light one bridge: its two floors, the line, the numbers, the topic; settle the previous one."""
        b = bridge(spec)
        cs_f = towers["cs"].floors[spec[0] - 1]
        o_f = towers[spec[2]].floors[spec[1] - 1]
        anims = [cs_f.animate.set_fill(HEAD, opacity=0.95), o_f.animate.set_fill(HEAD, opacity=0.95)]
        if old is not None:
            ob, of1, of2, ocol = old
            anims += [ob.line.animate.set_stroke(color=SETTLED, width=2.2),
                      ob.topic[1].animate.set_color(GREY_A), of1.animate.set_fill(DATA, opacity=0.95),
                      of2.animate.set_fill(ocol, opacity=0.95)]
        self.play(*anims, run_time=0.5)
        self.play(Create(b.line), FadeIn(b.tags), run_time=0.9)
        new_cap = wrapped_label(spec[5], 12.6, font_size=19, color=WHITE).to_edge(DOWN, buff=0.25)
        if caption[0] is None:
            self.play(FadeIn(b.topic), FadeIn(new_cap), run_time=0.6)
        else:
            self.play(FadeIn(b.topic), FadeOut(caption[0]), FadeIn(new_cap), run_time=0.6)
        caption[0] = new_cap
        return (b, cs_f, o_f, TOWERS[spec[2]][3])

    def towers(self):
        head = label(r"Where the towers touch", font_size=36).to_edge(UP, buff=0.3)
        tw = {k: series_tower(k) for k in TOWERS}
        caption = [None]
        with self.voiceover(
            "Draw the three series as towers, one floor for each part: AI, Built on the left, this series in the "
            "middle, Analysis, Built on the right. <bookmark mark='a'/> The first bridge is the one every model "
            "crosses. Part 23 set gradient descent against Newton's method; AI, Built's Part 11 trains every network "
            "with descendants of that step: momentum, Adam, and learning-rate schedules. <bookmark mark='b'/> Part "
            "57 asked when learning is possible at all, with PAC bounds and the VC dimension; AI, Built's Part 8 asks "
            "the same question of real models, with Rademacher complexity and double descent. <bookmark mark='c'/> "
            "Part 60 built a systolic array and put it on the roofline; AI, Built's Part 17 puts GPUs on the same "
            "roofline, and tiles matrix products to climb it. <bookmark mark='d'/> And Shannon's paper of 1948 sits "
            "under both. Part 28 proved his channel theorem with typical sets; AI, Built's first part met the same "
            "typical sets on the way to cross-entropy, the loss every language model is trained on."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(t[1:]) for t in tw.values()],
                      *[LaggedStart(*[FadeIn(f) for f in t.floors], lag_ratio=0.02) for t in tw.values()],
                      run_time=2.5)
            old = None
            for mk, spec in zip("abcd", AI_BRIDGES):
                vo.wait_until(mk)
                old = self.light(tw, spec, caption, old)
        with self.voiceover(
            "On the other side stands analysis. <bookmark mark='a'/> The lowest bridge is the oldest. Turing's paper "
            "of 1936 was called On Computable Numbers: a real number is computable if a machine can write out its "
            "digits. Analysis, Built's first part builds the real numbers and proves, with Cantor's diagonal, that "
            "they are uncountable. Machines can be listed, so almost every real number is one that no machine can "
            "write. <bookmark mark='b'/> Part 19's fast Fourier transform, from Cooley and Tukey in 1965, computes "
            "the Fourier transform of Analysis, Built's Part 9, taken on a finite cycle of points instead of the "
            "whole line. <bookmark mark='c'/> And Part 52's iterations, Newton's method above all, converge for the "
            "reasons Analysis, Built's Part 2 proves: Cauchy sequences, and Taylor's theorem with its remainder, "
            "which also says how fast."
        ) as vo:
            for mk, spec in zip("abc", AN_BRIDGES):
                vo.wait_until(mk)
                old = self.light(tw, spec, caption, old)
            ob, of1, of2, ocol = old
            self.play(ob.line.animate.set_stroke(color=SETTLED, width=2.2),
                      ob.topic[1].animate.set_color(GREY_A), of1.animate.set_fill(DATA, opacity=0.95),
                      of2.animate.set_fill(ocol, opacity=0.95))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def descent(self):
        head = label(r"One step, \ three towers", font_size=36).to_edge(UP, buff=0.3)
        eqs = [
            MathTex(r"f(x+h)", r"=", r"f(x)", r"+", r"f'(x)\,h", r"+", r"\tfrac{1}{2}f''(\xi)\,h^2", font_size=36),
            MathTex(r"f(x-\eta f'(x))", r"=", r"f(x)", r"-", r"\eta\,f'(x)^2", r"+",
                    r"\tfrac{1}{2}f''(\xi)\,\eta^2 f'(x)^2", font_size=36),
            MathTex(r"f(x-\eta f'(x))", r"\le", r"f(x)", r"-", r"\eta\left(1-\tfrac{L\eta}{2}\right)f'(x)^2",
                    font_size=36),
            MathTex(r"f\!\left(x-\tfrac{1}{L}f'(x)\right)", r"\le", r"f(x)", r"-", r"\frac{f'(x)^2}{2L}",
                    font_size=36),
        ]
        for e in eqs:
            e.move_to([0, 2.15, 0])
        whys = [
            r"Taylor's theorem, \ with $\xi$ between $x$ and $x+h$ \ (\textit{Analysis, Built} Part 2)",
            r"take Part 23's step: \ $h = -\eta\, f'(x)$, \ a step of size $\eta$ downhill",
            r"if the curvature is never more than $L$: \ $f''(\xi) \le L$",
            r"choose $\eta = 1/L$: \ every step goes down by at least $f'(x)^2/2L$",
        ]
        whys = [label(w, font_size=21, color=GREY_A).move_to([0, 1.3, 0]) for w in whys]
        ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[0, 3.0, 1], x_length=6.4, y_length=2.7,
                  axis_config={"color": GREY_D, "include_ticks": False}).move_to([-2.9, -1.75, 0])

        def f(x):
            return float(np.log(np.cosh(x)))

        curve = ax.plot(f, x_range=[-3.2, 3.2], color=GREY_A, stroke_width=2.5)
        xs = [3.0]
        for _ in range(4):
            xs.append(xs[-1] - float(np.tanh(xs[-1])))       # eta = 1/L with L = 1, since f'' = sech^2 <= 1
        dots = VGroup(*[Dot(ax.c2p(x, f(x)), radius=0.07, color=HEAD) for x in xs])
        hops = VGroup(*[Arrow(dots[i].get_center(), dots[i + 1].get_center(), buff=0.08, color=HEAD,
                              stroke_width=2.5, max_tip_length_to_length_ratio=0.2) for i in range(len(xs) - 1)])
        ill = note(r"illustrative: \ $f(x) = \log\cosh x$, \ $f'' \le 1$, \ so $L = 1$ and $\eta = 1$", font_size=17
                   ).next_to(ax, DOWN, buff=0.15)
        chips = VGroup(
            card_box(r"\textit{Analysis, Built} 2", r"Taylor's theorem with its remainder", YES, w=4.6, h=1.0),
            card_box(r"\textit{Computer Science, Built} 23", r"the step: \ go against the slope", DATA, w=4.6, h=1.0),
            card_box(r"\textit{AI, Built} 11", r"the learning rate has a ceiling: \ beyond $2/L$, \ no guarantee", LAM,
                     w=4.6, h=1.0),
        ).arrange(DOWN, buff=0.22).move_to([3.9, -1.6, 0])
        with self.voiceover(
            "Some ideas stand on all three towers at once. Take the step that trains every model. "
            "<bookmark mark='a'/> Taylor's theorem, from Analysis, Built's Part 2: f at x plus h is f at x, plus the "
            "slope times h, plus half the second derivative at some point in between, times h squared. "
            "<bookmark mark='b'/> Now take Part 23's step: h is minus eta times the slope. The middle term becomes "
            "minus eta times the slope squared. <bookmark mark='c'/> If the curvature is never more than L, the last "
            "term is at most L over two, times eta squared, times the slope squared, so f falls by at least eta "
            "times one minus L eta over two, times the slope squared. <bookmark mark='d'/> Choose eta equal to one "
            "over L, and every step lowers f by at least the slope squared over two L. <bookmark mark='e'/> That "
            "inequality is why a learning rate has a ceiling, an early lesson of AI, Built's Part 11: step further "
            "than two over L, and the guarantee is gone. In many dimensions the slope becomes the gradient, the "
            "derivative of Analysis, Built's Part 4."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(curve), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(whys[0]), FadeIn(chips[0], shift=LEFT * 0.1))
            vo.wait_until("b")
            self.play(TransformMatchingTex(eqs[0], eqs[1]), ReplacementTransform(whys[0], whys[1]),
                      FadeIn(chips[1], shift=LEFT * 0.1))
            self.play(FadeIn(dots[0], scale=0.5), GrowArrow(hops[0]), FadeIn(dots[1], scale=0.5))
            vo.wait_until("c")
            self.play(TransformMatchingTex(eqs[1], eqs[2]), ReplacementTransform(whys[1], whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(eqs[2], eqs[3]), ReplacementTransform(whys[2], whys[3]))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(hops[i]), FadeIn(dots[i + 1], scale=0.5))
                                    for i in range(1, len(hops))], lag_ratio=0.6), run_time=2.4)
            vo.wait_until("e")
            box = SurroundingRectangle(eqs[3], color=HEAD, buff=0.15)
            self.play(Create(box), FadeIn(chips[2], shift=LEFT * 0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def web(self):
        head = label(r"Seven crossings, \ and more", font_size=36).to_edge(UP, buff=0.3)
        tw = {k: series_tower(k) for k in TOWERS}
        lit = towers_with(AI_BRIDGES + AN_BRIDGES, tw)
        n_cs, _, w_cs, _, _, _ = TOWERS["cs"]
        n_ai, x_ai, w_ai, _, _, _ = TOWERS["ai"]
        extra = VGroup(*[DashedLine([-w_cs / 2, floor_y(n_cs, a), 0], [x_ai + w_ai / 2, floor_y(n_ai, b), 0],
                                    color=LAM, stroke_width=1.6, dash_length=0.08) for a, b in EXTRA])
        extra.set_z_index(-1)
        foot = wrapped_label(r"dashed: \ Part 18's PageRank, \ a Markov chain of \textit{AI, Built} Part 5; \ Part 20's "
                             r"random projections, \ Part 3's Johnson--Lindenstrauss; \ Part 54's proof assistants, "
                             r"\ Part 25's Lean", 12.6, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Draw every crossing at once, and three buildings start to look like one. <bookmark mark='a'/> There are "
            "more than these seven. Part 18's PageRank is a Markov chain from AI, Built's Part 5; Part 20's random "
            "projections are the Johnson-Lindenstrauss lemma of its Part 3; Part 54's proof assistants are the Lean "
            "of its Part 25. <bookmark mark='b'/> And a good research problem often lives on a bridge: a tool that "
            "is routine on one side, and not yet tried on the other."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(t) for t in tw.values()], FadeIn(lit), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in extra], lag_ratio=0.4), FadeIn(foot), run_time=2.0)
            vo.wait_until("b")
            self.play(*[Indicate(b.line, color=HEAD, scale_factor=1.0) for b in lit],
                      *[Indicate(b.topic[1], color=HEAD) for b in lit], run_time=1.5)
        self.wait(0.6)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
