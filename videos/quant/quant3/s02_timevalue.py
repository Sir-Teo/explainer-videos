from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, PART, VALUE, load

C_ = {r"V": VALUE, r"D_1": CASH, r"r": QC.IMPLIED, r"g": CASH}

IRR_CODE = [
    "def irr_bisect(cash_flows, lo=0.0, hi=1.0, steps=40):",
    "    f = lambda r: npv(r, cash_flows)",
    "    flo, brackets = f(lo), [(lo, hi)]",
    "    for _ in range(steps):",
    "        mid = (lo + hi) / 2",
    "        fm = f(mid)",
    "        if flo * fm <= 0:      # the sign changes in [lo, mid]",
    "            hi = mid",
    "        else:",
    "            lo, flo = mid, fm",
    "        brackets.append((lo, hi))",
    "    return (lo + hi) / 2, brackets",
]


def row(*parts, fs=42):
    return cmath(*parts, colors=C_, font_size=fs)


class TimeValue(VoiceoverScene, ThreeDScene):
    def construct(self):
        tv = load("timevalue")
        self.card()
        self.conveyor()
        self.annuity(tv)
        self.lab(tv)
        self.two_roots(tv)
        self.gordon()

    def card(self):
        c = chapter_card(1, r"Time value, IRR and the growing perpetuity", r"What is a dollar next year worth today?",
                         part=PART)
        with self.voiceover("Chapter one. Time value, the internal rate of return, and the growing perpetuity."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def conveyor(self):
        r = ValueTracker(0.02)
        n = 24

        def bars():
            g = VGroup()
            rr = r.get_value()
            for t in range(1, n + 1):
                h = 3.0 / (1 + rr) ** t
                col = interpolate_color(ManimColor(CASH), ManimColor(GREY_D), t / n)
                b = Rectangle(width=0.5, height=max(h, 0.01), fill_color=col, fill_opacity=0.85, stroke_width=0.6,
                              stroke_color=BLACK).rotate(PI / 2, RIGHT)  # a card standing up, facing the viewer
                b.move_to([0, 0.55 * t - 6.0, h / 2])
                g.add(b)
            return g

        conv = always_redraw(bars)
        floor = Line([0, -5.6, 0], [0, 0.55 * n - 5.8, 0], color=GREY_D, stroke_width=2)
        defn = definition_card(r"Present value", r"A payment $C$ in $t$ years is worth $C/(1 + r)^t$ today: the sum "
                               r"you would invest now at $r$ to have $C$ then. A project's net present value (NPV) "
                               r"adds this up over all its cash flows, costs negative.", width=5.6, color=VALUE,
                               font_size=21).to_corner(UL, buff=0.3)
        rd = VGroup(MathTex(r"r =", font_size=34, color=QC.IMPLIED),
                    DecimalNumber(2.0, num_decimal_places=1, font_size=34, color=QC.IMPLIED, unit=r"\%"))
        rd.arrange(RIGHT, buff=0.15)
        pv = VGroup(label(r"PV of 24 payments of 1:", font_size=24, color=GREY_A),
                    DecimalNumber(0, num_decimal_places=2, font_size=34, color=VALUE))
        pv.arrange(RIGHT, buff=0.2)
        far = VGroup(label(r"the 24th payment is worth today", font_size=22, color=GREY_A),
                     DecimalNumber(0, num_decimal_places=2, font_size=30, color=CASH)).arrange(RIGHT, buff=0.2)
        panel = VGroup(rd, pv, far).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(DR, buff=0.4)
        rd[1].set_value(2.0)
        pv[1].set_value(sum(1.02 ** -t for t in range(1, n + 1)))
        far[1].set_value(1.02 ** -n)
        self.set_camera_orientation(phi=72 * DEGREES, theta=-28 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(defn, panel)
        self.remove(defn, panel)
        with self.voiceover(
            "A dollar next year is worth less than a dollar today, because today's dollar could be invested. Here are twenty-four "
            "yearly payments on a conveyor running away from us; each bar is a payment's value today, divided by one plus r once "
            "for every year it waits. <bookmark mark='a'/> At two percent the far bars have barely shrunk. "
            "<bookmark mark='b'/> Raise the rate and watch where value goes: the near bars hardly move, the far ones collapse. "
            "At twelve percent the last payment is worth about six cents. <bookmark mark='c'/> Distant cash is the cash most "
            "exposed to the rate."
        ) as vo:
            self.play(FadeIn(defn), Create(floor))
            self.add(conv)
            self.play(FadeIn(panel))
            rd[1].add_updater(lambda m: m.set_value(100 * r.get_value()))
            pv[1].add_updater(lambda m: m.set_value(sum((1 + r.get_value()) ** -t for t in range(1, n + 1))))
            far[1].add_updater(lambda m: m.set_value((1 + r.get_value()) ** -n))
            vo.wait_until("a")
            self.move_camera(theta=-40 * DEGREES, run_time=2)
            vo.wait_until("b")
            self.play(r.animate.set_value(0.12), run_time=6, rate_func=smooth)
            vo.wait_until("c")
            self.move_camera(theta=-65 * DEGREES, phi=62 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        for m in (rd[1], pv[1], far[1]):
            m.clear_updaters()
        conv.clear_updaters()
        self.play(FadeOut(VGroup(conv, floor)), FadeOut(defn), FadeOut(panel))
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        self.clear_scene()

    def annuity(self, tv):
        rows = [
            row(r"\text{perpetuity}", r"=", r"\frac{C}{1+r} + \frac{C}{(1+r)^2} + \cdots", r"=", r"\frac{C}{r}"),
            row(r"\text{annuity}_n", r"=", r"\frac{C}{r}", r"-", r"\frac{1}{(1+r)^n}\,\frac{C}{r}"),
            row(r"\text{annuity}_n", r"=", r"\frac{C}{r}\Big(1 - (1+r)^{-n}\Big)"),
        ]
        whys = [why(r"a geometric series with ratio $1/(1+r)$"),
                why(r"a perpetuity starting now, minus the same perpetuity starting after year $n$, seen from today"),
                why(rf"factor out $C/r$: ten payments of 5 at 4\% are worth {tv['annuity']:.2f}")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            "Two closed forms do most of the work. A payment C forever is a geometric series summing to C over r, the "
            "perpetuity. <bookmark mark='a'/> An annuity for n years is a perpetuity now minus one starting after year n. "
            "<bookmark mark='b'/> Factor out C over r: ten payments of five at four percent are worth "
            f"{tv['annuity']:.2f}."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, tv):
        card = lab_card(r"the internal rate of return, by bisection", IRR_CODE,
                        source="explainer/quant/house/valuation.py", width=6.6, font_size=17)
        card.to_corner(UL, buff=0.3)
        br = [tuple(b) for b in tv["bond_brackets"]]
        nl = NumberLine(x_range=[0, 0.2, 0.05], length=5.6, include_numbers=False, color=GREY_C)
        nl.to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        ticks = VGroup(*[MathTex(f"{int(100 * v)}\\%", font_size=20, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.15)
                         for v in (0, 0.05, 0.1, 0.15, 0.2)])
        k = ValueTracker(0)

        def bracket():
            i = int(np.clip(round(k.get_value()), 0, len(br) - 1))
            lo, hi = br[i]
            seg = Line(nl.n2p(lo), nl.n2p(hi), color=QC.HOUSE, stroke_width=10)
            ends = VGroup(Line(nl.n2p(lo) + DOWN * 0.18, nl.n2p(lo) + UP * 0.18, color=QC.HOUSE, stroke_width=3),
                          Line(nl.n2p(hi) + DOWN * 0.18, nl.n2p(hi) + UP * 0.18, color=QC.HOUSE, stroke_width=3))
            txt = MathTex(rf"\text{{step}}\ {i}:\ [{100 * lo:.4f}\%,\ {100 * hi:.4f}\%]", font_size=26,
                          color=QC.HOUSE).next_to(nl, UP, buff=0.35)
            return VGroup(seg, ends, txt)

        brk = always_redraw(bracket)
        head = label(r"a bond: $-100$, then 5 a year for ten years, 100 back", font_size=22, color=GREY_A)
        head.next_to(nl, UP, buff=1.0).align_to(nl, LEFT)
        with self.voiceover(
            "The internal rate of return runs the question backwards: which rate makes the NPV zero? There is no formula in "
            "general, so the House bisects: start with a bracket where the NPV changes sign, halve it, keep the half where the "
            "sign still changes. <bookmark mark='a'/> Run it on a bond bought at a hundred, paying five a year for ten years. "
            "Each step halves the bracket. <bookmark mark='b'/> After thirty halvings: "
            f"{100 * tv['bond_irr']:.4f} percent, the coupon, as it must be at par."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Create(nl), FadeIn(ticks), FadeIn(head))
            self.add(brk)
            self.play(k.animate.set_value(12), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(len(br) - 1), run_time=1.0)
            brk.clear_updaters()
            lab_run(self, card, [f"irr_bisect(bond, 0.0, 0.2, steps=30)",
                                 f"root {tv['bond_irr']:.6f}   width {br[-1][1] - br[-1][0]:.1e}"])
        self.wait(0.4)
        self.clear_scene()

    def two_roots(self, tv):
        rs, npv = np.asarray(tv["rs"]), np.asarray(tv["npv"])
        g = axes([0, 0.32], [-1.6, 0.6], x_length=6.2, y_length=4.2, xlabel=r"discount rate $r$",
                 ylabel=r"NPV of $(-100,\ +230,\ -132)$", xticks=[0, 0.1, 0.2, 0.3], yticks=[-1.5, -1, -0.5, 0, 0.5],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.32, 0), color=GREY_B, stroke_width=1.5)
        line = curve(ax, rs, npv, VALUE, stroke_width=4)
        roots = VGroup(*[Dot(ax.c2p(x, 0), radius=0.09, color=QC.HOUSE) for x in (tv["root1"], tv["root2"])])
        rows = VGroup(
            cmath(r"-100 + \frac{230}{1+r} - \frac{132}{(1+r)^2}", r"=", r"0", font_size=32),
            cmath(r"100x^2 - 230x + 132", r"=", r"0,\quad x = 1 + r", font_size=32),
            cmath(r"x", r"=", r"1.1\ \text{or}\ 1.2", font_size=32, colors={r"1.1\ \text{or}\ 1.2": QC.HOUSE}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        w = why(r"multiply by $(1+r)^2$: a quadratic in $1+r$, so two roots", 20).next_to(rows, DOWN, buff=0.25)
        w.align_to(rows, LEFT)
        pp = desk_question(r"Pause and predict: the NPV crosses zero twice. At a cost of capital of 15\%, is the "
                           r"project worth doing?", width=6.0, font_size=22).to_edge(RIGHT, buff=0.4).shift(DOWN * 2.0)
        ans = label(rf"NPV at 15\%: ${tv['npv15']:+.2f}$: yes, between the roots", font_size=22, color=QC.GAIN)
        ans.next_to(pp, DOWN, buff=0.15)
        with self.voiceover(
            "Bisection finds a root; it does not promise the only one. A project costs a hundred, pays two hundred and thirty, "
            "then needs a hundred and thirty-two to clean up. <bookmark mark='a'/> Multiply its NPV by one plus r squared: a "
            "quadratic, with two roots, ten and twenty percent. <bookmark mark='b'/> Cash flows that change sign twice can cross "
            "zero twice, and the rule accept if the IRR beats the cost of capital has no answer. Pause and predict: at fifteen "
            "percent, is it worth doing? <bookmark mark='c'/> Yes: the NPV is positive between the roots. The NPV rule never "
            "breaks; the IRR rule is a shortcut."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(w))
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(Create(line), run_time=2)
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in roots], lag_ratio=0.4), FadeIn(pp))
            vo.wait_until("c")
            d15 = Dot(ax.c2p(0.15, tv["npv15"]), radius=0.09, color=QC.GAIN)
            self.play(FadeIn(d15, scale=1.5), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    def gordon(self):
        rows = [
            row(r"V", r"=", r"\frac{D_1}{1 + r} + \frac{D_1(1 + g)}{(1 + r)^2} + \frac{D_1(1 + g)^2}{(1 + r)^3} + \cdots"),
            row(r"V", r"=", r"\frac{D_1}{1 + r}\sum_{k \ge 0}\Big(\frac{1 + g}{1 + r}\Big)^k"),
            row(r"V", r"=", r"\frac{D_1}{1 + r}\cdot\frac{1 + r}{r - g}", r"=", r"\frac{D_1}{r - g}"),
        ]
        whys = [why(r"a dividend that grows at $g$ forever, discounted at $r$"),
                why(r"a geometric series with ratio $(1+g)/(1+r)$"),
                why(r"it converges when $g < r$: the Gordon growth model (Gordon and Shapiro 1956)")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-2.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "The model of a share every analyst knows. A dividend D one next year, growing at g forever, each one discounted. "
            "<bookmark mark='a'/> Factor out the first term: a geometric series with ratio one plus g over one plus r. "
            "<bookmark mark='b'/> If growth is slower than the discount rate it converges: the next dividend over r minus g. "
            "Williams valued shares as discounted dividends in 1938; this closed form is Gordon and Shapiro's, from 1956."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.6)
        self.clear_scene()
