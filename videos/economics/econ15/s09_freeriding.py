from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403


class FreeRiding(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Free riding measured", r"When people play the shared pot again and again, \ what happens, \ and "
             r"what keeps them giving?", "Chapter seven. Free riding measured.",
             lit={1995: r"Ledyard", 2000: r"Fehr and Gächter", 2001: r"conditional cooperators",
                  2008: r"antisocial punishment"}, scale=("person", "community"), horizon=("a day",))
        self.types()
        self.rounds()
        self.cities()

    def types(self):
        rows = VGroup(
            label(r"on a first play, \ people put in about half: \ more than theory's nothing, \ less than "
                  r"everything", font_size=23),
            label(r"Urs Fischbacher, \ Simon Gächter and Ernst Fehr, \ 2001: \ ask people what they'd give \ "
                  r"for each amount the others give", font_size=22, color=GREY_A),
            label(r"about half are conditional cooperators: \ they give more when others give more", font_size=24,
                  color=GOOD),
            label(r"about a third are free riders: \ they give nothing whatever others do", font_size=24,
                  color=SOCIAL),
            label(r"and conditional cooperators match others a little less than fully", font_size=24, color=DEMAND),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Ledyard (1995); \ Fischbacher, Gächter and Fehr, Economics Letters 71(3) (2001)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Chapter one's game has been played in laboratories thousands of times. <bookmark mark='a'/> On a first "
            "play, people put in about half: more than the nothing that self-interest predicts, and less than the "
            "everything that would be best for the group. <bookmark mark='b'/> In 2001 Urs Fischbacher, Simon "
            "Gächter and Ernst Fehr asked people how much they would give for each amount the others might give. "
            "<bookmark mark='c'/> About half were conditional cooperators: they gave more when others gave more. "
            "<bookmark mark='d'/> About a third were free riders, and gave nothing whatever the others did. "
            "<bookmark mark='e'/> And the conditional cooperators matched the others a little less than fully. That "
            "small shortfall is enough to unravel a group, round by round."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def rounds(self):
        v = load("vcm")
        rd = np.array(v["rounds"])
        ax = plane([0.5, 10.5], [0, 0.85], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4, y_length=4.6,
                   xticks=list(range(1, 11)), yticks=[0, 0.2, 0.4, 0.6, 0.8], xlabel=r"round",
                   ylabel=r"share of shells put in the pot", font_size=16, xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{100 * y:.0f}\\%")
        a = ax.ax
        c1 = path(ax, rd, v["plain"], color=SOCIAL, width=3.5, smooth=False)
        c2 = path(ax, rd, v["punish"], color=GOOD, width=3.5, smooth=False)
        d1 = VGroup(*[Dot(a.c2p(x, y), radius=0.05, color=SOCIAL) for x, y in zip(rd, v["plain"])])
        d2 = VGroup(*[Dot(a.c2p(x, y), radius=0.05, color=GOOD) for x, y in zip(rd, v["punish"])])
        l1 = label(r"no punishment", font_size=15, color=SOCIAL).next_to(a.c2p(10, v["plain"][-1]), DOWN, buff=0.15,
                                                                          aligned_edge=RIGHT)
        l2 = label(r"punishment allowed", font_size=15, color=GOOD).next_to(a.c2p(10, v["punish"][-1]), UP, buff=0.15,
                                                                             aligned_edge=RIGHT)
        side = VGroup(
            label(rf"Agora's players: \ half conditional cooperators, \\ a third free riders, \ in groups of "
                  rf"{v['n']}", font_size=20),
            label(r"the free riders give nothing; \\ the cooperators match a little less each round; \\ giving decays",
                  font_size=20, color=SOCIAL),
            label(r"now let anyone pay a shell \\ to take three from someone else", font_size=20, color=GOOD),
            label(r"cooperators punish the free riders, \\ who learn; \ giving rises, \\ and so, \ in time, do "
                  r"earnings", font_size=20, color=GOOD),
            label(r"Ernst Fehr and Simon Gächter, \ 2000: \\ the same in the laboratory; \ in fixed groups, \\ close "
                  r"to full cooperation", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Fehr and Gächter, AER 90(4) (2000); \ the curves: \ Agora's typed players, \ simulated",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Here is what that does, played out by Agora's typed players, in four hundred groups of four. "
            "<bookmark mark='a'/> Half are conditional cooperators and a third free riders. <bookmark mark='b'/> The "
            "free riders give nothing, the cooperators match a little less than the others gave last round, and "
            "giving decays, round after round, toward a sixth of the shells. Laboratory groups decay in just this "
            "way. <bookmark mark='c'/> Now change one rule: after each round, anyone may pay a shell to take three "
            "from someone else. Punishing costs the punisher, so self-interest says nobody will. "
            "<bookmark mark='d'/> But cooperators do punish, the free riders learn, and giving rises instead of "
            "falling. After a few rounds, earnings are higher too, punishment's cost included. "
            "<bookmark mark='e'/> In 2000 Ernst Fehr and Simon Gächter found the same with real players: with "
            "punishment allowed, cooperation rose, and in groups that stayed together, came close to complete."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c1), LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.1), FadeIn(l1), FadeIn(side[1]),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(c2), LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.1), FadeIn(l2), FadeIn(side[3]),
                      run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def cities(self):
        rows = VGroup(
            label(r"Benedikt Herrmann, \ Christian Thöni and Simon Gächter, \ 2008: \ the same game in sixteen cities",
                  font_size=22),
            label(r"in some, \ punishment fell on free riders, \ and cooperation rose", font_size=24, color=GOOD),
            label(r"in others, \ free riders punished the cooperators back: \ antisocial punishment", font_size=24,
                  color=SOCIAL),
            label(r"and there punishment did little good", font_size=24, color=SOCIAL),
            label(r"what sustains a public good is not punishment itself, \ but the norms behind who gets punished",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Herrmann, Thöni and Gächter, Science 319 (2008)", corner=DR, font_size=13)
        with self.voiceover(
            "There is a twist. <bookmark mark='a'/> In 2008 Benedikt Herrmann, Christian Thöni and Simon Gächter ran "
            "the game with punishment in sixteen cities around the world. <bookmark mark='b'/> In some, punishment "
            "fell on the free riders, and cooperation rose. <bookmark mark='c'/> In others, people who "
            "had been punished for free riding punished the cooperators in return, and some punished cooperators "
            "outright: antisocial punishment. <bookmark mark='d'/> Where that was common, punishment did little to "
            "help. <bookmark mark='e'/> What sustains a public good is not the power to punish, but the norms that "
            "decide who gets punished. Chapter eight finds the same in the commons."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
