from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403

METHODS = (("classifier", NAIVE), ("hand-labelled", JUDGE), ("prediction-powered", CAUSE))


class Text(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Text and images as data", r"How do words and pictures become numbers, \ and what if the "
             r"numbers are predictions?", "Chapter seven. Text and images as data.",
             lit={2016: r"Jean et al.", 2019: r"Gentzkow, Kelly and Taddy", 2023: r"Angelopoulos et al."},
             scale=("person", "world"), horizon=("a year",))
        self.sources()
        self.measure()

    def sources(self):
        steps = flow_chain([(r"newspapers, \ minutes, \ filings, \ reviews", TEXT),
                            (r"words counted, \ or embedded as vectors", TEXT),
                            (r"a model trained on a few hand labels", ALGO),
                            (r"a measure for every document", GDP)], box_w=2.9, box_h=1.2, font_size=19)
        steps.to_edge(UP, buff=0.8)
        if steps.width > 13.0:
            steps.width = 13.0
        cards = point_cards([
            (r"text", r"policy uncertainty from newspapers \ (Part 57), \ central banks' tone, \ firms' risks from "
             r"their filings, \ slant from politicians' words", TEXT),
            (r"images", r"satellite pictures of roofs, \ roads and fields predict village consumption in five African "
             r"countries, \ explaining up to three quarters of its variation \ (Jean et al.)", ALGO),
        ], cols=2, width=12.8, font_size=20).next_to(steps, DOWN, buff=0.7)
        tag = published_tag(r"Gentzkow, \ Kelly and Taddy, \ JEL 57(3) (2019); \ Jean et al., \ Science 353(6301) "
                            r"(2016)", corner=DL, font_size=12)
        with self.voiceover(
            "Much of what economists care about was never written down as a number. <bookmark mark='a'/> It sits "
            "in newspapers, meeting minutes, company filings and reviews; <bookmark mark='b'/> the words can be "
            "counted, or turned into vectors that place similar meanings near each other; <bookmark mark='c'/> a "
            "model trained on a few hundred documents labelled by hand <bookmark mark='d'/> can then label millions. "
            "<bookmark mark='e'/> Matthew Gentzkow, Bryan Kelly and Matt Taddy surveyed the methods: measures of "
            "policy uncertainty, of a central bank's tone, of the risks firms say they face, of politicians' "
            "slant. <bookmark mark='f'/> Images work the same way. Neal Jean and coauthors trained a network on "
            "satellite pictures to predict consumption in villages in five African countries, explaining up to "
            "three quarters of its variation, where surveys are rare."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [FadeIn(steps.boxes[k])]
                if k:
                    anims.append(GrowArrow(steps.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("e")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.1))
        self.clear_scene()

    def measure(self):
        X = load("text")
        ax = plane([0.08, 0.17], [-0.5, 2.5], center=RIGHT * 1.5 + DOWN * 0.1, x_length=7.4, y_length=4.2,
                   xticks=[0.09, 0.11, 0.13, 0.15], yticks=[], xlabel=r"estimated share of news about layoffs",
                   xfmt=lambda v: rf"{100 * v:.0f}\%", font_size=15)
        truth = vline(ax, X["share"], -0.5, 2.5, TRUTHC)
        rng = np.random.default_rng(64)
        rows = VGroup()
        names = VGroup()
        for r, (k, c) in enumerate(METHODS):
            y0 = 2 - r
            rows.add(VGroup(*[dot(ax, x, y0 + rng.uniform(-0.25, 0.25), c, 0.035) for x in X[k]["draws"]]))
            names.add(label(rf"{k}: \ $\pm${50 * X[k]['width']:.1f} points, \ covers "
                            rf"{100 * X[k]['coverage']:.0f}\%", font_size=16, color=c).next_to(ax.ax.c2p(0.08, y0),
                                                                                              LEFT, buff=0.15))
        if names.width > 4.2:
            names.scale_to_fit_width(4.2)
            for r, nm in enumerate(names):
                nm.next_to(ax.ax.c2p(0.08, 2 - r), LEFT, buff=0.15)
        head = label(rf"{X['N']:,} articles, \ {100 * X['share']:.0f}\% about layoffs; \ a classifier that catches "
                     rf"{100 * X['sens']:.0f}\% and wrongly flags {100 * (1 - X['spec']):.0f}\%; \ {X['labelled']} "
                     r"labelled by hand".replace(",", "{,}"), font_size=19, color=WHITE).to_edge(UP, buff=0.45)
        tag = published_tag(r"Angelopoulos, \ Bates, \ Fannjiang, \ Jordan and Zrnic, \ Science 382(6671) (2023); "
                            r"\ the Island: \ agora.learn.text\_measure", corner=DL, font_size=12)
        with self.voiceover(
            "But a predicted label is a measurement with error, and the error does not average away. On the "
            f"Island, {X['N']:,} news articles, {100 * X['share']:.0f} percent about layoffs. <bookmark mark='a'/> "
            f"A good classifier catches {100 * X['sens']:.0f} percent of them and wrongly flags "
            f"{100 * (1 - X['spec']):.0f} percent of the rest. Its estimate of the share is "
            f"{100 * X['classifier']['mean']:.1f} percent, every time, with a confident interval that never covers "
            "the truth. <bookmark mark='b'/> Labelling a random four hundred by hand is unbiased, but noisy: plus or "
            f"minus {50 * X['hand-labelled']['width']:.1f} points. <bookmark mark='c'/> Prediction-powered "
            "inference, from Anastasios Angelopoulos and colleagues, uses both: the classifier's share on "
            "everything, corrected by its average error on the hand-labelled four hundred. Unbiased, covering the "
            f"truth {100 * X['prediction-powered']['coverage']:.0f} percent of the time, and a third narrower than "
            "the hand labels alone. The same idea works for regressions whose outcome is a prediction."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(truth), FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in rows[k]], lag_ratio=0.005), FadeIn(names[k]),
                          run_time=1.2)
        self.clear_scene()
