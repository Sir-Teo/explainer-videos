from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403


class Simultaneity(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Two curves, one cloud", r"Why does the best-fitting line find neither curve?",
             "Chapter two. Two curves, one cloud.", scale=("market",), horizon=("a day", "a season"))
        self.days()
        self.groups()
        self.formula()

    def days(self):
        s = load("season")
        ax = fish_axes(center=LEFT * 2.4 + DOWN * 0.2)
        a = ax.ax
        g = s["groups"]
        q0, p0 = g["ordinary"]["q"], g["ordinary"]["p"]
        b, d, F, S = s["b"], s["d"], s["F"], s["S"]

        def dem(shift):
            return line_qp(ax, -b, q0 + shift, p0, E.DEMAND, width=4)

        def sup(shift):
            return line_qp(ax, d, q0 - shift, p0, E.SUPPLY, width=4)

        def cross(fs, ss):
            p = (F * fs + S * ss) / (b + d) + p0
            q = q0 + F * fs - b * (p - p0)
            return a.c2p(q, p)

        D = dem(0)
        Sp = sup(0)
        dot = Dot(cross(0, 0), radius=0.1, color=WHITE)
        stamp = label(r"an ordinary day", font_size=26).move_to(RIGHT * 1.9 + UP * 1.8, aligned_edge=LEFT)
        texts = {
            "feast": label(r"a feast: \ demand moves out; \\ the day slides along \emph{supply}", font_size=24,
                           color=FEAST),
            "storm": label(r"a storm: \ supply moves in; \\ the day slides along \emph{demand}", font_size=24,
                           color=STORM),
            "both": label(r"both at once", font_size=24, color="#E07B53"),
        }
        for t in texts.values():
            t.next_to(stamp, DOWN, buff=0.4).align_to(stamp, LEFT)
        tag = island_tag(r"simulated: the Island's planted lines", corner=DR, font_size=15)
        with self.voiceover(
            "Every day in the market, two lines meet. <bookmark mark='a'/> The islanders' demand, and the fishers' "
            "supply. The day's price and catch are where they cross: one dot. <bookmark mark='b'/> On a feast day "
            "the islanders want more fish at every price, so demand moves out, and the dot slides up along the "
            "supply curve. <bookmark mark='c'/> On a stormy day some boats stay in, supply moves in, and the dot "
            "slides up along the demand curve. <bookmark mark='d'/> Some days have both. And every day has small "
            "shocks of its own to each curve. The season's cloud is the record of all of this, every dot an "
            "intersection, and no dot belongs to either curve alone."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(D), Create(Sp))
            self.play(FadeIn(dot, scale=0.5), FadeIn(stamp))
            vo.wait_until("b")
            self.play(Transform(D, dem(F)), dot.animate.move_to(cross(1, 0)), FadeIn(texts["feast"]), run_time=1.5)
            trail1 = Dot(cross(1, 0), radius=0.07, color=FEAST)
            self.add(trail1)
            self.play(Transform(D, dem(0)), dot.animate.move_to(cross(0, 0)), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeOut(texts["feast"]), Transform(Sp, sup(S)), dot.animate.move_to(cross(0, 1)),
                      FadeIn(texts["storm"]), run_time=1.5)
            trail2 = Dot(cross(0, 1), radius=0.07, color=STORM)
            self.add(trail2)
            self.play(Transform(Sp, sup(0)), dot.animate.move_to(cross(0, 0)), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeOut(texts["storm"]), Transform(D, dem(F)), Transform(Sp, sup(S)),
                      dot.animate.move_to(cross(1, 1)), FadeIn(texts["both"]), run_time=1.5)
            self.add(Dot(cross(1, 1), radius=0.07, color="#E07B53"))
            self.play(FadeIn(day_dots(ax, s, radius=0.035), lag_ratio=0.004), FadeOut(D), FadeOut(Sp), FadeOut(dot),
                      run_time=2.0)
        self.clear_scene()

    def groups(self):
        s = load("season")
        ax = fish_axes(center=LEFT * 2.4 + DOWN * 0.2)
        a = ax.ax
        dots = day_dots(ax, s, radius=0.035).set_opacity(0.35)
        g = s["groups"]
        marks = VGroup()
        names = {"ordinary": (r"ordinary", ORDINARY), "feast": (r"feast", FEAST), "storm": (r"storm", STORM),
                 "both": (r"both", "#E07B53")}
        for k, (nm, col) in names.items():
            pt = a.c2p(g[k]["q"], g[k]["p"])
            marks.add(VGroup(Dot(pt, radius=0.13, color=col), label(rf"{nm} \ ({g[k]['n']})", font_size=20,
                                                                     color=col).next_to(pt, RIGHT, buff=0.15)))
        e1 = Line(a.c2p(g["ordinary"]["q"], g["ordinary"]["p"]), a.c2p(g["storm"]["q"], g["storm"]["p"]),
                  color=STORM, stroke_width=4)
        e2 = Line(a.c2p(g["ordinary"]["q"], g["ordinary"]["p"]), a.c2p(g["feast"]["q"], g["feast"]["p"]),
                  color=FEAST, stroke_width=4)
        rows = VGroup(
            label(r"the average day of each kind", font_size=26),
            label(r"ordinary $\to$ storm: \ along demand", font_size=24, color=STORM),
            label(r"ordinary $\to$ feast: \ along supply", font_size=24, color=FEAST),
            label(r"mix them all, \ and the cloud leans \\ whichever way moved more", font_size=24, color=OLSC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        tag = island_tag(r"simulated: the Island's season, days grouped by what happened", corner=DR, font_size=15)
        with self.voiceover(
            "Sort the days by what happened. <bookmark mark='a'/> Here is the average day of each kind: ordinary "
            "days, feasts, storms, and the few days with both. <bookmark mark='b'/> Going from the ordinary days to "
            "the stormy ones, only supply moved, so the step runs along the demand curve. <bookmark mark='c'/> "
            "Going to the feast days, only demand moved, so the step runs along supply. <bookmark mark='d'/> A line "
            "fitted to all the days mixes the two steps, and leans toward whichever curve moved less: this season "
            "there were more feasts than storms, so the cloud leans like supply."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(dots), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in marks], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(e1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(e2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def formula(self):
        s = load("season")
        eqs = VGroup(
            MathTex(r"\text{demand: } q = a - b\,p + u \qquad \text{supply: } q = c + d\,p + v", font_size=38),
            MathTex(r"\operatorname{plim}\ \hat\beta_{\text{least squares}} = "
                    r"\frac{d\,\sigma_u^2 - b\,\sigma_v^2}{\sigma_u^2 + \sigma_v^2}", font_size=42),
            MathTex(rf"= \frac{{{s['d']:.1f} \times {s['var_u']:.0f} - {s['b']:.1f} \times {s['var_v']:.0f}}}"
                    rf"{{{s['var_u']:.0f} + {s['var_v']:.0f}}} = {s['plim']:+.1f}", font_size=38, color=OLSC),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.6)
        notes = VGroup(
            label(r"only demand moves ($\sigma_v = 0$): \ you find supply, \ $d$", font_size=25, color=E.SUPPLY),
            label(r"only supply moves ($\sigma_u = 0$): \ you find demand, \ $-b$", font_size=25, color=E.DEMAND),
            label(r"both move: \ a weighted mixture, \ neither", font_size=25, color=OLSC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.55)
        tag = island_tag(r"simulated: the Island; this season's line came out at "
                         rf"{s['ols_slope']:+.1f}", corner=DR, font_size=15)
        with self.voiceover(
            "In symbols, which is what Working wrote in words. <bookmark mark='a'/> Demand and supply are two "
            "equations with shocks, u and v. <bookmark mark='b'/> The least-squares slope settles, in a long "
            "season, on a weighted mixture of the two curves' slopes, weighted by how much each curve moves. "
            "<bookmark mark='c'/> With the Island's planted numbers it comes to about plus fifteen; this "
            f"season's dots gave plus {s['ols_slope']:.0f}. <bookmark mark='d'/> If only demand moved, the cloud "
            "would trace supply; if only supply moved, it would trace demand. Since both move, it traces nothing. "
            "This is the identification problem, and it is not a problem of too little data. A million more days "
            "would give a more precise wrong answer."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in notes], lag_ratio=0.4))
        self.clear_scene()
