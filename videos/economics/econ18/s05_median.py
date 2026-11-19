from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403

WHO = ("ana", "bo", "chidi", "dara", "friday")


class Median(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Ways out: \ single peaks and May's theorem", r"When can majority rule be trusted?",
             "Chapter four. Ways out: single peaks and May's theorem.",
             lit={1948: r"Black", 1952: r"May", 1957: r"Downs"}, scale=("community", "nation"), horizon=("a year",))
        self.line()
        self.downs()
        self.may()

    def line(self):
        sp = load("peaks")
        nl = NumberLine(x_range=[0, 10, 1], length=11.0, include_numbers=True, font_size=22, color=GREY_B).move_to(
            DOWN * 0.6)
        head = label(r"five islanders' ideal size for the new granary, \ in hundreds of baskets", font_size=25,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        dots = VGroup()
        for k, x in zip(WHO, sp["peaks"]):
            c = color_of(k)
            dots.add(VGroup(Dot(nl.n2p(x), radius=0.12, color=c), islander(k, 0.55).next_to(nl.n2p(x), UP, buff=0.25)))
        rows = VGroup(
            label(r"each prefers sizes nearer their own: \ a single peak", font_size=23),
            label(r"3 against 5: \ the three whose peaks are 3 or below vote 3; \ 3 wins, \ 3 to 2", font_size=23,
                  color=WELF),
            label(rf"the median, \ {sp['median']:.0f}, \ beats every other size: \ the Condorcet winner",
                  font_size=24, color=E.ACCENT),
            label(rf"not the average, \ {sp['mean']:.1f}: \ the two who want a big granary can't pull it their way",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(nl, DOWN, buff=0.5)
        med = VGroup(DashedLine(nl.n2p(sp["median"]) + DOWN * 0.3, nl.n2p(sp["median"]) + UP * 1.6, color=E.ACCENT,
                                stroke_width=3),
                     label(r"median", font_size=19, color=E.ACCENT).next_to(nl.n2p(sp["median"]) + UP * 1.6, UP,
                                                                           buff=0.05))
        tag = published_tag(r"Black, JPE 56(1) (1948)", corner=DR, font_size=13)
        with self.voiceover(
            "The first way out restricts what people may want. Five islanders are deciding how big to build a new "
            "granary, and each has an ideal size. <bookmark mark='a'/> Each prefers sizes nearer their own ideal: "
            "their preferences have a single peak, on a line. <bookmark mark='b'/> Put three hundred baskets against "
            "five hundred. The three islanders whose ideals are three or below prefer three, and three wins. "
            "<bookmark mark='c'/> In fact the median ideal, three, beats every other size in a straight vote. "
            "Duncan Black proved in 1948 that with single-peaked preferences, the median voter's favourite is a "
            "Condorcet winner, and majority rule never cycles. <bookmark mark='d'/> Notice that it is the median, not "
            "the average of four point four: the two who want a much bigger granary cannot pull the outcome their "
            "way, however much they want it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nl), FadeIn(dots), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == "c":
                    self.play(Create(med[0]), FadeIn(med[1]))
        self.clear_scene()

    def downs(self):
        rows = VGroup(
            label(r"Anthony Downs, \ 1957: \ two parties competing for votes on one line", font_size=24),
            label(r"each moves toward the median voter, \ since that is where the majority is", font_size=24,
                  color=WELF),
            label(r"so platforms converge, \ and the median voter decides", font_size=24, color=E.ACCENT),
            label(r"but if politics has two dimensions, \ cycles return \ (McKelvey's chaos)", font_size=24,
                  color=CYCLE),
            label(r"and parties also answer to activists, \ donors and primaries: \ parts forty-seven and fifty-eight",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Downs, \emph{An Economic Theory of Democracy} (1957)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1957 Anthony Downs turned the result into a theory of elections. <bookmark mark='a'/> Two parties "
            "compete for votes along a single line from left to right. <bookmark mark='b'/> Each moves toward the "
            "median voter, because that is where the majority is. <bookmark mark='c'/> So their platforms converge, "
            "and the median voter decides. <bookmark mark='d'/> The escape is narrow, though. If politics has two "
            "dimensions, taxes and, say, immigration, single peaks no longer guarantee a winner, and the cycles come "
            "back. <bookmark mark='e'/> And real parties also answer to activists, donors and primary voters, as "
            "part forty-seven explores."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def may(self):
        rows = VGroup(
            label(r"with only two options, \ there is no cycle", font_size=26),
            label(r"anonymous: \ every voter counts the same", font_size=24, color=RULE),
            label(r"neutral: \ the two options are treated the same", font_size=24, color=RULE),
            label(r"positively responsive: \ one more vote for x never hurts x, \ and can break a tie for it",
                  font_size=24, color=RULE),
            label(r"Kenneth May, \ 1952: \ only simple majority rule satisfies all three", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"May, Econometrica 20(4) (1952)", corner=DR, font_size=13)
        with self.voiceover(
            "With only two options, the picture is clean. <bookmark mark='a'/> Ask for three things. The rule "
            "should be anonymous, counting every voter the same. <bookmark mark='b'/> It should be neutral, treating "
            "the two options the same. <bookmark mark='c'/> And it should be positively responsive: one more vote "
            "for x never hurts x, and breaks a tie in its favour. <bookmark mark='d'/> Kenneth May proved in 1952 "
            "that simple majority rule is the only rule with all three. Between two options, majority rule is not "
            "one choice among many; it is the fair one."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
