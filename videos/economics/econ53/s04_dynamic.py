from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Dynamic(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Beliefs on and off the path", r"What should you believe after something that should not "
                                                         r"happen?",
             "Chapter three. Beliefs on and off the path.", lit={1982: r"Kreps and Wilson", 1987: r"Cho and Kreps"},
             scale=("person",), horizon=("a day",))
        self.pbe()
        self.beer()
        self.intuitive()

    def pbe(self):
        rows = VGroup(
            label(r"a strategy for every player, \ at every point where they move", font_size=23, color=SENDER),
            label(r"a belief at every point, \ about what has happened before", font_size=23, color=BELIEF),
            label(r"strategies are best responses, \ given the beliefs", font_size=23, color=RECEIVER),
            label(r"beliefs follow Bayes's rule wherever it applies", font_size=23, color=THEORY),
            label(r"and off the path, \ where it does not, \ beliefs are free: \ that is the trouble", font_size=23,
                  color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"perfect Bayesian equilibrium", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Kreps and Wilson, \ Econometrica (1982): \ sequential equilibrium", corner=DR,
                            font_size=12)
        with self.voiceover(
            "When moves happen in turn and some players know more, a later player learns from what an earlier one "
            "did. The equilibrium has to say what everyone believes. <bookmark mark='a'/> A perfect Bayesian "
            "equilibrium specifies a strategy for every player at every point where they move, <bookmark "
            "mark='b'/> a belief at every point about what has happened before, <bookmark mark='c'/> strategies "
            "that are best given those beliefs, <bookmark mark='d'/> and beliefs that follow Bayes's rule wherever "
            "it can be applied. <bookmark mark='e'/> The trouble is the points that are never reached in "
            "equilibrium. Bayes's rule says nothing there, and an odd belief about something that should never "
            "happen can hold up a strange equilibrium. Part thirteen met this with Spence's signals."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def beer(self):
        Bq = load("beer")
        pools = Bq["pools"]
        head = label(r"beer or quiche", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        setup = VGroup(
            label(rf"a newcomer is strong \ ({100 * Bq['p_strong']:.0f}\%) \ or weak", font_size=21, color=WHITE),
            label(r"breakfast: \ the strong prefer beer, \ the weak quiche \ (worth 1)", font_size=21, color=WHITE),
            label(r"a bully sees the breakfast, \ then decides whether to duel", font_size=21, color=WHITE),
            label(r"the bully wins only against the weak; \ avoiding a duel is worth 2 to the newcomer",
                  font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.4)
        cards = VGroup()
        for pool, col in (("beer", STRONG), ("quiche", WEAK)):
            r = pools[pool]
            off = "quiche" if pool == "beer" else "beer"
            body = VGroup(
                label(rf"both types eat {pool}; \ no duel", font_size=19, color=WHITE),
                label(rf"strong gets {r['payoffs']['strong']:.0f}, \ weak gets {r['payoffs']['weak']:.0f}",
                      font_size=19, color=GREY_A),
                label(rf"after {off}: \ the bully believes ``weak'' and duels", font_size=19, color=BELIEF),
                label(r"no one wants to deviate: \ an equilibrium", font_size=19, color=GAIN),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            box = RoundedRectangle(width=5.8, height=2.3, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.08)
            title = label(rf"everyone has {pool}", font_size=22, color=col).next_to(box, UP, buff=0.1)
            cards.add(VGroup(box, body.move_to(box), title))
        cards.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Cho and Kreps, \ QJE 102(2) (1987)", corner=DR, font_size=12)
        with self.voiceover(
            "The classic example is In-Koo Cho and David Kreps's. <bookmark mark='a'/> A newcomer walks into a "
            "tavern. Ninety percent of newcomers are strong, the rest weak. <bookmark mark='b'/> The strong "
            "prefer beer for breakfast, the weak prefer quiche. <bookmark mark='c'/> A bully watches the "
            "breakfast and decides whether to pick a fight. <bookmark mark='d'/> He wins only against the weak, "
            "and avoiding a fight is worth more to the newcomer than the breakfast. <bookmark mark='e'/> One "
            "equilibrium: everyone has beer, and the bully, who learns nothing, does not fight. If he ever saw "
            "quiche, he would believe the eater weak and fight, so nobody eats quiche. <bookmark mark='f'/> A "
            "second: everyone has quiche, and the bully believes that whoever has beer is weak, so the strong "
            "swallow their quiche too. Both satisfy every rule so far."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r_ in zip("abcd", setup):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
        self.clear_scene()

    def intuitive(self):
        Bq = load("beer")
        q = Bq["pools"]["quiche"]
        rows = VGroup(
            label(r"in the quiche equilibrium, \ who could gain by switching to beer?", font_size=24, color=WHITE),
            label(rf"the weak: \ at best {q['deviation_best']['weak']:.0f}, \ against {q['payoffs']['weak']:.0f} now: "
                  r"\ never", font_size=23, color=WEAK),
            label(rf"the strong: \ at best {q['deviation_best']['strong']:.0f}, \ against {q['payoffs']['strong']:.0f} "
                  r"now: \ possibly", font_size=23, color=STRONG),
            label(r"so a beer drinker must be strong; \ the bully should not fight", font_size=24, color=BELIEF),
            label(r"then the strong would switch: \ the quiche equilibrium fails the intuitive criterion",
                  font_size=24, color=ERR),
            label(r"the beer equilibrium survives: \ only the weak could gain from quiche, \ and they would be "
                  r"fought", font_size=22, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(UP * 0.1)
        with self.voiceover(
            "Cho and Kreps asked which off-path beliefs are reasonable. <bookmark mark='a'/> In the quiche "
            "equilibrium, who could possibly gain by switching to beer? <bookmark mark='b'/> Not the weak: even "
            f"without a fight, beer gives them {q['deviation_best']['weak']:.0f}, less than the "
            f"{q['payoffs']['weak']:.0f} they get now. <bookmark mark='c'/> The strong could: beer without a fight "
            f"would give them {q['deviation_best']['strong']:.0f}, more than {q['payoffs']['strong']:.0f}. "
            "<bookmark mark='d'/> So the only sensible reading of a beer is that the drinker is strong, and the "
            "bully should leave him alone. <bookmark mark='e'/> But then the strong would switch, and the quiche "
            "equilibrium falls apart: it fails what they called the intuitive criterion. <bookmark mark='f'/> The "
            "beer equilibrium survives. The same test picks out the least costly separating equilibrium of "
            "Spence's education signals in Part thirteen."
        ) as vo:
            for mk, r_ in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
