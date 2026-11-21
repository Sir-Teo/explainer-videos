from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.payments()
        self.poverty()
        self.request()
        self.question()
        self.title()
        self.objectives()

    def payments(self):
        T = tables.CTC_2021.data
        months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"]
        coins = VGroup()
        for i, m in enumerate(months):
            paid = i < 6
            box = RoundedRectangle(width=1.3, height=1.3, corner_radius=0.14, stroke_color=NEW if paid else GREY_B,
                                   stroke_width=2.2, fill_color=NEW if paid else GREY_B,
                                   fill_opacity=0.18 if paid else 0.05)
            txt = VGroup(label(m, font_size=20, color=WHITE),
                         label(rf"\${T['monthly_young']}" if paid else r"---", font_size=18,
                               color=NEW if paid else GREY_B)).arrange(DOWN, buff=0.1).move_to(box)
            coins.add(VGroup(box, txt))
        coins.arrange(RIGHT, buff=0.22).move_to(UP * 0.8)
        yr = VGroup(label(r"2021", font_size=20, color=GREY_A).next_to(coins[:6], UP, buff=0.25),
                    label(r"2022", font_size=20, color=GREY_A).next_to(coins[6:], UP, buff=0.25))
        notes = VGroup(
            label(rf"\${T['monthly_young']} a month for each child under six, \ \${T['monthly_older']} for each child "
                  r"aged six to seventeen", font_size=22, color=WHITE),
            label(rf"the rest at tax time: \ \${T['young']:,} and \${T['older']:,} a year, \ even for families with "
                  r"no earnings".replace(",", "{,}"), font_size=22, color=GREY_A),
            label(r"then the law lapsed", font_size=24, color=LOSS),
        ).arrange(DOWN, buff=0.28).next_to(coins, DOWN, buff=0.7)
        tag = published_tag(tables.CTC_2021.tag, corner=DR, font_size=11)
        with self.voiceover(
            "On the fifteenth of July 2021, most American families with children received a payment they had never "
            "had before. <bookmark mark='a'/> Three hundred dollars for each child under six, two hundred and fifty "
            "for each child from six to seventeen, every month. <bookmark mark='b'/> The rest came at tax time: "
            f"{T['young']:,} dollars a year for a young child and {T['older']:,} for an older one, <bookmark "
            "mark='b2'/> even for families with no earnings at all, who had received little or nothing from the old "
            "credit. <bookmark mark='c'/> "
            "The payments came for six months. <bookmark mark='d'/> In January 2022 they stopped: the law that "
            "created them lapsed, and Congress did not renew it."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(c) for c in coins[:1]]), FadeIn(yr[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(notes[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(notes[1], shift=UP * 0.1))
            vo.wait_until("b2")
            self.play(Indicate(notes[1], color=NEW, scale_factor=1.04))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in coins[1:6]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(yr[1]), LaggedStart(*[FadeIn(c) for c in coins[6:]], lag_ratio=0.4), FadeIn(notes[2]),
                      run_time=1.5)
        self.clear_scene()

    def poverty(self):
        T = tables.CTC_2021.data
        ax = plane([-0.5, 2.5], [0, 20], center=LEFT * 2.2 + DOWN * 0.35, x_length=7.0, y_length=4.4, xticks=[],
                   yticks=[0, 5, 10, 15, 20], ylabel=r"children in poverty, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        bars = VGroup()
        for i, (yr, spm, opm) in enumerate(((2020, T["spm_2020"], T["opm_2020"]), (2021, T["spm_2021"], T["opm_2021"]),
                                            (2022, T["spm_2022"], None))):
            g = VGroup()
            p0, p1 = ax.ax.c2p(i - 0.05 - 0.3, 0), ax.ax.c2p(i - 0.05, spm)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=SPM,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            g.add(VGroup(r, label(f"{spm:.1f}", font_size=16, color=WHITE).next_to(r, UP, buff=0.05)))
            if opm is not None:
                q0, q1 = ax.ax.c2p(i + 0.05, 0), ax.ax.c2p(i + 0.35, opm)
                o = Rectangle(width=q1[0] - q0[0], height=q1[1] - q0[1], stroke_width=0, fill_color=OPM,
                              fill_opacity=0.6).move_to((q0 + q1) / 2)
                g.add(VGroup(o, label(f"{opm:.1f}", font_size=16, color=GREY_A).next_to(o, UP, buff=0.05)))
            g.add(label(str(yr), font_size=18, color=WHITE).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.15))
            bars.add(g)
        side = VGroup(
            label(r"green: \ the Supplemental \\ Poverty Measure, \\ which counts taxes \\ and credits", font_size=17,
                  color=SPM),
            label(r"grey: \ the official \\ measure, \ which \\ ignores them", font_size=17, color=OPM),
            label(rf"{T['spm_2020']} $\to$ {T['spm_2021']}: \\ the lowest on record", font_size=18, color=GAIN),
            label(rf"2022: \ {T['spm_2022']}", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"US Census Bureau, \ September 2022 and 2023", corner=DL, font_size=12)
        with self.voiceover(
            "What happened to child poverty? <bookmark mark='a'/> On the Census Bureau's Supplemental Poverty "
            "Measure, which counts taxes and credits as income, the share of American children in poverty was "
            f"{T['spm_2020']} percent in 2020. <bookmark mark='b'/> In 2021 it fell to {T['spm_2021']} percent, the "
            "lowest ever recorded, and the Census Bureau credited the child tax credit with much of the fall. "
            f"<bookmark mark='c'/> In 2022, with the payments gone, it was {T['spm_2022']}. <bookmark mark='d'/> The "
            "official measure, which counts only cash income before taxes, barely moved: "
            f"{T['opm_2020']} to {T['opm_2021']}. How a policy looks can depend on how it is measured, a theme this "
            "part returns to."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0][0], DOWN), FadeIn(bars[0][0][1]), FadeIn(bars[0][-1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0][0], DOWN), FadeIn(bars[1][0][1]), FadeIn(bars[1][-1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2][0][0], DOWN), FadeIn(bars[2][0][1]), FadeIn(bars[2][-1]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[0][1][0], DOWN), FadeIn(bars[0][1][1]), GrowFromEdge(bars[1][1][0], DOWN),
                      FadeIn(bars[1][1][1]), FadeIn(side[1]), run_time=1.5)
        self.clear_scene()

    def request(self):
        note = VGroup(
            label(r"From: \ the Island's Minister of Finance", font_size=22, color=GREY_A),
            label(r"To: \ you", font_size=22, color=GREY_A),
            label(r"Should the Island pay every family a monthly allowance for each child, \\ on the 2021 design? \ "
                  r"What would it do, \ what would it cost, \ and how sure are you?", font_size=24, color=WHITE),
            label(r"Four pages. \ Two weeks.", font_size=24, color=NEW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        frame = SurroundingRectangle(note, buff=0.45, corner_radius=0.12, color=GREY_B, stroke_width=1.6)
        VGroup(frame, note).move_to(ORIGIN)
        with self.voiceover(
            "Now a request lands on your desk. <bookmark mark='a'/> The Island's finance minister asks whether the "
            "Island should pay every family a monthly allowance for each child, on the American design of 2021, "
            "made permanent. What would it do, what would it cost, and how sure are you? <bookmark mark='b'/> Four "
            "pages, in two weeks. This part writes that memo, using only what the series has built: the models, the "
            "dials, the evidence, and the Island."
        ) as vo:
            self.play(Create(frame), FadeIn(note[0]), FadeIn(note[1]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(note[2], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(note[3], shift=UP * 0.1), Indicate(frame, color=WHITE, scale_factor=1.02))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what exactly is proposed, \ and who is affected?", font_size=26, color=CHILD),
            label(r"how will families respond, \ and how do we know?", font_size=26, color=WORK),
            label(r"what does it cost, \ and what is it worth?", font_size=26, color=BUDGET),
            label(r"how sure are we, \ and what would change the advice?", font_size=26, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: a minister asks whether to pay a child allowance. What do you write? <bookmark "
            "mark='a'/> First, what exactly is proposed, and who it touches. <bookmark mark='b'/> Then how families "
            "will respond, and how we know. <bookmark mark='c'/> Then what it costs and what it is worth. <bookmark "
            "mark='d'/> And how sure we are, and what would change the advice."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1989, 2024], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, CHILD, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 50 \ $\cdot$ \ The Policy Memo", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty: the policy memo."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IX \ $\cdot$ \ The Fields \ $\cdot$ \ the capstone", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the question made answerable; \ the family's budget, \ before and after",
            r"the dials that matter; \ your advice before the analysis",
            r"the margins, \ the budget, \ and the three best pieces of evidence",
            r"the policy run on the Island; \ its value; \ who gains; \ the uncertainty",
            r"the memo itself; \ how memos are used; \ what remains unknown",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> The question made answerable, and what the allowance does to a "
            "family's budget. <bookmark mark='b'/> The dials that matter, and your own advice before any analysis. "
            "<bookmark mark='c'/> The margins a textbook picture misses, the budget, and the three best pieces of "
            "evidence. <bookmark mark='d'/> The policy run on the Island, its value per dollar, who gains and who "
            "loses, and the uncertainty. <bookmark mark='e'/> And then the memo itself, how such memos are used and "
            "misused, and what nobody yet knows."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
