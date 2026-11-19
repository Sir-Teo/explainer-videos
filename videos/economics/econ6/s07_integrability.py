from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


def matrix_tex(S, color_pairs=None, font_size=34):
    rows = r" \\ ".join(" & ".join(f"{v:.1f}" for v in r) for r in S)
    return MathTex(r"\begin{pmatrix}" + rows + r"\end{pmatrix}", font_size=font_size)


class Integrability(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Integrability: \ is there a consumer behind the demand?", r"Given demand equations fitted "
             r"to data, could any preference have produced them?", "Chapter six. Integrability: is there a consumer "
             "behind the demand?")
        self.conditions()
        self.loop()
        self.meaning()

    def conditions(self):
        lp = load("loop")
        S = np.array(lp["symmetric"]["S"])
        Sc = np.array(lp["circular"]["S"])
        head = label(r"from demand back to a preference", font_size=34).to_edge(UP, buff=0.45)
        hist = label(r"Antonelli (1886); \ Hurwicz and Uzawa (1971)", font_size=22, color=GREY_B).next_to(
            head, DOWN, buff=0.15)
        conds = VGroup(
            label(r"1. \ spending adds up to income", font_size=31),
            label(r"2. \ homogeneous of degree zero", font_size=31),
            label(r"3. \ the Slutsky matrix is \\ \quad negative semidefinite", font_size=31),
            label(r"4. \ and it is \emph{symmetric}", font_size=31, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        m1 = VGroup(label(r"tastes that come from a preference", font_size=24, color=IC),
                    matrix_tex(S, font_size=36)).arrange(DOWN, buff=0.15)
        m2 = VGroup(label(r"tastes that go round in a circle", font_size=24, color=GIFF),
                    matrix_tex(Sc, font_size=36)).arrange(DOWN, buff=0.15)
        mats = VGroup(m1, m2).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.45)
        sym_note = label(r"fish, coconuts, cloth: \ compensated responses $S_{ij}$", font_size=21,
                         color=GREY_B).next_to(mats, UP, buff=0.15)
        two = label(r"with two goods, \ 1 and 2 make 4 automatic", font_size=27, color=GREY_A).next_to(
            conds, DOWN, buff=0.5).align_to(conds, LEFT)
        with self.voiceover(
            "Economists rarely observe a preference. They observe purchases, fit demand equations to them, and "
            "then use those equations for welfare. That only makes sense if some preference could have produced "
            "the equations. <bookmark mark='a'/> When can it? The question goes back to Giovanni Antonelli in 1886, "
            "and was settled by Leonid Hurwicz and Hirofumi Uzawa in 1971. <bookmark mark='b'/> Spending must add "
            "up to income; demand must be homogeneous; the matrix of substitution effects, the Slutsky matrix, must "
            "be negative semidefinite, which is the law of compensated demand for any combination of price "
            "changes; <bookmark mark='c'/> and that matrix must be symmetric. The compensated effect of the price of "
            "coconuts on fish must equal the compensated effect of the price of fish on coconuts. "
            "<bookmark mark='d'/> Here are two sets of tastes over fish, coconuts and cloth. The first matrix is "
            "symmetric. The second is not: its effects go round in a circle. <bookmark mark='e'/> With only two "
            "goods, symmetry comes for free; with three or more, it's a real restriction, and a testable one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hist))
            vo.wait_until("a")
            self.play(Indicate(hist, color=E.ACCENT))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.15) for c_ in conds[:3]], lag_ratio=0.5),
                      run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(conds[3], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(sym_note), FadeIn(m1))
            self.play(FadeIn(m2))
            vo.wait_until("e")
            self.play(FadeIn(two))
        self.clear_scene()

    def loop(self):
        lp = load("loop")
        from explainer.ai.viz import axes

        R = lp["radius"]
        pax = axes([-0.6, 0.6], [-0.6, 0.6], x_length=4.6, y_length=4.6, xticks=[-0.4, 0, 0.4], yticks=[-0.4, 0, 0.4],
                   xlabel=r"log price of fish", ylabel=r"log price of coconuts", font_size=17,
                   xfmt=lambda v: f"{v:+.1f}" if v else "0", yfmt=lambda v: f"{v:+.1f}" if v else "0",
                   center=LEFT * 3.9 + DOWN * 0.15)
        pa = pax.ax
        circ = Circle(radius=abs(pa.c2p(R, 0)[0] - pa.c2p(0, 0)[0]), color=GREY_B, stroke_width=2).move_to(
            pa.c2p(0, 0))
        mx = axes([0, 1], [-0.42, 0.12], x_length=6.2, y_length=4.6, xticks=[0, 0.25, 0.5, 0.75, 1.0],
                  yticks=[-0.4, -0.3, -0.2, -0.1, 0, 0.1], xlabel=r"how far round the loop",
                  ylabel=r"log of compensated income", font_size=17, xfmt=lambda v: f"{v:.2f}",
                  yfmt=lambda v: f"{v:+.2f}" if v else "0", center=RIGHT * 2.7 + DOWN * 0.15)
        ma = mx.ax
        n = len(lp["symmetric"]["log_m"])
        frac = np.linspace(0, 1, n)
        t = ValueTracker(0.0)
        path = np.array(lp["path"])

        def pt(fr):
            k = fr * (n - 1)
            i = int(min(np.floor(k), n - 2))
            w = k - i
            return (1 - w) * path[i] + w * path[i + 1]

        mover = always_redraw(lambda: Dot(pa.c2p(*pt(t.get_value())), radius=0.1, color=E.ACCENT))
        trails = {}
        for key, col in (("symmetric", IC), ("circular", GIFF)):
            lm = np.array(lp[key]["log_m"])
            full = VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(
                [ma.c2p(f, v) for f, v in zip(frac, lm)])
            tr = always_redraw(lambda full=full: full.copy().pointwise_become_partial(full, 0,
                                                                                     max(t.get_value(), 1e-3)))
            trails[key] = tr
        start = DashedLine(ma.c2p(0, 0), ma.c2p(1, 0), color=GREY_D, stroke_width=1.5)
        gap = lp["circular"]["gap"]
        gl = Line(ma.c2p(1, 0), ma.c2p(1, gap), color=GIFF, stroke_width=6)
        glab = label(rf"{100 * (np.exp(gap) - 1):.1f}\% \\ at the same \\ prices", font_size=22, color=GIFF).move_to(
            ma.c2p(0.87, -0.3))
        gpoint = Arrow(glab.get_top() + UP * 0.05, ma.c2p(0.99, gap / 2), color=GIFF, buff=0.05,
                       stroke_width=3, max_tip_length_to_length_ratio=0.2)
        leg = VGroup(label(r"symmetric: \ back where it started", font_size=20, color=IC),
                     label(r"circular: \ less money, \ same prices", font_size=20, color=GIFF)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(mx, UP, buff=0.1)
        green = MathTex(r"\oint d\log m = (\gamma_{21}-\gamma_{12})\times\text{area}"
                        rf" = ({lp['circular']['gamma'][1][0]:.2f}-{lp['circular']['gamma'][0][1]:.2f})"
                        rf"\times \pi\,{R}^2 = {lp['circular']['green']:.3f}", font_size=30,
                        color=E.ACCENT).to_edge(DOWN, buff=0.12)
        rule = label(r"at every step: \ $d\log m = \sum_i w_i\, d\log p_i$ \ (just enough money)", font_size=20,
                     color=GREY_A).next_to(pax, UP, buff=0.1)
        tag = agora_tag(r"computed: Agora, shares linear in log prices", corner=UR, font_size=13)
        with self.voiceover(
            "What goes wrong without symmetry? Take the consumer on a trip. <bookmark mark='a'/> Prices of fish "
            "and coconuts move round this circle, and come back to where they started; cloth's price never moves. "
            "<bookmark mark='b'/> At every step, adjust the consumer's money by just enough to compensate for that "
            "step's price change: the cost of what they buy, times how much each price moved. "
            "<bookmark mark='c'/> With tastes from a preference, compensated income is simply the expenditure "
            "function at fixed utility, so when the prices come home, so does the money. "
            "<bookmark mark='d'/> With the circular tastes, it doesn't. Back at the very same prices, the consumer "
            "needs three percent less money than they started with, yet at every step they were exactly "
            "compensated. Go round the other way, and they'd need three percent more. Someone could walk them "
            "round and round and collect the difference: Part five's money pump, built from a demand equation. "
            "<bookmark mark='e'/> And by Green's theorem, the gap is the asymmetry of the matrix times the area "
            "the loop encloses."
        ) as vo:
            self.play(FadeIn(pax), Create(circ), FadeIn(rule), FadeIn(tag))
            self.add(mover)
            vo.wait_until("a")
            self.play(FadeIn(mx), FadeIn(start))
            vo.wait_until("b")
            self.add(trails["symmetric"], trails["circular"])
            self.play(t.animate.set_value(0.5), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(1.0), run_time=4.0, rate_func=linear)
            self.play(FadeIn(leg[0]))
            vo.wait_until("d")
            self.play(Create(gl), FadeIn(glab), GrowArrow(gpoint), FadeIn(leg[1]))
            vo.wait_until("e")
            self.play(Write(green), run_time=2.0)
        self.clear_scene()

    def meaning(self):
        cards = point_cards([
            (r"a test", r"symmetry and homogeneity are restrictions \\ on fitted demand equations: \\ chapter 10 "
                        r"tests them", HICKS),
            (r"a licence", r"if they hold, \ a preference exists, \\ and its expenditure function \\ gives "
                           r"welfare in dollars", E.ACCENT),
            (r"Part 5, again", r"for a finite list of purchases, \\ the same question is GARP, \\ and Afriat's "
                               r"theorem answers it", SUB),
        ], width=13.0, cols=3, font_size=29).move_to(DOWN * 0.2)
        head = label(r"Integrability, in practice", font_size=36).to_edge(UP, buff=0.6)
        with self.voiceover(
            "So integrability matters in three ways. <bookmark mark='a'/> It's a test: an estimated demand system "
            "whose substitution matrix isn't symmetric can't come from any single consumer, and chapter ten tests "
            "it. <bookmark mark='b'/> It's a licence: when the conditions hold, a preference exists, and its "
            "expenditure function turns price changes into dollars. <bookmark mark='c'/> And it's Part five again. "
            "For a finite list of purchases rather than smooth equations, the same question is whether the "
            "purchases satisfy GARP, and Afriat's theorem gives the answer."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c_ in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.15))
        self.clear_scene()
