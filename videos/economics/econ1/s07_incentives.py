from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


class Incentives(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Incentives", r"Do people respond to a price on what they do, \ and always the way you "
             r"meant?", "Chapter six. Incentives.", scale=("person", "household"), horizon=("a year",))
        self.principle()
        self.haifa()
        self.result()
        self.did()
        self.meaning()

    # ------------------------------------------------------------------
    def principle(self):
        rows = point_cards([
            (r"in the pit", r"traders shaded their bids when deals happened below them, and raised them when they "
             r"missed out", E.DEMAND),
            (r"in the tin market", r"users with substitutes cut back most when the price rose", TIN),
            (r"on the island", r"Crusoe moved an hour to fishing only while a fish was worth what it cost", CRUSOE),
        ], width=12.6, cols=3, font_size=24).move_to(UP * 0.4)
        head = heading(r"People respond to incentives")
        q = label(r"So, to change what people do, \ put a price on it?", font_size=32, color=E.ACCENT)
        q.next_to(rows, DOWN, buff=0.7)
        with self.voiceover(
            "Everything so far has worked because people respond to incentives. <bookmark mark='a'/> The traders in "
            "the pit adjusted their bids. The tin users switched to copper. Crusoe moved an hour to fishing only "
            "while a fish was worth what it cost him. <bookmark mark='b'/> So here's a natural idea. If you want "
            "people to do less of something, put a price on it. Usually that works. Here is a famous case where "
            "it didn't."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.1))
        self.clear_scene()

    def haifa(self):
        f = load("fine")
        sc = study_card(r"A fine for late parents", r"Uri Gneezy and Aldo Rustichini (2000)",
                        [(r"where", r"10 private day-care centres in Haifa, January to June 1998"),
                         (r"varied", rf"from week 5, a fine of NIS {f['fine_nis']} (about \${f['fine_usd']:.2f}) "
                                     r"per child for picking up 10 minutes late, in 6 centres chosen at random"),
                         (r"controls", r"the other 4 centres: no fine"),
                         (r"then", r"week 17: the fine removed, with no explanation")],
                        design="RCT", width=9.4, font_size=24).move_to(UP * 0.5)
        pp = pause_card(r"Late pick-ups in the fined centres: \ fewer, the same, or more?", color=E.ACCENT,
                        width=8.6).next_to(sc, DOWN, buff=0.45)
        src = published_tag(tables.GNEEZY_RUSTICHINI_2000.tag, corner=DR, font_size=17)
        with self.voiceover(
            "Haifa, in Israel, 1998. Ten private day-care centres close at four in the afternoon, and some parents "
            "come late, which means a teacher has to stay with their child. <bookmark mark='a'/> Two economists, "
            "Uri Gneezy and Aldo Rustichini, counted the late arrivals at each centre for four weeks. Then, in six "
            "of the ten centres, chosen at random, the management announced a fine: "
            f"{f['fine_nis']} shekels, about {money_words(f['fine_usd'])}, for each child collected more than ten "
            "minutes late. The other four centres changed nothing. <bookmark mark='b'/> Twelve weeks later the fine "
            "was dropped, without explanation. <bookmark mark='c'/> Before you see the result: in the fined "
            "centres, did late pick-ups fall, stay the same, or rise?"
        ) as vo:
            self.play(FadeIn(sc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("c")
            self.play(FadeIn(pp, shift=UP * 0.1))
        self.wait(4.0)
        self.clear_scene()

    def result(self):
        f = load("fine")
        wk = f["weeks"]
        ax = axes([0.5, 20.5], [0, 22], x_length=10.0, y_length=4.6, xticks=[1, 4, 5, 8, 12, 16, 17, 20],
                  yticks=[0, 5, 10, 15, 20], xlabel=r"week", font_size=20, center=[0, -0.4, 0])
        yl = label(r"late pick-ups per centre, per week", font_size=22, color=GREY_A).next_to(ax.ax, UP,
                                                                                               buff=0.15)
        yl.align_to(ax.ax, LEFT)
        shade = Rectangle(width=ax.ax.c2p(16.5, 0)[0] - ax.ax.c2p(4.5, 0)[0],
                          height=ax.ax.c2p(0, 22)[1] - ax.ax.c2p(0, 0)[1], stroke_width=0, fill_color=FINE,
                          fill_opacity=0.08).move_to((ax.ax.c2p(4.5, 0) + ax.ax.c2p(16.5, 22)) / 2)
        sl = label(r"the fine", font_size=22, color=FINE).next_to(shade, UP, buff=0.05).shift(DOWN * 0.45)
        test = curve(ax.ax, wk, f["test"], FINE, 4)
        test4 = curve(ax.ax, wk[:4], f["test"][:4], FINE, 4)
        ctrl = curve(ax.ax, wk, f["control"], E.CTRL, 4)
        dt = VGroup(*[Dot(ax.ax.c2p(w, v), radius=0.05, color=FINE) for w, v in zip(wk, f["test"])])
        dc = VGroup(*[Circle(radius=0.05, stroke_color=E.CTRL, stroke_width=2).move_to(ax.ax.c2p(w, v))
                      for w, v in zip(wk, f["control"])])
        lt = label(r"6 fined centres", font_size=22, color=FINE).move_to(ax.ax.c2p(18.5, 21.0))
        lc = label(r"4 others", font_size=22, color=E.CTRL).move_to(ax.ax.c2p(18.5, 5.0))
        b, du, a = f["before"], f["during"], f["after"]
        src = data_tag(r"Gneezy and Rustichini (2000), Table 1, transcribed; averages computed", corner=DR,
                       font_size=17)
        with self.voiceover(
            "Here are the weekly averages. Blue, hollow: the four centres without a fine. Red, filled: the six with "
            f"one. <bookmark mark='a'/> In the first four weeks the fined centres averaged {b[0]:.0f} late "
            "pick-ups a week. <bookmark mark='b'/> Then the fine came in, and late arrivals went up. Not down: up. "
            "Over three or four weeks they climbed, and then settled at about "
            f"{du[0]:.0f} a week, {f['ratio_test']:.1f} times as many as before. <bookmark mark='c'/> Meanwhile the "
            f"centres without a fine stayed where they were, at about {du[1]:.0f}. <bookmark mark='d'/> And when "
            "the fine was removed, the late arrivals didn't come back down. In the last four weeks they averaged "
            f"{a[0]:.0f}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(src))
            self.play(Create(ctrl), FadeIn(dc), FadeIn(lc), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(test4), FadeIn(dt[:4]), FadeIn(lt))
            vo.wait_until("b")
            self.play(FadeIn(shade), FadeIn(sl))
            self.play(Create(test), FadeIn(dt[4:16]), run_time=3)
            self.remove(test4)
            vo.wait_until("d")
            self.play(FadeIn(dt[16:]), Indicate(dt[16:], color=FINE))
        self.ax, self.result_group = ax, VGroup(ax, yl, shade, sl, test, ctrl, dt, dc, lt, lc, src)

    def did(self):
        f = load("fine")
        b, du = f["before"], f["during"]
        rows = VGroup(
            MathTex(r"\text{fined:}", rf"\ {du[0]:.1f}", r"-", rf"{b[0]:.1f}", r"=", rf"{du[0] - b[0]:+.1f}",
                    font_size=34),
            MathTex(r"\text{not fined:}", rf"\ {du[1]:.1f}", r"-", rf"{b[1]:.1f}", r"=", rf"{du[1] - b[1]:+.1f}",
                    font_size=34),
            MathTex(r"\text{the fine's effect:}", rf"\ {du[0] - b[0]:+.1f}", r"-", rf"({du[1] - b[1]:+.1f})", r"=",
                    rf"{f['did']:+.1f}", font_size=36),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.25)
        rows[0].set_color(FINE)
        rows[1].set_color(E.CTRL)
        rows[2][-1].set_color(E.ACCENT)
        box = panel(rows.width + 0.8, rows.height + 0.7)
        g = VGroup(box, rows).to_corner(UL, buff=0.3)
        rows.move_to(box)
        lab = label(r"a difference in differences \ (Part 4)", font_size=20, color=GREY_B).next_to(box, DOWN,
                                                                                                  buff=0.1)
        lab.align_to(box, LEFT)
        with self.voiceover(
            "How big was the effect? Not simply the change in the fined centres, because something else might have "
            "changed in those weeks too. <bookmark mark='a'/> So compare the changes. The fined centres went up by "
            f"{du[0] - b[0]:.1f} a week. The others moved by {du[1] - b[1]:.1f}. <bookmark mark='b'/> The "
            f"difference between the two changes, about {f['did']:.0f} more late pick-ups a week at each fined "
            "centre, is the fine's effect. This is called a difference in differences, and it works here because "
            "the fines were assigned at random. Part four is about when designs like this can be trusted."
        ) as vo:
            self.play(self.result_group.animate.scale(0.76).to_edge(DOWN, buff=0.15).shift(RIGHT * 1.5))
            vo.wait_until("a")
            self.play(FadeIn(box), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(lab))
        self.clear_scene()

    def meaning(self):
        f = load("fine")
        before = VGroup(label(r"before", font_size=26, color=GREY_B),
                        label(r"a favour asked of the teacher", font_size=30, color=WHITE),
                        label(r"cost: \ guilt, and her goodwill", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15)
        after = VGroup(label(r"with the fine", font_size=26, color=GREY_B),
                       label(rf"a service, at NIS {f['fine_nis']}", font_size=30, color=FINE),
                       label(r"a babysitter costs NIS 15 to 20 an hour", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        g = VGroup(before, after).arrange(RIGHT, buff=2.0).move_to(UP * 1.5)
        arrow = Arrow(before.get_right(), after.get_left(), buff=0.3, color=GREY_B)
        title = label(r"``A Fine Is a Price''", font_size=40, color=E.ACCENT).to_edge(UP, buff=0.35)
        lessons = VGroup(
            label(r"an incentive works through what people think it means", font_size=28, color=WHITE),
            label(r"and a meaning, once changed, may not change back", font_size=28, color=WHITE),
            label(r"one study, ten centres: \ a later survey-based study did not find the same; \ its record is "
                  r"in Part 45", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=1.3)
        with self.voiceover(
            "Why? The authors' answer is in their title: a fine is a price. <bookmark mark='a'/> Before the fine, "
            "coming late meant asking a favour of the teacher, and paying for it in guilt and goodwill. "
            f"<bookmark mark='b'/> With the fine, it was a service with a price: {f['fine_nis']} shekels, when a "
            "babysitter cost fifteen to twenty an hour. Cheap. <bookmark mark='c'/> The incentive did work, just not "
            "the way the designers meant. It worked through what people took it to mean. And once the favour had "
            "become a purchase, removing the price didn't turn it back into a favour. <bookmark mark='d'/> One "
            "caution, because this series keeps a record. This is one study, in ten centres, and a later study "
            "that asked people what they would do did not find the same thing. The finding goes into the record "
            "with that history in Part forty-five, on behavioural economics."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(before, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(after, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(lessons[0]))
            self.play(FadeIn(lessons[1]))
            vo.wait_until("d")
            self.play(FadeIn(lessons[2]))
        self.clear_scene()
