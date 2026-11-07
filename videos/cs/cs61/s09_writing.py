from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono

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


def role_box(role: str, text: str, color, w=3.6):
    """One element of an argument: its role above, its content in a rounded box."""
    body = wrapped_label(text, w - 0.35, font_size=18, color=WHITE)
    r = RoundedRectangle(width=w, height=body.height + 0.35, corner_radius=0.1, stroke_color=color,
                         stroke_width=1.8, fill_color=color, fill_opacity=0.1)
    body.move_to(r)
    tag = label(role, font_size=20, color=color).next_to(r, UP, buff=0.08).align_to(r, LEFT)
    return VGroup(r, body, tag)


def chip(text: str, color, size=20):
    t = label(text, font_size=size, color=color)
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.08, stroke_color=color,
                         stroke_width=1.6, fill_color=BG, fill_opacity=1)
    return VGroup(r, t.move_to(r))


B = load("bias")
ENV_SPREAD = 100 * B["env_spread"]
LINK = B["link"]
MEDS = [r["median"] for r in LINK]
FLOOR = 0.138                                       # the cut axis of the misleading chart: just below every median
TALL = (max(MEDS) - FLOOR) / (min(MEDS) - FLOOR)    # how much taller its tallest bar looks
RUN_SPREADS = [100 * (max(r["runs"]) / min(r["runs"]) - 1) for r in LINK]
G = load("goldbach")
M = load("means")


class Writing(VoiceoverScene):
    def construct(self):
        self.card()
        self.argument()
        self.claims()
        self.figures()
        self.pipeline()
        self.labels()

    def card(self):
        card = chapter_card(8, r"Writing", r"How do you make a reader believe you, \ for the right reasons?",
                            lit=(1958, 1983), extra=((1958, r"Toulmin: \ \textit{The Uses of Argument}"),
                                                     (1983, r"Tufte: \ honest graphics")), part=PART)
        with self.voiceover("Chapter eight. Writing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def argument(self):
        head = label(r"The shape of an argument \ (Toulmin, \ 1958)", font_size=36).to_edge(UP, buff=0.3)
        data = role_box(r"data", rf"medians spread {ENV_SPREAD:.1f}\% across {len(B['env'])} environment sizes, "
                                 rf"\ {B['reps']} runs each", DATA)
        qual = role_box(r"qualifier", r"on this machine, \ for this program", GREY_B, w=3.0)
        claim = role_box(r"claim", r"an unused environment variable did not measurably change the speed", YES)
        warrant = role_box(r"warrant \ (since)", r"noise alone, \ with no variable at all, \ gives spreads this "
                                                 r"large", HEAD)
        backing = role_box(r"backing \ (because)", r"4{,}000 simulated experiments, \ drawn from the runs with an "
                                                   r"empty environment \ (chapter 2)", KERN)
        rebut = role_box(r"rebuttal \ (unless)", r"address randomization is hiding a real effect", NO, w=3.4)
        data.move_to([-4.7, 1.3, 0])
        qual.move_to([0.0, 1.3, 0])
        claim.move_to([4.7, 1.3, 0])
        warrant.move_to([-2.3, -0.75, 0])
        backing.move_to([-2.3, -2.65, 0])
        rebut.move_to([2.9, -0.75, 0])
        a1 = Arrow(data[0].get_right(), qual[0].get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
        a2 = Arrow(qual[0].get_right(), claim[0].get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
        mid = (data[0].get_right() + qual[0].get_left()) / 2
        a3 = Line(warrant[2].get_top() + UP * 0.05, mid + DOWN * 0.05, color=HEAD, stroke_width=2)
        a4 = Line(backing[2].get_top() + UP * 0.05, warrant[0].get_bottom() + DOWN * 0.05, color=KERN,
                  stroke_width=2)
        a5 = Line(rebut[2].get_top() + UP * 0.05, qual[0].get_bottom() + DOWN * 0.05, color=NO, stroke_width=2)
        foot = wrapped_label(r"weak papers give a claim and data, \ and leave the reader to supply the rest", 5.4,
                             font_size=19, color=GREY_A).to_corner(DR, buff=0.35)
        with self.voiceover(
            "Writing up research is making an argument, and in 1958 the philosopher Stephen Toulmin drew the shape "
            "of one. Take this part's own result from chapter two. <bookmark mark='a'/> The claim is what you want "
            "the reader to accept: an unused environment variable did not measurably change the program's speed. "
            "<bookmark mark='b'/> The data are the facts it rests on: the medians spread by "
            f"{say1(ENV_SPREAD)} percent across {say(len(B['env']))} sizes, {say(B['reps'])} runs each. "
            "<bookmark mark='c'/> The warrant is why those data support the claim: noise alone, with no variable "
            "at all, gives spreads this large. <bookmark mark='d'/> The backing is why the warrant holds: four "
            "thousand simulated experiments. <bookmark mark='e'/> The qualifier says how far the claim reaches: on "
            "this machine, for this program. <bookmark mark='f'/> And the rebuttal says when it would fail: unless "
            "address randomization is hiding a real effect. Weak papers stop at the claim and the data."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(claim))
            vo.wait_until("b")
            self.play(FadeIn(data), GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("c")
            self.play(FadeIn(warrant), Create(a3))
            vo.wait_until("d")
            self.play(FadeIn(backing), Create(a4))
            vo.wait_until("e")
            self.play(FadeIn(qual))
            vo.wait_until("f")
            self.play(FadeIn(rebut), Create(a5))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def claims(self):
        head = label(r"Every claim, \ its evidence", font_size=36).to_edge(UP, buff=0.3)
        lt = label(r"the introduction claims", font_size=22, color=HEAD).move_to([-3.5, 2.45, 0])
        rt = label(r"the paper supports it with", font_size=22, color=YES).move_to([3.6, 2.45, 0])
        spec = [(r"Skim hashes each word once", r"the algorithm, \ section 3", YES),
                (r"Skim is 2.1 times faster", r"figure 4, \ with intervals and a named baseline", YES),
                (r"it needs little extra memory", r"nothing", NO),
                (r"it works for any language", r"nothing", NO)]
        rows = VGroup()
        for i, (c, e, col) in enumerate(spec):
            y = 1.5 - 1.05 * i
            cl = VGroup(RoundedRectangle(width=5.4, height=0.7, corner_radius=0.1, stroke_color=HEAD,
                                         stroke_width=1.6, fill_color=HEAD, fill_opacity=0.08),
                        label(c, font_size=20, color=WHITE)).move_to([-3.5, y, 0])
            cl[1].move_to(cl[0])
            if col is YES:
                ev = VGroup(RoundedRectangle(width=4.8, height=0.7, corner_radius=0.1, stroke_color=YES,
                                             stroke_width=1.6, fill_color=YES, fill_opacity=0.08),
                            label(e, font_size=19, color=WHITE)).move_to([3.6, y, 0])
                ev[1].move_to(ev[0])
                if ev[1].width > 4.6:
                    ev[1].width = 4.6
                arr = Arrow(cl[0].get_right(), ev[0].get_left(), buff=0.08, color=YES, stroke_width=2.5)
            else:
                ev = VGroup(Cross(scale_factor=0.18, stroke_color=NO, stroke_width=5),
                            label(r"nothing in the paper", font_size=19, color=NO)).arrange(RIGHT, buff=0.2)
                ev.move_to([3.6, y, 0])
                arr = DashedLine(cl[0].get_right() + RIGHT * 0.08, ev.get_left() + LEFT * 0.15, color=NO,
                                 stroke_width=2)
            rows.add(VGroup(cl, arr, ev))
        ill = note(r"illustrative: \ the invented paper of chapter 6", font_size=16).next_to(rows, DOWN, buff=0.15)
        ill.align_to(rows, LEFT)
        fix = wrapped_label(r"for each unsupported claim: \ cut it, \ or add the evidence; \ and let the "
                            r"introduction say where each contribution is shown", 12.4, font_size=21,
                            color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A paper makes many claims, and each one needs its own evidence. Here is a test you can run on any "
            "draft, shown on chapter six's invented paper. <bookmark mark='a'/> First, list every claim the "
            "introduction makes, including the ones in passing. <bookmark mark='b'/> Then find, for each claim, "
            "the section, figure or theorem that supports it. Skim hashes each word once: that is the algorithm, "
            "in section three. Two point one times faster: figure four, if it has intervals and names its "
            "baseline. <bookmark mark='c'/> Little extra memory, and works for any language: nothing in the paper "
            "supports either. <bookmark mark='d'/> Each such claim must be cut, or the evidence added. A reviewer "
            "will run this test whether you do or not. A good introduction makes it easy, by saying where each "
            "contribution is shown."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lt), FadeIn(rt), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[0], shift=RIGHT * 0.15) for r in rows], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            for r in rows[:2]:
                self.play(GrowArrow(r[1]), FadeIn(r[2]))
            vo.wait_until("c")
            for r in rows[2:]:
                self.play(Create(r[1]), FadeIn(r[2]))
            vo.wait_until("d")
            self.play(FadeIn(fix), *[Indicate(r[0], color=NO) for r in rows[2:]])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def figures(self):
        head = label(r"Figures that carry the claim", font_size=36).to_edge(UP, buff=0.3)
        names = [r["order"].replace("+", " ") for r in LINK]
        cols = (DATA, KERN, LAM)
        # left: medians only, the axis cut just below the smallest
        hmax = 3.0
        lo_l, hi_l = FLOOR, 0.1396
        x0l, y0 = -6.0, -1.6
        bars = VGroup()
        for i, (m, c) in enumerate(zip(MEDS, cols)):
            h = (m - lo_l) / (hi_l - lo_l) * hmax
            bars.add(Rectangle(width=1.1, height=h, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to(
                [x0l + 0.9 + 1.6 * i, y0, 0], aligned_edge=DOWN))
        axl = Line([x0l, y0, 0], [x0l, y0 + hmax, 0], color=GREY_C, stroke_width=1.5)
        basel = Line([x0l, y0, 0], [x0l + 4.8, y0, 0], color=GREY_C, stroke_width=1.5)
        ytl = VGroup(*[label(rf"{v:.4f}", font_size=16, color=GREY_B).next_to(
            [x0l, y0 + (v - lo_l) / (hi_l - lo_l) * hmax, 0], LEFT, buff=0.08) for v in (0.1380, 0.1388, 0.1396)])
        xnl = VGroup(*[label(n, font_size=16, color=c).next_to([b.get_x(), y0, 0], DOWN, buff=0.12)
                       for n, b, c in zip(names, bars, cols)])
        tl = label(r"``Link order changes speed!''", font_size=22, color=NO).move_to([x0l + 2.4, 2.35, 0])
        cl = wrapped_label(r"medians only; \ the axis starts at 0.138 s", 5.0, font_size=18, color=GREY_A).next_to(
            xnl, DOWN, buff=0.2).align_to(axl, LEFT)
        left = VGroup(bars, axl, basel, ytl, xnl, tl, cl)
        left.shift(RIGHT * (-6.75 - ytl.get_left()[0]))
        # right: every run, an axis that shows the spread
        lo_r, hi_r = 0.12, 0.18
        x0r = 1.4
        yp = lambda v: y0 + (v - lo_r) / (hi_r - lo_r) * hmax  # noqa: E731
        axr = Line([x0r, y0, 0], [x0r, y0 + hmax, 0], color=GREY_C, stroke_width=1.5)
        baser = Line([x0r, y0, 0], [x0r + 4.8, y0, 0], color=GREY_C, stroke_width=1.5)
        ytr = VGroup(*[label(rf"{v:.2f}", font_size=16, color=GREY_B).next_to([x0r, yp(v), 0], LEFT, buff=0.08)
                       for v in (0.12, 0.14, 0.16, 0.18)])
        rng = np.random.default_rng(3)
        strips = VGroup()
        for i, (r, c) in enumerate(zip(LINK, cols)):
            xc = x0r + 0.9 + 1.6 * i
            ds = VGroup(*[Dot([xc + rng.uniform(-0.28, 0.28), yp(v), 0], radius=0.05, color=c)
                          for v in r["runs"]])
            med = Line([xc - 0.42, yp(r["median"]), 0], [xc + 0.42, yp(r["median"]), 0], color=WHITE,
                       stroke_width=3)
            strips.add(VGroup(ds, med))
        xnr = VGroup(*[label(n, font_size=16, color=c).next_to([x0r + 0.9 + 1.6 * i, y0, 0], DOWN, buff=0.12)
                       for i, (n, c) in enumerate(zip(names, cols))])
        tr = label(r"Link order: \ no difference beyond noise", font_size=22, color=YES).move_to(
            [x0r + 2.4, 2.35, 0])
        cr = wrapped_label(rf"every run \ ({len(LINK[0]['runs'])} per order); \ white lines: \ medians; \ "
                           r"seconds from 0.12", 5.0, font_size=18, color=GREY_A).next_to(xnr, DOWN, buff=0.2).align_to(
            axr, LEFT)
        same = note(r"the same data: \ chapter 2's three link orders, \ measured on this machine",
                    font_size=17).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A figure should carry the claim, and the same data can be made to carry opposite ones. These are "
            "chapter two's three link orders. <bookmark mark='a'/> On the left, only the medians, with the axis "
            f"cut just below the smallest. The tallest bar stands {say1(TALL)} times taller than the shortest, and "
            "the title announces that link order changes speed. <bookmark mark='b'/> On the right, the same "
            f"experiment: every one of the {say(sum(len(r['runs']) for r in LINK))} runs, the medians marked, and "
            "an axis that shows the spread. The medians differ by under one percent; the runs within each order "
            f"spread by {say(min(RUN_SPREADS))} to {say(max(RUN_SPREADS))} percent. <bookmark mark='c'/> And its "
            "title states the claim the figure supports. Edward Tufte, in 1983, put the rule this way: the "
            "representation of numbers should be directly proportional to the quantities they represent. Show the "
            "spread, label the units, and let the reader check you."
        ) as vo:
            self.play(FadeIn(head), FadeIn(same))
            vo.wait_until("a")
            self.play(Create(axl), Create(basel), FadeIn(ytl), FadeIn(xnl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(cl))
            self.play(FadeIn(tl))
            vo.wait_until("b")
            self.play(Create(axr), Create(baser), FadeIn(ytr), FadeIn(xnr))
            self.play(LaggedStart(*[FadeIn(s[0]) for s in strips], lag_ratio=0.3), run_time=2)
            self.play(*[Create(s[1]) for s in strips], FadeIn(cr))
            vo.wait_until("c")
            self.play(FadeIn(tr), Indicate(tr, color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipeline(self):
        head = label(r"Every number computed: \ how it travels", font_size=36).to_edge(UP, buff=0.3)
        stages = [(r"instrument", "method.py", DATA), (r"compute", "compute.py", KERN),
                  (r"cache", "bias.json", LAM), (r"scene", "load(\"bias\")", HEAD),
                  (r"screen \ and voice", "6.7%", YES)]
        boxes = VGroup()
        for t, m, c in stages:
            r = RoundedRectangle(width=2.3, height=1.1, corner_radius=0.1, stroke_color=c, stroke_width=1.8,
                                 fill_color=c, fill_opacity=0.1)
            inner = VGroup(label(t, font_size=20, color=c), mono(m, size=15, color=WHITE)).arrange(DOWN, buff=0.12)
            if inner.width > 2.15:
                inner.width = 2.15
            boxes.add(VGroup(r, inner.move_to(r)))
        boxes.arrange(RIGHT, buff=0.45).next_to(head, DOWN, buff=0.5)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.04, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.35) for i in range(4)])
        where = VGroup(*[note(t, font_size=16).next_to(b, DOWN, buff=0.1) for t, b in zip(
            (r"explainer/cs/research", r"one item per result", r".cache/cs61", r"never types a number",
             r"formatted from it"), boxes)])
        js = code_block(['"env_spread": ' + f"{B['env_spread']:.6f}" + ',', '"reps": ' + f"{B['reps']}" + ','],
                        size=16)
        py = code_block(['f"The median time moves by up to "',
                         'f"{100 * b[\'env_spread\']:.0f} percent."'], size=16)
        out = label(rf"``The median time moves by up to {ENV_SPREAD:.0f} percent.''", font_size=20,
                    color=YES)
        jsl = label(r"in the cache:", font_size=18, color=LAM)
        pyl = label(r"in the scene of the hook:", font_size=18, color=HEAD)
        outl = label(r"spoken:", font_size=18, color=YES)
        g1 = VGroup(jsl, js).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        g2 = VGroup(pyl, py).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        g3 = VGroup(outl, out).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        low = VGroup(g1, g2, g3).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(where, DOWN, buff=0.45)
        low.to_edge(LEFT, buff=0.8)
        tests = wrapped_label(r"the instrument has its own tests \ (tests/test\_cs61\_research.py); \ rerun it on "
                              r"another machine and every figure and sentence follows", 4.8, font_size=19,
                              color=WHITE).to_edge(RIGHT, buff=0.4).match_y(low)
        with self.voiceover(
            "This series holds itself to a rule: every number on screen is computed by our own code, or is "
            "published and named. Here is how a computed number travels. <bookmark mark='a'/> An instrument, a "
            "Python module with its own tests, does the work: here, the measurement-bias experiment. "
            "<bookmark mark='b'/> A compute script runs each item once and stores the result in a cache, as JSON, "
            "under the part's name. <bookmark mark='c'/> A scene loads it. A scene never computes the experiment "
            "and never types a number in. <bookmark mark='d'/> And the narration is formatted from the same "
            "value, so the sentence you hear cannot disagree with the measurement. <bookmark mark='e'/> Rerun "
            "the instrument on another machine, and every chart and every sentence that depends on it changes "
            "with it. You need not trust us; you can check."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(where[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]), FadeIn(where[1]))
            self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]), FadeIn(where[2]), FadeIn(g1))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[2]), FadeIn(boxes[3]), FadeIn(where[3]), FadeIn(g2))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[3]), FadeIn(boxes[4]), FadeIn(where[4]), FadeIn(g3))
            vo.wait_until("e")
            self.play(FadeIn(tests))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def labels(self):
        head = label(r"Three kinds of number, \ three labels", font_size=36).to_edge(UP, buff=0.3)
        bins_spec = [(r"computed here", r"by our instruments, \ on this machine", DATA),
                     (r"published", r"authors and year named", LAM),
                     (r"illustrative", r"invented, \ and marked so", HEAD)]
        bins = VGroup()
        for t, s, c in bins_spec:
            r = RoundedRectangle(width=4.0, height=2.7, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.06)
            tt = VGroup(label(t, font_size=22, color=c), label(s, font_size=17, color=GREY_A)).arrange(DOWN,
                                                                                                    buff=0.06)
            tt.next_to(r.get_top(), DOWN, buff=0.12)
            bins.add(VGroup(r, tt))
        bins.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1.05)
        nums = [
            (rf"{ENV_SPREAD:.1f}\% \ (ch.\ 2)", 0), (rf"{G['worst']:,} \ (ch.\ 5)", 0), (r"350 times \ (ch.\ 7)", 0),
            (r"$4 \times 10^{18}$ \ (2014)", 1), (r"906{,}150{,}257 \ (1980)", 1), (r"$144^5$ \ (1966)", 1),
            (r"2.1 times \ (ch.\ 6)", 2), (rf"{M['times_a'][0]:g} s and {M['times_a'][1]:g} s \ (ch.\ 3)", 2),
        ]
        chips = VGroup(*[chip(t, bins_spec[k][2], size=19) for t, k in nums])
        chips.arrange_in_grid(rows=2, buff=(0.3, 0.3)).next_to(head, DOWN, buff=0.45)
        targets = []
        count = [0, 0, 0]
        for (_, k) in nums:
            b = bins[k][0]
            j = count[k]
            count[k] += 1
            targets.append(b.get_center() + DOWN * 0.3 + DOWN * 0.5 * (j - 1))
        hamming = wrapped_label(r"Hamming: \ doing the work is not enough; \ write clearly and give talks, \ so "
                                r"that people read and listen \ (Zobel's \textit{Writing for Computer Science} "
                                r"is the handbook)", 12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Three kinds of number appear in this series, and each wears its label. <bookmark mark='a'/> Computed "
            f"numbers come from our instruments, on this machine, and say so: the {say1(ENV_SPREAD)} percent "
            "spread, the hardest Goldbach case below two million, the limit of three hundred and fifty. "
            "<bookmark mark='b'/> Published numbers are named, with their authors and year, in the narration: "
            "Goldbach checked to four times ten to the eighteenth, Pólya's conjecture failing near nine hundred "
            "and six million. <bookmark mark='c'/> Illustrative numbers "
            "are marked on screen: the invented paper's two point one, chapter three's "
            "one second and four. <bookmark mark='d'/> Readers trust a writer who shows them how to check. "
            "Hamming put it bluntly: doing the work is not enough; you must write clearly and give "
            "talks, so that people will read and listen. Justin Zobel's Writing for Computer Science is the "
            "handbook for the first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(chips), FadeIn(bins))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                idx = [i for i, (_, kk) in enumerate(nums) if kk == k]
                self.play(*[chips[i].animate.move_to(targets[i]) for i in idx], run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(hamming))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, YES)
