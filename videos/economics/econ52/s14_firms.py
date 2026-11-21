from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Firms(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Many firms: \ entry, \ exit and lumps", r"What if the agents are firms?",
             "Chapter twelve. Many firms: entry, exit and lumps.", lit={1992: r"Hopenhayn", 2008: r"Khan and Thomas"},
             scale=("firm", "market"), horizon=("a decade",))
        self.industry()
        self.cohorts()
        self.barrier()
        self.lumps()

    def industry(self):
        F = load("firms")
        r = F["rows"][0]
        phi = np.array(r["phi"])
        mu = np.array(r["mu"])
        stay = np.array(r["stay"]) > 0.5
        ax = plane([0, 3.0], [0, 0.25], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 1, 2, 3], yticks=[0, 0.05, 0.1, 0.15, 0.2, 0.25], xlabel=r"productivity",
                   ylabel=r"share of firms", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        share = mu / mu.sum()
        bars = VGroup()
        for k in range(len(phi)):
            if phi[k] > 3.0:
                break
            w = 0.6 * (phi[min(k + 1, len(phi) - 1)] - phi[max(k - 1, 0)]) / 2
            p0, p1 = ax.ax.c2p(phi[k] - w / 2, 0), ax.ax.c2p(phi[k] + w / 2, min(share[k], 0.25))
            bars.add(Rectangle(width=max(p1[0] - p0[0], 0.02), height=max(p1[1] - p0[1], 0.005), stroke_width=0,
                               fill_color=FIRM if stay[k] else ERR, fill_opacity=0.85).move_to((p0 + p1) / 2))
        thr = vline(ax, r["threshold"], 0, 0.24, ERR, 2.4)
        tl = label(r"exit below here", font_size=16, color=ERR).next_to(ax.ax.c2p(r["threshold"], 0.24), RIGHT,
                                                                         buff=0.1)
        steps = VGroup(
            label(r"pay to enter, \ then learn \\ your productivity", font_size=18, color=WHITE),
            label(r"each year: \ hire, \ produce, \\ pay a fixed cost", font_size=18, color=WHITE),
            label(r"productivity wanders; \\ exit if the future \\ is not worth the cost", font_size=18, color=ERR),
            label(r"free entry sets the price: \\ entering is worth exactly \\ its cost", font_size=18,
                  color=E.ACCENT),
            label(rf"each year {100 * r['entry_rate']:.1f}\% enter \\ and {100 * r['exit_rate']:.1f}\% leave",
                  font_size=19, color=FIRM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Hopenhayn, \ Econometrica 60(5) (1992)", corner=DR, font_size=12)
        with self.voiceover(
            "Households are not the only agents who differ. In 1992 Hugo Hopenhayn built a competitive industry "
            "out of a population of firms. <bookmark mark='a'/> A firm pays a cost to enter, and only then learns "
            "how productive it is. <bookmark mark='b'/> Each year it hires, produces and pays a fixed cost of "
            "operating. <bookmark mark='c'/> Its productivity wanders; when the future is no longer worth the "
            "fixed costs, it leaves. <bookmark mark='d'/> Entry continues until entering is worth exactly what it "
            "costs, and that pins down the price. <bookmark mark='e'/> In a steady state the industry is constant, "
            f"but its members are not: each year {100 * r['entry_rate']:.1f} percent of firms are new, and the "
            "same share leave. The bars show where the firms are; pink ones stay, red ones are about to go."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            for mk, s_ in zip("abcd", steps[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.1))
                if mk == "c":
                    self.play(Create(thr), FadeIn(tl))
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), FadeIn(steps[4]),
                      run_time=2.0)
        self.clear_scene()

    def cohorts(self):
        F = load("firms")
        r = F["rows"][0]
        surv = np.array(r["survival"])
        size = np.array(r["size_by_age"])
        ages = np.arange(len(surv))
        ax1 = plane([0, 20], [0, 1], center=LEFT * 3.4 + DOWN * 0.4, x_length=5.4, y_length=4.2,
                    xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"age, \ years",
                    ylabel=r"share of a cohort still alive", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                    font_size=13)
        top = float(np.ceil(size.max() / 10) * 10)
        ax2 = plane([0, 20], [0, top], center=RIGHT * 3.4 + DOWN * 0.4, x_length=5.4, y_length=4.2,
                    xticks=[0, 5, 10, 15, 20], yticks=[0, top / 2, top], xlabel=r"age, \ years",
                    ylabel=r"workers per surviving firm", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                    font_size=13)
        c1 = path(ax1, ages, surv, FIRM, 3.0, smooth=False)
        c2 = path(ax2, ages, size, MANY, 3.0, smooth=False)
        h = label(r"up or out: \ young firms either grow or die", font_size=24, color=E.ACCENT).to_edge(UP, buff=0.5)
        n1 = label(rf"after 5 years: \ {100 * surv[5]:.0f}\%", font_size=18, color=FIRM).next_to(
            ax1.ax.c2p(5, surv[5]), UR, buff=0.12)
        n2 = label(rf"from {size[0]:.0f} to {size[10]:.0f} workers \\ by age 10", font_size=18, color=MANY).next_to(
            ax2.ax.c2p(10, size[10]), DR, buff=0.15)
        with self.voiceover(
            "Follow one cohort of entrants. <bookmark mark='a'/> Many fail early: after five years "
            f"{100 * surv[5]:.0f} percent are still alive, and the failures come mostly in the first few years. "
            "<bookmark mark='b'/> The survivors grow: from about "
            f"{size[0]:.0f} workers at entry to {size[10]:.0f} by age ten, partly because they get more productive, "
            "and partly because the unproductive have left. <bookmark mark='c'/> Up or out: the pattern John "
            "Haltiwanger and his coauthors found in American firm data, where young firms are both the most likely "
            "to die and the fastest to grow."
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(ax2))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(n1), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(n2), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(h))
        self.clear_scene()

    def barrier(self):
        F = load("firms")
        lo, hi = F["rows"]
        items = [
            (r"price of the good", lo["p"], hi["p"], "{:.2f}"),
            (r"firms entering each year", 100 * lo["entry_rate"], 100 * hi["entry_rate"], r"{:.1f}\%"),
            (r"exit threshold \ (productivity)", lo["threshold"], hi["threshold"], "{:.2f}"),
            (r"average productivity", lo["productivity"], hi["productivity"], "{:.2f}"),
        ]
        head = VGroup(label(r"", font_size=20), label(rf"entry cost {lo['c_e']:.0f}", font_size=20, color=FIRM),
                      label(rf"entry cost {hi['c_e']:.0f}", font_size=20, color=ERR))
        grid = VGroup(*head)
        for nm, a, b, fmt in items:
            grid.add(label(nm, font_size=21, color=WHITE), label(fmt.format(a), font_size=22, color=FIRM),
                     label(fmt.format(b), font_size=22, color=ERR))
        grid.arrange_in_grid(rows=len(items) + 1, cols=3, buff=(0.8, 0.35), col_alignments="lcc").move_to(UP * 0.4)
        foot = label(r"a barrier to entry protects the unproductive: \ less churn, \ lower productivity, \ higher "
                     r"prices", font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Now double the cost of entering, as a licence, a permit or a bank that will not lend might. <bookmark "
            f"mark='a'/> The price of the good rises, from {lo['p']:.2f} to {hi['p']:.2f}. <bookmark mark='b'/> "
            f"Entry falls from {100 * lo['entry_rate']:.1f} to {100 * hi['entry_rate']:.1f} percent of firms a "
            "year. <bookmark mark='c'/> With fewer challengers, weaker incumbents can afford to stay: the "
            f"productivity below which firms exit falls from {lo['threshold']:.2f} to {hi['threshold']:.2f}, "
            f"<bookmark mark='d'/> and the average firm is {100 * (1 - hi['productivity'] / lo['productivity']):.0f} "
            "percent less productive. <bookmark mark='e'/> A barrier to entry protects the unproductive. A "
            "representative firm, which neither enters nor exits, could not show any of this."
        ) as vo:
            self.play(FadeIn(VGroup(*grid[:3])))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*grid[3 * (k + 1):3 * (k + 2)]), shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def lumps(self):
        F = load("firms")
        pl = np.array(F["plants"])
        agg = np.array(F["aggregate"])
        T = len(agg)
        ax1 = plane([0, T], [0, 1.2], center=UP * 1.5 + LEFT * 1.6, x_length=8.0, y_length=2.2,
                    xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 0.6, 1.2], ylabel=r"investment rate, \ 3 plants",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=12)
        ax2 = plane([0, T], [0, 0.2], center=DOWN * 1.7 + LEFT * 1.6, x_length=8.0, y_length=2.2,
                    xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 0.1, 0.2], xlabel=r"years",
                    ylabel=r"investment rate, \ 20{,}000 plants", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.1f}", font_size=12)
        cols = (FIRM, MANY, DIST)
        spikes = VGroup()
        for k, c in enumerate(cols):
            for t in range(T):
                v = float(np.clip(pl[t, k], 0, 1.2))
                if v > 0:
                    spikes.add(Line(ax1.ax.c2p(t + 0.25 * k, 0), ax1.ax.c2p(t + 0.25 * k, v), color=c,
                                    stroke_width=2.2))
        smooth = path(ax2, np.arange(T), np.clip(agg, 0, 0.2), WHITE, 2.8, smooth=False)
        shock = vline(ax2, F["shock_at"], 0, 0.2, E.ACCENT, 2.0)
        side = VGroup(
            label(rf"a plant invests only when \\ it is far from its target: \\ {100 * F['zero_share']:.0f}\% of "
                  r"plant-years, \\ nothing", font_size=18, color=FIRM),
            label(r"the sum is smooth", font_size=19, color=WHITE),
            label(r"a common shock: \ more plants \\ cross their thresholds \\ at once", font_size=18,
                  color=E.ACCENT),
            label(r"in general equilibrium, \\ prices smooth it further \\ (Khan and Thomas)", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"a sketch of (S,s) plants, \ not Khan and Thomas's model", corner=DL, font_size=12)
        with self.voiceover(
            "One more population. Plants do not invest a little every year; they invest in lumps, because "
            "adjusting has fixed costs. <bookmark mark='a'/> Here are three plants: years of nothing, then a "
            f"burst. In this sketch, {100 * F['zero_share']:.0f} percent of plant-years have no investment at all. "
            "<bookmark mark='b'/> Add up twenty thousand of them and the lumps vanish: aggregate investment is "
            "smooth. <bookmark mark='c'/> But not inert. When a common shock raises every plant's target, many "
            "plants cross their thresholds at once, and investment jumps. Whether such lumps matter for the "
            "business cycle was the question of Aubhik Khan and Julia Thomas. <bookmark mark='d'/> Their answer, "
            "in a general equilibrium where interest rates and wages respond, was that they matter much less than "
            "the plants suggest: prices smooth the aggregate further. Heterogeneity is not always decisive; it has "
            "to be checked."
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s_) for s_ in spikes], lag_ratio=0.01), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(ax2), Create(smooth), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(shock), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
