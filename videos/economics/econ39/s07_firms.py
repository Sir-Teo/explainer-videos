from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Firms(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Firms: \ the same worker, \ a different wage", r"How much of your pay is your employer?",
             "Chapter six. Firms: the same worker, a different wage.",
             lit={1999: r"Abowd, \ Kramarz and Margolis", 2013: r"Card, \ Heining and Kline"},
             scale=("person", "firm"), horizon=("a decade",))
        self.mover()
        self.decompose()
        self.bias()

    def mover(self):
        F = load("firms")
        Wk = F["worker"]
        yrs = np.arange(1, len(Wk["y"]) + 1)
        lo, hi = min(Wk["y"]) - 0.25, max(Wk["y"]) + 0.25
        ax = plane([0.5, len(yrs) + 0.5], [lo, hi], center=LEFT * 2.6 + DOWN * 0.6, x_length=6.6, y_length=4.2,
                   xticks=list(yrs), yticks=[round(lo + 0.1, 1), round((lo + hi) / 2, 1), round(hi - 0.1, 1)],
                   xlabel=r"year", ylabel=r"log wage", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}",
                   font_size=14)
        dots = VGroup(*[dot(ax, x, y, FIRM if Wk["firm"][k] == Wk["firm"][0] else SORT, 0.09)
                        for k, (x, y) in enumerate(zip(yrs, Wk["y"]))])
        lvls = VGroup()
        for k in range(len(yrs)):
            lvl = Wk["alpha"] + Wk["psi"][k]
            lvls.add(seg(ax, yrs[k] - 0.4, lvl, yrs[k] + 0.4, lvl, FIRM if Wk["firm"][k] == Wk["firm"][0] else SORT,
                         3))
        eq = MathTex(r"\ln w_{it} = \alpha_i + \psi_{J(i,t)} + \varepsilon_{it}", font_size=40).to_edge(UP, buff=0.5)
        side = VGroup(
            label(r"$\alpha_i$: \ the worker, \ wherever \\ they work", font_size=19, color=WORKER),
            label(r"$\psi_j$: \ the firm's premium, \\ for whoever works there", font_size=19, color=FIRM),
            label(rf"this islander's firms: \\ premiums {Wk['psi'][0]:+.2f} and {Wk['psi'][-1]:+.2f}", font_size=18,
                  color=WHITE),
            label(r"movers identify the firms", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Some employers pay more than others for the same work. To measure it, John Abowd, Francis Kramarz and "
            "David Margolis wrote each wage as the sum of two parts. <bookmark mark='a'/> A worker effect, alpha, "
            "which travels with the person, <bookmark mark='b'/> and a firm effect, psi, a premium the firm pays "
            "whoever works there. <bookmark mark='c'/> Here is one islander's log wage over six years. "
            "<bookmark mark='d'/> They change firms, and their wage jumps by the difference between the two firms' "
            f"premiums, from {Wk['psi'][0]:+.2f} to {Wk['psi'][-1]:+.2f}. <bookmark mark='e'/> Workers who move are "
            "what separate firm effects from worker effects: the same person, in two places. With millions of "
            "workers in administrative records, the model can be fitted to an entire country."
        ) as vo:
            k1 = next(k for k in range(len(yrs)) if Wk["firm"][k] != Wk["firm"][0])
            self.play(Write(eq), FadeIn(tag), FadeIn(ax), run_time=1.5)
            self.play(FadeIn(dots[:k1]), FadeIn(lvls[:k1]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(eq, color=WORKER, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(dots[:k1], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(dots[k1:]), FadeIn(lvls[k1:]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def decompose(self):
        F = load("firms")
        T, E_ = F["truth"], F["est"]
        vy = T["var_y"]
        comps = [("worker effects", T["var_alpha"] / vy, E_["share_alpha"], WORKER),
                 ("firm effects", T["var_psi"] / vy, E_["share_psi"], FIRM),
                 ("sorting: \\ 2 cov", T["cov2"] / vy, E_["share_cov"], SORT)]
        C = F["chk"]
        rows = VGroup()
        for k, (nm, tv, ev, col) in enumerate(comps):
            y = 1.6 - 1.25 * k
            bt = Rectangle(width=tv * 7, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.45).move_to(
                np.array([-2.6 + tv * 3.5, y + 0.22, 0]))
            be = Rectangle(width=ev * 7, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to(
                np.array([-2.6 + ev * 3.5, y - 0.22, 0]))
            rows.add(VGroup(label(nm, font_size=19, color=col).next_to(np.array([-2.7, y, 0]), LEFT, buff=0.1),
                            bt, label(f"{100 * tv:.0f}\\%", font_size=16, color=GREY_A).next_to(bt, RIGHT, buff=0.1),
                            be, label(f"{100 * ev:.0f}\\%", font_size=16, color=WHITE).next_to(be, RIGHT, buff=0.1)))
        keys = VGroup(label(r"pale: \ the Island's truth", font_size=17, color=GREY_A),
                      label(r"solid: \ AKM's estimate", font_size=17, color=WHITE)).arrange(RIGHT, buff=0.6).to_edge(
            UP, buff=0.5)
        chk = VGroup(
            label(r"West Germany \ (Card, \ Heining and Kline)", font_size=19, color=E.ACCENT),
            label(rf"firm effects: \ {C['psi1']}\% $\to$ {C['psi4']}\% of the variance", font_size=17, color=FIRM),
            label(rf"sorting: \ {C['cov1']}\% $\to$ {C['cov4']}\%", font_size=17, color=SORT),
            label(r"1985--91 to 2002--09", font_size=15, color=GREY_A),
            label(rf"of the rise in inequality: \\ workers {C['rise_alpha']}\%, \ firms {C['rise_psi']}\%, \\ "
                  rf"sorting {C['rise_cov']}\%", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.3)
        tag = published_tag(tables.CHK_2013.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "With the model fitted, the variance of log wages splits into parts. <bookmark mark='a'/> On the Island, "
            f"where the truth is planted, worker effects account for {100 * T['var_alpha'] / vy:.0f} percent of it, "
            f"<bookmark mark='b'/> firm effects for {100 * T['var_psi'] / vy:.0f} percent, <bookmark mark='c'/> and "
            f"sorting, the tendency of good workers to work at high-paying firms, for {100 * T['cov2'] / vy:.0f}. "
            "The estimates, from six years of a twenty-thousand-worker panel, land close. <bookmark mark='d'/> David "
            "Card, Jörg Heining and Patrick Kline fitted the model to West Germany's social security records. "
            f"Between the late 1980s and the 2000s the firm effects' share rose from {C['psi1']} to {C['psi4']} "
            f"percent, and sorting's from {C['cov1']} to {C['cov4']} percent. Of the whole rise in German wage "
            f"inequality, about a quarter came from wider gaps between firms and a third from better workers "
            "concentrating in better-paying firms."
        ) as vo:
            self.play(FadeIn(keys), FadeIn(tag))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c) for c in chk], lag_ratio=0.4), run_time=2.5)
        self.clear_scene()

    def bias(self):
        F = load("firms")
        sw = F["sweep"]
        mv = np.array([100 * s["move"] for s in sw])
        vpsi, tpsi = np.array([s["var_psi"] for s in sw]), np.array([s["true_var_psi"] for s in sw])
        cr, tcr = np.array([s["corr"] for s in sw]), np.array([s["true_corr"] for s in sw])
        lx = np.log10(mv)
        lt = [float(np.log10(v)) for v in (0.5, 1, 2, 5, 10, 20)]
        ax1 = plane([-0.45, 1.45], [0, 0.06], center=LEFT * 3.4 + DOWN * 0.4, x_length=5.6, y_length=4.0,
                    xticks=lt, yticks=[0, 0.02, 0.04, 0.06],
                    xlabel=r"share who move each year, \ \%", ylabel=r"variance of firm effects",
                    xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{v:.2f}", font_size=13)
        ax2 = plane([-0.45, 1.45], [-0.2, 0.4], center=RIGHT * 3.0 + DOWN * 0.4, x_length=5.6, y_length=4.0,
                    xticks=lt, yticks=[-0.2, 0, 0.2, 0.4],
                    xlabel=r"share who move each year, \ \%", ylabel=r"correlation of worker and firm",
                    xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{v:+.1f}", font_size=13)
        lx = np.log10(mv)
        e1, t1 = path(ax1, lx, vpsi, FIRM, 3.2, smooth=False), path(ax1, lx, tpsi, GREY_B, 2.2, smooth=False)
        e2, t2 = path(ax2, lx, cr, SORT, 3.2, smooth=False), path(ax2, lx, tcr, GREY_B, 2.2, smooth=False)
        d1 = VGroup(*[dot(ax1, x, y, FIRM, 0.06) for x, y in zip(lx, vpsi)])
        d2 = VGroup(*[dot(ax2, x, y, SORT, 0.06) for x, y in zip(lx, cr)])
        keys = label(r"grey: \ the truth; \ colour: \ AKM's estimate", font_size=18, color=GREY_A).to_edge(UP,
                                                                                                   buff=0.45)
        foot = label(r"too few movers: \ firm effects look more spread out, \ sorting looks negative",
                     font_size=19, color=E.ACCENT).to_edge(DOWN, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "But the method has a trap, and the Island can show it. Rerun the economy with fewer and fewer workers "
            "changing firms each year. <bookmark mark='a'/> With few movers, each firm's premium is estimated from a "
            "handful of people, and their noise looks like real differences between firms: the estimated variance "
            "of firm effects doubles when only half a percent move. <bookmark mark='b'/> Worse, the same noise "
            "enters a worker's effect with the opposite sign, so the correlation between good workers and good "
            "firms is pushed down, and can even turn negative, though the true correlation never changes. "
            "<bookmark mark='c'/> This limited-mobility bias made early studies find little sorting. Recent "
            "corrections, such as Kline, Saggio and Sølvsten's leave-out estimator, generally shrink the firm "
            "effects and raise the sorting."
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(ax2), FadeIn(keys), FadeIn(tag), Create(t1), Create(t2))
            vo.wait_until("a")
            self.play(Create(e1), FadeIn(d1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(e2), FadeIn(d2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
