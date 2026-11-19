from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 12, r"In practice: \ who evaluates for a living", r"Who turns data into evidence, and how do "
             r"they plan a test before they run it?", "Chapter twelve. In practice: who evaluates for a living.",
             lit=("government", "firms"), scale=("person", "firm", "nation"), horizon=("a year",))
        self.jobs()
        self.plan()
        self.power()

    def jobs(self):
        head = VGroup(heading(r"In practice"),
                      label(r"who turns data into evidence for a living", font_size=26, color=GREY_B))
        head[1].next_to(head[0], DOWN, buff=0.2)
        items = [
            (r"evaluation firms", r"MDRC was founded in 1974 to run Supported Work; \ it and others still run "
                                  r"the government's trials", EXP),
            (r"development labs", r"J-PAL and Innovations for Poverty Action: \ hundreds of field trials, \ in "
                                  r"dozens of countries", "#7BD88F"),
            (r"government units", r"evaluation offices and ``what works'' centres: \ is the programme worth "
                                  r"its budget?", E.GOVERNMENT),
            (r"experimentation teams", r"at online firms: \ thousands of A/B tests a year, \ with platforms "
                                       r"that warn against peeking", E.ACCENT),
            (r"expert witnesses", r"in discrimination, antitrust and damages cases: \ a regression, \ "
                                  r"cross-examined \ (Part 59)", E.OUGHT),
            (r"central bank researchers", r"identifying the effect of an interest-rate change \ when every change "
                                          r"is a choice \ (Part 55)", E.WORLD),
        ]
        pc = point_cards(items, width=12.8, cols=2, font_size=23).move_to(DOWN * 0.55)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Evaluation firms. MDRC was founded in 1974 to run the "
            "Supported Work demonstration, the experiment behind LaLonde's test, and firms like it still run many "
            "of the government's trials. <bookmark mark='b'/> Development labs such as J-PAL and Innovations for "
            "Poverty Action, which have run field trials in dozens of countries. <bookmark mark='c'/> Evaluation "
            "offices inside governments, which ask whether a programme is worth its budget. "
            "<bookmark mark='d'/> Experimentation teams at online firms, running thousands of controlled experiments "
            "a year, on platforms built to stop engineers from stopping a test the moment it looks good. "
            "<bookmark mark='e'/> Expert witnesses, whose regressions are cross-examined in discrimination, "
            "antitrust and damages cases. <bookmark mark='f'/> And researchers at central banks, who must identify "
            "the effect of an interest-rate change when every change is a deliberate choice. Part 55 is theirs."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c_ in zip("abcdef", pc.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
        self.clear_scene()

    def plan(self):
        steps = flow_chain([(r"the question, \ and the one number that answers it", E.ACCENT),
                            (r"power: \ how many people?", "#7BD88F"),
                            (r"a plan, \ registered before the data", GREY_A),
                            (r"randomize; \ check balance", EXP),
                            (r"run it; \ count who drops out", "#F2B84B"),
                            (r"analyse as planned; \ report everything", E.TRUTH)],
                           direction=DOWN, box_w=5.0, box_h=0.62, buff=0.22, font_size=21,
                           notes=[r"the effect of the offer, or of taking it up?",
                                  r"the next scene",
                                  r"the outcome, the comparison, the controls: \ no forking paths",
                                  r"a table of everything measured before",
                                  r"attrition that differs by group breaks the lottery",
                                  r"and every outcome, including the dull ones"], note_size=18)
        steps.move_to(LEFT * 1.6)
        tag = published_tag(r"AEA RCT Registry (2013--); Olken, JEP 29(3) (2015); Duflo, Glennerster and Kremer, "
                            r"\emph{Handbook of Development Economics} 4 (2007)", corner=DR, font_size=12)
        with self.voiceover(
            "Here is how a trial is planned, step by step. <bookmark mark='a'/> First the question, and the one "
            "number that will answer it. The effect of offering the apprenticeship is not the effect of taking it "
            "up, and the plan must say which. <bookmark mark='b'/> Then the size: enough people to see the effect "
            "if it's there. <bookmark mark='c'/> Then a plan written and registered before any data arrive: the "
            "outcome, the comparison, the controls. Since 2013 economists register their trials with the American "
            "Economic Association. Leamer's complaint was about choices made after seeing the data; a plan takes "
            "them away. <bookmark mark='d'/> Randomize, and check that the groups are alike on everything measured "
            "beforehand. <bookmark mark='e'/> Run it, and count who drops out: if the losers of the lottery leave "
            "more often than the winners, the lottery is broken again. <bookmark mark='f'/> And analyse as planned, "
            "reporting every outcome, the dull ones included."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                anims = [FadeIn(steps.boxes[k], shift=RIGHT * 0.2), FadeIn(steps.notes[k])]
                if k:
                    anims.append(GrowArrow(steps.arrows[k - 1]))
                self.play(*anims)
        self.clear_scene()

    def power(self):
        pw = load("power")
        N = np.array(pw["N"], float)
        mde = np.array(pw["mde"])
        ax = axes([2, 4.3], [0, 0.3], x_length=6.4, y_length=4.4, xticks=[2, 3, 4], yticks=[0, 0.1, 0.2, 0.3],
                  xfmt=lambda v: {2: "100", 3: "1{,}000", 4: "10{,}000"}[int(v)], xlabel=r"islanders in the trial",
                  ylabel=r"smallest effect it can reliably detect", font_size=19, center=LEFT * 2.8 + DOWN * 0.3)
        a = ax.ax
        curve = VMobject(stroke_color="#7BD88F", stroke_width=4).set_points_smoothly(
            [a.c2p(np.log10(n), m) for n, m in zip(N, mde)])
        eff = DashedLine(a.c2p(2, pw["effect"]), a.c2p(4.3, pw["effect"]), color=E.TRUTH, stroke_width=2.5)
        el = label(rf"the planted effect, \ {pw['effect']:.2f}", font_size=19, color=E.TRUTH).next_to(
            a.c2p(4.3, pw["effect"]), UP, buff=0.08).shift(LEFT * 1.0)
        nx = np.log10(pw["n_needed"])
        need = VGroup(DashedLine(a.c2p(nx, 0), a.c2p(nx, pw["effect"]), color=GREY_B, stroke_width=2),
                      Dot(a.c2p(nx, pw["effect"]), radius=0.08, color=WHITE))
        nl = label(rf"about {round(pw['n_needed'], -1):,.0f}".replace(",", "{,}"), font_size=19, color=WHITE).next_to(
            a.c2p(nx, 0), UP, buff=0.12).shift(RIGHT * 0.55)
        ours = Dot(a.c2p(np.log10(1600), float(np.interp(1600, N, mde))), radius=0.09, color=EXP)
        rows = VGroup(
            MathTex(r"\text{MDE} = (z_{.975} + z_{.80})\,\frac{\sigma}{\sqrt{p(1-p)\,N}}", font_size=34),
            label(rf"$\sigma = {pw['sigma']:.2f}$: \ the spread of log earnings; \ $p = 1/2$ treated", font_size=21,
                  color=GREY_A),
            label(rf"400 islanders: \ power {100 * pw['sim_power']['400']:.0f}\% \ (simulated)", font_size=22,
                  color="#7BD88F"),
            label(rf"1{{,}}600, \ the trial we ran: \ power {100 * pw['sim_power']['1600']:.0f}\%", font_size=22,
                  color=EXP),
            label(r"four times the people \\ to see an effect half the size", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        tag = island_tag(r"simulated: the apprenticeship trial, 400 draws at each size", corner=DR, font_size=13)
        with self.voiceover(
            "The second step deserves a picture. <bookmark mark='a'/> The smallest effect a trial can reliably "
            "detect shrinks with the square root of its size. Reliably means: with a five percent false-alarm "
            "rate, it finds a real effect of that size four times in five. <bookmark mark='b'/> On the Island, "
            f"earnings vary with a spread of about {pw['sigma']:.2f} in logs, and half the people are offered the "
            "apprenticeship. <bookmark mark='c'/> To detect its planted ten percent you need about "
            f"{round(pw['n_needed'], -1):.0f} islanders. <bookmark mark='d'/> With four hundred, a simulation finds "
            f"it {100 * pw['sim_power']['400']:.0f} times in a hundred. With the sixteen hundred we used, almost "
            "always. <bookmark mark='e'/> The square root is a hard master: to see an effect half the size, you "
            "need four times as many people. Many published trials were too small to see the effects they were "
            "looking for, which is one reason their findings so often fail to repeat."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(curve, run_time=2.0))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(eff), FadeIn(el), Create(need[0]), FadeIn(need[1], scale=1.5), FadeIn(nl))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(ours, scale=1.5), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
