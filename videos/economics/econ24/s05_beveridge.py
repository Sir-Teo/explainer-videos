from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403

SEG = ("#7EC8F5", "#F2C14E", "#F25F5C", "#7BD88F")


class Beveridge(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The Beveridge curve", r"When jobs are plentiful, \ are the unemployed few?",
             "Chapter four. The Beveridge curve.", lit={1944: r"Beveridge", 2015: r"Elsby, Michaels and Ratner"},
             scale=("market",), horizon=("years",))
        self.curve()
        self.read()
        self.landing()
        self.fact()

    def axes_(self, center=LEFT * 1.7 + DOWN * 0.3):
        return plane([3, 15], [1.5, 7.5], center=center, x_length=8.0, y_length=5.2, xticks=[3, 5, 7, 9, 11, 13, 15],
                     yticks=[2, 3, 4, 5, 6, 7], xlabel=r"unemployment rate, \ \%", ylabel=r"job openings rate, \ \%",
                     xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)

    def curve(self):
        b = load("beveridge")
        ax = self.axes_()
        segs = VGroup()
        side = VGroup()
        for s_, c in zip(b["segments"], SEG):
            segs.add(VGroup(path(ax, s_["u"], s_["v"], color=c, width=3, smooth=False),
                            *[dot(ax, x, y, color=c, r=0.035) for x, y in zip(s_["u"], s_["v"])]))
            side.add(label(s_["name"], font_size=21, color=c))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
        last = dot(ax, b["last_u"], b["last_v"], color=WHITE, r=0.08)
        last_l = label(rf"{b['last'][:7]}", font_size=17, color=WHITE).next_to(last, RIGHT, buff=0.12)
        tag = data_tag(r"BLS: \ JOLTS openings and the CPS, \ via FRED; \ openings rate $= $ openings $\div$ "
                       r"(employment $+$ openings)", corner=DR, font_size=12)
        with self.voiceover(
            "In 1944 William Beveridge, the architect of Britain's welfare state, defined full employment as having "
            "more vacant jobs than unemployed people. Plot the two against each other. Along the bottom, the "
            "American unemployment rate; up the side, job openings as a share of all jobs, filled or not, month by "
            "month since the end of 2000. <bookmark mark='a'/> In the 2000s the points trace a downward-sloping "
            "curve: when openings are plentiful, unemployment is low. The recession of 2008 slides the economy down "
            "and to the right. <bookmark mark='b'/> The slow recovery of the 2010s climbs back up, but to the right "
            "of the old curve: for the same openings, more unemployment. <bookmark mark='c'/> Then the pandemic: "
            "unemployment leaps to almost fifteen percent in a single month, and comes back fast. "
            "<bookmark mark='d'/> And from mid 2021, openings soar to levels never recorded, with unemployment "
            f"below four percent. <bookmark mark='e'/> The latest point, {b['last'][:7]}: unemployment "
            f"{b['last_u']:.1f} percent, openings {b['last_v']:.1f}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            for mk, sg, sd in zip("abcd", segs, side):
                vo.wait_until(mk)
                self.play(Create(sg[0]), FadeIn(sg[1:]), FadeIn(sd), run_time=2.5)
            vo.wait_until("e")
            self.play(GrowFromCenter(last), FadeIn(last_l))
        self.clear_scene()

    def read(self):
        d = load("dmp")
        ax = plane([2.5, 6.5], [4.5, 10], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.4, y_length=5.0,
                   xticks=[3, 4, 5, 6], yticks=[5, 6, 7, 8, 9, 10], xlabel=r"unemployment, \ \%",
                   ylabel=r"vacancies, \ \% of the labour force", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=16)
        a, z = d["bev"]
        ca = path(ax, 100 * np.array(a["u"]), 100 * np.array(a["v"]), color=TIGHT, width=4)
        cz = path(ax, 100 * np.array(z["u"]), 100 * np.array(z["v"]), color=HOLD, width=4)
        mover = dot(ax, 100 * a["u"][20], 100 * a["v"][20], color=WHITE, r=0.09)
        side = VGroup(
            label(r"the Island's model \ (chapter 6), \\ productivity from $0.8$ to $1.2$", font_size=20, color=TIGHT),
            label(r"booms and slumps in demand \\ for workers: \ \emph{along} the curve", font_size=21, color=TIGHT),
            label(r"matching 20\% less efficient, \\ or more separations: \\ the curve \emph{shifts out}", font_size=21,
                  color=HOLD),
            label(r"2010--2019: \ mismatch? \ longer benefits? \\ firms recruiting less hard? \\ economists still "
                  r"argue", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Chapter six builds the model that explains the curve. Here is what it says, in advance. "
            "<bookmark mark='a'/> When productivity rises and falls, firms post more or fewer vacancies, and the "
            "economy slides along a downward-sloping curve. <bookmark mark='b'/> A boom moves it up and to the left; "
            "a slump, down and to the right. <bookmark mark='c'/> But if workers and jobs find each other less "
            "efficiently, or if more matches break up, the whole curve moves outward: more unemployment and more "
            "vacancies at the same time. <bookmark mark='d'/> Why the American curve moved out after 2009 is still "
            "argued: a mismatch between the skills and places of the unemployed and the jobs on offer; extended "
            "unemployment benefits; or firms recruiting less intensively for each opening. Bart Hobijn and Ayşegül "
            "Şahin, and Michael Elsby, Ryan Michaels and David Ratner, survey the debate."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(ca), run_time=1.5)
            vo.wait_until("a")
            self.play(GrowFromCenter(mover))
            vo.wait_until("b")
            self.play(mover.animate.move_to(ax.ax.c2p(100 * a["u"][40], 100 * a["v"][40])), FadeIn(side[1]),
                      run_time=1.2)
            self.play(mover.animate.move_to(ax.ax.c2p(100 * a["u"][0], 100 * a["v"][0])), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(cz), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def landing(self):
        b = load("beveridge")
        ax = self.axes_(center=LEFT * 2.2 + DOWN * 0.3)
        last = b["segments"][3]
        old = VGroup(*[path(ax, s_["u"], s_["v"], color=GREY_D, width=2, smooth=False) for s_ in b["segments"][:3]])
        now = path(ax, last["u"], last["v"], color=SEG[3], width=3, smooth=False)
        k = int(np.argmax(np.array(last["v"]) / np.array(last["u"])))
        peak = dot(ax, last["u"][k], last["v"][k], color=E.ACCENT, r=0.08)
        end = dot(ax, b["last_u"], b["last_v"], color=WHITE, r=0.08)
        side = VGroup(
            label(rf"{b['peak_when'][:7]}: \ openings per \\ unemployed worker {b['peak_vu']:.1f}", font_size=20,
                  color=E.ACCENT),
            label(r"2022: \ to bring inflation down, \\ must unemployment rise a lot?", font_size=20, color=GREY_A),
            label(r"Blanchard, \ Domash and Summers: \\ yes, \ the curve is flat", font_size=20, color=SEP),
            label(r"Figura and Waller: \\ no, \ it is steep up there", font_size=20, color=MATCH),
            label(rf"since: \ openings fell to {b['last_v']:.1f}\%, \\ unemployment rose to {b['last_u']:.1f}\%",
                  font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Blanchard, Domash and Summers, PIIE PB 22-7 (2022); \ Figura and Waller, FEDS Notes "
                            r"(29 July 2022)", corner=DR, font_size=12)
        with self.voiceover(
            "The curve became a forecasting argument in 2022. <bookmark mark='a'/> In "
            f"{b['peak_when'][:4]}, there were almost two openings for every unemployed worker, and inflation was "
            "the highest in forty years. <bookmark mark='b'/> Could the Federal Reserve cool the labour market "
            "without a big rise in unemployment? <bookmark mark='c'/> Olivier Blanchard, Alex Domash and Lawrence "
            "Summers argued no: the curve was flat, so fewer openings would mean many more unemployed. "
            "<bookmark mark='d'/> Andrew Figura and Christopher Waller, at the Federal Reserve, replied that the "
            "curve is steep when openings are so plentiful: firms could cut vacancies with few lost jobs. "
            "<bookmark mark='e'/> Since then, openings have fallen most of the way back while unemployment has "
            "risen by well under a point: so far, closer to Figura and Waller."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(old), Create(now), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(GrowFromCenter(peak), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(GrowFromCenter(end), FadeIn(side[4]))
        self.clear_scene()

    def fact(self):
        b = load("beveridge")
        d = load("dmp")
        f = next(x for x in facts.FACTS if x.key == "beveridge")
        data_m = label(rf"JOLTS, \ 2000--{b['last'][:4]}: \\ a downward curve, \ shifted \\ out after 2009 and in "
                       r"2021", font_size=19, color=WHITE)
        theory_m = label(r"flows balance: \ $u = s / (s + f)$; \\ $f$ rises with openings \\ per searcher",
                         font_size=19, color=TIGHT)
        agora_m = label(rf"the Island: \ {pc(d['steady']['u'])} \ unemployed \\ and {pc(d['steady']['v'])} \ "
                        r"vacancies \\ at once \ (chapter 6)", font_size=19, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, TIGHT, None)).move_to(UP * 0.3)
        tag = published_tag(r"Beveridge, \emph{Full Employment in a Free Society} (1944); \ Elsby, Michaels and "
                            r"Ratner, JEL 53(3) (2015)", corner=DR, font_size=12)
        with self.voiceover(
            "One of the series' facts. <bookmark mark='a'/> In the data, openings and unemployment move in "
            "opposite directions along a curve that sometimes shifts. <bookmark mark='b'/> In theory, the curve is "
            "where the flows into and out of unemployment balance, with job finding rising in openings per "
            "searcher. <bookmark mark='c'/> And Agora's Island, which chapter six builds, has both at once in a "
            "perfectly steady state."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()
