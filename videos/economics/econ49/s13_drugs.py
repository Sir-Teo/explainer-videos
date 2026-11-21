from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Drugs(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Drugs, \ patents and despair", r"Who pays for new medicines, and what went wrong with "
             r"old ones?", "Chapter eleven. Drugs, patents and despair.",
             lit={2015: r"Case and Deaton", 2022: r"Alpert et al."}, scale=("market", "nation"),
             horizon=("a decade",))
        self.patent()
        self.despair()
        self.opioids()

    def patent(self):
        D = load("drug")
        A, c, pm, qm, qc = D["A"], D["cost"], D["p_mono"], D["q_mono"], D["q_comp"]
        ax = plane([0, 105], [0, 105], center=LEFT * 2.2 + DOWN * 0.35, x_length=6.8, y_length=4.6,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 25, 50, 75, 100], xlabel=r"courses sold, \ thousands",
                   ylabel=r"price of a course, \ \$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        dem = seg(ax, 0, A, A, 0, WHITE, 3.0)
        mc = seg(ax, 0, c, 102, c, GREY_B, 2.4)
        prof = Polygon(ax.ax.c2p(0, c), ax.ax.c2p(qm, c), ax.ax.c2p(qm, pm), ax.ax.c2p(0, pm), stroke_width=0,
                       fill_color=GAIN, fill_opacity=0.45)
        dwl = Polygon(ax.ax.c2p(qm, c), ax.ax.c2p(qc, c), ax.ax.c2p(qm, pm), stroke_width=0, fill_color=LOSS,
                      fill_opacity=0.5)
        pmk = DashedLine(ax.ax.c2p(0, pm), ax.ax.c2p(qm, pm), color=DRUG, stroke_width=2.0)
        side = VGroup(
            label(rf"making a course: \ \${c:.0f}", font_size=17, color=GREY_B),
            label(rf"under the patent: \\ \${pm:.0f}, \ {qm:.0f} thousand \\ courses", font_size=17, color=DRUG),
            label(rf"green: \ \${D['profit'] / 1000:.2f} million \\ a year, \ which pays \\ for the discovery",
                  font_size=17, color=GAIN),
            label(rf"red: \ \${D['dwl'] / 1000:.2f} million a year \\ of treatment not given, \\ until generics",
                  font_size=17, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A new medicine is expensive to discover and cheap to make. <bookmark mark='a'/> On the Island, a course "
            f"of a new drug costs {c:.0f} dollars to make. <bookmark mark='b'/> While the patent lasts, its owner "
            f"charges the monopoly price, {pm:.0f} dollars, and sells {qm:.0f} thousand courses a year. <bookmark "
            f"mark='c'/> The profit, {D['profit'] / 1000:.2f} million dollars a year, is what pays for the research "
            "that found the drug, and for the failures along the way. <bookmark mark='d'/> The red triangle is the "
            "cost: patients who would have paid more than the cost of making the drug, but not the patent price, go "
            f"without, {D['dwl'] / 1000:.2f} million dollars of value a year, <bookmark mark='e'/> until the "
            f"patent runs out and generics bring the price down to the cost, and {qc:.0f} thousand courses are sold. "
            "<bookmark mark='f'/> The patent trades that triangle now for medicines in the future; how long and how "
            "strong patents should be is a question of how much more research the profit calls forth."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(dem), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(mc), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pmk), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(prof), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(dwl), FadeIn(side[3]))
            vo.wait_until("e")
            gen = dot(ax, qc, c, WHITE, 0.09)
            gen_l = label(rf"generics: \ \${c:.0f}, \ {qc:.0f} thousand", font_size=15, color=WHITE).next_to(
                gen, UR, buff=0.1)
            self.play(pmk.animate.shift(ax.ax.c2p(0, c) - ax.ax.c2p(0, pm)), FadeIn(gen), FadeIn(gen_l),
                      prof.animate.set_opacity(0.15), dwl.animate.set_opacity(0.15), run_time=2.0)
            vo.wait_until("f")
            self.play(prof.animate.set_opacity(0.45), dwl.animate.set_opacity(0.5), run_time=1.0)
        self.clear_scene()

    def despair(self):
        T = tables.DRUGS_49.data
        cards = point_cards([
            (r"the reversal", r"white Americans \\ aged 45--54: \\ deaths rising, \\ 1999--2013", LOSS),
            (r"the causes", r"suicide, \ drug and \\ alcohol poisoning, \\ liver disease", DRUG),
            (r"the cost", rf"at 1998's death \\ rate, \ about \\ {T['avoided']:,} fewer \\ deaths".replace(",", "{,}"),
             LOSS),
            (r"the question", r"despair, \ or \\ the supply of \\ the drugs?", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"deaths of despair", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Case and Deaton, \ PNAS (2015)", corner=DR, font_size=11)
        with self.voiceover(
            "In 2015 Anne Case and Angus Deaton found something that should not happen in a rich country. <bookmark "
            "mark='a'/> The death rate of white Americans aged forty-five to fifty-four, which had fallen for "
            "decades, rose from 1999 to 2013, while it kept falling in other rich countries. <bookmark mark='b'/> "
            "The causes were suicide, poisoning by drugs and alcohol, and liver disease: deaths of despair, they "
            f"called them. <bookmark mark='c'/> Had the 1998 death rate held, about {T['avoided']:,} deaths would "
            "have been avoided. <bookmark mark='d'/> Case and Deaton pointed to decades of worsening prospects for "
            "Americans without degrees. Others asked about supply: were the drugs themselves the cause?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def opioids(self):
        T = tables.DRUGS_49.data
        chain = flow_chain([(r"1996: \ OxyContin \\ is launched", DRUG),
                            (rf"{T['triplicate']} states demand \\ triplicate forms", POLICE),
                            (r"the company sees \\ hard markets", GREY_B),
                            (rf"OxyContin there: \\ about {T['oxy_lower']}\% lower", GAIN)],
                           notes=[r"a strong opioid, \\ marketed hard", r"for prescriptions \\ of strong drugs",
                                  r"a paper trail \\ doctors avoided", r"overdose deaths \\ grow more slowly"],
                           box_w=2.9, font_size=19, note_size=17).move_to(UP * 1.2)
        res = VGroup(
            label(rf"with the triplicate states' exposure, \ the other states would have had about "
                  rf"{T['drug']}\% fewer", font_size=21, color=WHITE),
            label(rf"drug overdose deaths, \ and {T['opioid']}\% fewer opioid overdose deaths, \ each year, \ "
                  r"1996--2017", font_size=21, color=WHITE),
            label(r"supply mattered: \ prices, \ marketing and rules shape even an addiction", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.7)
        tag = published_tag(r"Alpert, \ Evans, \ Lieber and Powell, \ QJE (2022)", corner=DR, font_size=11)
        with self.voiceover(
            "Abby Alpert, William Evans, Ethan Lieber and David Powell found a natural experiment in supply. "
            "<bookmark mark='a'/> In 1996 Purdue Pharma launched OxyContin, a strong opioid, and marketed it hard. "
            f"<bookmark mark='b'/> But {T['triplicate']} states required doctors to write prescriptions for such "
            "drugs on special triplicate forms, which left a trail for the authorities. <bookmark mark='c'/> "
            "Doctors there disliked the forms, and the company's own planning treated those states as hard "
            "markets. <bookmark "
            f"mark='d'/> OxyContin's distribution was about {T['oxy_lower']} percent lower there, and their "
            "overdose deaths, once higher than elsewhere, grew more slowly, for twenty years. <bookmark mark='e'/> "
            f"Had the other states been as little exposed, they estimate, they would have had {T['drug']} percent "
            f"fewer drug overdose deaths <bookmark mark='f'/> and {T['opioid']} percent fewer opioid overdose "
            "deaths a year. <bookmark mark='g'/> Despair may explain who was vulnerable; the supply of the drug "
            "explains much of who died."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]), Indicate(chain.boxes[0], color=WHITE, scale_factor=1.04))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            for mk, r_ in zip("efg", res):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
