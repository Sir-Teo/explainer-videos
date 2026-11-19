from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Wages(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Efficiency wages", r"Why would a firm pay more than it must, \ and what does that do to "
             r"unemployment?", "Chapter ten. Efficiency wages.",
             lit={1914: r"Ford's five-dollar day", 1982: r"Akerlof's gift exchange", 1984: r"Shapiro and Stiglitz",
                  1987: r"Raff and Summers"},
             scale=("person", "economy"), horizon=("a year", "a decade"))
        self.ford()
        self.model()
        self.gifts()

    def ford(self):
        ic = tables.INCENTIVE_CASES.data
        hc = history_card(1914, r"the Ford Motor Company, \ Highland Park, \ Michigan", r"five dollars for an "
                          r"eight-hour day", color=PAY, width=11.0, font_size=25).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"roughly double what most of its workers had been earning", font_size=24, color=PAY),
            label(r"the assembly line: \ dull, \ fast work, \ and workers who quit or stayed away", font_size=23),
            label(r"crowds of job seekers at the gates the day after it was announced", font_size=23, color=SIGNAL),
            label(r"Daniel Raff and Lawrence Summers, \ 1987: \ long queues for Ford jobs, \ and productivity and "
                  r"profits rose", font_size=22, color=E.ACCENT),
            label(r"Ford, \ later: \ ``one of the finest cost-cutting moves we ever made''", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.36).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Raff and Summers, JOLE 5(4) (1987)", corner=DR, font_size=13)
        with self.voiceover(
            "In January 1914 the Ford Motor Company announced that it would pay five dollars for an eight-hour day. "
            "<bookmark mark='a'/> That was roughly double what most of its workers had been earning, and far more "
            "than other factories paid. <bookmark mark='b'/> Ford's new assembly line made work dull and fast, and "
            "workers quit, or simply didn't turn up. <bookmark mark='c'/> The day after the announcement, crowds of "
            "job seekers gathered at the factory gates. <bookmark mark='d'/> In 1987 Daniel Raff and Lawrence Summers "
            "went through the records. They found long queues for Ford jobs, which a wage that merely cleared the "
            "market would not produce, and they found that productivity and profits rose. "
            "<bookmark mark='e'/> Ford himself is quoted as calling it one of the finest cost-cutting moves the "
            "company ever made."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def model(self):
        s = load("shirking")
        L, nsc, dem = np.array(s["L"]), np.array(s["nsc"]), np.array(s["demand"])
        lab = s["labour"]
        ax = plane([0, 105], [0, 7], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 2, 4, 6], xlabel=r"workers employed, \ of 100",
                   ylabel=r"wage", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        cn = path(ax, L, nsc, color=RISK, width=3.5, yr=(0, 7))
        cd = path(ax, L, dem, color=SIGNAL, width=3.5)
        full = seg(ax, lab, 0, lab, 7, color=GREY_B, width=1.5, dashed=True)
        fl = label(r"everyone \\ employed", font_size=14, color=GREY_B).next_to(a.c2p(lab, 6.6), RIGHT, buff=0.05)
        ln = label(r"the wage that stops shirking", font_size=15, color=RISK).next_to(a.c2p(40, nsc[160]), DOWN,
                                                                                      buff=0.15)
        ld = label(r"what firms will pay \\ for that many workers", font_size=15, color=SIGNAL).next_to(
            a.c2p(45, 6 - 0.04 * 45), UR, buff=0.1)
        eq = Dot(a.c2p(s["L_eq"], s["w_eq"]), radius=0.09, color=E.ACCENT)
        gap = DoubleArrow(a.c2p(s["L_eq"], 0.5), a.c2p(lab, 0.5), buff=0, color=E.ACCENT, stroke_width=3,
                          tip_length=0.15)
        gl = label(rf"{100 * s['u_eq']:.0f} unemployed", font_size=15, color=E.ACCENT).next_to(gap, UP, buff=0.08)
        side = VGroup(
            label(r"a worker who shirks may be caught, \\ and fired", font_size=21),
            label(r"being fired hurts only if the job pays more \\ than what the worker would get without it",
                  font_size=21, color=RISK),
            label(r"the fewer the unemployed, \ the quicker a new job: \\ so the higher the wage must be", font_size=21,
                  color=RISK),
            label(r"in equilibrium some are left without work: \\ unemployment as a discipline device", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Shapiro and Stiglitz, AER 74(3) (1984); \ the curves: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "Why would a wage above the market's raise profits? Carl Shapiro and Joseph Stiglitz gave one answer in "
            "1984. <bookmark mark='a'/> A worker who shirks may be caught, and fired. <bookmark mark='b'/> But being "
            "fired is a punishment only if the job pays more than the worker could get without it. If every job "
            "paid the market wage, and another was easy to find, losing one would cost nothing. "
            "<bookmark mark='c'/> So firms pay more than the market wage, and how much more depends on how quickly a "
            "fired worker would find another job: the fewer the unemployed, the higher the wage that keeps workers "
            "honest. As employment nears everyone, it rises without limit. <bookmark mark='d'/> Where it meets what "
            "firms will pay, some workers are left without jobs. They would gladly work for less, but no firm will "
            "hire them for less, because at a lower wage it couldn't trust them to work. Shapiro and Stiglitz called "
            "it unemployment as a worker discipline device."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(full), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cn), FadeIn(ln), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(Create(cd), FadeIn(ld), run_time=1.5)
            self.play(FadeIn(eq, scale=1.5), GrowFromCenter(gap), FadeIn(gl), FadeIn(side[3]))
        self.clear_scene()

    def gifts(self):
        rows = VGroup(
            label(r"other reasons to pay more:", font_size=26, color=E.ACCENT),
            label(r"fewer quits, \ so less spent hiring and training", font_size=23, color=PAY),
            label(r"better applicants, \ since the able have better options", font_size=23, color=SIGNAL),
            label(r"George Akerlof, \ 1982: \ a gift exchange, \ more than the market wage repaid with more than the "
                  r"minimum effort", font_size=22, color=EFFORT),
            label(r"in the laboratory: \ Fehr, \ Kirchsteiger and Riedl, \ 1993: \ higher wages, \ more effort",
                  font_size=22, color=GREY_A),
            label(r"in the field: \ Gneezy and List, \ 2006: \ the extra effort faded within hours", font_size=22,
                  color=RISK),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.1)
        tag = published_tag(r"Akerlof, QJE 97(4) (1982); \ Fehr, Kirchsteiger and Riedl, QJE 108(2) (1993); \ Gneezy "
                            r"and List, Econometrica 74(5) (2006)", corner=DR, font_size=12)
        with self.voiceover(
            "Shirking is not the only reason. <bookmark mark='a'/> There are others. <bookmark mark='b'/> A better-paid "
            "worker quits less, which saves the cost of hiring and training a replacement; that was Ford's problem. "
            "<bookmark mark='c'/> A better wage attracts better applicants, since able people have better options. "
            "<bookmark mark='d'/> And in 1982 George Akerlof proposed that employment is partly a gift exchange: a "
            "firm that pays more than it must is repaid with more than the minimum effort. "
            "<bookmark mark='e'/> In the laboratory, Ernst Fehr, Georg Kirchsteiger and Arno Riedl found just that: "
            "players in the role of employers offered generous wages, and players in the role of workers answered "
            "with more effort. <bookmark mark='f'/> In the field, Uri Gneezy and John List hired people for a day's "
            "work, some at a higher wage than advertised. The better-paid worked harder at first, but within hours "
            "the difference was gone. Reciprocity is real, but how long it lasts is an open question."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
