from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ foundation models for economic data", r"When should a person defer to the "
             r"machine, \ and what comes after prediction?", "Chapter fifteen. Frontier: foundation models for "
             r"economic data.", scale=("person", "world"), horizon=("a decade",))
        self.defer()
        self.open_()

    def defer(self):
        S = load("sweep")
        rows = S["rows"]
        w = [r["signal"] for r in rows]
        cut = [100 * r["crime_cut"] for r in rows]
        ax = plane([-0.1, 1.9], [-55, 30], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[0, 0.45, 0.9, 1.35, 1.8], yticks=[-50, -25, 0, 25],
                   xlabel=r"how much the judge sees that the records do not", ylabel=r"failures prevented by the "
                   r"algorithm, \ \%", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}")
                   if v else "0", font_size=14)
        zero = seg(ax, -0.1, 0, 1.9, 0, GREY_C, 1.4)
        ln = path(ax, w, cut, ALGO, 3.4)
        ds = VGroup(*[dot(ax, x, y, ALGO if y >= 0 else JUDGE, 0.08) for x, y in zip(w, cut)])
        here = dot(ax, 0.45, cut[1], TRUTHC, 0.12)
        side = VGroup(
            label(r"the Island's courts again, \ with the judges' \\ courtroom signal made weaker or stronger",
                  font_size=19, color=WHITE),
            label(r"gold: \ the Island of this part", font_size=19, color=TRUTHC),
            label(r"when the judge sees enough, \\ the algorithm makes things worse", font_size=19, color=JUDGE),
            label(r"the frontier: \ combining the two, \\ and knowing when to defer", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.learn.signal\_sweep", corner=DL, font_size=12)
        with self.voiceover(
            "The frontier begins where this part's hook ended: the judge sees things the records do not. "
            "<bookmark mark='a'/> Rerun the Island's courts with the courtroom signal made weaker or stronger. "
            f"<bookmark mark='b'/> If judges see nothing extra, the algorithm prevents {cut[0]:.0f} percent of "
            f"failures at their detention rate; at this part's setting, {cut[1]:.0f}. <bookmark mark='c'/> As the "
            "signal grows, the advantage shrinks, and then reverses: when the judge sees enough, ranking by the "
            "records alone makes things worse. <bookmark mark='d'/> So the research question is not machine against "
            "human but how to combine them: which cases to hand over, when a person should defer, and why, in "
            "experiments with doctors and other experts, people often weigh the machine's advice badly."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(ds), FadeIn(here), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def open_(self):
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        cards = point_cards([
            (r"foundation models for economic data", r"models pretrained on millions of firms' accounts, \ prices or "
             r"job histories, \ then tuned to a question, \ as language models are tuned to a task", NET),
            (r"automated structural estimation", r"networks that learn the map from data to a model's parameters "
             r"by simulation \ (Part 54's amortized estimator), \ for models too slow to estimate otherwise", ALGO),
            (r"agents in markets", r"pricing, \ bidding and negotiating algorithms that learn from each other: \ "
             r"what does competition policy owe them?", JUDGE),
            (r"what remains hard", r"the old questions: \ what would have happened, \ and who decided what was "
             r"measured", HOLD),
        ], cols=2, width=12.8, font_size=20).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Foundation models for economic data: networks pretrained on "
            "millions of firms' accounts, prices or job histories, then tuned to a question, the way language "
            "models are tuned to a task. <bookmark mark='b'/> Automated structural estimation: networks that learn, "
            "by simulation, the map from data to a model's parameters, as Part fifty-four's amortized estimator "
            "did, for models too slow to estimate any other way. <bookmark mark='c'/> Agents in markets: pricing, "
            "bidding and negotiating algorithms that learn from each other, and what competition policy owes them. "
            "<bookmark mark='d'/> And the old questions, which no amount of data removes: what would have "
            "happened otherwise, and who decided what was measured."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
