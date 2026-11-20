from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Reference(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Reference dependence", r"Gains and losses from where?",
             "Chapter three. Reference dependence.",
             lit={1979: r"Kahneman and Tversky", 1990: r"Kahneman, Knetsch and Thaler", 2003: r"List"},
             scale=("person", "market"), horizon=("a day",))
        self.value()
        self.experience()
        self.where()

    def value(self):
        x = np.linspace(-60, 60, 241)
        v = behave.pt_value(x)
        ax = plane([-60, 60], [-90, 45], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                   xticks=[-60, -30, 0, 30, 60], yticks=[-90, -60, -30, 0, 30], xlabel=r"outcome, \ against the "
                   r"reference point", ylabel=r"how it feels", xfmt=lambda v_: f"{v_:.0f}",
                   yfmt=lambda v_: f"{v_:.0f}", font_size=14)
        gains = path(ax, x[x >= 0], v[x >= 0], GAIN, 3.4)
        losses = path(ax, x[x <= 0], v[x <= 0], LOSS, 3.4)
        g50, l50 = float(behave.pt_value(50.0)), float(behave.pt_value(-50.0))
        pg = VGroup(dot(ax, 50, g50, GAIN, 0.08), label(rf"+50 feels like {g50:.0f}", font_size=16,
                                                        color=GAIN).next_to(ax.ax.c2p(50, g50), UL, buff=0.12))
        pl = VGroup(dot(ax, -50, l50, LOSS, 0.08), label(rf"$-$50 feels like $-${-l50:.0f}", font_size=16,
                                                         color=LOSS).next_to(ax.ax.c2p(-50, l50), DR, buff=0.15))
        eq = MathTex(r"v(x) = \begin{cases} x^{\alpha} & x \ge 0 \\ -\lambda\,(-x)^{\beta} & x < 0 \end{cases}",
                     font_size=34, color=THEORY)
        side = VGroup(
            eq,
            label(r"$\alpha = \beta = 0.88$: \\ each extra dollar \\ matters a little less", font_size=18,
                  color=GREY_A),
            label(r"$\lambda = 2.25$: \ losses \\ loom larger", font_size=19, color=LOSS),
            label(r"and small chances \\ are overweighted \\ (Psychology, Built, \\ Part 26)", font_size=17,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.KKT_1990.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The mug market is prospect theory at work, the theory of choice that Daniel Kahneman and Amos Tversky "
            "published in 1979. <bookmark mark='a'/> Outcomes are felt as gains or losses against a reference "
            "point, here what you already hold, not as levels of wealth. <bookmark mark='b'/> Each additional dollar "
            "of gain feels a little less than the last, and so does each additional dollar of loss. "
            f"<bookmark mark='c'/> And losses loom larger: with the parameters Tversky and Kahneman estimated in "
            f"1992, losing fifty dollars feels like {say_num(l50, 0)}, winning fifty like {g50:.0f}. The ratio, "
            "lambda, is two and a quarter. An owner who sells a mug loses the mug; a buyer gains it. That asymmetry "
            "is the gap between asks and bids. <bookmark mark='d'/> The theory also weights small probabilities too "
            "heavily, the story of Part twenty-six of Psychology, Built; this part needs only the kink at the "
            "reference point."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(eq), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(gains), Create(losses), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pg), FadeIn(pl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def experience(self):
        X = load("experience")
        tr = np.array(X["trades"], float)
        sh = np.array(X["share_traded"])
        ax = plane([0, 50], [0, 0.6], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"trades the trader has made",
                   ylabel=r"share of goods that change hands", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        half = VGroup(seg(ax, 0, 0.5, 50, 0.5, GREY_B, 1.8, dashed=True),
                      label(r"the half predicted without loss aversion", font_size=15, color=GREY_B).next_to(
                          ax.ax.c2p(25, 0.5), UP, buff=0.08))
        ln = path(ax, tr, sh, SELL, 3.2, smooth=True)
        pts = VGroup(*[dot(ax, a, b, SELL, 0.08) for a, b in zip(tr, sh)])
        side = VGroup(
            label(r"the Island's assumption: \\ loss aversion over goods \\ meant for trade halves \\ every five "
                  r"trades", font_size=18, color=SELL),
            label(r"newcomers: \ a quarter \\ of the goods trade", font_size=18, color=LOSS),
            label(r"veterans: \ about half, \\ as theory predicts", font_size=18, color=GAIN),
            label(r"List, \ 2003: \ dealers at \\ a sports-card show \\ showed no endowment \\ effect; "
                  r"newcomers did", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.LIST_2003.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Is the endowment effect a fixed trait, or does it fade with practice? <bookmark mark='a'/> The Island "
            "assumes it fades: a trader's loss aversion over goods bought to be sold again halves every five trades. "
            f"<bookmark mark='b'/> Newcomers trade only {100 * sh[0]:.0f} percent of the goods that should change "
            f"hands. <bookmark mark='c'/> Veterans trade about half, as standard theory says. "
            "<bookmark mark='d'/> John List tested this at sports-card shows, where some traders were dealers and "
            "some were collectors attending for fun. Inexperienced traders showed the endowment effect; dealers and "
            "experienced traders did not. Markets can teach people out of an anomaly, at least for goods they "
            "handle often. Whether experience does the same for a pension, chosen once in a lifetime, is another "
            "question."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(half), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ln), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(pts[0], scale_factor=1.8), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(pts[-1], scale_factor=1.8), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def where(self):
        cards = point_cards([
            (r"what you hold", r"the mug in \\ your hands", SELL),
            (r"the status quo", r"your current plan, \\ job, \ or price", PLAN),
            (r"a goal", r"four hours, \ par, \\ the price you paid", GYM),
            (r"what you expected", r"Koszegi and Rabin: \\ recent expectations \\ set the point", SOPH),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"where is the reference point?", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"the theory is only as useful as its answer to this question", font_size=21,
                     color=HOLD).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.KKT_1990.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Everything depends on where the reference point sits. <bookmark mark='a'/> Sometimes it is what you "
            "hold. <bookmark mark='b'/> Sometimes the status quo: your current plan, your current job, last year's "
            "price. <bookmark mark='c'/> Sometimes a goal: a finishing time, par on a golf hole, the price you "
            "paid for a flat. <bookmark mark='d'/> Botond Koszegi and Matthew Rabin proposed that it is what you "
            "recently expected to happen. <bookmark mark='e'/> A theory that lets the reference point be anything "
            "can explain anything, so the test is to fix it in advance and check the predictions, which is what the "
            "next chapter does with goals."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
