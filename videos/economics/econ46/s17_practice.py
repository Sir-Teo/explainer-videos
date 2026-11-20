from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ evaluators, \ banks, \ cost-effectiveness", r"Who uses these ideas, and how?",
             "Chapter fifteen. In practice: evaluators, development banks, and cost-effectiveness.",
             lit={2003: r"J-PAL", 2025: r"GiveWell"}, scale=("organization", "world"), horizon=("a year",))
        self.people()
        self.givewell()
        self.called()

    def people(self):
        rows = VGroup(
            label(r"evaluators: \ J-PAL, \ Innovations for Poverty Action, \ the World Bank's impact teams",
                  font_size=22,
                  color=TRIAL),
            label(r"development banks: \ the World Bank and the regional banks, \ lending to governments",
                  font_size=22, color=TOWN),
            label(r"governments: \ ministries that run transfers, \ schools and clinics at national scale",
                  font_size=22, color=CASH),
            label(r"charities and their funders: \ deciding which programmes get the next dollar", font_size=22,
                  color=HEALTH),
            label(r"economists in all four: \ designing trials, \ and turning results into budgets", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        head = label(r"the people who use this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.PRACTICE_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Who uses development economics? <bookmark mark='a'/> Evaluators: the Abdul Latif Jameel Poverty Action "
            "Lab, founded at MIT in 2003, Innovations for Poverty Action, and the World Bank's own impact "
            "evaluation teams, who design and run trials with governments and charities. <bookmark mark='b'/> The "
            "development banks, which lend to governments for roads, schools and transfer programmes, and must "
            "decide what to fund. <bookmark mark='c'/> Governments, whose ministries run the programmes at a scale "
            "no charity can. <bookmark mark='d'/> Charities and the foundations that fund them. <bookmark "
            "mark='e'/> And economists in every one of these places, designing the trials, reading the evidence, "
            "and turning it into budgets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def givewell(self):
        T = tables.PRACTICE_46.data
        chain = flow_chain([(rf"a net: \\ about \${T['net']}", HEALTH), (r"nets per \\ child protected", HEALTH),
                            (r"deaths averted \\ per child", GAIN), (rf"about \${T['per_life']:,} \\ per life saved"
                                                                    .replace(",", "{,}"), E.ACCENT)],
                           notes=[r"bought and \\ delivered", r"use, \ wear, \\ who sleeps under it",
                                  r"malaria's toll \\ where it goes", r"a rough estimate, \\ 2022--2024"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.9)
        rows = VGroup(
            label(r"then compare: \ deworming, \ cash, \ vitamin A, \ vaccination incentives, \ on one scale",
                  font_size=21, color=GREY_A),
            label(r"and ask how much more each could absorb: \ chapter two's margin", font_size=21, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.PRACTICE_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Here is cost-effectiveness done in public. The charity evaluator GiveWell publishes its arithmetic. "
            f"<bookmark mark='a'/> A bed net costs about {T['net']} dollars, bought and delivered. <bookmark "
            "mark='b'/> It estimates how many children each net protects, allowing for how many are used and for "
            "how long. <bookmark mark='c'/> And how many deaths that averts, from malaria's toll where the nets "
            f"go. <bookmark mark='d'/> For the Against Malaria Foundation it arrives at about "
            f"{T['per_life']:,} dollars per life saved, for its grants from 2022 to 2024, and calls the number a "
            "rough estimate. <bookmark mark='e'/> The same arithmetic is done for deworming, cash and other "
            "programmes, on one scale, and then, as in chapter two, GiveWell asks how much more money each could "
            "use as well. The numbers are uncertain. Writing them down is what makes them arguable, and so "
            "improvable."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows], lag_ratio=0.6), run_time=2.0)
        self.clear_scene()

    def called(self):
        c = calls.CALLS["sachs_2005"]
        P = load("poverty")
        W = P["WLD"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18)
        cc.move_to(UP * 1.45)
        ax = plane([2004, 2026], [0, 32], center=DOWN * 2.05 + LEFT * 0.5, x_length=7.2, y_length=2.2,
                   xticks=[2005, 2010, 2015, 2020, 2025], yticks=[0, 10, 20, 30], xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=12)
        yr = [y for y in W["year"] if y >= 2005]
        vv = [v for y, v in zip(W["year"], W["value"]) if y >= 2005]
        ln = path(ax, yr, vv, POOR, 3.0, smooth=False)
        goal = VGroup(dot(ax, 2025, 0, GAIN, 0.09), label(r"the goal: \ zero by 2025", font_size=13, color=GAIN)
                      .next_to(ax.ax.c2p(2025, 0), UL, buff=0.08))
        cap = label(r"percent of the world \\ below \$3.00 a day", font_size=13, color=GREY_A).next_to(ax, LEFT,
                                                                                                    buff=0.3)
        last = label(rf"{W['last_year']}: \ {W['last']:.0f}\%", font_size=14, color=POOR).next_to(
            ax.ax.c2p(W["last_year"], W["last"]), UR, buff=0.08)
        tag = published_tag(tables.PRACTICE_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 2005 Jeffrey Sachs published The End of Poverty. He argued that "
            "extreme poverty could be ended by 2025, if rich countries raised their aid to between 135 and 195 "
            "billion dollars a year and spent it on health, schools, farms and roads. His Millennium Villages "
            "project was meant to show how. <bookmark mark='a2'/> Here is the share of the world below the line of "
            f"three dollars a day, from 2005, when it was {vv[0]:.0f} percent. <bookmark mark='b'/> Aid rose, but "
            "never to the share of rich countries' incomes his plan required. Poverty fell fast, mostly in Asia "
            "and mostly with growth, but in 2025 about 808 million people still lived below the line, "
            "one in ten. The Millennium Villages' final evaluation found gains on thirty of forty outcomes, with "
            "poverty itself less conclusive. <bookmark mark='c'/> The verdict: wrong. The goal was a good one, and "
            "the forecast underrated how hard it is to buy development from outside."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a2")
            self.play(FadeIn(ax), FadeIn(cap), Create(ln), FadeIn(goal), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cc.right), FadeIn(last))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
