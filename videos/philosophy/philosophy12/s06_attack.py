from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Attack(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"The coordinated attack", r"Can messages create common knowledge?", lit=(1990,),
                            part=PART)
        with self.voiceover("Chapter five. The coordinated attack."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.story()
        self.depth()
        self.theorem()
        self.brick()

    def story(self):
        head = label(r"Two generals, \ one valley", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        hill_a = Polygon([-6.6, -1.4, 0], [-4.4, -1.4, 0], [-5.5, 0.4, 0], color=AG["A"], fill_opacity=0.25)
        hill_b = Polygon([4.4, -1.4, 0], [6.6, -1.4, 0], [5.5, 0.4, 0], color=AG["B"], fill_opacity=0.25)
        valley = Rectangle(width=8.6, height=0.6, stroke_width=0, fill_color=BAD, fill_opacity=0.25).move_to(
            [0, -1.1, 0])
        vl = label(r"the enemy, \ in the valley", font_size=20, color=BAD).move_to(valley)
        la = label(r"General A", font_size=22, color=AG["A"]).next_to(hill_a, UP, buff=0.15)
        lb = label(r"General B", font_size=22, color=AG["B"]).next_to(hill_b, UP, buff=0.15)
        rows = VGroup(
            label(r"they win only if they attack together; \ alone, \ the attacker is destroyed", font_size=23),
            label(r"they can talk only by messengers, \ who must cross the valley, \ and may be caught",
                  font_size=23, color=LOSS),
            label(r"A sends: \ `attack at dawn'. \ Will B attack? \ Only if he knows A knows he got it\dots",
                  font_size=23, color=GOAL)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        msg = Dot([-4.6, -0.4, 0], color=WHITE, radius=0.1)
        with self.voiceover(
            "The coordinated attack problem was told by Jim Gray in 1978 and analysed by Joseph Halpern and Yoram "
            "Moses. <bookmark mark='a'/>Two generals camp on hills on either side of a valley. In the valley is the "
            "enemy. <bookmark mark='b'/>If both attack together, they win. If one attacks alone, his army is "
            "destroyed. <bookmark mark='c'/>They can communicate only by messengers, who must cross the valley and "
            "may be caught. <bookmark mark='d'/>A sends a messenger: attack at dawn. The messenger gets through. "
            "Will B attack? Only if he can be sure that A will. But A does not know the messenger arrived, so A "
            "cannot be sure that B knows the plan, and will not attack unless he hears back."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hill_a), FadeIn(hill_b), FadeIn(valley), FadeIn(vl), FadeIn(la), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.add(msg)
            self.play(msg.animate.move_to([4.6, -0.4, 0]), run_time=2.5, rate_func=smooth)
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def depth(self):
        d = load("attack")
        head = label(r"Acknowledgements, \ and how high the tower gets", font_size=30, color=CONN).to_edge(UP,
                                                                                                    buff=0.35)
        ax, bx = -5.6, -1.6
        top, step = 2.1, 0.55
        line_a = Line([ax, top + 0.2, 0], [ax, top - 6.2 * step, 0], color=AG["A"], stroke_width=3)
        line_b = Line([bx, top + 0.2, 0], [bx, top - 6.2 * step, 0], color=AG["B"], stroke_width=3)
        ta = label(r"A", font_size=24, color=AG["A"]).next_to(line_a, UP, buff=0.1)
        tb = label(r"B", font_size=24, color=AG["B"]).next_to(line_b, UP, buff=0.1)
        msgs = VGroup()
        for k in range(6):
            y0 = top - k * step
            src, dst = (ax, bx) if k % 2 == 0 else (bx, ax)
            msgs.add(Arrow([src, y0, 0], [dst, y0 - step * 0.85, 0], buff=0.05, color=WHITE, stroke_width=2.5,
                           max_tip_length_to_length_ratio=0.08))
        hd = [label(r"messages delivered", font_size=20, color=P.CLAIM),
              label(r"deepest $E^k$(plan)", font_size=20, color=P.CLAIM),
              label(r"common?", font_size=20, color=P.CLAIM)]
        rows = [[label(str(r["delivered"]), font_size=21),
                 label(r"---" if r["depth"] < 0 else rf"$E^{{{r['depth']}}}$" if r["depth"] else r"B knows; \ not E",
                       font_size=21),
                 mark(r["common"], 24)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[2.6, 2.8, 1.4], cell_h=0.46, font_size=20).move_to([3.4, -0.2, 0])
        foot = label(r"each delivered message adds one storey; \ the top storey is always missing", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So they acknowledge. <bookmark mark='a'/>B sends back: got it. A sends back: got your got it. And so "
            "on, each messenger crossing the valley at risk. <bookmark mark='b'/>The Reasoner builds the model: a "
            "world for each number of messengers who got through. A cannot tell apart the worlds where his last "
            "messenger did or did not arrive; nor can B. Then it measures, after each number of delivered messages, "
            "the height of the tower of 'everyone knows' about the plan. <bookmark mark='c'/>After one message, B "
            "knows the plan, but A does not know that B knows. After two, everyone knows it. After three, everyone "
            "knows that everyone knows. Each delivered message adds exactly one storey. <bookmark mark='d'/>And the "
            "last column never changes. However many messengers get through, the plan is never common knowledge."
        ) as vo:
            self.play(FadeIn(head), Create(line_a), Create(line_b), FadeIn(ta), FadeIn(tb))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(m) for m in msgs], lag_ratio=0.4), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r][:2])) for r in range(len(rows))], lag_ratio=0.5),
                      run_time=5)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][2]) for r in range(len(rows))], lag_ratio=0.2))
            self.play(FadeIn(foot))
        self.clear_scene()

    def theorem(self):
        head = label(r"Halpern and Moses (1990)", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        thm = label(r"over a channel that can lose messages, \ no protocol ever makes anything new common knowledge",
                    font_size=26, color=COMMON).next_to(head, DOWN, buff=0.4)
        steps = VGroup(
            label(r"suppose some run of the protocol attains common knowledge \ after the fewest messages, $n$",
                  font_size=23),
            label(r"the sender of the last message cannot tell whether it arrived", font_size=23, color=GREY_A),
            label(r"so the run where it was lost looks the same to him: \ he attacks there too", font_size=23,
                  color=GREY_A),
            label(r"so the common knowledge already held after $n - 1$ messages: \ contradiction", font_size=23,
                  color=BAD),
            label(r"therefore no coordinated attack is ever guaranteed: \ the generals never both attack",
                  font_size=25, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.8, 0])
        with self.voiceover(
            "The theorem behind this is due to Halpern and Moses. <bookmark mark='a'/>Over a channel that can lose "
            "messages, no protocol, however clever, ever makes anything new common knowledge. The proof is an "
            "induction. <bookmark mark='b'/>Suppose some run of a protocol attains common knowledge, and take the "
            "run that does it with the fewest messages, n. <bookmark mark='c'/>The sender of the last message cannot "
            "tell whether it arrived. <bookmark mark='d'/>So the run where it was lost looks exactly the same to "
            "him, and whatever he knows in one he knows in the other. <bookmark mark='e'/>Then common knowledge "
            "already held after n minus one messages, which contradicts our choice of n. <bookmark mark='f'/>And "
            "since attacking together requires common knowledge that both will attack, the generals, if they are "
            "cautious, never attack."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            for mk, s_ in zip("bcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.1))
        self.clear_scene()

    def brick(self):
        w = wall(upto=12, current=12).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(12, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the twelfth brick in the Wall. <bookmark mark='a'/>The dream: to create common knowledge by "
            "sending messages. <bookmark mark='b'/>The wall: Halpern and Moses's theorem, that over an unreliable "
            "channel it cannot be done. <bookmark mark='c'/>What it forces: act without certainty. Settle for "
            "probabilities, deadlines and timeouts, and for agreement that is very likely rather than guaranteed. "
            "That is exactly what the engineers of the next chapter do."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[12], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1]))
            vo.wait_until("c")
            self.play(Indicate(card, color=P.WALL, scale_factor=1.02))
        self.clear_scene()
