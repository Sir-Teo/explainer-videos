from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class HoldUp(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Specific assets and hold-up", r"Why might a supplier refuse to make an investment that would "
             r"pay?", "Chapter eleven. Specific assets and hold-up: Fisher Body and General Motors.",
             lit={1978: r"Klein, Crawford and Alchian"}, scale=("firm", "market"), horizon=("a decade",))
        self.model()
        self.fisher_body()
        self.record()

    def model(self):
        b = load("boundary")
        h = b["holdup"]
        i = np.array(b["i"])
        ax = plane([0, 140], [0, 260], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 25, 50, 75, 100, 125], yticks=[0, 100, 200], xlabel=r"investment in the special dies, "
                   r"$i$", ylabel=r"\$", font_size=17)
        a = ax.ax
        val = path(ax, i, b["value"], color=OUT, width=3.5)
        half = path(ax, i, b["theta"] * np.array(b["value"]), color=HOLD, width=3, smooth=True)
        cost = path(ax, i, i, color=GREY_B, width=2.5, smooth=False)
        P1 = Dot(a.c2p(h["first_best"], 2 * b["V"] * np.sqrt(h["first_best"])), radius=0.08, color=OUT)
        P2 = Dot(a.c2p(h["held_up"], b["theta"] * 2 * b["V"] * np.sqrt(h["held_up"])), radius=0.08, color=HOLD)
        names = VGroup(label(r"value to the car maker", font_size=19, color=OUT).move_to(a.c2p(42, 215)),
                       label(r"the body maker's half", font_size=19, color=HOLD).next_to(
                           a.c2p(124, b["theta"] * 2 * b["V"] * np.sqrt(124)), DOWN, buff=0.3),
                       label(r"its cost", font_size=19, color=GREY_B).next_to(a.c2p(130, 130), RIGHT, buff=0.05))
        side = VGroup(
            label(r"a body maker can invest in dies \\ that fit only one car maker's model", font_size=23),
            label(r"value $2V\sqrt{i}$, \ cost $i$; \ $V = 10$", font_size=23, color=OUT),
            label(rf"together: \ invest {h['first_best']:.0f}, \ surplus {h['surplus_first']:.0f}", font_size=24,
                  color=OUT),
            label(r"apart: \ once the dies exist, the buyer can \\ bargain the price down to half the surplus", font_size=22,
                  color=HOLD),
            label(rf"knowing that, the body maker invests {h['held_up']:.0f}: \\ surplus {h['surplus_held']:.0f}, \ "
                  rf"{h['loss']:.0f} lost", font_size=24, color=HOLD),
            label(r"the fix: \ a long contract, \ or one owner for both", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is what goes wrong. <bookmark mark='a'/> A maker of car bodies can invest in dies that stamp out "
            "panels for one car maker's model, and for nobody else's. <bookmark mark='b'/> The more it invests, the "
            "more the dies are worth to the car maker, with diminishing returns. <bookmark mark='c'/> If the two "
            "acted as one, they'd invest until the last dollar added a dollar of value: a hundred, for a surplus of "
            "a hundred. <bookmark mark='d'/> But they're separate firms, and once the dies exist they're worth "
            "nothing elsewhere, so the car maker can bargain the price down. Say they split the surplus evenly after "
            "the investment is made. <bookmark mark='e'/> The body maker, foreseeing that, invests only until half "
            "the extra value covers its cost: twenty-five, for a surplus of seventy-five. A quarter of the value is "
            "lost, and nobody did anything irrational. This is the hold-up problem. <bookmark mark='f'/> The cures "
            "are a long contract that fixes the terms in advance, or a single owner for both."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(cost), FadeIn(names[2]))
            vo.wait_until("b")
            self.play(Create(val), FadeIn(names[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(P1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(half), FadeIn(names[1]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(P2), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def fisher_body(self):
        c1 = history_card(1919, r"General Motors and Fisher Body", r"GM buys a large stake and signs a ten-year "
                          r"contract: \ Fisher will be GM's exclusive supplier of closed bodies, \ at a price set "
                          r"by cost plus a margin", color=MARKET, width=11.6, font_size=24)
        c2 = history_card(1926, r"GM buys the rest", r"the 40\% of Fisher Body it did not own", color=FIRM,
                          width=11.6, font_size=24)
        c3 = history_card(1978, r"Klein, Crawford and Alchian", r"the textbook story: \ Fisher held GM up, \ "
                          r"refusing to build plants near GM's and charging too much; \ integration ended it",
                          color=HOLD, width=11.6, font_size=24)
        g = VGroup(c1, c2, c3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)
        tag = published_tag(r"Klein, Crawford and Alchian, JLE 21(2) (1978); Coase, JLE 43(1) (2000)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "The most famous example in economics is a real merger. <bookmark mark='a'/> In 1919 General Motors bought "
            "a large stake in Fisher Body and signed a ten-year contract making Fisher its exclusive supplier of "
            "closed car bodies, at a price based on cost. <bookmark mark='b'/> In 1926 GM bought the remaining forty "
            "percent. <bookmark mark='c'/> In 1978 Benjamin Klein, Robert Crawford and Armen Alchian told the story "
            "that went into the textbooks: protected by its contract, Fisher held GM up, refusing to build body "
            "plants next to GM's assembly plants and charging too much, and GM ended the hold-up by buying it."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abc", (c1, c2, c3)):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.2))
        self.clear_scene()

    def record(self):
        q = quote_card(r"There was no holdup.", r"Ronald Coase, ``The Acquisition of Fisher Body by General Motors'', "
                       r"\emph{Journal of Law and Economics} (2000)", width=10.4, font_size=30,
                       color=HOLD).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"2000: \ the \emph{Journal of Law and Economics} re-examines the record", font_size=26),
            label(r"Coase: \ the prevailing view gives ``a completely false picture'' \\ of the events that led "
                  r"to the acquisition", font_size=24, color=GREY_A),
            label(r"Freeland: \ ``Creating Holdup through Vertical Integration''; \ Casadesus-Masanell and Spulber: "
                  r"\\ ``The Fable of Fisher Body''", font_size=23, color=GREY_A),
            label(r"Klein replies: \ the facts fit the hold-up account", font_size=24, color=GREY_A),
            label(r"the theory survives the dispute; \ the example may not: \\ check the record before you teach "
                  r"the story", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(q, DOWN, buff=0.45)
        tag = published_tag(r"Journal of Law and Economics 43(1) (2000)", corner=DR, font_size=14)
        with self.voiceover(
            "Then, in 2000, the record was examined. <bookmark mark='a'/> A whole issue of the Journal of Law and "
            "Economics was devoted to it. <bookmark mark='b'/> Coase, then nearly ninety, went back to the evidence "
            "and concluded flatly: there was no hold-up, and the prevailing view gave a completely false picture of "
            "the events that led to the merger. <bookmark mark='c'/> Robert Freeland argued that, if anything, "
            "integration created hold-up rather than ending it; Ramon Casadesus-Masanell and Daniel "
            "Spulber called the textbook story a fable. <bookmark mark='d'/> Klein replied that the facts fit his "
            "account. <bookmark mark='e'/> The theory of hold-up doesn't depend on one merger, and survives. The "
            "example may not. The lesson for any economist is to check the record before you teach the story."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(q, shift=UP * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
