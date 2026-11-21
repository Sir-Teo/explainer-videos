from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Culture(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Culture and relational contracts", r"Why can't a firm just copy a better-run rival's "
             r"practices?", "Chapter twelve. Culture and relational contracts.",
             lit={1984: r"NUMMI", 2012: r"Gibbons and Henderson"}, scale=("person", "firm"), horizon=("a decade",))
        self.relational()
        self.copying()

    def relational(self):
        R = load("relational")
        d, e = np.array(R["deltas"]), np.array(R["effort"])
        ax = plane([0, 1], [0, 11], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.4,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 5, 10], xlabel=r"how likely the relationship goes on "
                   r"($\delta$)", ylabel=r"effort the relationship can sustain", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        pe = path(ax, d, e, MGR, 3.2, smooth=False)
        fb = seg(ax, 0, R["first_best"], 1, R["first_best"], GREY_B, 1.4, dashed=True)
        th = vline(ax, R["threshold"], 0, 11, WHITE, 1.4)
        side = VGroup(
            label(r"effort no court can verify: \ care, \ initiative, \ telling the boss the truth", font_size=19,
                  color=WHITE),
            label(r"the firm promises a bonus for it; \ nothing but the future makes the promise good",
                  font_size=19, color=MGR),
            MathTex(r"\text{bonus} \le \frac{\delta}{1 - \delta}\,(\text{future surplus})", font_size=28,
                    color=WHITE),
            label(r"below $\delta$ = 0.5 the promise cannot cover the effort it asks for", font_size=19,
                  color=COST),
            label(r"a relational contract: \ an equilibrium, \ not a document \ (Part 14)", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ agora.contracts.relational, \ Part 14's model", corner=DL, font_size=12)
        with self.voiceover(
            "Much of what makes a firm well run is never written down. <bookmark mark='a'/> Care, initiative, "
            "telling the boss the truth: effort that no court could verify. <bookmark mark='b'/> A firm can promise "
            "to reward it, but nothing makes the promise good except the value of keeping the relationship going. "
            "<bookmark mark='c'/> The bonus the firm will actually pay is limited by what it would lose by reneging: "
            "the future surplus, weighed by the chance the relationship continues. <bookmark mark='d'/> In Part "
            "fourteen's model, below a continuation chance of one half, the promise cannot cover the effort it asks "
            "for, and effort falls. <bookmark mark='e'/> This is a relational contract: an equilibrium of "
            "expectations, not a document. And it explains a puzzle."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(fb))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(pe))
            vo.wait_until("d")
            self.play(Create(th), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def copying(self):
        cards = point_cards([
            (r"the puzzle", r"Toyota's methods were studied and written up for decades, \ yet rivals who copied the "
             r"visible parts rarely matched the results", COST),
            (r"NUMMI, \ 1984", r"General Motors and Toyota run a California plant together; \ it reaches Toyota's "
             r"quality with GM's former workers, \ but GM struggles to spread the system", MGR),
            (r"the explanation", r"the practices rest on relational contracts: \ shared understanding of what is "
             r"expected and what will be rewarded, \ built over years", OWN),
            (r"why it does not transfer", r"a new rule can be copied in a day; \ the trust that makes people "
             r"follow it cannot", GAIN),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"why practices do not travel", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Gibbons and Henderson, \ Organization Science 23(5) (2012)", corner=DL, font_size=12)
        with self.voiceover(
            "If the practices of chapter four are so cheap, why do so few firms copy them? <bookmark mark='a'/> "
            "Toyota's production methods were studied and written up for decades, yet rivals who copied the "
            "visible parts rarely matched the results. <bookmark mark='b'/> In 1984 General Motors and Toyota "
            "opened a joint plant in California, NUMMI, staffed largely by GM's former workers there; it reached "
            "Toyota's quality, and still GM struggled to spread the system through its own plants. <bookmark "
            "mark='c'/> Robert Gibbons and Rebecca Henderson's explanation: the practices rest on relational "
            "contracts, a shared understanding of what is expected and what will be rewarded, built over years. "
            "<bookmark mark='d'/> A new rule can be copied in a day. The trust that makes people follow it cannot, "
            "which is one reason the dispersion of chapter one lasts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
