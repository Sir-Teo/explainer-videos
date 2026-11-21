from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ micro data in macro models", r"What should a model of many households be "
                                                                   r"fitted to?",
             "Chapter fifteen. Frontier: micro data in macro models.",
             lit={2020: r"Auclert, Rognlie, Straub", 2021: r"Fagereng, Holm, Natvik"}, scale=("household", "world"),
             horizon=("a decade",))
        self.impc()
        self.open_questions()

    def impc(self):
        Hk = load("hank")
        rows = {r["liquid"]: r for r in Hk["rows"]}
        yrs = np.arange(6)
        ax = plane([0, 5], [0, 0.6], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"years after the windfall",
                   ylabel=r"share of it spent that year", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        cols = {1.0: POOR, 4.0: MANY, 16.0: RICH}
        curves = VGroup(*[path(ax, yrs, rows[k]["impc"], c, 3.0, smooth=False) for k, c in cols.items()])
        dots = VGroup(*[VGroup(*[dot(ax, x, y, c, 0.07) for x, y in zip(yrs, rows[k]["impc"])])
                        for k, c in cols.items()])
        side = VGroup(
            label(r"orange: \ 1 quarter of liquid wealth", font_size=18, color=POOR),
            label(r"green: \ 4 quarters", font_size=18, color=MANY),
            label(r"blue: \ 16 quarters", font_size=18, color=RICH),
            label(r"Norway's lottery winners: \\ most spent in the year of \\ winning, \ back to normal \\ within "
                  r"five years", font_size=18, color=DATA),
            label(r"the whole curve is a target, \\ not one number", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Fagereng, \ Holm and Natvik, \ AEJ: Macro (2021); \ Auclert, \ Rognlie and Straub "
                            r"(2020)", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier is in fitting these models to the households they describe. One number, the share of a "
            "windfall spent in a quarter, is not enough. What matters for policy is the whole path: how much is "
            "spent in the first year, the second, the third. <bookmark mark='a'/> Here are those paths for the "
            "economies of this part. The less liquid wealth, the more is spent at once and the faster the spending "
            "dies away. <bookmark mark='b'/> In Norway, where tax records cover every household, Andreas "
            "Fagereng, Martin Holm and Gisle Natvik followed lottery winners: spending peaks in the year of "
            "winning and returns to normal within about five years. <bookmark mark='c'/> Adrien Auclert, Matthew "
            "Rognlie and Ludwig Straub argued that a model should be fitted to that whole curve, and that one "
            "which is, with sluggish expectations added, produces both the jumps seen in household data and the "
            "slow humps seen in aggregate data."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            self.play(Create(curves[0]), FadeIn(dots[0]), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves[1:]], lag_ratio=0.3), FadeIn(dots[1:]),
                      FadeIn(side[1:3]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()

    def open_questions(self):
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        cards = point_cards([
            (r"estimation", r"fitting the whole distribution to household and national data at once", MANY),
            (r"beliefs", r"households disagree about inflation and their own futures; \ how to model it", DIST),
            (r"big shocks", r"nonlinear aggregate risk with many households, \ beyond linearization", ERR),
            (r"climate and inequality", r"who bears a carbon tax, \ and who adapts, \ in one model", INDIRECT),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.3)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Estimation: fitting a model's whole distribution to "
            "household records and to national accounts at the same time. <bookmark mark='b'/> Beliefs: households "
            "disagree wildly about inflation and about their own prospects, and models with many households are "
            "only beginning to let their beliefs differ too. <bookmark mark='c'/> Big shocks: the sequence-space "
            "methods linearize in the aggregates; a deep recession, or a crisis, may need the full nonlinear "
            "economy, and that is still hard. <bookmark mark='d'/> And climate: who bears a carbon tax and who can "
            "adapt to a warmer world are questions about distributions, and the models that answer them are being "
            "built now."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c_ in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
        self.clear_scene()
