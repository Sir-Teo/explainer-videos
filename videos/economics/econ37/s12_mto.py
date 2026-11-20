from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class Neighbourhoods(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Neighbourhoods and children", r"Does where a child grows up change the adult?",
             "Chapter ten. Neighbourhoods and children.",
             lit={1994: r"Moving to Opportunity", 2016: r"Chetty, \ Hendren and Katz"},
             scale=("household", "city"), horizon=("a century",))
        self.lottery()
        self.children()

    def lottery(self):
        C = load("housing")["chk"]
        steps = flow_chain([(rf"{C['families']:,} families \\ in public housing", CITY),
                            (r"a lottery", E.ACCENT), (r"three groups", WHITE)],
                           notes=[rf"{C['cities']} cities, \ {C['start']}--{C['end']}", r"chance decides, \\ "
                                  r"not choice", r""], box_w=3.2, font_size=21, note_size=17).move_to(UP * 1.4)
        arms = point_cards([
            (r"experimental", rf"a voucher usable only \\ where under {C['poverty']}\% \\ of people are poor", GAIN),
            (r"Section 8", r"an ordinary \\ housing voucher", GOLD),
            (r"control", r"no voucher", GREY_B),
        ], width=11.4, cols=3, font_size=20).move_to(DOWN * 1.4)
        why = label(r"the cure for sorting, \ as in chapter 4: \ randomize who moves", font_size=20,
                    color=E.ACCENT).to_edge(DOWN, buff=0.35)
        tag = published_tag(tables.CHK_2016.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Schelling's board sorts people into neighbourhoods. Does the neighbourhood then change them? "
            "Comparing families in rich and poor areas confuses the place with the people who chose it, the sorting "
            "problem of chapter four. <bookmark mark='a'/> From 1994 to 1998 an American experiment called Moving "
            f"to Opportunity enrolled {C['families']:,} families living in public housing in {C['cities']} cities, "
            "<bookmark mark='b'/> and a lottery split them into three groups: <bookmark mark='c'/> vouchers they "
            "could use only in low-poverty neighbourhoods, ordinary housing vouchers, or nothing. "
            "<bookmark mark='d'/> Chance, not choice, decided who moved."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes), FadeIn(steps.notes), *[GrowArrow(a) for a in steps.arrows],
                      run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(steps.boxes[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(Indicate(steps.boxes[1], color=WHITE, scale_factor=1.05))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in arms.cards], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.clear_scene()

    def children(self):
        C = load("housing")["chk"]
        ax = plane([0.4, 2.6], [0, 16000], center=LEFT * 2.4 + DOWN * 0.45, x_length=5.6, y_length=4.6, xticks=[],
                   yticks=[0, 4000, 8000, 12000, 16000], ylabel=r"income in their mid-twenties, \ \$ a year",
                   yfmt=lambda v: f"{v:,.0f}", font_size=14)
        vals = (C["control"], C["control"] + C["gain"])
        cols = (GREY_B, GAIN)
        names = (r"control", r"moved \\ before 13")
        bars, nms = VGroup(), VGroup()
        for k, (v, col, n) in enumerate(zip(vals, cols, names)):
            p0, p1 = ax.ax.c2p(k + 0.7, 0), ax.ax.c2p(k + 1.3, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            nms.add(VGroup(label(n, font_size=17, color=col), label(f"\\${v:,.0f}", font_size=17, color=WHITE))
                    .arrange(DOWN, buff=0.06).next_to(ax.ax.c2p(k + 1, 0), DOWN, buff=0.12))
        side = VGroup(
            label(rf"+\${C['gain']:,} a year: \ +{C['pct']}\%", font_size=24, color=GAIN),
            label(r"more college, \\ less single parenthood", font_size=19, color=WHITE),
            label(r"moved as teenagers: \\ no gain, \ slightly worse", font_size=19, color=RENT),
            label(r"what matters is years \\ of childhood spent there: \\ exposure \ (Part 40)", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.6)
        tag = published_tag(tables.CHK_2016.tag + r"; \ treatment on the treated", corner=DR, font_size=12)
        with self.voiceover(
            "Early studies found little effect on the parents' earnings, though their health improved. Then, in "
            "2016, Raj Chetty, "
            "Nathaniel Hendren and Lawrence Katz followed the children into adulthood with tax records. "
            "<bookmark mark='a'/> Children whose families used the experimental voucher before they turned thirteen "
            f"earned about {C['gain']:,} dollars a year more in their mid-twenties, {C['pct']} percent more than "
            f"the control group's {C['control']:,}. <bookmark mark='b'/> They were more likely to go to college, "
            "and less likely to become single parents. <bookmark mark='c'/> Children who moved as teenagers gained "
            "nothing, and did slightly worse, perhaps from the disruption. <bookmark mark='d'/> The gain grows with "
            "the years of childhood spent in the better place. Part forty maps this exposure effect for every county "
            "in America."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(bars[0]), FadeIn(nms[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(nms[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
