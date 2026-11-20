from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Optimal(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Optimal policy: \ discretion and commitment", r"What is the best a central bank can do "
             r"after a cost shock?", "Chapter ten. Optimal policy: discretion and commitment.",
             lit={1999: r"Clarida, \ Gal\'i and Gertler", 2003: r"Woodford"}, scale=("nation",),
             horizon=("a quarter", "three years"))
        self.loss()
        self.paths()
        self.level()

    def loss(self):
        O = load("optimal")
        rows = VGroup(
            label(r"why is inflation costly here?", font_size=26, color=E.ACCENT),
            label(r"with Calvo pricing, \ inflation means some prices are new and some old: \ relative prices "
                  r"spread", font_size=22, color=INFL),
            label(r"identical goods sell at different prices, \ so people buy the wrong mix", font_size=22,
                  color=GREY_A),
            label(r"the welfare loss, \ derived from utility (Woodford):", font_size=22, color=GREY_A),
            MathTex(r"\mathcal{L} = \sum_t \beta^t \big(\pi_t^2 + \tfrac{\kappa}{\varepsilon}\, x_t^2\big)",
                    font_size=40, color=CB),
            label(rf"on the Island \ $\kappa/\varepsilon = {O['weight']:.3f}$: \ inflation is far costlier than a "
                  r"gap", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Woodford, \ \emph{Interest and Prices} (2003), \ ch.\ 6; \ Gal\'i (2015), \ ch.\ 4",
                            corner=DR, font_size=12)
        with self.voiceover(
            "To ask what the best policy is, first ask why inflation is costly in this model. "
            "<bookmark mark='a'/> With Calvo pricing, inflation means some prices were set recently and some long "
            "ago, so relative prices spread out. <bookmark mark='b'/> Goods that cost the same to make sell at "
            "different prices, and people buy the wrong mix of them. <bookmark mark='c'/> Michael Woodford derived "
            "the welfare loss from the household's own utility: <bookmark mark='d'/> a sum of squared inflation "
            "and squared output gaps, with a weight of kappa over epsilon on the gap. "
            f"<bookmark mark='e'/> On the Island that weight is {O['weight']:.3f}: a point of inflation costs as "
            "much as several points of output gap, because of all the price dispersion it causes."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                if isinstance(r_, MathTex):
                    self.play(Write(r_), run_time=1.3)
                else:
                    self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def paths(self):
        O = load("optimal")
        q = np.array(O["q"])
        top = plane([0, 11], [-0.4, 0.9], center=LEFT * 1.9 + UP * 1.35, x_length=8.0, y_length=2.4,
                    xticks=[0, 4, 8], yticks=[0, 0.4, 0.8], ylabel=r"inflation, \ annual rate", xfmt=lambda v: "",
                    yfmt=lambda v: f"{v:.1f}", font_size=14)
        bot = plane([0, 11], [-2.0, 0.4], center=LEFT * 1.9 + DOWN * 1.85, x_length=8.0, y_length=2.4,
                    xticks=[0, 4, 8], yticks=[-2, -1, 0], ylabel=r"output gap, \ \%", xlabel=r"quarters",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        z1, z2 = seg(top, 0, 0, 11, 0, GREY_D, 1.2), seg(bot, 0, 0, 11, 0, GREY_D, 1.2)
        pd_ = path(top, q, O["pi_d"], INFL, 3, smooth=False)
        pc_ = path(top, q, O["pi_c"], CB, 3, smooth=False)
        xd = path(bot, q, O["x_d"], INFL, 3, smooth=False)
        xc = path(bot, q, O["x_c"], CB, 3, smooth=False)
        side = VGroup(
            label(r"a cost-push shock of one point, \\ fading by half each quarter", font_size=19, color=COST),
            label(r"red: \ discretion: \ do what is \\ best each quarter", font_size=19, color=INFL),
            label(r"green: \ commitment: \ promise \\ a slump that lasts", font_size=19, color=CB),
            label(rf"loss: \ {O['loss_d']:.3f} against {O['loss_c']:.3f}", font_size=19, color=E.ACCENT),
            label(r"the promise does the work: \\ expected deflation later \\ lowers inflation now", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Clarida, \ Gal\'i and Gertler, \ \emph{JEL} 37(4) (1999); \ the Island", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Now a cost-push shock of one point, fading by half each quarter, and two ways to respond. "
            "<bookmark mark='a'/> Under discretion, the central bank does what is best each quarter, taking "
            "expectations as given. It splits the pain: inflation rises "
            f"{O['pi_d'][0]:.2f} points and output falls, both fading with the shock. <bookmark mark='b'/> Under "
            "commitment, it promises to keep output a little low even after the shock has gone. "
            "<bookmark mark='c'/> Because Calvo's firms look ahead, that promise lowers inflation immediately: "
            f"{O['pi_c'][0]:.2f} on impact instead of {O['pi_d'][0]:.2f}, then slightly below zero for a while. "
            f"<bookmark mark='d'/> The loss falls from {O['loss_d']:.3f} to {O['loss_c']:.3f}, about a third less. "
            "<bookmark mark='e'/> The promise does the work, but it is only worth anything if it is believed, and "
            "it is tempting to break later: Part twenty-eight's time inconsistency again."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(z1), FadeIn(z2), FadeIn(side[0]), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(pd_), Create(xd), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(pc_), Create(xc), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def level(self):
        O = load("optimal")
        q = np.array(O["q"])
        ax = plane([0, 11], [0, 0.45], center=LEFT * 1.9 + DOWN * 0.3, x_length=8.0, y_length=4.6,
                   xticks=[0, 4, 8], yticks=[0, 0.1, 0.2, 0.3, 0.4], xlabel=r"quarters",
                   ylabel=r"the price level, \ \% above where it started", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=15)
        d = path(ax, q, O["price_d"], INFL, 3.5, smooth=False)
        c = path(ax, q, O["price_c"], CB, 3.5, smooth=False)
        side = VGroup(
            label(rf"discretion: \ prices end {O['price_d'][-1]:.2f}\% higher, \\ for good", font_size=20,
                  color=INFL),
            label(r"commitment: \ the price level \\ comes back", font_size=20, color=CB),
            label(r"optimal commitment \\ looks like price-level targeting: \\ bygones are not bygones",
                  font_size=20, color=E.ACCENT),
            label(r"compare the Federal Reserve's \\ average inflation targeting, \\ 2020 \ (Part 31)",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The clearest difference is in the price level. <bookmark mark='a'/> Under discretion, the price "
            f"level ends {O['price_d'][-1]:.2f} percent higher and stays there: bygones are bygones. "
            "<bookmark mark='b'/> Under commitment, the brief deflation after the shock brings the price level "
            "back to where it started. <bookmark mark='c'/> So the best policy looks like targeting the price "
            "level, making up for past inflation, and that is what makes people expect lower inflation today. "
            "<bookmark mark='d'/> The Federal Reserve's move in 2020 to average inflation targeting, making up for "
            "past shortfalls, borrowed this idea, as Part thirty-one explains."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(d), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
