from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.parking()
        self.sum()
        self.question()
        self.title()
        self.objectives()

    def parking(self):
        T = tables.BECKER_1968.data
        head = label(r"New York, \ the 1960s", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        opts = VGroup()
        for t_, sub, col in ((r"the car park", r"a sure cost, \\ paid every time", REGULAR),
                             (r"the street", r"free, \ unless a warden \\ comes by: \ then a fine", FINE)):
            box = RoundedRectangle(width=4.6, height=1.9, corner_radius=0.14, stroke_color=col, stroke_width=2.4,
                                   fill_color=col, fill_opacity=0.08)
            txt = VGroup(label(t_, font_size=28, color=col), label(sub, font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.18).move_to(box)
            opts.add(VGroup(box, txt))
        opts.arrange(RIGHT, buff=1.2).move_to(UP * 0.6)
        vs = label(r"or", font_size=24, color=GREY_B).move_to(opts)
        who = VGroup(label(r"Gary Becker, \ late for a student's oral examination at Columbia", font_size=22,
                           color=WHITE),
                     label(r"Columbia had no faculty parking", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15)
        who.next_to(opts, DOWN, buff=0.7)
        weigh = VGroup(*[label(t_, font_size=20, color=c_) for t_, c_ in (
            (r"the chance of a ticket", CHANCE), (r"$\times$ \ the fine", FINE),
            (r"against \ the price of the car park", REGULAR))]).arrange(RIGHT, buff=0.3)
        weigh.next_to(opts, DOWN, buff=0.35)
        who.next_to(weigh, DOWN, buff=0.45)
        res = label(r"he parked in the street, \ and was not ticketed", font_size=22, color=GAIN).next_to(who, DOWN,
                                                                                                       buff=0.35)
        city = label(r"and the city? \ how often to check the cars, \ how large to make the fine", font_size=21,
                     color=E.ACCENT).next_to(res, DOWN, buff=0.3)
        tag = published_tag(tables.BECKER_1968.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Some time in the 1960s, an economist was driving to Columbia University in New York, late for the oral "
            "examination of a student in economic theory. <bookmark mark='a'/> Columbia had no parking for its "
            "teachers. He had two choices. <bookmark mark='b'/> A car park, which cost money for certain. <bookmark "
            "mark='c'/> Or the street, which was illegal and free, unless a warden came by and wrote a ticket. "
            "<bookmark mark='d'/> There was no time to think about it for long. He weighed the chance of a ticket, "
            "the size of the fine, and the price of the car park, and parked in the street. <bookmark mark='e'/> He "
            "was not ticketed. The economist was Gary Becker. <bookmark mark='f'/> On the walk to the examination "
            "room, he said later, it occurred to him that the city had probably made a similar calculation, in "
            "deciding how often to check "
            "the cars and how large to make the fine. His paper, Crime and Punishment: An Economic Approach, "
            f"appeared in {T['paper']}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(who[0], shift=UP * 0.1), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(who[1]))
            vo.wait_until("b")
            self.play(FadeIn(opts[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(vs), FadeIn(opts[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(w_, shift=UP * 0.1) for w_ in weigh], lag_ratio=0.5), run_time=2.0)
            self.play(Indicate(opts[1], color=WHITE, scale_factor=1.04), opts[0].animate.set_opacity(0.35))
            vo.wait_until("e")
            self.play(FadeIn(res, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(city, shift=UP * 0.1))
        self.clear_scene()

    def sum(self):
        eq = MathTex(r"\text{street if}\quad", r"p", r"\times", r"F", r"\;<\;", r"c", font_size=60)
        eq[1].set_color(CHANCE)
        eq[3].set_color(FINE)
        eq[5].set_color(REGULAR)
        eq.move_to(UP * 1.6)
        keys = VGroup(
            label(r"$p$: \ the chance of a ticket", font_size=22, color=CHANCE),
            label(r"$F$: \ the fine", font_size=22, color=FINE),
            label(r"$c$: \ the price of the car park", font_size=22, color=REGULAR),
        ).arrange(RIGHT, buff=0.8).next_to(eq, DOWN, buff=0.6)
        ex = VGroup(
            label(r"a ticket one day in ten, \ a \$30 fine: \ \$3 expected", font_size=22, color=WHITE),
            label(r"a car park at \$5: \ the street is cheaper", font_size=22, color=WHITE),
            label(r"the same arithmetic for a theft, \ a tax return, \ a speed limit", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(keys, DOWN, buff=0.7)
        with self.voiceover(
            "The arithmetic is short. <bookmark mark='a'/> Park in the street if the chance of a ticket times the "
            "fine is less than the price of the car park. <bookmark mark='b'/> Say a warden comes one day in ten "
            "and the fine is thirty dollars: an expected cost of three dollars. <bookmark mark='c'/> If the car park "
            "costs five, the street is cheaper, for anyone who does not mind the risk. <bookmark mark='d'/> Becker's "
            "claim was that the same arithmetic, the gain from an act against the chance and size of a penalty, "
            "applies to theft, to cheating on taxes and to speeding, and that most offenders are not different "
            "kinds of people, just people facing different prices."
        ) as vo:
            self.play(Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k) for k in keys], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(ex[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(ex[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(ex[2], shift=UP * 0.1), Indicate(eq, color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"crime: \ do prices deter, \ and how would we know?", font_size=26, color=CRIME),
            label(r"the family: \ time, \ marriage, \ children, \ who decides", font_size=26, color=WOMEN),
            label(r"schools and health: \ what do they produce, \ and for what?", font_size=26, color=SCHOOL),
            label(r"addiction, \ and where the method breaks", font_size=26, color=DRUG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        nobel = label(r"1992: \ the Nobel prize, \ for extending the analysis of choice \ to behaviour outside "
                      r"markets", font_size=24, color=GREY_A).move_to(DOWN * 0.3)
        with self.voiceover(
            "Becker spent the next thirty years applying the model of choice under constraint to things economists "
            "had left to others, <bookmark mark='n'/> and won the Nobel prize for it in 1992. This part's question: "
            "how far can that model be pushed into the rest of life? <bookmark mark='a'/> To crime: do penalties "
            "deter, and how would we know? <bookmark mark='b'/> To the family: the use of time, marriage, how many "
            "children and who decides. <bookmark mark='c'/> To schools and health. <bookmark mark='d'/> And to "
            "addiction, where the model is most strained, and where its critics say it breaks."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            vo.wait_until("n")
            self.play(FadeIn(nobel, shift=UP * 0.1))
            self.play(nobel.animate.scale(0.8).to_edge(DOWN, buff=0.6), run_time=1.0)
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1950, 2023], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, CHILD, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 49 \ $\cdot$ \ The Economic Approach", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-nine: the economic approach."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IX \ $\cdot$ \ The Fields", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"crime as a choice; \ you choose a deterrent; \ police and crime, \ measured",
            r"the household as a factory; \ marriage as a market; \ children; \ bargaining",
            r"schools on real data: \ Tennessee's experiment, \ teachers; \ early childhood",
            r"health, \ drugs, \ addiction: \ models and data; \ the critics",
            r"three dials; \ the people who use this; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Crime as a choice, a deterrent chosen by you, and what happens "
            "when economists try to measure whether police reduce crime. <bookmark mark='b'/> The household as a "
            "small factory, marriage as a market, the number of children, and bargaining between husband and wife. "
            "<bookmark mark='c'/> Schools, on the data from Tennessee's class-size experiment, teachers, and early "
            "childhood. <bookmark mark='d'/> Health, drugs and addiction, and the critics of the whole enterprise. "
            "<bookmark mark='e'/> Three dials, the people who use these ideas, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
