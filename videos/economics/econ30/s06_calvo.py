from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Calvo(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Calvo's fairy: \ the New Keynesian Phillips curve", r"What does inflation depend on when "
             r"prices are set for months at a time?", "Chapter five. Calvo's fairy: the New Keynesian Phillips curve.",
             lit={1983: r"Calvo", 1999: r"Gal\'i and Gertler"}, scale=("firm", "nation"), horizon=("a quarter",))
        self.fairy()
        self.reset()
        self.nkpc()
        self.slope()

    def fairy(self):
        C = load("calvo")
        b = C["base"]
        rng = np.random.default_rng(30)
        n = 60
        grid = VGroup(*[Square(side_length=0.3, stroke_width=0, fill_color=GREY_D, fill_opacity=1)
                        for _ in range(n)]).arrange_in_grid(rows=6, cols=10, buff=0.14).move_to(LEFT * 3.4 + DOWN * 0.3)
        side = VGroup(
            label(r"Guillermo Calvo, \ 1983", font_size=22, color=E.ACCENT),
            label(r"each quarter a fairy visits a random third of the firms; \\ only they may reset their price",
                  font_size=19, color=PRICE),
            label(rf"a price lasts {b['mean_months']:.0f} months on average \\ (the median: \ about "
                  rf"{b['median_months']:.0f})", font_size=19, color=STICKY),
            label(r"absurd as a story; \\ wonderfully tractable as mathematics", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Calvo, \ \emph{Journal of Monetary Economics} 12(3) (1983)", corner=DR, font_size=12)
        with self.voiceover(
            "How should sticky prices enter a model of the whole economy? Guillermo Calvo's answer, in 1983, is "
            "a fairy. <bookmark mark='a'/> Each quarter, a randomly chosen fraction of firms, one minus theta, may "
            "reset their price; the rest must keep the price they have. With theta at two thirds, a third of firms "
            "reset each quarter, whatever has happened to them and however long they have waited. "
            f"<bookmark mark='b'/> A price then lasts {b['mean_months']:.0f} months on average. "
            "<bookmark mark='c'/> As a description of a firm, it is absurd: no firm waits for a fairy. As "
            "mathematics it is wonderful, because the firms that reset are a random sample, so one equation "
            "describes them all."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            for _ in range(3):
                pick = rng.random(n) < 1 / 3
                self.play(*[sq.animate.set_fill(PRICE if p else GREY_D) for sq, p in zip(grid, pick)],
                          run_time=0.6)
                self.wait(0.6)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def reset(self):
        rows = VGroup(
            label(r"a firm that may reset knows its price could last a long time", font_size=23, color=PRICE),
            MathTex(r"p^*_t = (1 - \beta\theta) \sum_{k=0}^{\infty} (\beta\theta)^k\, \mathbb{E}_t\big[\, \mu + "
                    r"mc_{t+k} + p_{t+k} \big]", font_size=36),
            label(r"a weighted average of the costs it expects, \ weighted by the chance the price is still in force",
                  font_size=22, color=GREY_A),
            MathTex(r"p_t = \theta\, p_{t-1} + (1 - \theta)\, p^*_t", font_size=36),
            label(r"the price level: \ a third reset, \ two thirds keep last quarter's", font_size=22,
                  color=STICKY),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Gal\'i, \ \emph{Monetary Policy, Inflation, and the Business Cycle} (2nd ed., 2015), "
                            r"\ ch.\ 3", corner=DR, font_size=12)
        with self.voiceover(
            "Now take a firm the fairy has visited. <bookmark mark='a'/> It knows its new price may last a long "
            "time, so it looks ahead. <bookmark mark='b'/> In logs, its best price is its markup plus a weighted "
            "average of the nominal marginal costs it expects in every future quarter, <bookmark mark='c'/> each "
            "weighted by the chance that the price will still be in force then, theta to the power k, and by "
            "discounting. <bookmark mark='d'/> And the price level is an average of the new prices and the old "
            "ones: <bookmark mark='e'/> a third reset, two thirds carried over from last quarter."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                if isinstance(r_, MathTex):
                    self.play(Write(r_), run_time=1.3)
                else:
                    self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def nkpc(self):
        rows = VGroup(
            label(r"combine the two, \ and write marginal cost through the output gap $x$", font_size=23,
                  color=GREY_A),
            MathTex(r"\pi_t = \beta\, \mathbb{E}_t\, \pi_{t+1} + \kappa\, x_t", font_size=48, color=INFL),
            MathTex(r"\kappa = \frac{(1-\theta)(1-\beta\theta)}{\theta}\,\Theta\,\Big(\sigma + "
                    r"\frac{\varphi + \alpha}{1-\alpha}\Big)", font_size=32),
            label(r"solve it forward:", font_size=23, color=GREY_A),
            MathTex(r"\pi_t = \kappa \sum_{k=0}^{\infty} \beta^k\, \mathbb{E}_t\, x_{t+k}", font_size=40,
                    color=INFL),
            label(r"inflation today is the discounted sum of all the output gaps people expect", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.05)
        tag = published_tag(r"Gal\'i (2015), \ ch.\ 3; \ Woodford, \ \emph{Interest and Prices} (2003)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Put the two equations together, use the fact that marginal cost rises with the output gap, the "
            "percentage gap between output and what it would be with flexible prices, <bookmark mark='a'/> and "
            "out comes the New Keynesian Phillips curve: inflation today equals beta times expected inflation next "
            "quarter, plus kappa times the output gap. <bookmark mark='b'/> Kappa, the slope, shrinks as prices "
            "get stickier, as theta rises, and depends on how fast costs rise with output. "
            "<bookmark mark='c'/> Now solve it forward, <bookmark mark='d'/> and inflation today is kappa times the "
            "discounted sum of every output gap people expect. <bookmark mark='e'/> Compare Part twenty-eight's "
            "curve, which looked backward at last year's inflation. This one looks forward: firms raise prices "
            "today because they expect costs to be high later."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(rows[1]), run_time=1.3)
            vo.wait_until("b")
            self.play(Write(rows[2]), run_time=1.3)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(Write(rows[4]), run_time=1.3)
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def slope(self):
        C = load("calvo")
        T = island.truths(30)["nk"]
        th = np.linspace(0.42, 0.9, 120)
        ks = [nk.kappa(t, T["beta"], T["sigma"], T["phi"], T["alpha"], T["eps"]) for t in th]
        ax = plane([0.4, 0.9], [0, 0.8], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.8, y_length=4.8,
                   xticks=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                   xlabel=r"$\theta$, \ the chance a price survives a quarter", ylabel=r"$\kappa$, \ the slope",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=15)
        line = path(ax, th, ks, INFL, 3.5, yr=(0, 0.8))
        pts = []
        for name, t, col in ((r"Bils--Klenow", C["theta_bk"], FLEX), (r"Gal\'i's baseline", T["theta"], PRICE),
                             (r"Nakamura--Steinsson", C["theta_ns"], STICKY)):
            k = nk.kappa(t, T["beta"], T["sigma"], T["phi"], T["alpha"], T["eps"])
            d = dot(ax, t, k, col, 0.09)
            lab = label(rf"{name}: \ $\theta = {t:.2f}$, \ $\kappa = {k:.2f}$", font_size=17, color=col).next_to(
                d, DR if name.startswith("Nakamura") else UR, buff=0.08)
            pts.append((d, lab))
        side = VGroup(
            label(r"stickier prices, \\ a flatter curve", font_size=21, color=INFL),
            label(r"from 4 months to 10, \\ the slope falls more than fourfold", font_size=19, color=E.ACCENT),
            label(r"a flat curve: \ slack moves \\ inflation only slowly", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How steep is the curve? <bookmark mark='a'/> Here is kappa against theta, holding the rest of the "
            "Island's economy fixed. Stickier prices mean a flatter curve. <bookmark mark='b'/> If prices last about "
            f"four months, as Bils and Klenow found, theta is about {C['theta_bk']:.1f} and kappa about "
            f"{nk.kappa(C['theta_bk'], T['beta'], T['sigma'], T['phi'], T['alpha'], T['eps']):.2f}. "
            "<bookmark mark='c'/> Galí's baseline, prices lasting nine months, gives "
            f"{C['base']['kappa']:.2f}, which the Island uses. <bookmark mark='d'/> Nakamura and Steinsson's regular "
            "prices give about "
            f"{nk.kappa(C['theta_ns'], T['beta'], T['sigma'], T['phi'], T['alpha'], T['eps']):.2f}. "
            "<bookmark mark='e'/> The difference between those two numbers decides how much output a central bank "
            "must sacrifice to move inflation, the sacrifice ratio of Part twenty-eight."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]), run_time=1.5)
            for mk, (d, lab) in zip("bcd", pts):
                vo.wait_until(mk)
                self.play(GrowFromCenter(d), FadeIn(lab))
            vo.wait_until("e")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()
