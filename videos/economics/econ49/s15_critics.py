from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Critics(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Economics imperialism, \ and the reply", r"Where does the price model break?",
             "Chapter thirteen. Economics imperialism, and the reply.",
             lit={1970: r"Titmuss", 2000: r"Lazear; Gneezy and Rustichini", 2008: r"Mellström and Johannesson"},
             scale=("person", "nation"), horizon=("a year",))
        self.claim()
        self.daycare()
        self.blood()
        self.verdict()

    def claim(self):
        left = VGroup(
            label(r"Lazear: \ economics imperialism", font_size=26, color=E.ACCENT),
            label(r"a single model of rational choice, \\ an equilibrium, \ and attention \\ to what can be "
                  r"measured", font_size=20, color=WHITE),
            label(r"so it travels: \ to crime, \ the family, \\ law, \ politics, \ religion", font_size=20,
                  color=WHITE),
        ).arrange(DOWN, buff=0.3)
        right = VGroup(
            label(r"the critics", font_size=26, color=HOLD),
            label(r"people are not only prices: \\ duty, \ shame, \ identity, \\ meaning", font_size=20,
                  color=WHITE),
            label(r"and putting a price on a thing \\ can change what it is", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        tag = published_tag(r"Lazear, \ QJE (2000)", corner=DR, font_size=11)
        with self.voiceover(
            "By 2000, Edward Lazear could title a paper Economic Imperialism, and mean it as praise. <bookmark "
            "mark='a'/> Economics, he argued, had spread into the other social sciences because it had something "
            "they lacked: one model of rational choice, an equilibrium, and an insistence on what can be measured. "
            "<bookmark mark='b'/> So it travelled: to crime, the family, law, politics, even religion. <bookmark "
            "mark='c'/> The critics, sociologists, psychologists and many economists, answered that people are not "
            "moved by prices alone, but by duty, shame, identity and meaning. <bookmark mark='d'/> And they made a "
            "sharper claim, which can be tested: that putting a price on something can change what it is."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(left[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(left[1]))
            vo.wait_until("b")
            self.play(FadeIn(left[2]))
            vo.wait_until("c")
            self.play(FadeIn(right[0]), FadeIn(right[1]))
            vo.wait_until("d")
            self.play(FadeIn(right[2]))
        self.clear_scene()

    def daycare(self):
        T = tables.CRITICS_49.data
        chain = flow_chain([(rf"{T['centres']} day-care \\ centres in Haifa", CHILD),
                            (rf"{T['weeks']} weeks: \\ count the late \\ parents", GREY_B),
                            (rf"a fine in {T['fined']}: \\ late by more than \\ {T['late_min']} minutes", FINE),
                            (r"lateness rises, \\ and stays up \\ when it is removed", LOSS)],
                           notes=[r"parents collect \\ at closing time", r"a teacher \\ has to wait",
                                  r"the other four: \\ no change", r"a fine is a price"],
                           box_w=2.9, font_size=19, note_size=17).move_to(UP * 1.2)
        why = VGroup(
            label(r"before: \ being late was a favour asked of a teacher, \ with guilt attached", font_size=21,
                  color=WHITE),
            label(r"after: \ it was a service, \ priced and paid for, \ and cheap", font_size=21, color=FINE),
            label(r"the fine did not raise the cost of lateness: \ it changed what lateness meant", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.7)
        tag = published_tag(r"Gneezy and Rustichini, \ J. Legal Studies (2000)", corner=DR, font_size=11)
        with self.voiceover(
            "The most famous test is Uri Gneezy and Aldo Rustichini's. <bookmark mark='a'/> Ten day-care centres in "
            "the Israeli city of Haifa, where parents sometimes came late to collect their children and a teacher "
            f"had to wait. <bookmark mark='b'/> For {T['weeks']} weeks they counted the late parents. <bookmark "
            f"mark='c'/> Then {T['fined']} of the centres introduced a small fine for arriving more than "
            f"{T['late_min']} minutes late. Becker's model says lateness should fall. <bookmark mark='d'/> It rose, "
            "and when the fine was removed some weeks later, it stayed up. <bookmark mark='e'/> The authors' "
            "reading: before the fine, lateness was a favour asked of a teacher, with some guilt attached. <bookmark "
            "mark='f'/> The fine made it a service with a price, and the price was low. <bookmark mark='g'/> The "
            "fine did not add to the cost of lateness; it replaced one cost with another, and the guilt did not come "
            "back."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]), Indicate(chain.boxes[0], color=WHITE, scale_factor=1.04))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            for mk, r_ in zip("efg", why):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def blood(self):
        T = tables.CRITICS_49.data
        ax = plane([-0.5, 2.5], [0, 0.65], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.2, xticks=[],
                   yticks=[0, 0.2, 0.4, 0.6], ylabel=r"women who became donors", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        vals = ((r"no payment", T["blood_before"] / 100, GREY_B), (rf"paid \\ {T['sek']} kronor", T["blood_paid"] / 100,
                                                                   LOSS),
                (r"paid, \ or give \\ it to charity", T["blood_before"] / 100, GAIN))
        bars = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            p0, p1 = ax.ax.c2p(i - 0.32, 0), ax.ax.c2p(i + 0.32, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85 if i < 2 else 0.4).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(rf"{100 * v:.0f}\%" if i < 2 else r"about \\ the same", font_size=15,
                                     color=WHITE).next_to(r, UP, buff=0.05),
                            label(nm, font_size=15, color=col).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.15)))
        side = VGroup(
            label(r"Sweden: \ people \\ asked to give blood", font_size=17, color=WHITE),
            label(r"a payment of about \\ \$7 cut women's \\ giving; \ men's \\ did not change", font_size=17,
                  color=LOSS),
            label(r"allowing the money to \\ go to charity undid \\ the fall", font_size=17, color=GAIN),
            label(r"Titmuss's fear, \\ in part confirmed", font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Mellström and Johannesson, \ JEEA (2008); \ Titmuss (1970)", corner=DR, font_size=11)
        with self.voiceover(
            "In 1970 Richard Titmuss argued that paying for blood would drive out those who give it freely. "
            "<bookmark mark='a'/> Carl Mellström and Magnus Johannesson tested it in Sweden, asking people to "
            f"become blood donors. <bookmark mark='b'/> Without payment, {T['blood_before']} percent of the women "
            f"did. <bookmark mark='c'/> Offered {T['sek']} kronor, about seven dollars, only {T['blood_paid']} "
            "percent did. For men, payment made no difference. <bookmark mark='d'/> And when the money could be "
            "given to charity instead, women's giving returned. Paying people to be generous made generosity look "
            "like work, for some of them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[i][0], DOWN), FadeIn(bars[i][1]), FadeIn(bars[i][2]),
                          FadeIn(side[i + 1]) if i else Indicate(side[0], color=WHITE), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def verdict(self):
        cards = point_cards([
            (r"Swiss villages", r"support for a nuclear \\ waste site fell \\ when compensation \\ was offered",
             HOLD),
            (r"what breaks", r"prices that change \\ meaning: \ gifts, \\ duties, \ norms", LOSS),
            (r"what survives", r"crime, \ schools, \\ children, \ smoking: \\ prices matter, \\ measurably", GAIN),
            (r"the reply", r"put the motives \\ in the model, \\ and test it: \ which \\ is what economists did",
             E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"the verdict", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Frey and Oberholzer-Gee, \ AER (1997); \ Bénabou and Tirole, \ AER (2006)",
                            corner=DR, font_size=11)
        with self.voiceover(
            "There are more such findings. <bookmark mark='a'/> Bruno Frey and Felix Oberholzer-Gee found that Swiss "
            "residents' support for a nuclear waste site near them fell when compensation was offered. <bookmark "
            "mark='b'/> So the model breaks where a price changes the meaning of an act: a gift, a duty, a norm. "
            "<bookmark mark='c'/> But it survives where this part has tested it: penalties deter, mostly through "
            "the chance of being caught; class size and teachers matter; children respond to their price; smokers "
            "respond to theirs. <bookmark mark='d'/> And the reply to the critics was the economic approach "
            "itself: put duty, identity and the wish to look good into the model, as Roland Bénabou and Jean "
            "Tirole did, and test it. The method was extended, not abandoned."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
