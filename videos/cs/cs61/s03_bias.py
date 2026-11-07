from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono, module_box

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'one hundred and twenty-eight')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))


B = load("bias")
ENV = B["env"]
LINK = B["link"]
ONE = LINK[0]["runs"]      # the first link order with an empty environment: the same setting as ENV's first point
MED = [r["median"] for r in ENV]
MINS = [r["min"] for r in ENV]
MIN_SPREAD = (max(MINS) - min(MINS)) / min(MINS)
ONE_RANGE = (max(ONE) - min(ONE)) / min(ONE)
POOL = [x for r in LINK for x in r["runs"]]   # every run with an empty environment, all three link orders
STEP = ENV[1]["bytes"] - ENV[0]["bytes"]


def null_spreads(trials: int = 4000, seed: int = 0) -> np.ndarray:
    """Noise alone: as many medians of ``reps`` as the experiment had settings, drawn from the runs with an empty
    environment (link order made no detectable difference); the spread of those medians, ``trials`` times."""
    rng = np.random.default_rng(seed)
    m = np.median(rng.choice(np.asarray(POOL), (trials, len(ENV), B["reps"])), axis=2)
    return (m.max(axis=1) - m.min(axis=1)) / m.min(axis=1)


NULL = null_spreads()
NULL_MED = float(np.median(NULL))
NULL_ABOVE = float(np.mean(NULL >= B["env_spread"]))


class Bias(VoiceoverScene):
    def construct(self):
        self.card()
        self.stack()
        self.env_size()
        self.link_order()
        self.paper()
        self.verdict()

    def card(self):
        card = chapter_card(2, r"Measurement bias", r"Can a variable nobody reads change a program's speed?",
                            lit=(2009, 2013), extra=((2009, r"Mytkowicz et al.: \ wrong data"),
                                                     (2013, r"Curtsinger and Berger: \ Stabilizer")), part=PART)
        with self.voiceover("Chapter two. Measurement bias."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def stack(self):
        head = label(r"Where the environment lives", font_size=36).to_edge(UP, buff=0.3)

        def column(env_h):
            parts = [(r"environment strings", DATA, env_h), (r"argument strings", GREY_B, 0.42),
                     (r"pointers, \ auxiliary vector", GREY_B, 0.42), (r"\texttt{main}'s frame", LAM, 0.5),
                     (r"\texttt{count}'s frame: \ hot locals", HEAD, 0.5)]
            g = VGroup()
            for t, c, h in parts:
                r = Rectangle(width=3.3, height=h, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.12)
                g.add(VGroup(r, label(t, font_size=17, color=WHITE).move_to(r)))
            g.arrange(DOWN, buff=0)
            return g.move_to([-4.6, 0, 0]).align_to([0, 2.45, 0], UP)
        small, big = column(0.45), column(1.25)
        top = label(r"top of the stack \ (high addresses)", font_size=17, color=GREY_A).next_to(small, UP, buff=0.1)
        grow = Arrow([-2.55, 1.9, 0], [-2.55, -0.6, 0], buff=0, color=GREY_C, stroke_width=2.5)
        grow_t = label(r"frames below", font_size=16, color=GREY_B).next_to(grow, RIGHT, buff=0.08).shift(UP * 0.4)
        cols = {r"e": DATA, r"16": KERN}
        rows = VGroup(
            cmath(r"a", r"=", r"T", r"-", r"e", r"-", r"c", colors=cols, font_size=34),
            cmath(r"a", r"=", r"16", r"\left\lfloor \frac{T - e - c}{16} \right\rfloor", r"+", r"k", colors=cols,
                  font_size=34),
            cmath(r"a \bmod 64", r"\in", r"\{k,\ k{+}16,\ k{+}32,\ k{+}48\}", colors=cols, font_size=32),
            cmath(r"a \bmod 4096", r":", r"256", r"\text{ places}", colors=cols, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([2.6, 0.7, 0])
        whys = VGroup(
            label(r"$a$: \ a hot local; \ $e$: \ environment bytes; \ $T$, \ $c$: \ fixed", font_size=17,
                  color=GREY_B),
            label(r"the calling convention aligns the stack to 16 bytes", font_size=17, color=GREY_B),
            label(r"where it sits in a 64-byte cache line \ (Part 9)", font_size=17, color=GREY_B),
            label(r"where it sits in a 4 KiB page", font_size=17, color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        # a ruler of four cache lines, in 16-byte cells; a 48-byte object slides as the environment grows
        cw = 0.66
        cells = VGroup(*[Rectangle(width=cw, height=0.38, stroke_color=GREY_D, stroke_width=1) for _ in range(16)])
        cells.arrange(RIGHT, buff=0).move_to([0.2, -3.05, 0])
        bounds = VGroup(*[Line(cells[i].get_corner(UL) + UP * 0.08, cells[i].get_corner(DL) + DOWN * 0.08,
                               color=GREY_A, stroke_width=3) for i in (0, 4, 8, 12)],
                        Line(cells[15].get_corner(UR) + UP * 0.08, cells[15].get_corner(DR) + DOWN * 0.08,
                             color=GREY_A, stroke_width=3))
        rl = label(r"four 64-byte cache lines", font_size=16, color=GREY_B).next_to(cells, LEFT, buff=0.2)
        ill = note(r"illustrative", font_size=16).next_to(cells, RIGHT, buff=0.2)

        def obj(start, color):
            r = Rectangle(width=3 * cw - 0.06, height=0.26, stroke_width=0, fill_color=color, fill_opacity=0.85)
            return r.move_to(cells[start]).align_to(cells[start], LEFT).shift(RIGHT * 0.03)
        o1 = obj(5, YES)
        o2 = obj(2, NO)
        split = label(r"split across two lines", font_size=16, color=NO).next_to(cells, UP, buff=0.12).align_to(
            cells[2], LEFT)
        with self.voiceover(
            "Why would a variable nobody reads matter? <bookmark mark='a'/> When Linux starts a program, it copies "
            "the environment strings and the arguments to the very top of the new stack, then the pointers to "
            "them, and only below those do the program's own frames begin. <bookmark mark='b'/> So every byte "
            "added to the environment pushes every frame down. Write the address of a hot local variable as the "
            "top, minus the environment, minus everything else. <bookmark mark='c'/> The calling convention keeps "
            "the stack aligned to sixteen bytes, so the address moves in sixteen-byte steps. "
            "<bookmark mark='d'/> Within a sixty-four-byte cache line, from Part 9, it can sit in four places, "
            "<bookmark mark='e'/> and within a four-kilobyte page in two hundred and fifty-six. An object split "
            "across two lines costs two accesses, and a load whose address matches an earlier store's in its low "
            "twelve bits can be held up by the processor, which compares only those bits at first. Which case you "
            "get depends on the environment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(small), FadeIn(top), GrowArrow(grow), FadeIn(grow_t))
            vo.wait_until("a")
            self.play(Indicate(small[0], color=DATA), Indicate(small[1], color=GREY_A))
            vo.wait_until("b")
            self.play(Transform(small, big), run_time=2)
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]), FadeIn(cells), FadeIn(bounds), FadeIn(rl), FadeIn(ill),
                      FadeIn(o1))
            self.play(Transform(o1, o2), FadeIn(split), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def env_size(self):
        head = label(r"Experiment one: \ the environment grows", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = 0.125, 0.165
        ax = Axes(x_range=[0, 4096, 1024], y_range=[lo, hi, 0.01], x_length=7.4, y_length=4.4,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_tip": False}).move_to(
            [-2.1, -0.15, 0])
        xt = VGroup(*[label(rf"{v:,}", font_size=16, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.1)
                      for v in (0, 1024, 2048, 3072, 4096)])
        xl = label(r"bytes added to the environment", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yt = VGroup(*[label(rf"{v:.2f}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for v in (0.13, 0.14, 0.15, 0.16)])
        yl = label(r"seconds", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(yt, LEFT)
        meds = VGroup(*[Dot(ax.c2p(r["bytes"], r["median"]), radius=0.055, color=HEAD) for r in ENV])
        mins = VGroup(*[Dot(ax.c2p(r["bytes"], r["min"]), radius=0.04, color=DATA) for r in ENV])
        mline = VMobject(color=HEAD, stroke_width=1.4).set_points_as_corners([d.get_center() for d in meds])
        sx = ax.get_right()[0] + 0.75
        rng = np.random.default_rng(3)
        strip = VGroup(*[Dot([sx + rng.uniform(-0.16, 0.16), ax.c2p(0, v)[1], 0], radius=0.045, color=NO)
                         for v in ONE])
        ymin, ymax = ax.c2p(0, min(ONE))[1], ax.c2p(0, max(ONE))[1]
        brace = BraceBetweenPoints([sx + 0.3, ymax, 0], [sx + 0.3, ymin, 0], RIGHT, color=NO)
        st = VGroup(label(r"one setting,", font_size=16, color=NO),
                    label(rf"{len(ONE)} runs", font_size=16, color=NO)).arrange(DOWN, buff=0.06).next_to(
            [sx, ax.c2p(0, lo)[1], 0], DOWN, buff=0.12)
        notes = VGroup(
            wrapped_label(rf"medians of {B['reps']}: \ spread {100 * B['env_spread']:.1f}\%", 2.9, font_size=19,
                          color=HEAD),
            wrapped_label(rf"fastest of each {B['reps']}: \ spread {100 * MIN_SPREAD:.1f}\%", 2.9, font_size=19,
                          color=DATA),
            wrapped_label(rf"one unchanged setting: \ its own runs range over {100 * ONE_RANGE:.0f}\%", 2.9,
                          font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([5.3, 0.3, 0])
        foot = note(rf"measured on this machine: \ {len(ENV)} sizes $\times$ {B['reps']} runs, \ interleaved",
                    font_size=17).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here is the first experiment from the hook again, with more of what we measured. <bookmark mark='a'/> "
            f"For each of {say(len(ENV))} environment sizes, from nothing to four kilobytes in steps of "
            f"{say(STEP)} bytes, we ran the program {say(B['reps'])} times, interleaved, so that slow changes in "
            "the machine fall on every setting alike. The yellow dots are the medians; they spread by about "
            f"{say(100 * B['env_spread'])} percent. <bookmark mark='b'/> The blue dots are the fastest of each "
            f"{say(B['reps'])}; they spread by about {say(100 * MIN_SPREAD)}. <bookmark mark='c'/> Now, at the "
            f"right, {say(len(ONE))} more runs of one unchanged setting, the empty environment, taken just after. "
            f"They range over {say(100 * ONE_RANGE)} percent, {say(ONE_RANGE / B['env_spread'])} times the whole "
            "spread of the medians. Before "
            "we blame the stack for anything, we have to know how much the machine moves on its own."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yt), FadeIn(yl), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in meds], lag_ratio=0.06), run_time=2.5)
            self.play(Create(mline), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in mins], lag_ratio=0.04), run_time=2)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d, shift=LEFT * 0.2) for d in strip], lag_ratio=0.08), FadeIn(st),
                      run_time=2)
            self.play(GrowFromCenter(brace), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def link_order(self):
        head = label(r"Experiment two: \ the link order", font_size=36).to_edge(UP, buff=0.3)
        colmap = {"kernel": HEAD, "mix": LAM, "main": DATA}
        lays = VGroup()
        for r in LINK:
            names = r["order"].split("+")
            cmd = mono("gcc -O2 " + " ".join(f"{n}.o" for n in names), size=15, color=GREY_A)
            boxes = VGroup(*[module_box(rf"\texttt{{{n}}}", colmap[n], w=1.55, h=0.46, font=17) for n in names])
            boxes.arrange(RIGHT, buff=0)
            lays.add(VGroup(cmd, boxes).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        lays.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-4.3, 0.55, 0])
        addr = label(r"code laid out in this order, \ low addresses to high", font_size=17,
                     color=GREY_B).next_to(lays, DOWN, buff=0.3).align_to(lays, LEFT)
        lo, hi = 0.125, 0.18
        ax = Axes(x_range=[0, 3, 1], y_range=[lo, hi, 0.01], x_length=5.4, y_length=4.4,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False,
                               "include_tip": False}).move_to([3.5, -0.2, 0])
        yt = VGroup(*[label(rf"{v:.2f}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for v in (0.13, 0.15, 0.17)])
        yl = label(r"seconds", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(yt, LEFT)
        rng = np.random.default_rng(7)
        strips, medl, names = VGroup(), VGroup(), VGroup()
        for i, r in enumerate(LINK):
            c = colmap[r["order"].split("+")[0]]
            strips.add(VGroup(*[Dot(ax.c2p(i + 0.5 + rng.uniform(-0.18, 0.18), v), radius=0.045, color=c)
                                for v in r["runs"]]))
            medl.add(Line(ax.c2p(i + 0.22, r["median"]), ax.c2p(i + 0.78, r["median"]), color=WHITE, stroke_width=3))
            names.add(mono(r["order"].replace("+", " "), size=13, color=GREY_A).next_to(ax.c2p(i + 0.5, lo), DOWN,
                                                                                         buff=0.15))
        spread = label(rf"medians differ by {100 * B['link_spread']:.1f}\%", font_size=21, color=YES).next_to(
            ax, UP, buff=0.12).align_to(ax, RIGHT)
        foot = wrapped_label(r"white bars: \ medians of 15 runs each, \ empty environment; \ measured on this "
                             r"machine", 6.0, font_size=17, color=GREY_B).to_edge(DOWN, buff=0.2).align_to(ax, LEFT)
        with self.voiceover(
            "The second experiment changes nothing in the source, only the order in which the linker is handed "
            "the three object files. <bookmark mark='a'/> The linker lays the code out in that order, so every "
            "function lands at a new address. That changes how the hot loop lines up with the blocks in which the "
            "processor fetches instructions, and which branch-predictor entries its branches share. "
            f"<bookmark mark='b'/> Here are {say(len(LINK[0]['runs']))} runs of each order, with the environment "
            "empty. The medians differ by under one percent, far inside the scatter of the runs. "
            "<bookmark mark='c'/> On this machine, for this small loop, link order shows no effect we can detect. "
            "That is not the same as no effect: an effect smaller than the noise would look exactly like this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lays[0]), FadeIn(addr))
            vo.wait_until("a")
            self.play(FadeIn(lays[1], shift=DOWN * 0.15), FadeIn(lays[2], shift=DOWN * 0.15))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yt), FadeIn(yl), FadeIn(names), FadeIn(foot))
            self.play(LaggedStart(*[LaggedStart(*[FadeIn(d, scale=0.5) for d in s], lag_ratio=0.1) for s in strips],
                                  lag_ratio=0.4), run_time=3)
            self.play(Create(medl), FadeIn(spread))
            vo.wait_until("c")
            self.play(Indicate(spread, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def paper(self):
        head = label(r"What Mytkowicz and colleagues found", font_size=36).to_edge(UP, buff=0.3)
        frame = RoundedRectangle(width=6.0, height=1.9, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.6,
                                 fill_color=GREY_E, fill_opacity=0.5)
        ptxt = VGroup(wrapped_label(r"\textit{Producing Wrong Data Without Doing Anything Obviously Wrong!}", 5.6,
                                    font_size=21, color=WHITE),
                      label(r"Mytkowicz, \ Diwan, \ Hauswirth and Sweeney", font_size=18, color=GREY_A),
                      label(r"ASPLOS, \ 2009", font_size=18, color=HEAD)).arrange(DOWN, buff=0.15).move_to(frame)
        card = VGroup(frame, ptxt).move_to([-3.55, 1.75, 0])
        finds = VGroup(
            wrapped_label(r"bias on every processor and both compilers they tried, \ in most of the SPEC CPU2006 C "
                          r"programs", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"environment size or link order could change whether \texttt{-O3} looked faster than "
                          r"\texttt{-O2}", 6.0, font_size=19, color=NO),
            wrapped_label(r"of more than a hundred recent papers they surveyed, \ none adequately accounted for it",
                          6.0, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(card, DOWN, buff=0.4).align_to(card, LEFT)
        # remedy one: setup randomization
        r1t = label(r"1. \ setup randomization", font_size=22, color=YES)
        rng = np.random.default_rng(11)
        setups = VGroup(*[tag_box_(rf"setup {i + 1}", GREY_A) for i in range(4)]).arrange(RIGHT, buff=0.12)
        vals = rng.normal(0, 1, 400)
        cnt, _ = np.histogram(vals, bins=11, range=(-2.75, 2.75))
        hist = VGroup(*[Rectangle(width=0.16, height=max(0.03, 0.9 * c / cnt.max()), stroke_width=0, fill_color=YES,
                                  fill_opacity=0.85) for c in cnt]).arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
        row1 = VGroup(setups, hist).arrange(RIGHT, buff=0.5)
        arr1 = Arrow(setups.get_right(), hist.get_left(), buff=0.08, color=GREY_C, stroke_width=2)
        r1n = wrapped_label(r"random environment sizes and link orders; \ report the distribution and its interval "
                            r"\ (schematic)",
                            6.0, font_size=18, color=GREY_A)
        rem1 = VGroup(r1t, VGroup(row1, arr1), r1n).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        # remedy two: causal analysis
        r2t = label(r"2. \ causal analysis", font_size=22, color=LAM)
        steps = VGroup(tag_box_(r"suspect a cause", LAM), tag_box_(r"change only it", LAM),
                       tag_box_(r"does the effect follow?", LAM)).arrange(RIGHT, buff=0.4)
        arr2 = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.05, color=GREY_C,
                              stroke_width=2, max_tip_length_to_length_ratio=0.3) for i in range(2)])
        r2n = wrapped_label(r"if the effect does not follow, \ the cause lies elsewhere", 6.0, font_size=18,
                            color=GREY_A)
        rem2 = VGroup(r2t, VGroup(steps, arr2), r2n).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rems = VGroup(rem1, rem2).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([3.5, 0.55, 0])
        stab = wrapped_label(r"Curtsinger and Berger's \textsc{Stabilizer} \ (2013) \ re-randomizes code, \ stack "
                             r"and heap layout while the program runs", 6.2, font_size=18, color=WHITE).next_to(
            rems, DOWN, buff=0.45).align_to(rems, LEFT)
        with self.voiceover(
            "This is what Todd Mytkowicz, Amer Diwan, Matthias Hauswirth and Peter Sweeney reported at ASPLOS in "
            "2009, under the title Producing Wrong Data Without Doing Anything Obviously Wrong. "
            "<bookmark mark='a'/> They found measurement bias on every processor and both compilers they tried, "
            "and in most of the SPEC CPU2006 C programs. Changing the environment size or the link order could "
            "change whether the compiler's O3 setting looked faster than O2. Of more than a hundred recent papers "
            "they surveyed, none had adequately accounted for it. <bookmark mark='b'/> They proposed two remedies. "
            "Setup randomization: measure under many randomly chosen setups, and report the distribution, not one "
            "lucky point. <bookmark mark='c'/> And causal analysis: when you believe an effect has a cause, change "
            "that cause alone, and check that the effect follows. <bookmark mark='d'/> In 2013 Charlie Curtsinger "
            "and Emery Berger built Stabilizer, which keeps re-randomizing the layout while the program runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(card))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in finds], lag_ratio=0.6), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(r1t), FadeIn(setups))
            self.play(GrowArrow(arr1), LaggedStart(*[GrowFromEdge(h, DOWN) for h in hist], lag_ratio=0.1),
                      FadeIn(r1n))
            vo.wait_until("c")
            self.play(FadeIn(r2t), FadeIn(steps[0]))
            self.play(GrowArrow(arr2[0]), FadeIn(steps[1]))
            self.play(GrowArrow(arr2[1]), FadeIn(steps[2]), FadeIn(r2n))
            vo.wait_until("d")
            self.play(FadeIn(stab))
        self.wait(0.4)
        self.clear_scene()

    def verdict(self):
        head = label(r"What our measurement shows, \ and what it does not", font_size=36).to_edge(UP, buff=0.3)
        cnt, edges = np.histogram(NULL, bins=30, range=(0.0, 0.30))
        bw = 0.19
        bars = VGroup(*[Rectangle(width=bw - 0.02, height=max(0.02, 3.0 * c / cnt.max()), stroke_width=0,
                                  fill_color=GREY_B, fill_opacity=0.8) for c in cnt])
        bars.arrange(RIGHT, buff=0.02, aligned_edge=DOWN).move_to([-3.6, -0.4, 0]).align_to([0, -1.8, 0], DOWN)
        x0 = bars.get_left()[0]
        xpos = lambda f: x0 + f / 0.30 * bars.width  # noqa: E731
        base = Line([x0, -1.8, 0], [bars.get_right()[0], -1.8, 0], color=GREY_C, stroke_width=1.5)
        xt = VGroup(*[label(rf"{v}\%", font_size=16, color=GREY_B).move_to([xpos(v / 100), -2.05, 0])
                      for v in (0, 10, 20, 30)])
        xl = label(rf"spread of {len(ENV)} medians, \ noise alone", font_size=17, color=GREY_A).next_to(
            xt, DOWN, buff=0.12)
        obs = DashedLine([xpos(B["env_spread"]), -1.8, 0], [xpos(B["env_spread"]), 1.5, 0], color=HEAD,
                         stroke_width=3)
        obs_t = label(rf"ours: \ {100 * B['env_spread']:.1f}\%", font_size=18, color=HEAD).next_to(
            obs.get_end(), LEFT, buff=0.1)
        typ = wrapped_label(rf"noise alone: \ typically {100 * NULL_MED:.0f}\%; \ {100 * NULL_ABOVE:.0f}\% of "
                            r"trials exceed ours", 6.0, font_size=19, color=GREY_A).move_to([0, 2.45, 0]).align_to(
            bars, LEFT)
        how = wrapped_label(rf"4{{,}}000 imaginary experiments: \ {len(ENV)} medians of {B['reps']}, \ each drawn "
                            rf"from the {len(POOL)} runs with an empty environment", 6.0, font_size=17,
                            color=GREY_B).to_edge(DOWN, buff=0.25).align_to(bars, LEFT)
        shown = VGroup(label(r"shown", font_size=22, color=YES),
                       wrapped_label(rf"the medians moved by {100 * B['env_spread']:.0f}\% as an unused variable "
                                     rf"grew, \ and by under 1\% across link orders", 5.6, font_size=19,
                                     color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        not_shown = VGroup(label(r"not shown", font_size=22, color=NO),
                           wrapped_label(r"that the environment caused it: \ noise alone explains a spread this size",
                                         5.6, font_size=19, color=WHITE),
                           wrapped_label(r"Linux starts the stack at a random place on every run, \ in 16-byte steps: "
                                         r"\ checked here", 5.6, font_size=19, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        VGroup(shown, not_shown).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.7, 0.2, 0])
        with self.voiceover(
            "So what does our measurement show? <bookmark mark='a'/> Suppose nothing but noise were acting. Draw "
            f"{say(len(ENV))} medians of {say(B['reps'])} from the {say(len(POOL))} runs with an empty environment, "
            "measure their spread,"
            " and repeat that four thousand times. <bookmark mark='b'/> Noise alone typically gives about "
            f"{say(100 * NULL_MED)} percent. Our {say(100 * B['env_spread'])} percent sits well inside it. "
            f"<bookmark mark='c'/> We have shown that the medians moved by {say(100 * B['env_spread'])} percent "
            "while an unused variable grew, and by under one percent across link orders. <bookmark mark='d'/> We "
            "have not shown that the environment caused it. And there is a reason it may not have: on this "
            "machine, with address randomization on, Linux starts the stack at a different place on every run, "
            "in sixteen-byte steps; we checked. That is a setup randomization done for us, and it smears the "
            "alignment effect into every setting's noise. To find a cause, you would switch it off and intervene."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(xt), FadeIn(xl), FadeIn(how))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(obs), FadeIn(obs_t), FadeIn(typ))
            vo.wait_until("c")
            self.play(FadeIn(shown))
            vo.wait_until("d")
            self.play(FadeIn(not_shown))
        self.wait(0.4)
        self.clear_scene()


def tag_box_(text: str, color, size=17):
    """A step drawn as a rounded box with a Tex caption."""
    t = label(text, font_size=size, color=WHITE)
    box = RoundedRectangle(width=t.width + 0.3, height=0.5, corner_radius=0.08, stroke_color=color, stroke_width=1.6,
                           fill_color=color, fill_opacity=0.12)
    t.move_to(box)
    return VGroup(box, t)


_ = (BG,)
