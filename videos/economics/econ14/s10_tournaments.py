from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Tournaments(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Tournaments and promotions", r"Why is the boss paid so much more than the deputies, \ and "
             r"what does it do to the deputies?", "Chapter eight. Tournaments and promotions.",
             lit={1981: r"Lazear and Rosen", 1986: r"Rosen's ladders", 1990: r"Ehrenberg and Bognanno",
                  1996: r"Brown, Harlow and Starks"},
             scale=("person", "firm"), horizon=("a career",))
        self.ladder()
        self.curves()
        self.evidence()

    def ladder(self):
        widths = [2.2, 3.0, 4.4, 6.4]
        names = [r"chief executive", r"vice presidents", r"managers", r"staff"]
        pays = [r"pay $\times$ 3", r"pay $\times$ 1.5", r"pay $\times$ 1.3", r"pay"]
        steps = VGroup()
        for i, (w, nm, pay) in enumerate(zip(widths, names, pays)):
            box = Rectangle(width=w, height=0.8, stroke_color=TEAM, stroke_width=2.5, fill_color=TEAM,
                            fill_opacity=0.12 + 0.08 * (3 - i))
            t = label(nm, font_size=19).move_to(box)
            p = label(pay, font_size=17, color=PAY).next_to(box, RIGHT, buff=0.25)
            steps.add(VGroup(box, t, p))
        steps.arrange(DOWN, buff=0.12).move_to(LEFT * 2.8 + DOWN * 0.2)
        arrow = Arrow(steps[1].get_left() + LEFT * 0.3, steps[0].get_left() + LEFT * 0.3, buff=0.05, color=E.ACCENT,
                      stroke_width=4).shift(LEFT * 0.4)
        side = VGroup(
            label(r"pay jumps at each step up, \\ most at the top", font_size=22, color=PAY),
            label(r"the chief executive's pay \\ is not a wage for a harder job", font_size=22),
            label(r"it is a prize, \ and the vice presidents \\ are the contestants", font_size=22, color=E.ACCENT),
            label(r"only the order is needed: \\ who did better, \ not by how much", font_size=22, color=SIGNAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.35)
        tag = illustrative_tag(r"illustrative pay ratios", corner=DR, font_size=13)
        with self.voiceover(
            "Firms pay people in a second way: by promotion. <bookmark mark='a'/> Pay jumps at each step up the "
            "ladder, and most at the top. A chief executive is often paid several times as much as the vice "
            "presidents below, though the job can hardly be several times harder. <bookmark mark='b'/> In 1981 "
            "Edward Lazear and Sherwin Rosen proposed that the top pay is not a wage for the job at all. "
            "<bookmark mark='c'/> It is a prize, and the vice presidents are the contestants. Whoever does best wins "
            "it, and the size of the prize is what makes them try. <bookmark mark='d'/> A tournament needs only the "
            "order, who did better, not by how much, which is often all a firm can judge."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in reversed(steps)], lag_ratio=0.3),
                      FadeIn(side[0]), FadeIn(tag), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def curves(self):
        t = load("tournament")
        sp, e, en = np.array(t["spread"]), np.array(t["effort"]), np.array(t["effort_noisy"])
        ax = plane([0, sp[-1]], [0, max(e) * 1.1], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=list(np.linspace(0, sp[-1], 5)), yticks=list(np.linspace(0, max(e), 3)),
                   xlabel=r"the prize: \ winner's pay less loser's", ylabel=r"each contestant's effort", font_size=16,
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        c1 = path(ax, sp, e, color=PAY, width=3.5, smooth=False)
        c2 = path(ax, sp, en, color=RISK, width=3.5, smooth=False)
        l1 = label(r"performance shows skill", font_size=16, color=PAY).next_to(a.c2p(sp[-1], e[-1]), LEFT,
                                                                                buff=0.15).shift(UP * 0.2)
        l2 = label(r"twice as much luck", font_size=16, color=RISK).next_to(a.c2p(3.0, en[60]), DOWN, buff=0.3)
        side = VGroup(
            label(r"two contestants, \ each with luck; \\ the better result wins", font_size=21),
            label(r"effort rises with the gap between the prizes, \\ not with the pay level", font_size=21,
                  color=PAY),
            label(r"more luck: \ effort counts for less \\ in who wins, \ so less effort", font_size=21, color=RISK),
            label(r"so the gap must be wider \\ where luck matters more", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Lazear and Rosen, JPE 89(5) (1981); \ Rosen, AER 76(4) (1986); \ the curves: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "Agora has Lazear and Rosen's model. <bookmark mark='a'/> Two contestants, each with luck; the better "
            "result wins. Each extra unit of effort raises the chance of winning a little, and that chance times the "
            "prize is what effort earns. <bookmark mark='b'/> So effort rises in proportion to the gap between the "
            "winner's pay and the loser's, and has nothing to do with the level of pay: raise everyone's pay by the "
            "same amount, and nobody works harder. <bookmark mark='c'/> With twice as much luck, effort counts for "
            "half as much in who wins, and contestants put in half the effort. <bookmark mark='d'/> So the prize "
            "must be wider where luck matters more. And in 1986 Rosen showed that it should widen sharply at the top of "
            "a firm, because the winner there has no further rungs to compete for."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            self.play(Create(c1), FadeIn(l1), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(c1, color=PAY))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(l2), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def evidence(self):
        c1 = study_card(r"Professional golf", r"Ronald Ehrenberg and Michael Bognanno, \ 1990", [
            (r"varied", r"prize money from one tournament to the next"),
            (r"found", r"larger prizes, \ lower scores, \ most of all in the final rounds"),
        ], design="regression", width=6.2, font_size=21)
        c2 = study_card(r"Mutual funds", r"Keith Brown, \ W. V. Harlow and Laura Starks, \ 1996", [
            (r"the race", r"investors' money flows to the year's top funds"),
            (r"found", r"funds behind at midyear took on more risk in the second half"),
        ], design="regression", width=6.2, font_size=21)
        VGroup(c1, c2).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.9)
        rows = VGroup(
            label(r"the dark side: \ a contestant gains as much by pulling a rival down \ as by pushing up", font_size=22,
                  color=RISK),
            label(r"Lazear, \ 1989: \ where sabotage is easy, \ narrow the prizes", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Ehrenberg and Bognanno, JPE 98(6) (1990); \ Brown, Harlow and Starks, JF 51(1) (1996); "
                            r"\ Lazear, JPE 97(3) (1989)", corner=DR, font_size=12)
        with self.voiceover(
            "Two places where the tournament is on display. <bookmark mark='a'/> In professional golf, the prize "
            "money changes from one tournament to the next, and Ronald Ehrenberg and Michael Bognanno found that "
            "players scored better when there was more to win, most of all in the final rounds. "
            "<bookmark mark='b'/> Mutual funds run a race every year, because investors' money flows to the top "
            "performers. Keith Brown, Van Harlow and Laura Starks found that funds behind at midyear took on more "
            "risk in the second half: when you are losing a tournament, a gamble is cheap. "
            "<bookmark mark='c'/> And there is a dark side. In a tournament a contestant gains as much by pulling a "
            "rival down as by pushing themselves up. <bookmark mark='d'/> In 1989 Lazear argued that where "
            "sabotage is easy, a firm should narrow its prizes, and accept less effort for more cooperation."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
