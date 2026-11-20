from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Incidence(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Who pays the corporate tax?", r"Does a tax fall on whoever hands over the money?",
             "Chapter one. Who pays the corporate tax?", lit={1962: r"Harberger", 2018: r"Fuest, \ Peichl and "
                                                                                      r"Siegloch"},
             scale=("firm", "nation", "world"), horizon=("a decade",))
        self.statutory()
        self.mobility()
        self.evidence()

    def statutory(self):
        steps = flow_chain([(r"the firm \\ pays the tax", CAPITAL), (r"capital \\ earns less", CAPITAL),
                            (r"capital leaves, \\ or is not built", RATE),
                            (r"workers have \\ less to work with", WORKER)],
                           notes=[r"the statutory \\ incidence", r"if capital \\ cannot move", r"if it can: \\ abroad, "
                                  r"\\ or not saved", r"the wage \\ falls"], box_w=2.7, font_size=19,
                           note_size=15).move_to(UP * 0.8)
        head = label(r"the corporate tax: \ who pays it, \ and who bears it?", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"Part 2: \ a tax on a market falls on whichever side can least escape it", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Part two showed that a tax on a market falls on whichever side can least escape it, not on whoever "
            "hands the money to the government. The corporate tax is the hardest case. <bookmark mark='a'/> The firm "
            "pays it. <bookmark mark='b'/> If capital cannot go anywhere, its owners simply earn less, and that is "
            "the end of it. <bookmark mark='c'/> But capital can move abroad, or simply not be built, if the return "
            "after tax falls. <bookmark mark='d'/> Then workers have less machinery to work with, their productivity "
            "falls, and so does the wage. Who pays depends on how mobile capital is. In 1962 Arnold Harberger worked "
            "this out for a closed economy, with a fixed stock of capital, and found that capital bears about all of "
            "it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("a")
            self.play(Indicate(steps.boxes[0], color=CAPITAL))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(steps.arrows[2]), FadeIn(steps.boxes[3]), FadeIn(steps.notes[3]))
        self.clear_scene()

    def mobility(self):
        H = load("harberger")
        eta = np.array(H["eta"])
        x = np.where(eta > 0, np.log10(np.maximum(eta, 1e-9)), -1.6)
        sh = np.array(H["share"])
        ax = plane([-1.6, 2.4], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[-1, 0, 1, 2], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"how readily capital supply responds to its return \ (elasticity, \ log scale)",
                   ylabel=r"workers' share of the burden", xfmt=lambda v: f"{10 ** v:g}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, x[eta > 0], sh[eta > 0], WORKER, 3.4)
        c0 = dot(ax, -1.6, 0.0, CAPITAL, 0.09)
        marks = VGroup(*[dot(ax, np.log10(float(k)), v["worker_share"], WORKER, 0.07)
                         for k, v in H["marks"].items() if float(k) > 0])
        O = H["open"]
        side = VGroup(
            label(rf"the Island: \ a {100 * H['tau']:.0f}\% tax on \\ the return to capital; \\ capital's share of "
                  rf"output {100 * H['alpha']:.0f}\%", font_size=17, color=GREY_A),
            label(r"closed, \ capital fixed: \\ workers bear nothing", font_size=18, color=CAPITAL),
            label(rf"open, \ capital mobile: \\ workers lose {100 * O['worker_per_revenue']:.0f}\% \\ of the revenue "
                  r"raised", font_size=18, color=WORKER),
            label(rf"the excess, \ {100 * O['dwl'] / O['revenue']:.0f}\% of revenue: \\ the deadweight loss",
                  font_size=17, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island, put a tax of twenty percent on the return to capital, and let capital respond to what it "
            f"earns after tax. <bookmark mark='a'/> If the stock is fixed, the closed economy Harberger studied, "
            "workers bear none of it: the wage does not move, and owners lose exactly what the government collects. "
            "<bookmark mark='b'/> As capital becomes more mobile, it leaves until its return after tax is restored, "
            "and the burden shifts to workers. <bookmark mark='c'/> In a small open economy, where capital earns the "
            "world's return or goes elsewhere, workers bear all of it, and more: their wages fall by "
            f"{100 * O['worker_per_revenue']:.0f} percent of the revenue raised. <bookmark mark='d'/> The extra "
            f"{100 * O['dwl'] / O['revenue']:.0f} percent is the deadweight loss, output that is never produced "
            "because the capital went away."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(c0, scale=1.5), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_, scale=1.4) for m_ in marks], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def evidence(self):
        F = load("harberger")["fps"]
        cards = point_cards([
            (r"the design", rf"about {F['changes']:,} changes \\ in German towns' \\ business tax, \\ over twenty "
                            r"years", WHITE),
            (r"the finding", rf"workers bear \\ about {F['fps_workers']}\% \\ of the burden", WORKER),
            (r"it varies", r"with labour market \\ institutions, \\ and with how easily \\ firms shift profits", RATE),
            (r"what it means", r"a corporate tax \\ is partly a tax \\ on wages", E.ACCENT),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what the data say: \ Fuest, \ Peichl and Siegloch (2018)", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.HARBERGER_1962.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Where between the extremes are real economies? <bookmark mark='a'/> German towns set their own rate "
            "of a local business tax, and changed it thousands of times over twenty years, which lets Clemens "
            "Fuest, Andreas Peichl and Sebastian Siegloch compare wages in firms whose town raised the tax with "
            "firms whose town did not. <bookmark mark='b'/> Workers bore about half of the burden. "
            "<bookmark mark='c'/> How much depended on labour market institutions and on how easily firms could "
            "move profits elsewhere. <bookmark mark='d'/> A tax that looks like a tax on capital is, to an important "
            "degree, a tax on wages."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
