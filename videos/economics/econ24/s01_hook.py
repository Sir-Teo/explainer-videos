from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.taboo()
        self.equilibria()
        self.both()
        self.question()
        self.title()
        self.objectives()

    def taboo(self):
        trees = VGroup(*[palm(height=1.8) for _ in range(5)]).arrange(RIGHT, buff=1.0).move_to(UP * 0.6)
        rows = VGroup(
            label(r"Peter Diamond's island, \ 1982", font_size=28, color=E.ACCENT),
            label(r"coconuts grow on tall palms; \ a taboo forbids eating one you picked yourself", font_size=23,
                  color=GREY_A),
            label(r"so a coconut is worth climbing for only if you will meet someone else who climbed", font_size=23,
                  color=JOB),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Diamond, JPE 90(5) (1982): \ 881--894", corner=DR, font_size=12)
        with self.voiceover(
            "In 1982 Peter Diamond imagined an island. <bookmark mark='a'/> Coconuts grow on tall palm trees, and "
            "climbing one is hard work. A taboo forbids eating a coconut you picked yourself. You may only eat one "
            "you trade for. <bookmark mark='b'/> So climbing is worth the effort only if you expect to meet someone "
            "else who has climbed, someone to trade with."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in trees], lag_ratio=0.15), FadeIn(rows[0]),
                      FadeIn(tag), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def equilibria(self):
        d = load("diamond")
        ax = plane([0, 1], [0, 1], center=LEFT * 2.4 + DOWN * 0.3, x_length=5.4, y_length=5.0,
                   xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], xlabel=r"share expected to climb",
                   ylabel=r"share for whom climbing pays", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                   font_size=16)
        diag = seg(ax, 0, 0, 1, 1, color=GREY_B, width=2, dashed=True)
        curve = path(ax, d["e"], d["G"], color=JOB, width=4)
        eqs = VGroup(*[dot(ax, e, e, color=MATCH if k != 1 else HOLD, r=0.1) for k, e in enumerate(d["equilibria"])])
        side = VGroup(
            label(r"if few climb, \ few find partners, \\ so climbing does not pay", font_size=20, color=SEP),
            label(r"if most climb, \ partners are \\ easy to find, \ so it does", font_size=20, color=MATCH),
            label(rf"three equilibria: \ nobody, \\ {100 * d['equilibria'][1]:.0f}\% \ (unstable), \ "
                  rf"almost everyone", font_size=20, color=WHITE),
            label(r"the same island, \ the same people, \\ the same trees: \ a slump or a boom", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Draw it. Along the bottom, the share of islanders you expect to be climbing. Up the side, the share for "
            "whom climbing then pays. <bookmark mark='a'/> If few climb, partners are scarce, and climbing does not "
            "pay. <bookmark mark='b'/> If most climb, partners are easy to find, and it does. "
            "<bookmark mark='c'/> Where the curve meets the diagonal, expectations are self-fulfilling: nobody "
            "climbs; or almost everyone does; with an unstable point in between. <bookmark mark='d'/> The same "
            "island, the same people, the same trees, and either a slump or a boom. Diamond shared the Nobel prize in "
            "2010 with Dale Mortensen and Christopher Pissarides, for the theory of markets where people must search "
            "for each other."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), Create(curve), FadeIn(tag), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(e) for e in eqs], lag_ratio=0.3), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def both(self):
        b = load("beveridge")
        d, v = data.fred("JTSJOL"), data.fred("UNEMPLOY")
        jol = d["value"][-1]
        une = next(x for x in reversed(v["value"]) if np.isfinite(x))
        left = VGroup(label(r"job openings", font_size=26, color=JOB),
                      label(rf"{jol / 1000:.1f} million", font_size=48, color=JOB),
                      label(rf"{d['date'][-1][:7]}", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"unemployed people", font_size=26, color=WORKER),
                       label(rf"{une / 1000:.1f} million", font_size=48, color=WORKER),
                       label(rf"{v['date'][-1][:7]}", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=2.0).move_to(UP * 0.8)
        note_ = label(r"millions of people looking for work, \ and millions of jobs looking for people, \ at the same "
                      r"time", font_size=24, color=E.ACCENT).to_edge(DOWN, buff=1.4)
        tag = data_tag(rf"BLS, \ JOLTS and the Current Population Survey, \ via FRED \ (retrieved {data.fred('JTSJOL')['retrieved']})",
                       corner=DR, font_size=12)
        with self.voiceover(
            "Real labour markets look like that island. <bookmark mark='a'/> In the latest American figures, firms "
            f"were advertising about {jol / 1000:.1f} million job openings. <bookmark mark='b'/> At the same time, "
            f"about {une / 1000:.1f} million people were unemployed and looking for work. <bookmark mark='c'/> In a "
            "frictionless market of Part two's kind, one of those numbers would be zero: the price would clear the "
            "market. Here both are large at once, every month."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        del b
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how should someone looking for work decide which offer to take?", font_size=26, color=WORKER),
            label(r"how do workers and jobs meet, \ and what sets the wage when they do?", font_size=26, color=WAGE),
            label(r"and why does unemployment swing so much more than the theory says?", font_size=26, color=SEP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: why are there unemployed workers and unfilled jobs at the same time? "
            "<bookmark mark='a'/> How should someone looking for work decide which offer to take? "
            "<bookmark mark='b'/> How do workers and jobs meet, and what sets the wage when they do? "
            "<bookmark mark='c'/> And why does unemployment swing so much more than the theory says it should?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        b = load("beveridge")
        mini = plane([3, 15], [1.5, 7.5], x_length=4.2, y_length=1.6)
        logo = path(mini, b["u"], b["v"], color=TIGHT, width=3, smooth=False)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 24 \ $\cdot$ \ Looking for Work", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty-four: looking for work."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act V \ $\cdot$ \ The Long Run", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"stocks and flows: \ millions of hires and separations every month",
            r"search: \ your stopping rule against the reservation wage",
            r"the Beveridge curve; \ the matching function; \ the DMP model derived",
            r"bargaining, \ efficiency and the Hosios condition; \ the volatility puzzle",
            r"ins and outs; \ job ladders; \ the natural rate; \ dials; \ online vacancies",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part closes Act Five. <bookmark mark='a'/> You'll see how many jobs begin and end in a quiet "
            "month. <bookmark mark='b'/> You'll play a search game and compare your stopping rule with the best "
            "one. <bookmark mark='c'/> You'll draw the Beveridge curve from American data, estimate the matching "
            "function, and derive the model that central banks use for the labour market. "
            "<bookmark mark='d'/> Then how wages are bargained, when the market creates the right number of jobs, "
            "and why the model's unemployment barely moves. <bookmark mark='e'/> And what drives unemployment over "
            "the cycle, how workers climb job ladders, the natural rate, two dials, and the new data from job "
            "boards."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
