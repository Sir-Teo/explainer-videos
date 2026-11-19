from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


def fbox(title: str, sub: str, formula: str, color, width=4.2, height=1.9) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.08)
    t = VGroup(MathTex(formula, font_size=40, color=color), label(title, font_size=25),
               label(sub, font_size=19, color=GREY_A)).arrange(DOWN, buff=0.12).move_to(box)
    g = VGroup(box, t)
    g.box = box
    return g


class Duality(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Duality: \ four functions, \ one consumer", r"Why describe the same consumer four ways?",
             "Chapter five. Duality: four functions, one consumer.")
        self.two_problems()
        self.square()
        self.shephard()
        self.checks()

    def two_problems(self):
        b = load("bo")
        ax = goods_axes(center=LEFT * 3.2 + DOWN * 0.3, top=11, x_length=5.6, y_length=5.6, ticks=(0, 2, 4, 6, 8, 10))
        a = ax.ax
        xs = np.array(b["xs"])
        ic0 = curve(ax, xs, np.array(b["ic0"]), color=IC, width=3, top=11)
        line = budget_line(ax, 6.0, 10.0)
        A = Dot(a.c2p(*b["A"]), radius=0.1, color=CHOICE)
        k = ValueTracker(110.0)
        slide = always_redraw(lambda: DashedVMobject(Line(a.c2p(min(k.get_value() / 10, 11), 0 if k.get_value() / 10
                                                                <= 11 else (k.get_value() - 110) / 6),
                                                          a.c2p(0 if k.get_value() / 6 <= 11 else
                                                                (k.get_value() - 66) / 10, min(k.get_value() / 6, 11)),
                                                          color=HICKS, stroke_width=3), num_dashes=24))
        cost = always_redraw(lambda: label(rf"spend \${k.get_value():.0f}", font_size=24, color=HICKS).move_to(
            a.c2p(8.5, 10.2)))
        p1 = VGroup(label(r"Bo's problem", font_size=28, color=WHO["bo"]),
                    label(r"the most satisfaction \$60 can buy", font_size=24),
                    MathTex(r"\Rightarrow\; x(p, m),\;\; v(p, m)", font_size=34, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        p2 = VGroup(label(r"the shopkeeper's problem", font_size=28, color=HICKS),
                    label(r"the least money that reaches \\ Bo's indifference curve", font_size=24),
                    MathTex(r"\Rightarrow\; h(p, u),\;\; e(p, u)", font_size=34, color=HICKS)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        same = label(r"the same bundle, \ the same \$60: \\ each problem's answer solves the other", font_size=25,
                     color=E.ACCENT)
        VGroup(p1, p2, same).arrange(DOWN, aligned_edge=LEFT, buff=0.55).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Everything so far started from one problem. <bookmark mark='a'/> Bo has sixty dollars, and he wants "
            "the most satisfaction they can buy. Its answers are his demand, x of p and m, and the satisfaction he "
            "reaches, the indirect utility, v of p and m. <bookmark mark='b'/> Now turn the problem inside out. "
            "Fix the indifference curve, and ask what is the least money that reaches it at these prices. Start "
            "with a budget that's far too big, and shrink it. <bookmark mark='c'/> The cheapest budget that still "
            "touches the curve touches it at the same bundle, and costs exactly sixty dollars. "
            "<bookmark mark='d'/> Its answers are Hicks's compensated demand, h of p and u, and the expenditure "
            "function, e of p and u: the cost of a given level of satisfaction at given prices. The two problems "
            "are duals: the answer to each solves the other."
        ) as vo:
            self.play(FadeIn(ax), Create(ic0), FadeIn(p1[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(A), FadeIn(p1[1:]))
            vo.wait_until("b")
            self.add(slide, cost)
            self.play(FadeIn(p2))
            self.play(k.animate.set_value(60.0), run_time=4.0, rate_func=smooth)
            vo.wait_until("c")
            self.play(Indicate(A, color=E.ACCENT, scale_factor=1.6))
            vo.wait_until("d")
            self.play(FadeIn(same))
        self.clear_scene()

    def square(self):
        X = fbox(r"Marshall's demand", r"what is bought with money $m$", r"x(p, m)", WHITE)
        H = fbox(r"Hicks's demand", r"what is bought to reach utility $u$", r"h(p, u)", HICKS)
        V = fbox(r"indirect utility", r"the most $m$ can reach", r"v(p, m)", WHITE)
        Ef = fbox(r"expenditure function", r"the least that reaches $u$", r"e(p, u)", HICKS)
        grid = VGroup(X, H, V, Ef).arrange_in_grid(rows=2, cols=2, buff=(3.4, 1.4)).move_to(DOWN * 0.15)
        ar = VGroup(
            DoubleArrow(V.get_right(), Ef.get_left(), buff=0.12, color=E.ACCENT, stroke_width=4, tip_length=0.2),
            DoubleArrow(X.get_right(), H.get_left(), buff=0.12, color=E.ACCENT, stroke_width=4, tip_length=0.2),
            Arrow(V.get_top(), X.get_bottom(), buff=0.12, color=SUB, stroke_width=4, tip_length=0.2),
            Arrow(Ef.get_top(), H.get_bottom(), buff=0.12, color=SUB, stroke_width=4, tip_length=0.2),
        )
        labs = VGroup(
            label(r"inverses: \\ $e(p, v(p,m)) = m$", font_size=22, color=E.ACCENT).next_to(ar[0], DOWN, buff=0.12),
            label(r"$h(p,u) = x(p, e(p,u))$", font_size=22, color=E.ACCENT).next_to(ar[1], UP, buff=0.12),
            label(r"Roy's identity \\ $x = -\dfrac{\partial v/\partial p}{\partial v/\partial m}$", font_size=21,
                  color=SUB).next_to(ar[2], LEFT, buff=0.15),
            label(r"Shephard's lemma \\ $h = \dfrac{\partial e}{\partial p}$", font_size=21, color=SUB).next_to(
                ar[3], RIGHT, buff=0.15),
        )
        head = label(r"one consumer, \ four functions", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "So one consumer can be described by four functions. <bookmark mark='a'/> Two demands: Marshall's, "
            "which you can see in a shop, and Hicks's, which holds satisfaction fixed. And two value functions: the "
            "indirect utility, and the expenditure function. <bookmark mark='b'/> They are tied together by "
            "identities. The indirect utility and the expenditure function are inverses: the least money that "
            "reaches what sixty dollars can reach is sixty dollars. And Hicks's demand is Marshall's, evaluated at "
            "just enough money. <bookmark mark='c'/> Going up the left side, Roy's identity, from René Roy in 1947: "
            "demand is the slope of indirect utility in a price, divided by its slope in money. "
            "<bookmark mark='d'/> Up the right, Shephard's lemma, from Ronald Shephard in 1953: compensated demand "
            "is simply the slope of the expenditure function in that good's price. Know any one of the four "
            "functions, and you can recover the other three."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g_, scale=0.95) for g_ in grid], lag_ratio=0.3), run_time=2.4)
            vo.wait_until("b")
            self.play(GrowFromCenter(ar[0]), FadeIn(labs[0]), GrowFromCenter(ar[1]), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(GrowArrow(ar[2]), FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(GrowArrow(ar[3]), FadeIn(labs[3]))
        self.clear_scene()

    def shephard(self):
        d = load("duality")
        b = load("bo")
        from explainer.ai.viz import axes

        ax = axes([0, 30], [0, 140], x_length=7.0, y_length=5.2, xticks=[0, 5, 10, 15, 20, 25, 30],
                  yticks=[0, 20, 40, 60, 80, 100, 120, 140], xlabel=r"price of fish (\$)",
                  ylabel=r"money to stay on Bo's old curve (\$)", font_size=18, center=LEFT * 2.2 + DOWN * 0.3)
        a = ax.ax
        px, e, pas = np.array(d["px"]), np.array(d["e"]), np.array(d["passive"])
        ecur = VMobject(stroke_color=HICKS, stroke_width=5).set_points_smoothly([a.c2p(x, y) for x, y in zip(px, e)
                                                                                 if y <= 140])
        keep = pas <= 140
        tline = Line(a.c2p(px[keep][0], pas[keep][0]), a.c2p(px[keep][-1], pas[keep][-1]), color=BUDGET,
                     stroke_width=3)
        p0 = d["p0"]
        dot = Dot(a.c2p(p0, 60), radius=0.1, color=WHITE)
        gap_p = 6.0
        e6 = float(np.interp(gap_p, px, e))
        gap = VGroup(*[Line(a.c2p(q, float(np.interp(q, px, e))), a.c2p(q, 3.6 * q + 24), color=SUB, stroke_width=5)
                       for q in (2.0, gap_p, 18.0, 27.0)])
        side = VGroup(
            label(r"the curve: \ $e(p_x, u_0)$", font_size=25, color=HICKS),
            label(rf"the line: \ the cost of Bo's old bundle, \\ ${b['A'][0]:.1f}\,p_x + 24$", font_size=24,
                  color=BUDGET),
            label(rf"they touch at \$10; \ the slope there is \\ {d['x_fish']:.1f} fish: \ Shephard's lemma",
                  font_size=24),
            label(rf"at \$6 the gap is \${3.6 * gap_p + 24 - e6:.2f}: \\ Slutsky's \${b['m_slutsky']:.2f} against "
                  rf"Hicks's \${b['m_hicks']:.2f}", font_size=24, color=SUB),
            label(r"the curve lies below every such line: \\ $e$ is concave in prices, \\ so compensated demand "
                  r"slopes down", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: Agora's demand systems", corner=DR, font_size=14)
        with self.voiceover(
            "Shephard's lemma deserves a picture, because it explains the sign promised in chapter three. "
            "<bookmark mark='a'/> This curve is the expenditure function: the money Bo needs to stay on his old "
            "indifference curve, as the price of fish varies. <bookmark mark='b'/> This straight line is the cost "
            "of his old bundle, three point six fish and four coconuts, at each price: what he'd need if he never "
            "changed what he buys. <bookmark mark='c'/> At ten dollars they touch, and the slope of the curve there "
            "is three point six: the fish in his compensated bundle. That is Shephard's lemma. "
            "<bookmark mark='d'/> Away from ten dollars, the curve lies below the line, because Bo can always do "
            "at least as well as his old bundle, and usually better by substituting. At six dollars the gap is one "
            "dollar forty-four, exactly the difference between Slutsky's compensation and Hicks's. "
            "<bookmark mark='e'/> A curve that lies below all its tangent lines is concave. So its slope, the "
            "compensated demand, can only fall as the price rises. Compensated demand slopes down, for every "
            "consumer. And that gap under the line will come back in chapter nine as the substitution bias in a "
            "price index."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ecur), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(tline), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dot, scale=1.6), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(gap), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def checks(self):
        d = load("duality")
        names = list(d["errors"].keys())
        idents = list(d["errors"][names[0]].keys())
        short = {"e(p, v(p, m)) = m": r"$e(p, v) = m$", "v(p, e(p, u)) = u": r"$v(p, e) = u$",
                 "h(p, v(p, m)) = x(p, m)": r"$h(p, v) = x$", "Shephard: de/dp = h": r"Shephard",
                 "Roy: -v_p / v_m = x": r"Roy"}
        cols = [label(r"", font_size=20)] + [label(short[i], font_size=26, color=E.ACCENT) for i in idents]
        rows = [cols]
        disp = {"Cobb-Douglas": r"Cobb--Douglas", "CES, sigma 0.5": r"CES, $\sigma = 0.5$",
                "linear expenditure": r"linear expenditure", "AIDS": r"AIDS"}
        for n_ in names:
            r = [label(disp[n_], font_size=26)]
            for i in idents:
                v = d["errors"][n_][i]
                txt = r"$< 10^{-15}$" if v < 1e-15 else rf"${v / 10 ** np.floor(np.log10(v)):.0f}\times10^{{{int(np.floor(np.log10(v)))}}}$"
                r.append(label(txt, font_size=25, color=GREY_A))
            rows.append(r)
        tab = VGroup(*[m for r in rows for m in r]).arrange_in_grid(rows=len(rows), cols=len(cols), buff=(0.5, 0.4))
        tab.move_to(UP * 0.2)
        head = label(r"the identities, checked numerically \ (largest relative error)", font_size=30).to_edge(
            UP, buff=0.5)
        foot = label(r"three goods, \ prices (2, 3, 1.5), \ income 100; \ derivatives by central differences",
                     font_size=21, color=GREY_B).next_to(tab, DOWN, buff=0.45)
        why = label(r"why it matters: \ estimate one function, \ and the others follow, \ welfare included",
                    font_size=26, color=HICKS).to_edge(DOWN, buff=0.5)
        tag = agora_tag(r"computed: agora.demand.duality\_errors", corner=DR, font_size=14)
        with self.voiceover(
            "These identities are exact, and Agora checks them. <bookmark mark='a'/> Four demand systems you'll "
            "meet in this part: Cobb–Douglas, CES, the linear expenditure system and the almost ideal demand "
            "system, each with three goods. For each, every identity holds to within about one part in a billion, "
            "which is the precision of the numerical derivatives. <bookmark mark='b'/> Why care? Because the "
            "functions you can estimate are the ones you can see, demands, and the ones you want for welfare are "
            "the ones you can't, expenditure and utility. Duality is the bridge. Chapter eight walks across it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in [tab[i * len(cols):(i + 1) * len(cols)]
                                                                  for i in range(len(rows))]], lag_ratio=0.4),
                      FadeIn(foot), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(why, shift=UP * 0.1))
        self.clear_scene()
