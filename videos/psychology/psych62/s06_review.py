from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Review(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Peer review, \ shown", r"What do reviewers ask, \ and how do you answer?")
        self.power()
        self.reviews()

    def power(self):
        d = load("power")
        head = heading(r"The design check, \ on simulated people")
        tr = np.asarray(d["true_rel"])
        tab = np.asarray(d["table"])
        A = axes([0.3, 4.7], [0, 1.0], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"share of simulated studies", center=[-3.3, 0.3, 0],
                 font_size=12)
        cols = [AUTH, GREY_B, GOOD]
        stacks = VGroup()
        for i in range(len(tr)):
            base = 0.0
            for j, c in enumerate(cols):
                h = float(tab[i, j])
                if h > 0:
                    r = Rectangle(width=0.6 * A.ax.x_axis.unit_size, height=h * A.ax.y_axis.unit_size,
                                  stroke_width=0, fill_color=c, fill_opacity=0.85)
                    r.move_to(A.ax.c2p(i + 1, base + h / 2))
                    stacks.add(r)
                base += h
        names = VGroup(*[label(rf"{t:.2f}", font_size=13, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1)
                         for i, t in enumerate(tr)])
        nl = label(r"true reliability", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        key = VGroup(label(r"H1 supported", font_size=13, color=AUTH), label(r"inconclusive", font_size=13, color=GREY_B),
                     label(r"H1 refuted", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.35)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"54 simulated people, \ 200 simulated studies at each true reliability, \ the registered rule applied",
             WHITE),
            (rf"if the truth is 0.4, \ the rule says ``supported'' {100 * tab[0, 0]:.0f}\% of the time; \ at 0.85, \ "
             rf"``refuted'' {100 * tab[3, 2]:.0f}\%", MODEL),
            (rf"near 0.7 it is almost always inconclusive ({100 * tab[2, 1]:.0f}\%): \ 54 people cannot pin a "
             rf"reliability to within a tenth", AUTH),
            (r"so the report must say in advance: \ an inconclusive result is a likely outcome, \ not a failure", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{thesis.power}")
        with self.voiceover(
            "Before review, the design check, run on simulated people from the Pool. <bookmark mark='a'/> Fifty-four "
            "simulated people, two hundred simulated studies at each true reliability, and the registered rule "
            "applied to each. <bookmark mark='b'/> If the truth is zero point four, the rule says supported about "
            "two thirds of the time. At zero point eight five, it says refuted about three quarters of the time. "
            "<bookmark mark='c'/> Near zero point seven it's almost always inconclusive. Fifty-four people can't "
            "pin a reliability down to within a tenth. <bookmark mark='d'/> So the report must say in advance that "
            "an inconclusive result is a likely outcome, not a failure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(nl), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(s_) for s_ in stacks], lag_ratio=0.1))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def reviews(self):
        chips_section(self, r"Three reviews, \ written for this film", [
            (r"reviewer 1", r"``The design cannot detect a reliability near 0.70.'' \ Response: agreed; the "
                            r"design check states it in advance", MODEL),
            (r"reviewer 2", r"``Why odd and even trials, \ and why a minimum of four per cell?'' \ Response: "
                            r"odd and even balance practice and fatigue; the minimum keeps slopes estimable", PERSON),
            (r"reviewer 3", r"``Report the mean time's reliability as a check that the data are not simply noisy.'' "
                            r"\ Response: that is H2", GOOD),
            (r"the editor", r"in-principle acceptance: \ the paper will be published whatever the result", YOU),
        ], "Now three reviews. They were written for this film, to show what a Stage 1 review asks, and the plan "
           "you saw already carries the answers. <bookmark mark='a'/> Reviewer one: the design can't detect a reliability near "
           "zero point seven. The response: agreed, and the design check states it, so an "
           "inconclusive result is expected, not explained away. <bookmark mark='b'/> Reviewer two: why odd and even trials, and why a minimum of four per "
           "cell? The response: odd and even trials balance practice and fatigue, and the minimum keeps the slopes "
           "estimable. <bookmark mark='c'/> Reviewer three: report the mean time's reliability, as a check that the "
           "data aren't simply noisy. The response: that's H2. <bookmark mark='d'/> And the editor gives "
           "in-principle acceptance: the paper will be published whatever the result.", chip_w=2.8, text_w=9.6)
