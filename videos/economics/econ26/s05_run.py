from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Two equilibria: \ the bank and the run", r"Can the same bank be sound and fail?",
             "Chapter four. Two equilibria: the bank and the run.", lit={1983: r"Diamond and Dybvig"},
             scale=("firm",), horizon=("a day",))
        self.table()
        self.line_up()
        self.sunspots()

    def table(self):
        d = load("dd")
        head = VGroup(label(r"", font_size=20), label(r"others stay", font_size=22, color=STAY),
                      label(r"others run", font_size=22, color=RUN))
        r1 = VGroup(label(r"you stay", font_size=22, color=STAY), MathTex(f"{d['c2']:.2f}", font_size=36, color=STAY),
                    MathTex("0", font_size=36, color=RUN))
        r2 = VGroup(label(r"you run", font_size=22, color=RUN), MathTex(f"{d['c1']:.2f}", font_size=36, color=GREY_A),
                    MathTex(rf"\text{{{d['c1']:.2f} with chance }}{d['served_in_run']:.2f}", font_size=30,
                            color=RUN))
        grid = VGroup(head, r1, r2)
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                cell.move_to([-3.6 + 3.6 * c, 1.8 - 1.2 * r, 0])
        box_good = SurroundingRectangle(r1[1], color=STAY, buff=0.2)
        box_run = SurroundingRectangle(r2[2], color=RUN, buff=0.2)
        rows = VGroup(
            label(r"if others stay, \ staying is best: \ the good equilibrium", font_size=23, color=STAY),
            label(r"if others run, \ running is best: \ the run", font_size=23, color=RUN),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.9)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Write down what a patient depositor gets. <bookmark mark='a'/> If everyone else waits, waiting pays "
            f"{d['c2']:.2f}, and withdrawing only {d['c1']:.2f}: so wait. That is the good equilibrium. "
            "<bookmark mark='b'/> If everyone else runs, the bank must sell every loan at one to pay "
            f"{d['c1']:.2f} each, and it can pay only {100 * d['served_in_run']:.0f} percent of the queue. Those who "
            "wait get nothing. So run. <bookmark mark='c'/> Both are equilibria. The same bank, with the same loans, "
            "is sound if people believe it is, and fails if they believe it will."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(box_good), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(box_run), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(rows, color=WHITE, scale_factor=1.02))
        self.clear_scene()

    def line_up(self):
        r = load("run")
        n = 40
        k = int(round(r["share_served"] * n))
        dots_ = VGroup(*[Dot(radius=0.11, color=GREY_B) for _ in range(n)]).arrange_in_grid(rows=4, cols=10,
                                                                                            buff=0.35)
        dots_.move_to(UP * 0.6)
        door = label(r"the bank's door", font_size=20, color=GREY_A).next_to(dots_, LEFT, buff=0.5)
        rows = VGroup(
            label(rf"sequential service: \ paid in order of arrival, \ {r['c1']:.2f} each, \ until the cash is gone",
                  font_size=22, color=GREY_A),
            label(rf"{r['served']} of {r['asked']} are paid in full; \ the rest get nothing", font_size=24,
                  color=RUN),
            label(r"so being early is everything, \ and waiting to see is the worst choice", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The run is made worse by a rule of banking: first come, first served. <bookmark mark='a'/> In a run, "
            f"the bank pays {r['c1']:.2f} to each depositor in the order they arrive, until the money runs out. "
            f"<bookmark mark='b'/> On the Island, {r['served']} of {r['asked']} depositors are paid in full and the "
            "rest get nothing. <bookmark mark='c'/> So being early is everything, and waiting to see what happens "
            "is the worst thing you can do. That is why a run, once it starts, is fast."
        ) as vo:
            self.play(FadeIn(dots_), FadeIn(door), FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[d_.animate.set_color(STAY) for d_ in dots_[:k]], lag_ratio=0.08), run_time=3)
            vo.wait_until("b")
            self.play(*[d_.animate.set_color(RUN) for d_ in dots_[k:]], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def sunspots(self):
        rows = VGroup(
            label(r"what decides which equilibrium happens?", font_size=27, color=E.ACCENT),
            label(r"in the model, \ anything people treat as a signal: \ a \emph{sunspot}", font_size=23,
                  color=GREY_A),
            label(r"a rumour, \ a queue outside a branch, \ a falling share price, \ a post that goes viral",
                  font_size=23, color=RUN),
            label(r"so runs can hit sound banks; \ and weak banks are more exposed, \ because less news can tip them",
                  font_size=22, color=GREY_A),
            label(r"chapter 10 shows how a refinement picks one equilibrium after all", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "What decides which one happens? <bookmark mark='a'/> In the model, nothing about the bank: any event "
            "people treat as a signal will do. Economists call it a sunspot. <bookmark mark='b'/> In life: a rumour, "
            "a queue outside a branch, a falling share price, a post that spreads. <bookmark mark='c'/> So runs can "
            "hit sound banks. But weak banks are more exposed, because less bad news is needed to tip them over. "
            "<bookmark mark='d'/> Chapter ten shows how a refinement of the model picks one equilibrium after all."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
