from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Triangle(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The cost of a tax grows with its square", r"What does a tax cost beyond the revenue?",
             "Chapter two. The cost of a tax grows with its square.", lit={1844: r"Dupuit", 1964: r"Harberger"},
             scale=("market",), horizon=("a year",))
        self.diagram()
        self.square()
        self.last_dollar()

    def diagram(self):
        Tr = load("triangle")
        r = Tr["at"]["0.2"]
        ed, es = Tr["eps_d"], Tr["eps_s"]
        q = np.linspace(0.6, 1.4, 120)
        ax = plane([0.6, 1.4], [0.6, 1.5], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.8,
                   xticks=[0.6, 0.8, 1.0, 1.2, 1.4], yticks=[0.8, 1.0, 1.2, 1.4], xlabel=r"quantity \ (untaxed = 1)",
                   ylabel=r"price \ (untaxed = 1)", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        dem = path(ax, q, q ** (-1 / ed), DEMAND, 3.2, yr=(0.6, 1.5))
        sup = path(ax, q, q ** (1 / es), SUPPLY, 3.2, yr=(0.6, 1.5))
        qq, pb, ps = r["q"], r["p_buy"], r["p_sell"]
        rev = Polygon(ax.ax.c2p(0.6, ps), ax.ax.c2p(qq, ps), ax.ax.c2p(qq, pb), ax.ax.c2p(0.6, pb), stroke_width=0,
                      fill_color=REVENUE, fill_opacity=0.35)
        qs = np.linspace(qq, 1.0, 30)
        tri = Polygon(*[ax.ax.c2p(x, x ** (-1 / ed)) for x in qs], *[ax.ax.c2p(x, x ** (1 / es)) for x in qs[::-1]],
                      stroke_width=0, fill_color=LOSS, fill_opacity=0.6)
        side = VGroup(
            label(rf"a tax of {100 * r['t']:.0f}\% of the price", font_size=19, color=WHITE),
            label(rf"buyers pay {100 * (pb - 1):.0f}\% more, \\ sellers keep {100 * (1 - ps):.0f}\% less", font_size=18,
                  color=GREY_A),
            label(rf"gold: \ revenue, \ {r['revenue']:.3f}", font_size=19, color=REVENUE),
            label(rf"red: \ deadweight loss, \ {r['dwl']:.4f}: \\ trades that no longer \\ happen", font_size=18,
                  color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "What does a tax cost beyond the money it raises? Take the Island's market for fuel, with demand "
            f"elasticity {ed:g} and supply elasticity {es:g}. <bookmark mark='a'/> Put on a tax of twenty percent of "
            "the price. <bookmark mark='b'/> Buyers pay more, sellers receive less, and the wedge between them is "
            f"the tax: here buyers bear about {say_pct((pb - 1) / 0.2, 0)} of it, because they are the less elastic "
            "side. <bookmark mark='c'/> The gold rectangle is the revenue, money that moves from buyers and sellers "
            "to the government, a transfer and not a loss. <bookmark mark='d'/> The red triangle is the loss: the "
            "trades that were worth making at the untaxed price and no longer happen. Jules Dupuit described it in "
            "1844; Arnold Harberger made it a tool, and it carries his name."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(dem), Create(sup), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(rev), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(tri), FadeIn(side[3]))
        self.clear_scene()

    def square(self):
        Tr = load("triangle")
        t = np.array(Tr["t"])
        ax = plane([0, 0.6], [0, 0.06], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.02, 0.04, 0.06],
                   xlabel=r"tax, \ share of the price", ylabel=r"deadweight loss \ (untaxed spending = 1)",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.2f}", font_size=14)
        ln = path(ax, t, Tr["dwl"], LOSS, 3.4)
        ap = path(ax, t, Tr["approx"], WHITE, 2.0)
        at = Tr["at"]
        pts = VGroup(*[dot(ax, float(k), v["dwl"], LOSS, 0.08) for k, v in at.items()])
        eq = MathTex(r"\mathrm{DWL} \approx \tfrac{1}{2}\, t^{2}\, \frac{\varepsilon_d\, \varepsilon_s}"
                     r"{\varepsilon_d + \varepsilon_s}\, p\, q", font_size=32).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"red: \ the exact loss; \\ white: \ Harberger's formula", font_size=17, color=GREY_A),
            *[label(rf"{100 * float(k):.0f}\%: \ loss {100 * v['dwl'] / v['revenue']:.1f}\% \\ of the revenue",
                    font_size=18, color=LOSS) for k, v in at.items()],
            label(r"twice the rate, \\ four times the loss", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        r1, r2, r4 = at["0.1"], at["0.2"], at["0.4"]
        with self.voiceover(
            "The triangle's area grows with the square of the tax, because both its height and its width grow with "
            "the rate. <bookmark mark='a'/> Harberger's approximation: half the tax squared, times an elasticity, "
            "times spending. <bookmark mark='b'/> At ten percent the loss is "
            f"{say_pct(r1['dwl'] / r1['revenue'], 1)} of the revenue; <bookmark mark='c'/> at twenty, "
            f"{say_pct(r2['dwl'] / r2['revenue'], 1)}; <bookmark mark='d'/> at forty, "
            f"{say_pct(r4['dwl'] / r4['revenue'], 1)}. <bookmark mark='e'/> Twice the rate, four times the loss. So "
            "it is cheaper to raise money with many small taxes on broad bases than with a few large ones on narrow "
            "bases, and the last dollar raised by a high tax costs far more than the first."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), Create(ln), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(ap))
            for mk, k in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(pts[k], scale=1.4), FadeIn(side[1 + k]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def last_dollar(self):
        Mc = load("mcpf")
        lo, hi = Mc["0.25"], Mc["1.0"]
        ax = plane([0, 0.8], [1, 5], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[1, 2, 3, 4, 5], xlabel=r"tax rate",
                   ylabel=r"cost to taxpayers of the last dollar raised", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"\\${v:.0f}", font_size=14)
        one = seg(ax, 0, 1, 0.8, 1, GREY_B, 1.6, dashed=True)
        c_lo = path(ax, lo["t"], lo["m"], TOP, 3.4, yr=(1, 5))
        c_hi = path(ax, hi["t"], hi["m"], LOSS, 3.4, yr=(1, 5))
        top_lo = vline(ax, lo["top"], 1, 5, TOP)
        top_hi = vline(ax, hi["top"], 1, 5, LOSS)
        pts_lo = VGroup(*[dot(ax, float(x), v, TOP, 0.08) for x, v in lo["at"].items()])
        pts_hi = VGroup(*[dot(ax, float(x), v, LOSS, 0.08) for x, v in hi["at"].items()])
        eq = MathTex(r"\text{MCPF} \;=\; \frac{1 - t}{1 - t - t\,e}", font_size=34).to_edge(UP, buff=0.35)
        a_lo, a_hi = lo["at"], hi["at"]
        side = VGroup(
            label(r"raise the rate a little: \\ taxpayers lose the tax \\ on all their income; \\ the government gets "
                  r"less, \\ because income shrinks", font_size=17, color=GREY_A),
            label(rf"$e$ = 0.25: \\ \${a_lo['0.2']:.2f} at 20\%, \ \${a_lo['0.4']:.2f} at 40\%, \\ "
                  rf"\${a_lo['0.6']:.2f} at 60\%", font_size=18, color=TOP),
            label(rf"$e$ = 1: \\ \${a_hi['0.2']:.2f} at 20\%, \ \${a_hi['0.4']:.2f} at 40\%", font_size=18,
                  color=LOSS),
            label(r"at the top of the \\ Laffer curve: \\ infinite", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How much does that last dollar cost? Go back to the napkin's economy, where taxed income shrinks with "
            "an elasticity e. Raise the rate a little. Taxpayers lose the extra tax on all of their income, but the "
            "government gets less than that, because income shrinks in response. The ratio of the two is the "
            "marginal cost of public funds: one minus t over one minus t minus t times e. <bookmark mark='a'/> With "
            f"an elasticity of a quarter, the last dollar raised at a rate of twenty percent costs taxpayers "
            f"{say_num(a_lo['0.2'], 2)} dollars; at forty percent, {say_num(a_lo['0.4'], 2)}; at sixty, "
            f"{say_num(a_lo['0.6'], 2)}. <bookmark mark='b'/> With an elasticity of one, "
            f"{say_num(a_hi['0.2'], 2)} at twenty percent and {say_num(a_hi['0.4'], 1)} at forty. "
            "<bookmark mark='c'/> At the top of the Laffer curve the cost is infinite: the government raises "
            "nothing more, and taxpayers still pay. <bookmark mark='d'/> So a public project paid for with taxes "
            "must return more than a dollar for each dollar it spends, and how much more depends on how high the "
            "rates already are and how strongly the base responds."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), Create(one), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(c_lo), FadeIn(pts_lo), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c_hi), FadeIn(pts_hi), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(top_lo), Create(top_hi), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Indicate(eq, color=E.ACCENT))
        self.clear_scene()
